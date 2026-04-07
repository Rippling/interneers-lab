import React from "react";
import { useNavigate } from "react-router-dom";
import "./Home.css";

const Home = () => {
  const navigate = useNavigate();
  return (
    <div className="home-container">
      <div className="home-card">
        <h1>Welcome to ProductAPI Dashboard!</h1>

        <p>
          This is a full-stack warehouse management system built using{" "}
          <strong>Django</strong>, <strong>MongoDB</strong>, and{" "}
          <strong>React</strong>.
        </p>

        <p>
          You can explore products, filter and sort them, manage categories, and
          dynamically assign products to categories using REST APIs.
        </p>

        <div className="home-buttons">
          <button
            className="home-btn primary"
            onClick={() => navigate("/products")}
          >
            View Products
          </button>

          <button
            className="home-btn secondary"
            onClick={() => navigate("/categories")}
          >
            View Categories
          </button>
        </div>
      </div>
    </div>
  );
};

export default Home;
