import { useState } from "react";
import { useNavigate } from "react-router-dom";
import "./RegisterPage.css";

import api from "../api/api";

function RegisterPage() {
  const navigate = useNavigate();
  const [successMessage, setSuccessMessage] = useState("");

  const [formData, setFormData] = useState({
    first_name: "",
    last_name: "",
    email: "",
    password: "",
  });

  const [error, setError] = useState({});
  const [apiError, setApiError] = useState("");
  const [submitted, setSubmitted] = useState(false);

  function handleChange(event) {
    const { name, value } = event.target;

    setFormData((current) => ({
      ...current,
      [name]: value,
    }));
  }

  function validatePage() {
    let localErrors = {};
    const emailinput = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

    if (!formData.first_name.trim()) {
      localErrors.first_name = "First Name is required";
    }
    if (!formData.last_name.trim()) {
      localErrors.last_name = "Last Name is required";
    }
    if (!formData.email) {
      localErrors.email = "Email is required";
    } else if (!emailinput.test(formData.email)) {
      localErrors.email = "Invalid email format";
    }
    if (!formData.password) {
      localErrors.password = "Password is required";
    } else if (formData.password.length < 6) {
      localErrors.password = "Password must be at least 6 characters";
    }

    setError(localErrors);
    return Object.keys(localErrors).length === 0;
  }

  async function handleSubmit(event) {
    event.preventDefault();

    if (validatePage()) {
      try {
        const response = await api.post("/auth/register", formData);

        const isSuccessful = true;

        if (isSuccessful) {
          setSuccessMessage("Registration successful!");

          setTimeout(() => setSuccessMessage(""), 3000);
        }

        setSubmitted(true);
        setApiError("");
        navigate("/login");
      } catch (requestError) {
        setApiError(
          requestError.response?.data?.error ??
            "Registration failed. Please try again.",
        );
        setSubmitted(false);
      }
    }
  }

  return (
    <section>
      <h1 className="welcome-text">Welcome to 💼Job Application Tracker🔎</h1>

      <div className="page">
        <h1 className="text">Register</h1>
        {submitted && <p>Registration successful!</p>}
        <form onSubmit={handleSubmit}>
          <div className="f-field">
            <label htmlFor="email">Email</label>
            <input
              id="email"
              name="email"
              type="email"
              className="input"
              value={formData.email}
              onChange={handleChange}
              required
            />
            {error.email && (
              <span style={{ color: "red", fontSize: "12px" }}>
                {error.email}
              </span>
            )}
          </div>

          <div className="f-field">
            <label htmlFor="password">Password</label>
            <input
              id="password"
              name="password"
              type="password"
              className="input"
              value={formData.password}
              onChange={handleChange}
              required
            />
            {error.password && (
              <span style={{ color: "red", fontSize: "12px" }}>
                {error.password}
              </span>
            )}
          </div>

          <div className="f-field">
            <label htmlFor="first_name">First Name</label>
            <input
              id="first_name"
              name="first_name"
              type="text"
              className="input"
              value={formData.first_name}
              onChange={handleChange}
              required
            />
            {error.first_name && (
              <span style={{ color: "red", fontSize: "12px" }}>
                {error.first_name}
              </span>
            )}
          </div>

          <div className="f-field">
            <label htmlFor="last_name">Last Name</label>
            <input
              id="last_name"
              name="last_name"
              type="text"
              className="input"
              value={formData.last_name}
              onChange={handleChange}
              required
            />
            {error.last_name && (
              <span style={{ color: "red", fontSize: "12px" }}>
                {error.last_name}
              </span>
            )}
          </div>

          {apiError && (
            <span style={{ color: "red", fontSize: "12px" }}>{apiError}</span>
          )}
          {successMessage && (
            <div className="success-display">{successMessage}</div>
          )}
          <button type="submit" className="sign-up-button">
            Sign Up
          </button>
        </form>
      </div>
    </section>
  );
}

export default RegisterPage;
