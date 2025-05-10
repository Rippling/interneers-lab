// components/ProductList.tsx
import React from "react";

type Product = {
  product_id: number;
  name: string;
  description: string;
  brand: string;
  category_id: number;
  category_Id: number;
};

interface Props {
  products: Product[];
  onProductClick: (product: Product) => void;
}

const productImages: { [key: number]: string } = {
  1: "https://img.freepik.com/free-photo/creative-reels-composition_23-2149711507.jpg?semt=ais_hybrid&w=740",
  2: "https://img.freepik.com/free-photo/still-life-rendering-jackets-display_23-2149745036.jpg?semt=ais_hybrid&w=740",
  3: "https://images.pexels.com/photos/18105/pexels-photo.jpg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=2",
  4: "https://picsum.photos/id/15/200/300",
  5: "https://picsum.photos/id/21/200/300",
  6: "https://picsum.photos/id/40/200/300",
  7: "https://picsum.photos/id/41/200/300",
  8: "https://picsum.photos/id/32/200/300",
  9: "https://picsum.photos/id/33/200/300",
  10: "https://picsum.photos/id/51/200/300",
};

const ProductList: React.FC<Props> = ({ products, onProductClick }) => {
  console.log("Products:", products);
  return (
    <div
      style={{
        display: "flex",
        flexWrap: "wrap",
        gap: "20px",
        padding: "20px",
      }}
    >
      {products.map((product) => (
        <div
          key={product.product_id}
          onClick={() => onProductClick(product)}
          style={{
            border: "1px solid #ccc",
            padding: "10px",
            borderRadius: "8px",
            width: "250px",
            cursor: "pointer",
          }}
        >
          <img
            src={
              productImages[product.product_id] ||
              "https://via.placeholder.com/150"
            }
            alt={product.name}
            style={{ width: "100%", height: "150px", objectFit: "cover" }}
          />
          <h4>{product.name}</h4>
          <p>
            <strong>Brand:</strong> {product.brand}
          </p>
          <p>
            <strong>productID:</strong> {product.product_id}
          </p>
          <p>
            <strong>Description:</strong> {product.description}
          </p>
        </div>
      ))}
    </div>
  );
};

export default ProductList;
