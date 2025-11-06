from flask import Flask, jsonify
from flask_cors import CORS
from portfolio_manager import PortfolioManager
from trading_engine import TradingEngine

# Initialize Flask
app = Flask(__name__)
CORS(app)  # Allow frontend to call backend

# Initialize portfolio + trading system
portfolio_manager = PortfolioManager()
trading_engine = TradingEngine(portfolio_manager)


@app.route("/")
def home():
    return jsonify({"message": "Backend is running!"})


@app.route("/portfolio", methods=["GET"])
def get_portfolio():
    # Get portfolio total value
    total_value = portfolio_manager.get_portfolio_value()

    # Get holdings dictionary (or change to match your attribute name)
    holdings = portfolio_manager.assets if hasattr(portfolio_manager, "assets") else {}

    return jsonify({
        "total_value": total_value,
        "holdings": holdings
    })


if __name__ == "__main__":
    app.run(debug=True)
