import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { useCategories } from "../../context/CategoryContext";
import "./CreateProduct.css";

const PRODUCT_URL = "http://127.0.0.1:8001/api/product/";

const CreateProduct = () => {
  const navigate = useNavigate();
  const { categories, loading: categoryLoading } = useCategories();

  const [form, setForm] = useState({
    name: "",
    price: "",
    brand: "",
    category: "",
  });

  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState("");

  const handleChange = (
    e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>,
  ) => {
    setForm({
      ...form,
      [e.target.name]: e.target.value,
    });
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setMessage("");

    try {
      const res = await fetch(PRODUCT_URL, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          name: form.name,
          price: Number(form.price),
          brand: form.brand,
        }),
      });

      if (!res.ok) throw new Error("Failed to create product");

      const data = await res.json();
      const productId = data.id || data._id;

      if (form.category) {
        await fetch(
          `http://127.0.0.1:8001/api/categories/${form.category}/products/`,
          {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ id: productId }),
          },
        );
      }

      setMessage("Product created successfully");

      setTimeout(() => navigate("/products"), 800);
    } catch (err) {
      console.error(err);
      setMessage("Error creating product");
    } finally {
      setLoading(false);
    }
  };

  if (categoryLoading) {
    return <p className="loading-text">Loading categories...</p>;
  }

  return (
    <div className="create-product-container">
      <h2>Create Product</h2>

      <form onSubmit={handleSubmit} className="create-product-form">
        <input
          type="text"
          name="name"
          placeholder="Product Name"
          value={form.name}
          onChange={handleChange}
          required
        />

        <input
          type="number"
          name="price"
          placeholder="Price"
          value={form.price}
          onChange={handleChange}
          required
        />

        <input
          type="text"
          name="brand"
          placeholder="Brand"
          value={form.brand}
          onChange={handleChange}
        />

        <select name="category" value={form.category} onChange={handleChange}>
          <option value="">Uncategorized</option>
          {categories.map((c) => (
            <option key={c.id} value={c.id}>
              {c.title}
            </option>
          ))}
        </select>

        <button type="submit" disabled={loading}>
          {loading ? "Creating..." : "Create Product"}
        </button>
      </form>

      {message && <p className="message">{message}</p>}
    </div>
  );
};

export default CreateProduct;
