import { useEffect, useState } from "react";

export default function PriceTable() {
  const [prices, setPrices] = useState({});
  const [loading, setLoading] = useState(true);

  async function fetchPrices() {
    try {
      const response = await fetch("http://localhost:5000/api/prices?symbols=AAPL,BTC-USD,ETH-USD");
      const data = await response.json();
      setPrices(data);
      setLoading(false);
    } catch (err) {
      console.error("Error fetching prices:", err);
    }
  }

  useEffect(() => {
    fetchPrices();          // initial call
    const interval = setInterval(fetchPrices, 5000); // update every 5 seconds
    return () => clearInterval(interval);
  }, []);

  if (loading) return <p>Loading prices…</p>;

  return (
    <div style={{ padding: "20px" }}>
      <h2>Live Prices</h2>
      <table border="1" cellPadding="10">
        <thead>
          <tr>
            <th>Symbol</th>
            <th>Price (USD)</th>
          </tr>
        </thead>
        <tbody>
          {Object.entries(prices).map(([symbol, price]) => (
            <tr key={symbol}>
              <td>{symbol}</td>
              <td>${price.toLocaleString()}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
