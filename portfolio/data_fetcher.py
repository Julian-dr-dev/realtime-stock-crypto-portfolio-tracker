

import yfinance as yf 
import requests 


class DataFetcher: 

    def __init__(self):
        self.crypto_api_url = "https://min-api.cryptocompare.com/data/price"

    def get_stock_price(self, ticker: str) -> float:
        try:
            stock = yf.Ticker
            price = yf.Ticker(ticker).history(period="1d")["Close"].iloc[-1]
            return price
        except Exception as e:
            print("Erroer fetching stock price for {ticker}: {e}")
            return None
        
    def get_stock_history(self, ticker: str, period="1mo") -> dict:
        try:
            stock = yf.Ticker(ticker)
            hist = stock.history(period=period)
            return hist["Close"].to_dict()
        except Exception as e:
            print("Error Fetching stock history for {ticker}: {e}")
            return {}



