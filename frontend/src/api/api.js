import axios from "axios";

export async function fetchPrices() {
  const res = await axios.get("http://localhost:5000/api/prices");
  return res.data;
}
