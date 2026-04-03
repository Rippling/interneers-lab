import React from "react";
import Product, { ProductType } from "./Product";

interface ProductListProps {
  products: ProductType[];
  categories: string[];
  onMoveCategory: (productId: number, newCategory: string) => void;
}

function ProductList({
  products,
  categories,
  onMoveCategory,
}: ProductListProps) {
  return (
    <section className="product-list-section">
      <h1>Product List</h1>
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
    </section>
  );
}

export default ProductList;
