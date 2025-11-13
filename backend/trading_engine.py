import json
import os
import random
from datetime import datetime
from data_fetcher import DataFetcher

class TradingEngine:
    def __init__(self, portfolio_manager, log_path="data/trade_log.json"):
        self.data_fetcher = DataFetcher()
        self.portfolio = portfolio_manager
        self.log_path = log_path
        self.trade_history = []
        self.max_risk_per_trade = 0.05
        self.load_trade_history()

    def get_trade_signal(self, symbol, price):
        return random.choice(["BUY", "SELL", "HOLD"])

    def calculate_position_size(self, portfolio_value, price):
        risk_cap = portfolio_value * self.max_risk_per_trade
        units = risk_cap / price
        return round(units, 4)

    def execute_trade(self, symbol, signal, price):
        portfolio_value = self.portfolio.get_portfolio_value({symbol: price})
        quantity = self.calculate_position_size(portfolio_value + 1e-6, price)

        if signal == "BUY":
            self.portfolio.add_asset(symbol, quantity)
            action = f"Bought {quantity} {symbol} @ {price:.2f}"

        elif signal == "SELL":
            self.portfolio.remove_asset(symbol, quantity)
            action = f"Sold {quantity} {symbol} @ {price:.2f}"

        else:
            action = f"Held {symbol}"

        self.record_trade(symbol, signal, quantity, price)
        self.portfolio.save_to_file()
        self.save_trade_history()
        return action

    def run(self, symbols):
        prices = self.data_fetcher.get_prices(symbols)

        for symbol, price in prices.items():
            signal = self.get_trade_signal(symbol, price)
            self.execute_trade(symbol, signal, price)

    def record_trade(self, symbol, signal, quantity, price):
        trade = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "symbol": symbol,
            "action": signal,
            "quantity": quantity,
            "price": price
        }
        self.trade_history.append(trade)

    def save_trade_history(self):
        os.makedirs(os.path.dirname(self.log_path), exist_ok=True)
        with open(self.log_path, "w") as f:
            json.dump(self.trade_history, f, indent=4)

    def load_trade_history(self):
        if os.path.exists(self.log_path):
            with open(self.log_path, "r") as f:
                self.trade_history = json.load(f)
        else:
            self.trade_history = []

    def get_status_snapshot(self):
        holdings = self.portfolio.assets
        symbols = list(holdings.keys())
        prices = self.data_fetcher.get_prices(symbols) if symbols else {}
        value = self.portfolio.get_portfolio_value(prices)

        return {
            "holdings": holdings,
            "portfolio_value": round(value, 2),
            "recent_trades": self.trade_history[-5:]
        }
