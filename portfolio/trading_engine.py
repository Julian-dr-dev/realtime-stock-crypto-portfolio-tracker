
from portfolio.data_fetcher import DataFetcher
from portfolio.portfolio_manager import PortfolioManager

class TradingEngine:
    def __init__(self):
        self.data_fetcher = DataFetcher()
        self.portfolio = PortfolioManager()
        self.balance = 10000

    def evaluate_signal(self, symbol, price_data):
        if len(price_data) < 2:
            return None

        prev_price = price_data[-2]
        curr_price = price_data[-1]

        change = (curr_price - prev_price) / prev_price * 100

        if change <= -2:
            return "buy"
        

        

