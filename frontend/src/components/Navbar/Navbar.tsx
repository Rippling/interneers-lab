import React from "react";
import { useNavigate, useLocation } from "react-router-dom";
import "./Navbar.css";

const Navbar = () => {
  const navigate = useNavigate();
  const location = useLocation();

  const isActive = (path: string) => location.pathname === path;
  return (
    <nav className="navbar">
      <div className="navbar-logo" onClick={() => navigate("/")}>
        ProductAPI
      </div>

      <div className="navbar-links">
        <button
          className={`nav-btn ${isActive("/products") ? "active" : ""}`}
          onClick={() => navigate("/products")}
        >
          View Products
        </button>

        <button
          className={`nav-btn ${isActive("/categories") ? "active" : ""}`}
          onClick={() => navigate("/categories")}
        >
          View Categories
        </button>
      </div>
    </nav>
  );
};

export default Navbar;
