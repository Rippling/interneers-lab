import React from "react";
import { Link, useParams } from "react-router-dom";
import ProductList from "./ProductList";
import { ProductType } from "./Product";

interface CategoryPageProps {
  categories: string[];
  products: ProductType[];
  onMoveCategory: (productId: number, newCategory: string) => void;
}

function CategoryPage({
  categories,
  products,
  onMoveCategory,
}: CategoryPageProps) {
  const { categoryName } = useParams();

  const category = categories.find((item) => item === categoryName);

  if (!category) {
    return (
      <section className="category-page">
        <h1>Category Not Found</h1>
        <Link className="inline-link" to="/categories">
          Back to Categories
        </Link>
      </section>
    );
  }

  const filteredProducts = products.filter(
    (product) => product.category === category,
  );

  return (
    <section className="category-page">
      <div className="category-page__header">
        <h1>{category}</h1>
        <p>This page shows the category information and all products inside it.</p>
        <Link className="inline-link" to="/categories">
          Back to Categories
        </Link>
      </div>

      <ProductList
        title={`${category} Products`}
        products={filteredProducts}
        categories={categories}
        onMoveCategory={onMoveCategory}
      />
    </section>
  );
}

export default CategoryPage;
