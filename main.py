import yfinance as yf

# Quick test: fetch Apple stock closing price
ticker = yf.Ticker("AAPL")
price = ticker.history(period="1d")["Close"].iloc[-1]
print(f"Apple closing price: ${price:.2f}")

