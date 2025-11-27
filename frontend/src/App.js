import { useEffect, useState } from "react";
import axios from "axios";

function App() {
  const [prices, setPrices] = useState({});
  const [loading, setLoading] = useState(false);

  const fetchPrices = async () => {
    try {
      const res = await axios.get(
        "http://localhost:5000/api/prices?symbols=BTC,ETH,AAPL,TSLA"
      );
      setPrices(res.data.prices || {});
    } catch (err) {
      console.error("Error fetching prices:", err);
    }
  };

  // Run fetchPrices every 5 seconds
  useEffect(() => {
    fetchPrices(); // run immediately when page loads
    const interval = setInterval(fetchPrices, 5000); // repeat every 5s
    return () => clearInterval(interval); // cleanup
  }, []);

  return (
    <div style={{ padding: 20 }}>
      <h1>Live Crypto + Stock Prices</h1>

      {loading && Object.keys(prices).length === 0 && (
        <p>Loading...</p>
      )}

      {Object.keys(prices).length === 0 && !loading && (
        <p>No data yet...</p>
      )}

      {Object.keys(prices).length > 0 && (
        <table border="1" cellPadding="10">
          <thead>
            <tr>
              <th>Symbol</th>
              <th>Price</th>
            </tr>
          </thead>
          <tbody>
            {Object.entries(prices).map(([sym, price]) => (
              <tr key={sym}>
                <td>{sym}</td>
                <td>${price.toLocaleString()}</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
}

export default App;
