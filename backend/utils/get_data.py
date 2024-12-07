import json
import requests
import yfinance as yf
import json
import numpy as np 
from sentence_transformers import SentenceTransformer 
from sklearn.metrics.pairwise import cosine_similarity  


def get_company_tickers() :
    url = "https://raw.githubusercontent.com/team-headstart/Financial-Analysis-and-Automation-with-LLMs/main/company_tickers.json"
    response = requests.get(url)

    if response.status_code == 200:
        company_tickers = json.loads(response.content.decode('utf-8'))
        return company_tickers
    else:
        raise ValueError(f"Failed to fetch tickers. Status code: {response.status_code}")

def get_stock_info(symbol: str) :
    data = yf.Ticker(symbol)
    stock_info = data.info

    return {
        "Ticker": stock_info.get('symbol', 'N/A'),
        'Name': stock_info.get('longName', 'N/A'),
        'Business Summary': stock_info.get('longBusinessSummary'),
        'City': stock_info.get('city', 'N/A'),
        'State': stock_info.get('state', 'N/A'),
        'Country': stock_info.get('country', 'N/A'),
        'Industry': stock_info.get('industry', 'N/A'),
        'Sector': stock_info.get('sector', 'N/A'),
    }

