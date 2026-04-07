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

  const { categoryMap, loading: categoryLoading } = useCategories();

  const fetchProducts = async () => {
    setLoading(true);
    try {
      const res = await fetch(`${PRODUCT_URL}?sortby=${sort}`); //TODO: implement various filteting implemented in backend
      const data = await res.json();

      setProducts(data); //TODO: handle pagination
    } catch (err) {
      console.error("Error fetching products", err);
    }
    setLoading(false);
  };

  useEffect(() => {
    fetchProducts();
  }, [sort]);

  if (loading || categoryLoading) {
    return <p>LOADING...</p>; //TODO: create a spinner;
  }

  return (
    <div className="products-container">
      <div className="products-header">
        <h2>All Products</h2>

        <select
          value={sort}
          onChange={(e) => setSort(e.target.value as "asc" | "desc")}
        >
          <option value="desc">Newest First</option>
          <option value="asc">Oldest First</option>
        </select>
      </div>

      <div className="products-grid">
        {products.length === 0 ? (
          <p>No products found.</p>
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
    </div>
  );
};

export default Products;
