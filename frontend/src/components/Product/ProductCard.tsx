import React from "react";
import { Product } from "./Product";
import "./ProductCard.css";

type props = {
  product: Product;
};

const ProductCard = (Props: props) => {
  return (
    <div className="prodcard">
      <h2 className="title">{Props.product.name}</h2>
      <h4 className="brand">{Props.product.brand}</h4>
      <p>{Props.product.price}</p>
    </div>
  );
};

export default ProductCard;
