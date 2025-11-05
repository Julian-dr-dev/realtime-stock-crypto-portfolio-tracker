from flask import Flask, jsonify
from flask_cors import CORS
from trading_engine import TradingEngine

app = Flask(__name__)

#front end connection
CORS(app)

engine = TradingEngine(mode="live")

@app.route("/api/status", methods=["GET"])

def get_status():
    snapshot = engine.get_status_snapshot()
    return jsonify(snapshot)

if __name__ == "__main__":
    app.run(debug=True)


