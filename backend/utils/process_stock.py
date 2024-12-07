
from langchain_pinecone import PineconeVectorStore
from langchain_community.embeddings import HuggingFaceEmbeddings
import os
from dotenv import load_dotenv
from langchain.schema import Document
from get_data import get_company_tickers, get_stock_info
import concurrent.futures

load_dotenv()


successful_tickers, unsuccessful_tickers = [], []
def process_stock(stock_ticker: str) -> str:
 
    if stock_ticker in successful_tickers:
        return f"Already processed {stock_ticker}"

    try:
        # Get and store stock data
        stock_data = get_stock_info(stock_ticker)
        stock_description = stock_data.get('Business Summary', '')

        if not stock_description:
            raise ValueError(f"No description available for {stock_ticker}.")

        # Store stock description in Pinecone
        vectorstore = PineconeVectorStore.from_documents(
            documents=[Document(page_content=stock_description, metadata=stock_data)],
            embedding=HuggingFaceEmbeddings(),
            index_name="stocks",
            namespace="stock-descriptions"
        )

        # Track success
        with open('successful_tickers.txt', 'a') as f:
            f.write(f"{stock_ticker}\n")
        successful_tickers.append(stock_ticker)

        return f"Processed {stock_ticker} successfully."

    except Exception as e:
        # Track failure
        with open('unsuccessful_tickers.txt', 'a') as f:
            f.write(f"{stock_ticker}\n")
        unsuccessful_tickers.append(stock_ticker)

        return f"ERROR processing {stock_ticker}: {e}"


def parallel_process_stocks(tickers: list, max_workers: int = 10) -> None:
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_ticker = {
            executor.submit(process_stock, ticker): ticker
            for ticker in tickers
        }

        for future in concurrent.futures.as_completed(future_to_ticker):
            ticker = future_to_ticker[future]
            try:
                result = future.result()
                print(result)

                # Stop on error
                if result.startswith("ERROR"):
                    print(f"Stopping program due to error in {ticker}")
                    executor.shutdown(wait=False)
                    raise SystemExit(1)

            except Exception as exc:
                print(f'{ticker} generated an exception: {exc}')
                print("Stopping program due to exception.")
                executor.shutdown(wait=False)
                raise SystemExit(1)



tickers_to_process = [ticker['ticker'] for ticker in get_company_tickers().values()]

# Process them
parallel_process_stocks(tickers_to_process, max_workers=10)