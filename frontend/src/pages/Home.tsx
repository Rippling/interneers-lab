import React from "react";
import Categories from "../components/categories";
import ProductList from "../components/ProductList";
import "./Home.css";

type products = {
  product_id: number;
  name: string;
  description: string;
  brand: string;
  //image_url: string;
};

const Home: React.FC = () => {
  const [products, setProducts] = React.useState<products[]>([]);
  //const [categoryId, setCategoryId] = React.useState<number | null>(null);

  const fetchProducts = async (category_id: number) => {
    const res = await fetch(
      `http://127.0.0.1:8000/api/category/${category_id}/products`,
    );
    const data: products[] = await res.json();
    console.log(data);
    setProducts(data);
  };

  const productImages: { [key: number]: string } = {
    1: "https://img.freepik.com/free-photo/creative-reels-composition_23-2149711507.jpg?semt=ais_hybrid&w=740",
    2: "https://img.freepik.com/free-photo/still-life-rendering-jackets-display_23-2149745036.jpg?semt=ais_hybrid&w=740",
    3: "https://images.pexels.com/photos/18105/pexels-photo.jpg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=2",
    4: "https://picsum.photos/id/15/200/300",
    5: "https://picsum.photos/id/21/200/300",
    6: "https://picsum.photos/id/10/200/300",
  };

  return (
    <div className="App">
      <div className="main-content">
        <Categories onclick={fetchProducts} />
      </div>
      <div className="products-list">
        <div>
          <h2
            className="products-header"
            //   style={{
            //     fontSize: "24px",
            //     backgroundColor: "#4a90e2",
            //     color: "white",
            //     padding: "10px 20px",
            //     borderRadius: "8px",
            //     margin: "20px auto", // auto centers horizontally
            //     height: "50px",
            //     width: "fit-content", // shrink to content
            //     display: "flex",
            //     justifyContent: "center",
            //     alignItems: "center",
            //   }}
          >
            Products
          </h2>
        </div>
        <div className="products">
          {products.map((product) => (
            <div key={product.product_id} className="product-item">
              <img
                src={
                  productImages[product.product_id] ||
                  "https://via.placeholder.com/150?text=Product"
                }
                alt={product.name}
                className="product-image"
              />
              <h3>
                <strong>Product Name:</strong>{" "}
                <span style={{ fontWeight: "normal" }}>{product.name}</span>
              </h3>
              <h3>
                <strong>Description:</strong>{" "}
                <span style={{ fontWeight: "normal" }}>
                  {product.description}
                </span>
              </h3>
              <h3>
                <strong>Brand:</strong>{" "}
                <span style={{ fontWeight: "normal" }}>{product.brand}</span>
              </h3>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default Home;
