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
        elif change >= 3:
            return "sell"
        return None 

    def execute_trade(self, symbol, action, amount=1000):
        price = self.data_fetcher.get_current_price(symbol, asset_type="stock")

        if not price:
            print(f"Price for {symbol} unavailable. Skipping trade.")
            return
        
        if action == "buy" and self.balance >= amount:
            quantity = amount / price
            self.portfolio.add_asset(symbol, quantity)
            self.balance -= amount
            print(f"Bought {quantity:.4f} {symbol} at ${price:.2f} | New balance: ${self.balance:.2f}")

        elif action == "sell":
            quantity_owned = self.portfolio.get_quantity(symbol)
            if quantity_owned > 0:
                sell_value = quantity_owned * price
                self.portfolio.remove_asset(symbol, quantity_owned)
                self.balance += sell_value
                print(f"Sold {quantity_owned:.4f} {symbol} at ${price:.2f} | New balance: ${self.balance:.2f}")
            else:
                print(f"No holdings found for {symbol}. Skipping sell.")

        else:
            print(f"Not enough balance to buy {symbol}.")

    def show_status(self):
        total_value = self.portfolio.get_portfolio_value()
        print(f"\nBalance: ${self.balance:.2f}")
        print(f"Portfolio Value: ${total_value:.2f}")
        print(f"Total Equity: ${(self.balance + total_value):.2f}\n")
