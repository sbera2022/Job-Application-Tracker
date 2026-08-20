import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import "./LoginPage.css";

import api from "../api/api";

function LoginPage() {
  const navigate = useNavigate();

  const [formData, setFromData] = useState({
    email: "",
    password: "",
  });

  const [error, setError] = useState("");
  const [isSubmitting, setIsSubmitting] = useState(false);

  function handleChange(event) {
    const { name, value } = event.target;

    setFromData((current) => ({
      ...current,
      [name]: value,
    }));
  }

  async function handleSubmit(event) {
    event.preventDefault();
    setError("");
    setIsSubmitting(true);

    try {
      const response = await api.post("/auth/login", formData);

      localStorage.setItem("accessToken", response.data.access_token);

      navigate("/dashboard");
    } catch (requestError) {
      setError(
        requestError.response?.data?.error ??
          "Unable to log in. Please try again.",
      );
    } finally {
      setIsSubmitting(false);
    }
  }

  return (
    <section>
      <h1 className="welcome-text">Welcome to 💼Job Application Tracker🔎</h1>

      <div className="outline">
        <h1 className="text">Log in</h1>

        <form onSubmit={handleSubmit}>
          <div className="form-field">
            <label htmlFor="email">Email</label>
            <input
              className="input-login"
              id="email"
              name="email"
              type="email"
              value={formData.email}
              onChange={handleChange}
              required
            />
          </div>

          <div className="form-field">
            <label htmlFor="password">Password</label>
            <input
              className="input-login"
              id="password"
              name="password"
              type="password"
              value={formData.password}
              onChange={handleChange}
              required
            />
          </div>

          <button
            type="submit"
            disabled={isSubmitting}
            className="log-in-button"
          >
            {isSubmitting ? "Logging in..." : "Log in"}
          </button>
        </form>
        {error && (
          <span style={{ color: "red", fontSize: "12px" }}>{error}</span>
        )}

        <p>
          No account? <Link to="/register">Register</Link>
        </p>
      </div>
    </section>
  );
}

export default LoginPage;
