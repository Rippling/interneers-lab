import React, { useState } from "react";
import { MOCK_PRODUCTS } from "./MOCK_PRODUCTS";
import ProductDetail from "../Product/ProductDetail";
import { Product } from "../../types/Product";

const ProductList = () => {
  const [selectedProduct, setSelectedProduct] = useState<Product | null>(null);

  return (
    <div>
      <h1>Products</h1>

      {MOCK_PRODUCTS.map((prod) => (
        <div
          key={prod.id}
          onClick={() => setSelectedProduct(prod)}
          style={{
            cursor: "pointer",
            border: "1px solid #ddd",
            padding: "10px",
            margin: "10px",
          }}
        >
          {prod.name}
        </div>
      ))}

      {selectedProduct && (
        <ProductDetail
          product={selectedProduct}
          onClose={() => setSelectedProduct(null)}
        />
      )}
    </div>
  );
};

export default ProductList;
