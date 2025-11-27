function PriceTable({ prices }) {
  if (!prices) return <p>No data yet...</p>;

  return (
    <table style={{ width: "300px", marginTop: 20, borderCollapse: "collapse" }}>
      <thead>
        <tr>
          <th style={{ borderBottom: "1px solid #ccc", padding: 8 }}>Symbol</th>
          <th style={{ borderBottom: "1px solid #ccc", padding: 8 }}>Price</th>
        </tr>
      </thead>
      <tbody>
        {Object.entries(prices).map(([symbol, price]) => (
          <tr key={symbol}>
            <td style={{ padding: 8 }}>{symbol}</td>
            <td style={{ padding: 8 }}>${price}</td>
          </tr>
        ))}
      </tbody>
    </table>
  );
}

export default PriceTable;
