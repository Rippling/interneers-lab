import React from "react";
import { Link, useParams } from "react-router-dom";
import ProductList from "./ProductList";
import { CategoryType, ProductType } from "./Product";

interface CategoryPageProps {
  categories: CategoryType[];
  products: ProductType[];
  onMoveCategory: (productId: string, newCategoryId: string) => void;
  onDeleteProduct: (productId: string) => void;
}

function CategoryPage({
  categories,
  products,
  onMoveCategory,
  onDeleteProduct,
}: CategoryPageProps) {
  const { categoryId } = useParams();

  const category = categories.find((item) => item.id === categoryId);

  if (!category) {
    return (
      <section className="mx-auto max-w-3xl">
        <h1 className="mb-4 text-3xl font-bold text-slate-900">
          Category Not Found
        </h1>
        <Link
          className="font-semibold text-cyan-700 hover:underline"
          to="/categories"
        >
          Back to Categories
        </Link>
      </section>
    );
  }

  const filteredProducts = products.filter(
    (product) => product.categoryId === category.id,
  );

  return (
    <section>
      <div className="mb-6 rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
        <h1 className="mb-3 text-3xl font-bold text-slate-900">
          {category.title}
        </h1>
        <p className="mb-3 text-slate-600">{category.description}</p>
        <p className="mb-3 text-sm font-semibold text-slate-500">
          Total Products: {filteredProducts.length}
        </p>
        <Link
          className="font-semibold text-cyan-700 hover:underline"
          to="/categories"
        >
          Back to Categories
        </Link>
      </div>

      <ProductList
        title={`${category.title} Products`}
        products={filteredProducts}
        categories={categories}
        onMoveCategory={onMoveCategory}
        onDeleteProduct={onDeleteProduct}
      />
    </section>
  );
}

export default CategoryPage;
