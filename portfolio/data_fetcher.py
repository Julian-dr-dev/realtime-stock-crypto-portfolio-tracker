

import yfinance as yf 
import requests 


class DataFetcher: 

    def __init__(self):
        self.crypto_api_url = "https://min-api.cryptocompare.com/data/price"