import { useEffect, useState } from "react";
import axios from "axios";

function App() {
  const [prices, setPrices] = useState({});
  const [loading, setLoading] = useState(true);

  const fetchPrices = async () => {
    try {
      const res = await axios.get("http://localhost:5000/api/prices");
      setPrices(res.data);
    } catch (err) {
      console.error("Error fetching prices:", err);
    }
    setLoading(false);
  };

  // Auto-refresh every 5 seconds
  useEffect(() => {
    fetchPrices();
    const interval = setInterval(fetchPrices, 5000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div style={{ padding: "20px", fontFamily: "Arial" }}>
      <h1>Live Price Table</h1>

      {loading && <p>Loading...</p>}

      {!loading && (
        <table
          style={{
            borderCollapse: "collapse",
            width: "50%",
            marginTop: "20px",
          }}
        >
          <thead>
            <tr>
              <th style={{ border: "1px solid #ccc", padding: "8px" }}>
                Symbol
              </th>
              <th style={{ border: "1px solid #ccc", padding: "8px" }}>
                Price
              </th>
            </tr>
          </thead>

          <tbody>
            {Object.entries(prices).map(([symbol, price]) => (
              <tr key={symbol}>
                <td style={{ border: "1px solid #ccc", padding: "8px" }}>
                  {symbol}
                </td>
                <td style={{ border: "1px solid #ccc", padding: "8px" }}>
                  ${price.toLocaleString()}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
}

export default App;
