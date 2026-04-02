import React from "react";

export interface ProductType {
  id: number;
  name: string;
  brand: string;
  price: number;
  quantity: number;
  category: string;
}

interface ProductProps {
  product: ProductType;
}

function Product({ product }: ProductProps) {
  return (
    <article className="product-card">
      <h2>{product.name}</h2>
      <p>
        <strong>Brand:</strong> {product.brand}
      </p>
      <p>
        <strong>Price:</strong> Rs. {product.price}
      </p>
      <p>
        <strong>Quantity:</strong> {product.quantity}
      </p>
      <p>
        <strong>Category:</strong> {product.category}
      </p>
    </article>
  );
}

export default Product;
