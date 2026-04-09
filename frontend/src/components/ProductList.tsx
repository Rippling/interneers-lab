import React from "react";
import Product, { CategoryType, ProductType } from "./Product";

interface ProductListProps {
  title?: string;
  products: ProductType[];
  categories: CategoryType[];
  onMoveCategory: (productId: string, newCategoryId: string) => void;
}

function ProductList({
  title = "Product List",
  products,
  categories,
  onMoveCategory,
}: ProductListProps) {
  return (
    <section className="product-list-section">
      <h1>{title}</h1>

      {products.length === 0 ? (
        <div className="empty-state">No products found in this category.</div>
      ) : (
        <div className="product-list">
          {products.map((product) => (
            <Product
              key={product.id}
              product={product}
              categories={categories}
              onMoveCategory={onMoveCategory}
            />
          ))}
        </div>
      )}
    </section>
  );
}

export default ProductList;
