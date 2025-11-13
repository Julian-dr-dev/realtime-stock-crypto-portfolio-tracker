import React, { useEffect, useState } from "react";
import Plot from "react-plotly.js";

const Dashboard = () => {
  const [portfolioValue, setPortfolioValue] = useState(null);
  const [holdings, setHoldings] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch("http://127.0.0.1:5000/api/portfolio")
      .then((res) => res.json())
      .then((data) => {
        setPortfolioValue(data.total_value || 0);
        setHoldings(data.holdings || []);
        setLoading(false);
      })
      .catch((err) => {
        console.error("Error fetching portfolio:", err);
        setLoading(false);
      });
  }, []);

  if (loading) return <h3>Loading portfolio...</h3>;

  return (
    <div style={{ padding: "2rem" }}>
      <h1>📊 Portfolio Dashboard</h1>
      <h2>
        Total Portfolio Value: $
        {portfolioValue !== null ? portfolioValue.toFixed(2) : "0.00"}
      </h2>

      {holdings.length > 0 ? (
        <Plot
          data={[
            {
              x: holdings.map((h) => h.symbol),
              y: holdings.map((h) => h.value),
              type: "bar",
            },
          ]}
          layout={{ title: "Holdings Breakdown" }}
          style={{ width: "100%", height: "400px" }}
        />
      ) : (
        <p>No holdings to display.</p>
      )}
    </div>
  );
};

export default Dashboard;
