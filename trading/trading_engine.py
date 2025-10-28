import pandas as pd
import numpy as np
from portfolio.data_fetcher import DataFetcher
from portfolio.portfolio_manager import PortfolioManager

class TradingEngine:
    def __init__(self):
        self.data_fetcher = DataFetcher()
        self.portfolio = PortfolioManager()
        self.balance = 10000

    def evaluate_signal(self, symbol, price_data):
        """
        Determines buy/sell signals using Moving Average Crossover and RSI.
        """
        if len(price_data) < 20:  # Need at least 20 data points
            return None

        # Create a DataFrame for easier analysis
        df = pd.DataFrame(price_data, columns=["price"])

        # Calculate short-term (5-day) and long-term (20-day) moving averages
        df["SMA_short"] = df["price"].rolling(window=5).mean()
        df["SMA_long"] = df["price"].rolling(window=20).mean()

        # RSI (Relative Strength Index) Calculation
        delta = df["price"].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / loss
        df["RSI"] = 100 - (100 / (1 + rs))

        # Get the most recent indicators
        short_ma = df["SMA_short"].iloc[-1]
        long_ma = df["SMA_long"].iloc[-1]
        rsi = df["RSI"].iloc[-1]

        # --- Signal Logic ---
        if short_ma > long_ma and rsi < 70:
            return "buy"
        elif short_ma < long_ma and rsi > 30:
            return "sell"
        else:
            return None

    def execute_trade(self, symbol, action, amount=1000):
        price = self.data_fetcher.get_current_price(symbol)

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
