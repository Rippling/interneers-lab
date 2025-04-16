import { useState } from "react";
import { products } from "../data/products";
import ProductItem from "./ProductItem";
import "../styles.css";

const ProductList = () => {
  const [expandedId, setExpandedId] = useState<number | null>(null);

  return (
    <div className="product-list">
      {products.map((product) => (
        <ProductItem
          key={product.id}
          product={product}
          expanded={product.id === expandedId}
          onClick={() =>
            setExpandedId(product.id === expandedId ? null : product.id)
          }
        />
      ))}
    </div>
  );
};

export default ProductList;
