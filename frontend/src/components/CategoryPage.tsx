import React from "react";
import { Link, useParams } from "react-router-dom";
import ProductList from "./ProductList";
import { CategoryType, ProductType } from "./Product";

interface CategoryPageProps {
  categories: CategoryType[];
  products: ProductType[];
  onMoveCategory: (productId: string, newCategoryId: string) => void;
}

function CategoryPage({
  categories,
  products,
  onMoveCategory,
}: CategoryPageProps) {
  const { categoryId } = useParams();

  const category = categories.find((item) => item.id === categoryId);

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
    (product) => product.categoryId === category.id,
  );

  return (
    <section className="category-page">
      <div className="category-page__header">
        <h1>{category.title}</h1>
        <p>{category.description}</p>
        <Link className="inline-link" to="/categories">
          Back to Categories
        </Link>
      </div>

      <ProductList
        title={`${category.title} Products`}
        products={filteredProducts}
        categories={categories}
        onMoveCategory={onMoveCategory}
      />
    </section>
  );
}

export default CategoryPage;
