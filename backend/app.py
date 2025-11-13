from flask import Flask, jsonify
from flask_cors import CORS

from portfolio_manager import PortfolioManager
from trading_engine import TradingEngine
from data_fetcher import DataFetcher

app = Flask(__name__)
CORS(app)

# Initialize core components
portfolio = PortfolioManager()
engine = TradingEngine(portfolio_manager=portfolio)
fetcher = DataFetcher()

@app.route("/api/status", methods=["GET"])
def status():
    snapshot = engine.get_status_snapshot()
    return jsonify(snapshot)

@app.route("/api/run", methods=["POST"])
def run():
    # You can modify the symbol list anytime you want
    symbols = ["BTC", "ETH", "AAPL"]
    engine.run(symbols)
    return jsonify({"message": "Trading cycle complete"})

if __name__ == "__main__":
    app.run(debug=True)
