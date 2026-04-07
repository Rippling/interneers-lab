import React from "react";
import { useNavigate } from "react-router-dom";
import { Product } from "../../types/Product";
import "./ProductCard.css";

type Props = {
  product: Product;
  categoryTitle?: string;
};

const ProductCard = ({ product, categoryTitle }: Props) => {
  const navigate = useNavigate();

  return (
    <div
      className="product-card"
      onClick={() => navigate(`/products/${product.id}`)}
    >
      <h3>{product.name}</h3>

      <p className="brand">{product.brand}</p>

      <p className="price">₹ {product.price ?? "N/A"}</p>

      <div className="category-tag">{categoryTitle || "Uncategorized"}</div>
    </div>
  );
};

export default ProductCard;
