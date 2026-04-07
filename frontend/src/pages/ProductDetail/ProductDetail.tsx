import React, { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { Product } from "../../types/Product";
import { useCategories } from "../../context/CategoryContext";
import "./ProductDetail.css";

const PRODUCT_URL = "http://127.0.0.1:8001/api/product/";

const ProductDetail = () => {
  const { id } = useParams();
  const navigate = useNavigate();

  const [product, setProduct] = useState<Product | null>(null);
  const [loading, setLoading] = useState(true);
  const [updating, setUpdating] = useState(false);

  const { categories, categoryMap, loading: categoryLoading } = useCategories();

  const fetchProduct = async () => {
    setLoading(true);
    try {
      const res = await fetch(`${PRODUCT_URL}${id}/`);
      const data = await res.json();

      setProduct({
        ...data,
        id: data.id || data._id,
      });
    } catch (err) {
      console.error("Error fetching product", err);
    }
    setLoading(false);
  };

  useEffect(() => {
    fetchProduct();
  }, [id]);

  const handleCategoryChange = async (categoryId: string) => {
    if (!product) return;

    setUpdating(true);

    try {
      await fetch(
        `http://127.0.0.1:8001/api/categories/${categoryId}/products/`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({ id: product.id }),
        },
      );

      fetchProduct();
    } catch (err) {
      console.error("Error updating category", err);
    }

    setUpdating(false);
  };

  if (loading || categoryLoading) {
    return <p className="loading-text">Loading product...</p>;
  }

  if (!product) {
    return <p>Product not found</p>;
  }

  const category = product.category ? categoryMap.get(product.category) : null;

  return (
    <div className="detail-container">
      <div className="detail-card">
        <h2>{product.name}</h2>

        <p className="brand">{product.brand}</p>

        <p className="price">₹ {product.price ?? "N/A"}</p>

        <p className="description">
          {product.description || "No description available."}
        </p>

        <div className="category-section">
          <span className="label">Category:</span>

          {category ? (
            <span
              className="category-link"
              onClick={() => navigate(`/categories/${category.id}`)}
            >
              {category.title}
            </span>
          ) : (
            <span className="uncategorized">Uncategorized</span>
          )}
        </div>

        <div className="edit-section">
          <label>Change Category:</label>

          <select
            disabled={updating}
            value={product.category || ""}
            onChange={(e) => handleCategoryChange(e.target.value)}
          >
            <option value="">Uncategorized</option>
            {categories.map((c) => (
              <option key={c.id} value={c.id}>
                {c.title}
              </option>
            ))}
          </select>
        </div>

        {updating && <p className="updating-text">Updating...</p>}
      </div>
    </div>
  );
};

export default ProductDetail;
