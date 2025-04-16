import React from "react";
import "../styles.css";

interface Product {
  id: number;
  name: string;
  price: number;
  description: string;
  image: string;
}

interface ProductItemProps {
  product: Product;
  expanded: boolean;
  onClick: () => void;
}

const ProductItem: React.FC<ProductItemProps> = ({
  product,
  expanded,
  onClick,
}) => {
  return (
    <div className="product-card" onClick={onClick}>
      <img src={product.image} alt={product.name} />
      <div className="product-info">
        <div className="product-title">{product.name}</div>
        <div className="product-description">{product.description}</div>
        <div className="product-price">${product.price}</div>

        <div className={`product-details ${expanded ? "show" : ""}`}>
          <p>Additional details about {product.name}...</p>
        </div>
      </div>
    </div>
  );
};

export default ProductItem;
