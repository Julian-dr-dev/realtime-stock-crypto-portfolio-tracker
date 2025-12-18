import json
import os
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

    # ------------------------------
    # SIGNAL LOGIC
    # ------------------------------
    def get_trade_signal(self, prices):
        """
        Simple moving average crossover strategy.
        prices: list of floats (historical prices)
        """
        if len(prices) < 5:
            return "HOLD"

        short_ma = sum(prices[-3:]) / 3
        long_ma = sum(prices[-5:]) / 5

        if short_ma > long_ma:
            return "BUY"
        elif short_ma < long_ma:
            return "SELL"
        return "HOLD"

    # ------------------------------
    # POSITION SIZING
    # ------------------------------
    def calculate_position_size(self, portfolio_value, price):
        risk_capital = portfolio_value * self.max_risk_per_trade
        units = risk_capital / price
        return round(units, 4)

    # ------------------------------
    # TRADE EXECUTION
    # ------------------------------
    def execute_trade(self, symbol, signal, price):
        portfolio_value = self.portfolio.get_portfolio_value({symbol: price})
        quantity = self.calculate_position_size(portfolio_value + 1e-6, price)

        if signal == "BUY":
            self.portfolio.add_asset(symbol, quantity)
            action = f"BUY {quantity} {symbol} @ {price:.2f}"

        elif signal == "SELL":
            self.portfolio.remove_asset(symbol, quantity)
            action = f"SELL {quantity} {symbol} @ {price:.2f}"

        else:
            return "HOLD"

        self.record_trade(symbol, signal, quantity, price)
        self.portfolio.save_to_file()
        self.save_trade_history()
        return action

    # ------------------------------
    # MAIN ENGINE LOOP
    # ------------------------------
    def run_for_symbol(self, symbol):
        history = self.data_fetcher.get_stock_history(symbol, period="1mo")

        if not history:
            return "NO DATA"

        prices = list(history.values())
        current_price = prices[-1]

        signal = self.get_trade_signal(prices)
        return self.execute_trade(symbol, signal, current_price)

    # ------------------------------
    # LOGGING
    # ------------------------------
    def record_trade(self, symbol, signal, quantity, price):
        self.trade_history.append({
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "symbol": symbol,
            "action": signal,
            "quantity": quantity,
            "price": price
        })

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

    # ------------------------------
    # API SNAPSHOT
    # ------------------------------
    def get_status_snapshot(self):
        holdings = self.portfolio.assets
        symbols = list(holdings.keys())

        prices = {
            s: self.data_fetcher.get_current_price(
                s, "crypto" if s in {"BTC","ETH","LTC","XRP"} else "stock"
            )
            for s in symbols
        }

        value = self.portfolio.get_portfolio_value(prices)

        return {
            "portfolio_value": round(value, 2),
            "holdings": holdings,
            "recent_trades": self.trade_history[-5:]
        }
