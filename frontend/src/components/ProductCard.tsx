import React from "react";
import { Link } from "react-router-dom";

export interface ProductCardType {
  id: string;
  name: string;
  brand: string;
  price: number;
  quantity: number;
  description: string;
  categoryId: string | null;
  categoryName: string;
}

interface ProductCardProps {
  product: ProductCardType;
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
            <strong>Category:</strong>{" "}
            {product.categoryId ? (
              <Link className="inline-link" to={`/categories/${product.categoryId}`}>
                {product.categoryName}
              </Link>
            ) : (
              "No Category"
            )}
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

