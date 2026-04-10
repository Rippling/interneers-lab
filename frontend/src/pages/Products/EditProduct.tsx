import React, { useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import { useCategories } from "../../context/CategoryContext";
import "./CreateProduct.css";

const PRODUCT_URL = "http://127.0.0.1:8001/api/product/";

const EditProduct = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const { categories, loading: categoryLoading } = useCategories();

  const [form, setForm] = useState({
    name: "",
    price: "",
    brand: "",
    category: "",
  });

  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);

  useEffect(() => {
    const fetchProduct = async () => {
      try {
        const res = await fetch(`${PRODUCT_URL}${id}/`);
        const data = await res.json();

        setForm({
          name: data.name || "",
          price: data.price?.toString() || "",
          brand: data.brand || "",
          category: data.category || "",
        });
      } catch (err) {
        console.error(err);
      } finally {
        setLoading(false);
      }
    };

    fetchProduct();
  }, [id]);

  const handleChange = (
    e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>,
  ) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setSaving(true);

    try {
      await fetch(`${PRODUCT_URL}${id}/`, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          name: form.name,
          price: Number(form.price),
          brand: form.brand,
        }),
      });

      if (form.category) {
        await fetch(
          `http://127.0.0.1:8001/api/categories/${form.category}/products/`,
          {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ id }),
          },
        );
      }

      navigate(`/products/${id}`);
    } catch (err) {
      console.error("Error updating product", err);
    } finally {
      setSaving(false);
    }
  };

  if (loading || categoryLoading) {
    return <p className="loading-text">Loading...</p>;
  }

  return (
    <div className="create-product-container">
      <h2>Edit Product</h2>

      <form onSubmit={handleSubmit} className="create-product-form">
        <input
          type="text"
          name="name"
          value={form.name}
          onChange={handleChange}
          required
        />

        <input
          type="number"
          name="price"
          value={form.price}
          onChange={handleChange}
          required
        />

        <input
          type="text"
          name="brand"
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

        <button type="submit" disabled={saving}>
          {saving ? "Updating..." : "Update Product"}
        </button>
      </form>
    </div>
  );
};

export default EditProduct;
