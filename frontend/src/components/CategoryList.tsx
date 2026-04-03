import React from "react";
import { Link } from "react-router-dom";
import { ProductType } from "./Product";

interface CategoryListProps {
  categories: string[];
  products: ProductType[];
}

function CategoryList({ categories, products }: CategoryListProps) {
  return (
    <section className="category-list-section">
      <h1>Product Categories</h1>

      <div className="category-list">
        {categories.map((category) => {
          const count = products.filter(
            (product) => product.category === category,
          ).length;

          return (
            <Link
              key={category}
              className="category-card"
              to={`/categories/${category}`}
            >
              <h2>{category}</h2>
              <p>{count} product(s)</p>
            </Link>
          );
        })}
      </div>
    </section>
  );
}

export default CategoryList;
