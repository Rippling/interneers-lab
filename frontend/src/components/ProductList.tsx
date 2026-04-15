import React from "react";
import Product, { CategoryType, ProductType } from "./Product";

interface ProductListProps {
  title?: string;
  products: ProductType[];
  categories: CategoryType[];
  onMoveCategory: (productId: string, newCategoryId: string) => void;
  onDeleteProduct: (productId: string) => void;
}

function ProductList({
  title = "Product List",
  products,
  categories,
  onMoveCategory,
  onDeleteProduct,
}: ProductListProps) {
  return (
    <section>
      <div className="mb-6 flex items-center justify-between">
        <h1 className="text-3xl font-bold text-slate-900">{title}</h1>
        <p className="text-sm font-semibold text-slate-500">
          {products.length} product(s)
        </p>
      </div>

      {products.length === 0 ? (
        <div className="rounded-2xl border border-slate-200 bg-white px-6 py-8 text-center text-slate-500 shadow-sm">
          No products found. Try changing your search or filters.
        </div>
      ) : (
        <div className="grid grid-cols-1 gap-5 md:grid-cols-2 xl:grid-cols-3">
          {products.map((product) => (
            <Product
              key={product.id}
              product={product}
              categories={categories}
              onMoveCategory={onMoveCategory}
              onDeleteProduct={onDeleteProduct}
            />
          ))}
        </div>
      )}
    </section>
  );
}

export default ProductList;
