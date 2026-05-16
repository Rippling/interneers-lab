/**
 * ProductList — renders a grid of product cards.
 * Clicking a card expands inline to show full product details.
 * Cards now show a product image thumbnail if image_url is set.
 */

import React, { useState } from "react";
import type { Product } from "../types";
import ProductDetail from "./Product";
import "./ProductList.css";

interface Props {
  products: Product[];
  loading?: boolean;
  emptyMessage?: string;
  onEdit?: (product: Product) => void;
  onDelete?: (product: Product) => void;
}

function ProductCard({
  product,
  isSelected,
  onClick,
}: {
  product: Product;
  isSelected: boolean;
  onClick: () => void;
}) {
  const [imgError, setImgError] = useState(false);

  return (
    <div
      className={`product-card ${isSelected ? "selected" : ""}`}
      onClick={onClick}
      role="button"
      tabIndex={0}
      onKeyDown={(e) => e.key === "Enter" && onClick()}
      aria-expanded={isSelected}
    >
      {/* Thumbnail */}
      <div className="product-card-image-wrap">
        {product.image_url && !imgError ? (
          <img
            src={product.image_url}
            alt={product.name}
            className="product-card-image"
            onError={() => setImgError(true)}
          />
        ) : (
          <div className="product-card-image-placeholder">📦</div>
        )}
      </div>

      <div className="product-card-category">
        {product.category?.title ?? "Uncategorized"}
      </div>
      <div className="product-card-name">{product.name}</div>
      <div className="product-card-desc">{product.description}</div>
      <div className="product-card-footer">
        <span className="product-card-price">${product.price.toFixed(2)}</span>
        <span className={`product-card-stock ${product.quantity <= 5 ? "low" : ""}`}>
          <span className="stock-dot" />
          {product.quantity} in stock
        </span>
      </div>
      <div className="product-card-expand-hint">
        {isSelected ? "▲ collapse" : "▼ details"}
      </div>
    </div>
  );
}

export default function ProductList({
  products,
  loading = false,
  emptyMessage = "No products found",
  onEdit,
  onDelete,
}: Props) {
  const [selectedId, setSelectedId] = useState<string | null>(null);

  const selectedProduct = products.find((p) => p.id === selectedId) ?? null;

  function handleCardClick(id: string) {
    setSelectedId((prev) => (prev === id ? null : id));
  }

  if (loading) {
    return (
      <div className="product-list-grid">
        {Array.from({ length: 6 }).map((_, i) => (
          <div key={i} className="product-card-skeleton" />
        ))}
      </div>
    );
  }

  if (products.length === 0) {
    return (
      <div className="product-list-empty">
        <div className="product-list-empty-icon">◈</div>
        <div className="product-list-empty-text">{emptyMessage}</div>
      </div>
    );
  }

  return (
    <div className="product-list-wrap">
      <div className="product-list-grid">
        {products.map((product) => (
          <ProductCard
            key={product.id}
            product={product}
            isSelected={selectedId === product.id}
            onClick={() => handleCardClick(product.id)}
          />
        ))}
      </div>

      {selectedProduct && (
        <ProductDetail
          product={selectedProduct}
          onClose={() => setSelectedId(null)}
          onEdit={onEdit}
          onDelete={onDelete}
        />
      )}
    </div>
  );
}
