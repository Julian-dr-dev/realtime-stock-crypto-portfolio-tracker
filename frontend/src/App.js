import { useState } from "react";
import axios from "axios";

function App() {
  const [prices, setPrices] = useState(null);
  const [loading, setLoading] = useState(false);

  const fetchPrices = async () => {
    setLoading(true);
    try {
      const res = await axios.get("http://localhost:5000/api/prices");
      setPrices(res.data);
    } catch (err) {
      console.error("Error fetching prices:", err);
    }
    setLoading(false);
  };

  return (
    <div style={{ padding: 20 }}>
      <h1>Frontend → Backend Test</h1>

      <button
        onClick={fetchPrices}
        style={{
          padding: "10px 20px",
          background: "blue",
          color: "white",
          border: "none",
          borderRadius: "6px",
          cursor: "pointer"
        }}
      >
        Test Backend Call
      </button>

      {loading && <p>Loading...</p>}

      {prices && (
        <pre>{JSON.stringify(prices, null, 2)}</pre>
      )}
    </div>
  );
}

export default App;
