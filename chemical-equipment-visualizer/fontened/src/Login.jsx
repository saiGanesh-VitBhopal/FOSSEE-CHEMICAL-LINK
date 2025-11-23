// Login.jsx
import { useState } from "react";
import "bootstrap/dist/css/bootstrap.min.css";

export default function Login({ onLogin }) {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const submitForm = (e) => {
    e.preventDefault();

    // Dummy check (you can replace it with your backend later)
    if (email.trim() === "" || password.trim() === "") {
      alert("Please enter both fields");
      return;
    }

    // Pass data back to App if needed
    if (onLogin) onLogin({ email });
  };

  return (
    <div className="d-flex justify-content-center align-items-center vh-100 bg-light">
      <div
        className="card shadow p-4"
        style={{ width: "380px", borderRadius: "12px" }}
      >
        <h3 className="text-center mb-4">Login</h3>

        <form onSubmit={submitForm}>
          {/* Email */}
          <div className="mb-3">
            <label className="form-label">User Name</label>
            <input
              type=""
              className="form-control"
              placeholder="Enter your username"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
            />
          </div>

          {/* Password */}
          <div className="mb-3">
            <label className="form-label">Password</label>
            <input
              type="password"
              className="form-control"
              placeholder="Enter your password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />
          </div>

          {/* Login Button */}
          <button type="submit" className="btn btn-primary w-100 mt-2">
            Login
          </button>
        </form>

        <p className="text-center text-muted mt-3" style={{ fontSize: "14px" }}>
          © 2025 Chemical Visualizer
        </p>
      </div>
    </div>
  );
}
