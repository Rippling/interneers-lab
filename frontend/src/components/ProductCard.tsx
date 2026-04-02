import React from "react";

export interface Product {
  id: number;
  name: string;
  brand: string;
  price: number;
  quantity: number;
  description: string;
  category: string;
}

interface ProductCardProps {
  product: Product;
  isExpanded: boolean;
  onClick: () => void;
}

function ProductCard({ product, isExpanded, onClick }: ProductCardProps) {
  return (
    <article
      className={`product-card ${isExpanded ? "expanded" : ""}`}
      onClick={onClick}
    >
      <div className="product-card__summary">
        <h2>{product.name}</h2>
        <p>
          <strong>Brand:</strong> {product.brand}
        </p>
        <p>
          <strong>Price:</strong> Rs. {product.price}
        </p>
      </div>

      {isExpanded && (
        <div className="product-card__details">
          <p>
            <strong>Quantity:</strong> {product.quantity}
          </p>
          <p>
            <strong>Category:</strong> {product.category}
          </p>
          <p>
            <strong>Description:</strong> {product.description}
          </p>
        </div>
      )}
    </article>
  );
}

export default ProductCard;
