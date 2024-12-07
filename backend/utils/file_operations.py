def read_tickers(file_path: str) -> list:
    try:
        with open(file_path, 'r') as file:
            return [line.strip() for line in file if line.strip()]
    except FileNotFoundError:
        return []

def write_ticker(file_path: str, ticker: str):
    with open(file_path, 'a') as file:
        file.write(ticker + "\n")
