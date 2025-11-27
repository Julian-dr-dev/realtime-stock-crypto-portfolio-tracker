# backend/app.py
from flask import Flask, jsonify, request
from flask_cors import CORS
from datetime import datetime

from data_fetcher import DataFetcher
from portfolio_manager import PortfolioManager
from trading_engine import TradingEngine

app = Flask(__name__)
CORS(app)

# Core backend objects
data_fetcher = DataFetcher()
portfolio_manager = PortfolioManager()
trading_engine = TradingEngine(portfolio_manager)


@app.route("/")
def home():
    return jsonify({
        "message": "Backend is running!",
        "timestamp": datetime.now().isoformat()
    })


# -------------------------------------------------------------
# GET PORTFOLIO
# -------------------------------------------------------------
@app.route("/api/portfolio", methods=["GET"])
def get_portfolio():
    try:
        holdings_raw = getattr(portfolio_manager, "assets", {})  # {symbol: qty}
        holdings_list = [{"symbol": s, "quantity": q} for s, q in holdings_raw.items()]

        # Get prices for all symbols
        price_map = {
            s: data_fetcher.get_current_price(
                s,
                "crypto" if s.upper() in ["BTC", "ETH", "LTC", "XRP"] else "stock"
            )
            for s in holdings_raw.keys()
        }

        total_value = portfolio_manager.get_portfolio_value(price_map)

        return jsonify({
            "total_value": total_value,
            "holdings": holdings_list
        })

    except Exception as e:
        app.logger.exception("Error in /api/portfolio")
        return jsonify({"error": str(e)}), 500


# -------------------------------------------------------------
# GET LIVE PRICES FOR ANY SYMBOLS
# -------------------------------------------------------------
@app.route("/api/prices", methods=["GET"])
def get_prices():
    try:
        symbols_param = request.args.get("symbols", "")
        if not symbols_param:
            return jsonify({
                "error": "query parameter 'symbols' required (e.g. symbols=BTC,AAPL)"
            }), 400

        asset_type_param = request.args.get("asset_type", "auto").lower()
        symbols = [s.strip().upper() for s in symbols_param.split(",") if s.strip()]

        prices = {}

        for sym in symbols:

            # Auto-detect asset type
            if asset_type_param == "auto":
                is_crypto = sym in {"BTC", "ETH", "LTC", "XRP", "DOGE"}
                atype = "crypto" if is_crypto else "stock"
            else:
                atype = asset_type_param

            # Fetch price
            price = data_fetcher.get_current_price(sym, atype)
            prices[sym] = price

            # Space out API requests
            data_fetcher.wait_for_next_request(0.5)

        # FINAL response (after loop)
        response = {
            "timestamp": datetime.now().isoformat(),
            "prices": prices
        }

        return jsonify(response)

    except Exception as e:
        app.logger.exception("Error in /api/prices")
        return jsonify({"error": str(e)}), 500


# START SERVER
if __name__ == "__main__":
    app.run(debug=True)
