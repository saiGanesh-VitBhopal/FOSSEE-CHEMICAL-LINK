import React from "react";
import { createRoot } from "react-dom/client";
import App from "./App.jsx";
import Login from "./Login.jsx";
import "bootstrap/dist/css/bootstrap.min.css";

function Wrapper() {
  const [loggedIn, setLoggedIn] = React.useState(false);

  return loggedIn ? (
    <App onLogout={() => setLoggedIn(false)} />
  ) : (
    <Login onLogin={() => setLoggedIn(true)} />
  );
}

createRoot(document.getElementById("root")).render(
  <React.StrictMode>
    <Wrapper />
  </React.StrictMode>
);
