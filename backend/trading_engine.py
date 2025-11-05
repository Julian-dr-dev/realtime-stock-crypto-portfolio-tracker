import random
import json
import time
from datetime import datetime

from data_fetcher import DataFetcher
from portfolio_manager import PortfolioManager


class TradingEngine:
    def __init__(self, portfolio_file="portfolio.json", trade_log="trade_history.json", mode="simulation"):
        self.data_fetcher = DataFetcher()
        self.portfolio = PortfolioManager(portfolio_file)
        self.trade_log_file = trade_log
        self.mode = mode  # 'simulation' or 'live'

        # Risk parameters
        self.max_risk_per_trade = 0.05    # 5% of portfolio value
        self.trade_fee = 1.00             # flat fee per trade (simulation)

        # Load previous trade history if it exists
        try:
            with open(self.trade_log_file, "r") as file:
                self.trade_history = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            self.trade_history = []


    def get_trade_signal(self, symbol, price_data):
        return random.choice(["BUY", "SELL", "HOLD"])


    def calculate_position_size(self, price):
        portfolio_value = self.portfolio.get_portfolio_value()
        risk_amount = portfolio_value * self.max_risk_per_trade
        shares = int(risk_amount // price)
        return max(shares, 0)


    def execute_trade(self, symbol, signal, price):
        if signal == "BUY":
            quantity = self.calculate_position_size(price)
            if quantity > 0:
                self.portfolio.buy(symbol, quantity, price)
                trade_info = self.record_trade(symbol, "BUY", quantity, price)
                print(f"[BUY] {quantity} shares of {symbol} at ${price:.2f}")
                return trade_info

        elif signal == "SELL":
            quantity = self.portfolio.get_position(symbol)
            if quantity > 0:
                self.portfolio.sell(symbol, quantity, price)
                trade_info = self.record_trade(symbol, "SELL", quantity, price)
                print(f"[SELL] {quantity} shares of {symbol} at ${price:.2f}")
                return trade_info

        elif signal == "HOLD":
            print(f"[HOLD] No action for {symbol}")

        return None


    def run(self, symbols, iterations=10, delay=5):
        print(f"🚀 Starting Trading Engine in {self.mode.upper()} mode...\n")

        for i in range(iterations):
            print(f"Iteration {i + 1}/{iterations}")

            for symbol in symbols:
                price_data = self.data_fetcher.get_latest_price(symbol)
                current_price = price_data.get("price", 0)
                if not current_price:
                    continue

                signal = self.get_trade_signal(symbol, price_data)
                trade_info = self.execute_trade(symbol, signal, current_price)

                if trade_info:
                    self.trade_history.append(trade_info)
                    self.save_trade_history()

            self.portfolio.save()
            print(f"💰 Portfolio Value: ${self.portfolio.get_portfolio_value:.2f}\n")

            if self.mode == "simulation":
                time.sleep(delay)

        print("✅ Trading session complete!\n")


    def record_trade(self, symbol, action, quantity, price):
        trade_info = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "symbol": symbol,
            "action": action,
            "quantity": quantity,
            "price": price,
            "total_cost": round(quantity * price, 2),
            "fee": self.trade_fee
        }
        return trade_info


    def save_trade_history(self):
        with open(self.trade_log_file, "w") as file:
            json.dump(self.trade_history, file, indent=4)


    def get_status_snapshot(self):
        return {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "mode": self.mode,
            "portfolio_value": self.portfolio.get_portfolio_value(),
            "positions": self.portfolio.get_positions(),
            "cash_balance": self.portfolio.get_cash_balance(),
            "recent_trades": self.trade_history[-5:]
        }


if __name__ == "__main__":
    engine = TradingEngine(mode="simulation")
    engine.run(["AAPL", "MSFT", "GOOG"], iterations=5, delay=2)
