import React from "react";
import { useNavigate } from "react-router-dom";
import { useCategories } from "../../context/CategoryContext";
import "./Categories.css";

const Categories = () => {
  const navigate = useNavigate();
  const { categories, loading } = useCategories();

  if (loading) {
    return <p className="loading-text">Loading categories...</p>;
  }

  return (
    <div className="categories-container">
      <h2>All Categories</h2>

      <div className="categories-grid">
        {categories.map((c) => (
          <div
            key={c.id}
            className="category-card"
            onClick={() => navigate(`/categories/${c.id}`)}
          >
            <h3>{c.title}</h3>
            <p>{c.description || "No description available"}</p>
          </div>
        ))}
      </div>
    </div>
  );
};

export default Categories;
