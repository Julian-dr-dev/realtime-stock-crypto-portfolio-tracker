import React from "react";
import ReactDOM from "react-dom/client";
import App from "./App";   // ← THIS MUST MATCH your real file

const root = ReactDOM.createRoot(document.getElementById("root"));
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
