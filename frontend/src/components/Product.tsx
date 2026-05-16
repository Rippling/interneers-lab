/**
 * Product — displays a single product's full details.
 * Shows the product image if image_url is set, otherwise a placeholder.
 */

import React from "react";
import type { Product as ProductType } from "../types";
import "./Product.css";

interface Props {
  product: ProductType;
  onClose?: () => void;
  onEdit?: (product: ProductType) => void;
  onDelete?: (product: ProductType) => void;
}

function formatPrice(price: number): string {
  return "$" + price.toFixed(2);
}

export default function Product({ product, onClose, onEdit, onDelete }: Props) {
  const isLowStock = product.quantity <= 5;

  return (
    <div className="product-detail">
      <div className="product-detail-header">
        <div className="product-detail-category">{product.category?.title ?? "Uncategorized"}</div>
        <div className="product-detail-header-actions">
          {onEdit && (
            <button className="btn-edit" onClick={() => onEdit(product)}>
              Edit
            </button>
          )}
          {onDelete && (
            <button className="btn-delete" onClick={() => onDelete(product)}>
              Delete
            </button>
          )}
          {onClose && (
            <button className="product-detail-close" onClick={onClose}>
              ✕
            </button>
          )}
        </div>
      </div>

      {/* Product image */}
      <div className="product-detail-image-wrap">
        {product.image_url ? (
          <img
            src={product.image_url}
            alt={product.name}
            className="product-detail-image"
            onError={(e) => {
              (e.target as HTMLImageElement).style.display = "none";
              (e.target as HTMLImageElement).nextElementSibling?.classList.remove("hidden");
            }}
          />
        ) : null}
        <div className={`product-detail-image-placeholder ${product.image_url ? "hidden" : ""}`}>
          <span className="product-detail-image-icon">📦</span>
          <span className="product-detail-image-label">No image</span>
        </div>
      </div>

      <h2 className="product-detail-name">{product.name}</h2>
      <p className="product-detail-desc">{product.description}</p>

      <div className="product-detail-grid">
        <div className="product-detail-stat">
          <span className="product-detail-stat-label">Price</span>
          <span className="product-detail-stat-value accent">{formatPrice(product.price)}</span>
        </div>
        <div className="product-detail-stat">
          <span className="product-detail-stat-label">Brand</span>
          <span className="product-detail-stat-value">{product.brand}</span>
        </div>
        <div className="product-detail-stat">
          <span className="product-detail-stat-label">In Stock</span>
          <span className={`product-detail-stat-value ${isLowStock ? "danger" : ""}`}>
            {product.quantity}
            {isLowStock && <span className="low-stock-badge">LOW</span>}
          </span>
        </div>
        <div className="product-detail-stat">
          <span className="product-detail-stat-label">ID</span>
          <span className="product-detail-stat-value muted">{product.id}</span>
        </div>
      </div>

      <div className="product-detail-dates">
        <span>Added {new Date(product.created_at).toLocaleDateString()}</span>
        <span>Updated {new Date(product.updated_at).toLocaleDateString()}</span>
      </div>
    </div>
  );
}
