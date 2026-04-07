import React, { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import ProductCard from "../../components/Product/ProductCard";
import { Product } from "../../types/Product";
import { useCategories } from "../../context/CategoryContext";
import "./CategoryProducts.css";

const CategoryProducts = () => {
  const { categoryId } = useParams();

  const [products, setProducts] = useState<Product[]>([]);
  const [loading, setLoading] = useState(true);

  const { categoryMap } = useCategories();

  const fetchProducts = async () => {
    setLoading(true);
    try {
      const res = await fetch(
        `http://127.0.0.1:8001/api/categories/${categoryId}/products/`,
      );
      const data = await res.json();

      setProducts(data.results || data);
    } catch (err) {
      console.error("Error fetching category products", err);
    }
    setLoading(false);
  };

  useEffect(() => {
    fetchProducts();
  }, [categoryId]);

  const category = categoryId ? categoryMap.get(categoryId) : null;

  if (loading) {
    return <p className="loading-text">Loading products...</p>;
  }

  return (
    <div className="category-products-container">
      <h2>{category ? category.title : "Category"} Products</h2>

      <div className="products-grid">
        {products.length === 0 ? (
          <p>No products in this category.</p>
        ) : (
          products.map((p) => (
            <ProductCard
              key={p.id}
              product={p}
              categoryTitle={category?.title}
            />
          ))
        )}
      </div>
    </div>
  );
};

export default CategoryProducts;
