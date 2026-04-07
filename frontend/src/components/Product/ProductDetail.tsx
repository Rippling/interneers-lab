import React from "react";
import { Product } from "../../types/Product";
import "./ProductDetail.css";

type Props = {
  product: Product;
  onClose: () => void;
};

const ProductDetail = ({ product, onClose }: Props) => {
  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal-content" onClick={(e) => e.stopPropagation()}>
        <button className="modal-close" onClick={onClose}>
          ✕
        </button>
        <div className="product-card">
          <div className="product-info">
            <h2 className="product-title">
              {product.brand} - {product.name}
            </h2>
            <p className="product-price">₹{product.price}</p>
            <p className="product-description">{product.description}</p>
          </div>
        </div>
      </div>
    </div>
  );
};
export default ProductDetail;
