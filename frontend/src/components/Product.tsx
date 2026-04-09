import React, { useState } from "react";
import { Link } from "react-router-dom";

export interface CategoryType {
  id: string;
  title: string;
  description: string;
}

export interface ProductType {
  id: string;
  name: string;
  brand: string;
  price: number;
  quantity: number;
  categoryId: string | null;
  categoryName: string;
  description: string;
}

interface ProductProps {
  product: ProductType;
  categories: CategoryType[];
  onMoveCategory: (productId: string, newCategoryId: string) => void;
}

function Product({ product, categories, onMoveCategory }: ProductProps) {
  const [selectedCategory, setSelectedCategory] = useState(
    product.categoryId || "",
  );

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
        {product.categoryId ? (
          <Link
            className="inline-link"
            to={`/categories/${product.categoryId}`}
          >
            {product.categoryName}
          </Link>
        ) : (
          "No Category"
        )}
      </p>

      <div className="product-card__actions">
        <select
          value={selectedCategory}
          onChange={(event) => setSelectedCategory(event.target.value)}
        >
          <option value="">No Category</option>
          {categories.map((category) => (
            <option key={category.id} value={category.id}>
              {category.title}
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
