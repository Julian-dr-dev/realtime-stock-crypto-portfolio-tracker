import json
import os
from datetime import datetime

class PortfolioManager:
    def __init__(self, save_path="data/portfolio_state.json"):
        self.save_path = save_path
        self.assets = {}  # {symbol: quantity}
        self.load_from_file()

    def add_asset(self, symbol, quantity):
        """Add (or increase) holdings for a symbol."""
        self.assets[symbol] = self.assets.get(symbol, 0) + quantity
        self.save_to_file()

    def remove_asset(self, symbol, quantity):
        """Sell (or reduce) holdings for a symbol."""
        if symbol in self.assets:
            self.assets[symbol] -= quantity
            if self.assets[symbol] <= 0:
                del self.assets[symbol]
            self.save_to_file()

    def get_quantity(self, symbol):
        """Return quantity held for a symbol."""
        return self.assets.get(symbol, 0)

    def get_portfolio_value(self, price_data):
        """
        Calculate total value based on provided price data.
        Expects a dict like {'BTC': 30000, 'ETH': 2000}
        """
        total = 0
        for symbol, qty in self.assets.items():
            price = price_data.get(symbol, 0)
            total += qty * price
        return total

    def get_holdings_summary(self):
        """Return a human-readable summary of current holdings."""
        if not self.assets:
            return "No holdings in portfolio."
        summary = "Current Holdings:\n"
        for sym, qty in self.assets.items():
            summary += f"  - {sym}: {qty:.4f} units\n"
        return summary

    def save_to_file(self):
        """Persist portfolio state to JSON."""
        os.makedirs(os.path.dirname(self.save_path), exist_ok=True)
        data = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "assets": self.assets
        }
        with open(self.save_path, "w") as f:
            json.dump(data, f, indent=4)

    def load_from_file(self):
        """Load portfolio state from JSON if it exists."""
        if os.path.exists(self.save_path):
            with open(self.save_path, "r") as f:
                data = json.load(f)
                self.assets = data.get("assets", {})
        else:
            self.assets = {}
