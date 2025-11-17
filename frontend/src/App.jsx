import { useEffect, useState } from "react";

function App() {
  const [prices, setPrices] = useState({});
  const [loading, setLoading] = useState(true);

  // Fetch prices from backend
  const fetchPrices = async () => {
    try {
      const response = await fetch(
        "http://localhost:5000/api/prices?symbols=AAPL,TSLA,BTC-USD"
      );
      const data = await response.json();
      setPrices(data);
      setLoading(false);
    } catch (err) {
      console.error("Error fetching prices:", err);
      setLoading(false);
    }
  };

  // Fetch once on load
  useEffect(() => {
    fetchPrices();

    // Fetch every 5 seconds (real-time updates)
    const interval = setInterval(fetchPrices, 5000);
    return () => clearInterval(interval);
  }, []);

  if (loading) return <h2>Loading prices…</h2>;

  return (
    <div style={{ padding: "20px", fontFamily: "Arial" }}>
      <h1>Real-Time Price Tracker</h1>
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
              <td>{price}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default App;
