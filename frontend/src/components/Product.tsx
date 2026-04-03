import React, { useState } from "react";
import { Link } from "react-router-dom";

export interface ProductType {
  id: number;
  name: string;
  brand: string;
  price: number;
  quantity: number;
  category: string;
  description: string;
}

interface ProductProps {
  product: ProductType;
  categories: string[];
  onMoveCategory: (productId: number, newCategory: string) => void;
}

function Product({ product, categories, onMoveCategory }: ProductProps) {
  const [selectedCategory, setSelectedCategory] = useState(product.category);

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
        <strong>Category:</strong>{" "}
        <Link className="inline-link" to={`/categories/${product.category}`}>
          {product.category}
        </Link>
      </p>

      <div className="product-card__actions">
        <select
          value={selectedCategory}
          onChange={(event) => setSelectedCategory(event.target.value)}
        >
          {categories.map((category) => (
            <option key={category} value={category}>
              {category}
            </option>
          ))}
        </select>

        <button onClick={() => onMoveCategory(product.id, selectedCategory)}>
          Move Category
        </button>
      </div>

      <Link className="product-link" to={`/products/${product.id}`}>
        Edit Product
      </Link>
    </article>
  );
}

export default Product;
