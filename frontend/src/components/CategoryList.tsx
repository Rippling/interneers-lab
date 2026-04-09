import React from "react";
import { Link } from "react-router-dom";
import { CategoryType, ProductType } from "./Product";

interface CategoryListProps {
  categories: CategoryType[];
  products: ProductType[];
}

function CategoryList({ categories, products }: CategoryListProps) {
  return (
    <section className="category-list-section">
      <h1>Product Categories</h1>

      <div className="category-list">
        {categories.map((category) => {
          const count = products.filter(
            (product) => product.categoryId === category.id,
          ).length;

          return (
            <Link
              key={category.id}
              className="category-card"
              to={`/categories/${category.id}`}
            >
              <h2>{category.title}</h2>
              <p>{category.description}</p>
              <p>{count} product(s)</p>
            </Link>
          );
        })}
      </div>
    </section>
  );
}

export default CategoryList;
