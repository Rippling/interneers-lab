import React, { useEffect, useState } from "react";
import ProductCard from "../../components/Product/ProductCard";
import { Product } from "../../types/Product";
import { useCategories } from "../../context/CategoryContext";
import "./Products.css";

const PRODUCT_URL = "http://127.0.0.1:8001/api/product/";

const Products = () => {
  const [products, setProducts] = useState<Product[]>([]);
  const [sort, setSort] = useState<"asc" | "desc">("desc");
  const [loading, setLoading] = useState(true);

  const [page, setPage] = useState(1);

  const [minPrice, setMinprice] = useState(0);
  const [maxPrice, setMaxprice] = useState<number | null>(null);
  const [name, setName] = useState("");
  const [brand, setBrand] = useState("");

  const { categoryMap, loading: categoryLoading } = useCategories();

  const fetchProducts = async () => {
    setLoading(true);
    try {
      const query = new URLSearchParams();

      query.append("sortby", sort);
      query.append("page", page.toString());

      if (name) query.append("name", name);
      if (brand) query.append("brand", brand);
      if (minPrice) query.append("min_price", minPrice.toString());
      if (maxPrice !== null) query.append("max_price", maxPrice.toString());

      const res = await fetch(`${PRODUCT_URL}?${query.toString()}`);
      const data = await res.json();

      setProducts(data);
    } catch (err) {
      console.error("Error fetching products", err);
    }
    setLoading(false);
  };

  useEffect(() => {
    const delay = setTimeout(() => {
      fetchProducts();
    }, 400);

    return () => clearTimeout(delay);
  }, [sort, page, name, brand, minPrice, maxPrice]);

  useEffect(() => {
    setPage(1);
  }, [name, brand, minPrice, maxPrice]);

  if (loading || categoryLoading) {
    return <p className="loading">Loading products...</p>;
  }

  return (
    <div className="products-container">
      <div className="products-header">
        <h2>All Products</h2>

        <div className="controls">
          <select
            value={sort}
            onChange={(e) => setSort(e.target.value as "asc" | "desc")}
          >
            <option value="desc">Newest First</option>
            <option value="asc">Oldest First</option>
          </select>

          <div className="filter-form">
            <input
              type="text"
              placeholder="Search name..."
              value={name}
              onChange={(e) => setName(e.target.value)}
            />

            <input
              type="text"
              placeholder="Search brand..."
              value={brand}
              onChange={(e) => setBrand(e.target.value)}
            />

            <input
              type="number"
              placeholder="Min ₹"
              value={minPrice}
              onChange={(e) => setMinprice(Number(e.target.value))}
            />

            <input
              type="number"
              placeholder="Max ₹"
              value={maxPrice ?? ""}
              onChange={(e) =>
                setMaxprice(e.target.value ? Number(e.target.value) : null)
              }
            />
          </div>
        </div>
      </div>

      <div className="products-grid">
        {products.length === 0 ? (
          <p className="no-products">No products found.</p>
        ) : (
          products.map((p) => (
            <ProductCard
              key={p.id}
              product={p}
              categoryTitle={
                p.category ? categoryMap.get(p.category)?.title : undefined
              }
            />
          ))
        )}
      </div>

      <div className="pagination">
        <button
          disabled={page === 1}
          onClick={() => setPage((prev) => prev - 1)}
        >
          ← Prev
        </button>

        <span>Page {page}</span>

        <button
          disabled={products.length === 0}
          onClick={() => setPage((prev) => prev + 1)}
        >
          Next →
        </button>
      </div>
    </div>
  );
};

export default Products;
