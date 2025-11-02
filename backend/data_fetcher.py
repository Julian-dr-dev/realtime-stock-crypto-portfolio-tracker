

import yfinance as yf 
import requests 
from datetime import datetime
import time



class DataFetcher: 

    def __init__(self):
        self.crypto_api_url = "https://min-api.cryptocompare.com/data/price"

    def get_stock_price(self, ticker: str) -> float:
        try:
            stock = yf.Ticker(ticker)
            price = stock.history(period="1d")["Close"].iloc[-1]
            return float(price)
        except Exception as e:
            print(f"Erroer fetching stock price for {ticker}: {e}")
            return None
        
    def get_stock_history(self, ticker: str, period="1mo") -> dict:
        try:
            stock = yf.Ticker(ticker)
            hist = stock.history(period=period)
            return hist["Close"].to_dict()
        except Exception as e:
            print("Error Fetching stock history for {ticker}: {e}")
            return {}
        




        

    def get_crypto_price(self, symbol: str, currency="USD") -> float:
        try:
            response = requests.get(
                self.crypto_api_url,
                params={"fsym": symbol.upper(), "tsyms": currency.upper()},
            )
            response.raise_for_status()
            data = response.json()
            return float(data.get(currency.upper()))
        except Exception as e:
            print(f"[{datetime.now()}] Error fetching crypto price for {symbol}: {e}")
            return None
        

    def get_current_price(self, symbol: str, asset_type: str = "stock") -> float:
        
        asset_type = asset_type.lower()

        if asset_type == "stock":
            return self.get_stock_price(symbol)
        elif asset_type == "crypto": 
            return self.get_crypto_price(symbol)
        else: 
            raise ValueError("asset_type must be either 'stock' or 'crypto'.")
        


    def wait_for_next_request(self, delay=2):
        """
        Optional delay between API calls to avoid rate limiting.
        """
        time.sleep(delay)
        
        




