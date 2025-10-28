from trading.trading_engine import TradingEngine
import time
import random


def simulate_price_data(symbol, num_points=20):
    base_price = random.uniform(90, 110)
    prices = [base_price]

    for _ in range (num_points - 1):
        change = random.uniform(-3, 3)
        new_price = prices[-1] * (1 + change / 100)
        prices.append(round(new_price, 2))
    return prices

def main(): 
    engine = TradingEngine()
    symbol = "AAPL"

    print(f"\n--- Starting Trading Simulation for {symbol} ---\n")

    prices = simulate_price_data(symbol, num_points=15)
    print("Generated price data:", prices)

    for i in range(2, len(prices)):
        window = price[:i]
        singal = engine.evaluate_signal(symbol, window) 

        if signal:
            print(f"Signal detected: {signal.upper()} at price ${window[-1]:.2f}")
            engine.execute_trade(symbol, signal)
        else: 
            print(f"No action at price ${window[-1]:.2f}")

        time.sleep(0.5)


    engine.show_status()
    print("\n--- Simulation Complete ---")








    