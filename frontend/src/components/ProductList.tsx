import React from "react";
import Product, { ProductType } from "./Product";

const dummyProducts: ProductType[] = [
  {
    id: 1,
    name: "iPhone 15",
    brand: "Apple",
    price: 799,
    quantity: 10,
    category: "Electronics",
  },
  {
    id: 2,
    name: "Galaxy S24",
    brand: "Samsung",
    price: 699,
    quantity: 8,
    category: "Electronics",
  },
  {
    id: 3,
    name: "T-Shirt",
    brand: "H&M",
    price: 19.99,
    quantity: 25,
    category: "Fashion",
  },
];

function ProductList() {
  return (
    <section className="product-list-section">
      <h1>Product List</h1>
      <div className="product-list">
        {dummyProducts.map((product) => (
          <Product key={product.id} product={product} />
        ))}
      </div>
    </section>
  );
}

export default ProductList;
