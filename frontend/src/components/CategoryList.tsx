import React from "react";
import { Link } from "react-router-dom";
import { CategoryType, ProductType } from "./Product";

interface CategoryListProps {
  categories: CategoryType[];
  products: ProductType[];
}

function CategoryList({ categories, products }: CategoryListProps) {
  return (
    <section>
      <div className="mb-6 flex items-center justify-between">
        <h1 className="text-3xl font-bold text-slate-900">
          Product Categories
        </h1>
        <p className="text-sm font-semibold text-slate-500">
          {categories.length} category(s)
        </p>
      </div>

      <div className="grid grid-cols-1 gap-5 md:grid-cols-2 xl:grid-cols-3">
        {categories.map((category) => {
          const count = products.filter(
            (product) => product.categoryId === category.id,
          ).length;

          return (
            <Link
              key={category.id}
              className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm transition hover:-translate-y-1 hover:shadow-lg"
              to={`/categories/${category.id}`}
            >
              <h2 className="mb-3 text-xl font-bold text-slate-900">
                {category.title}
              </h2>
              <p className="mb-3 text-sm leading-6 text-slate-500">
                {category.description}
              </p>
              <p className="text-sm font-semibold text-cyan-700">
                {count} product(s)
              </p>
            </Link>
          );
        })}
      </div>
    </section>
  );
}

export default CategoryList;
