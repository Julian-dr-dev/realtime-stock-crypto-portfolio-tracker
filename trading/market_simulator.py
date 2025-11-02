import time
from backend.data_fetcher import DataFtercher
from backend.portfolio_manager import PortfolioManager
from portfolio.trading_engine import TradingEngine


class MarketSimulaotr: 
    def __init__(self, symbol="BTC", steps=50, delay=0.5):
        self.symbol = symbol 
        self.steps = steps
        self.delay = delay
        self.engine = TradingEngine()
        self.price_history = []
    
    def run(self):
        print(f"Starting simulation for {self.symbol}...\n")
        for i in range(self.steps):
            curr_price = self.engine.data_fetcher.get_current_price(self.symbol)
            if not curr_price:
                print(f"Price unavailable, skipping this round")
                continue
            
            self.price_history.append(curr_price)
            if len(self.price_history) > 50:
                self.price_history.pop(0)

            signal = self.engine.evaluate_signal(self.symbol, self.price_history)
            if signal:
                self.engine.execute_trade(self.symbol, signal)

            self.engine.show_status()


            time.sleep(self.delay)
            print("\n Simulation complete")

            self.engine.show_status()





                                



