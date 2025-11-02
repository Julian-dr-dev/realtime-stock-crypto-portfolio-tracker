import React, { useEffect, useState } from "react";
import Plot from "react-plotly.js";

const Dashboard = () => {
  const [status, setStatus] = useState(null);

  useEffect(() => {
    fetch("http://127.0.0.1:5000/api/status")
      .then((res) => res.json())
      .then((data) => setStatus(data))
      .catch((err) => console.error("Error fetching backend:", err));
  }, []);

  if (!status) return <p className="text-center mt-10">Loading portfolio...</p>;

  const recentTrades = status.recent_trades || [];
  const holdings = status.holdings || {};
  const symbols = Object.keys(holdings);
  const quantities = Object.values(holdings);

  return (
    <div className="p-10 font-sans">
      <h1 className="text-3xl font-bold mb-4">Trading Dashboard</h1>

      <div className="mb-6">
        <h2 className="text-xl">Portfolio Value: ${status.portfolio_value}</h2>
        <p>Mode: {status.mode}</p>
        <p>Last Updated: {status.timestamp}</p>
      </div>

      <Plot
        data={[
          {
            type: "bar",
            x: symbols,
            y: quantities,
            marker: { color: "rgb(34, 150, 243)" },
          },
        ]}
        layout={{
          title: "Current Holdings",
          xaxis: { title: "Symbol" },
          yaxis: { title: "Quantity" },
          autosize: true,
        }}
        style={{ width: "100%", height: "400px" }}
      />

      <h2 className="text-2xl mt-10 mb-3">Recent Trades</h2>
      <ul>
        {recentTrades.length > 0 ? (
          recentTrades.map((t, i) => (
            <li key={i}>
              {t.timestamp} — {t.action} {t.quantity} {t.symbol} @ ${t.price}
            </li>
          ))
        ) : (
          <li>No recent trades found.</li>
        )}
      </ul>
    </div>
  );
};

export default Dashboard;
