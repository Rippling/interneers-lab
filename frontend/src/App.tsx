import React, { useEffect, useState } from "react";
import { Link, Route, Routes, useLocation } from "react-router-dom";
import "./App.css";
import ProductList from "./components/ProductList";
import ProductPage from "./components/ProductPage";
import CategoryList from "./components/CategoryList";
import CategoryPage from "./components/CategoryPage";
import LoadingSpinner from "./components/LoadingSpinner";
import { ProductType } from "./components/Product";

const initialProducts: ProductType[] = [
  {
    id: 1,
    name: "iPhone 15",
    brand: "Apple",
    price: 799,
    quantity: 10,
    category: "Electronics",
    description: "A premium smartphone with advanced camera features.",
  },
  {
    id: 2,
    name: "Galaxy S24",
    brand: "Samsung",
    price: 699,
    quantity: 8,
    category: "Electronics",
    description: "A flagship Android phone with a bright display.",
  },
  {
    id: 3,
    name: "T-Shirt",
    brand: "H&M",
    price: 19.99,
    quantity: 25,
    category: "Fashion",
    description: "Comfortable cotton T-shirt for everyday wear.",
  },
  {
    id: 4,
    name: "Lamp",
    brand: "IKEA",
    price: 34.5,
    quantity: 12,
    category: "Home",
    description: "A simple decorative lamp for home interiors.",
  },
];

const categories = ["Electronics", "Fashion", "Home", "Books"];

function App() {
  const [products, setProducts] = useState<ProductType[]>(initialProducts);
  const [error, setError] = useState<string>("");
  const [loading, setLoading] = useState<boolean>(false);
  const location = useLocation();

  useEffect(() => {
    setLoading(true);

    const timer = setTimeout(() => {
      setLoading(false);
    }, 500);

    return () => clearTimeout(timer);
  }, [location.pathname]);

  const moveProductToCategory = (productId: number, newCategory: string) => {
    const product = products.find((item) => item.id === productId);

    if (!product) {
      setError("Product could not be found.");
      return;
    }

    if (!newCategory) {
      setError("Please select a category.");
      return;
    }

    if (product.category === newCategory) {
      setError("Product is already in that category.");
      return;
    }

    setProducts((currentProducts) =>
      currentProducts.map((item) =>
        item.id === productId ? { ...item, category: newCategory } : item,
      ),
    );
    setError("");
  };

  const updateProduct = (updatedProduct: ProductType) => {
    if (!updatedProduct.name.trim()) {
      setError("Product name is required.");
      return false;
    }

    if (!updatedProduct.brand.trim()) {
      setError("Brand is required.");
      return false;
    }

    if (updatedProduct.price <= 0) {
      setError("Price must be greater than zero.");
      return false;
    }

    if (updatedProduct.quantity < 0) {
      setError("Quantity cannot be negative.");
      return false;
    }

    setProducts((currentProducts) =>
      currentProducts.map((item) =>
        item.id === updatedProduct.id ? updatedProduct : item,
      ),
    );
    setError("");
    return true;
  };

  return (
    <div className="app-shell">
      <header className="app-header">
        <div className="brand">Product Store</div>
        <nav className="app-nav">
          <Link to="/">Products</Link>
          <Link to="/categories">Categories</Link>
        </nav>
      </header>

      <main className="app-main">
        {error && <div className="error-banner">{error}</div>}
        {loading ? (
          <LoadingSpinner />
        ) : (
          <Routes>
            <Route
              path="/"
              element={
                <ProductList
                  title="Product List"
                  products={products}
                  categories={categories}
                  onMoveCategory={moveProductToCategory}
                />
              }
            />
            <Route
              path="/categories"
              element={
                <CategoryList
                  categories={categories}
                  products={products}
                />
              }
            />
            <Route
              path="/categories/:categoryName"
              element={
                <CategoryPage
                  categories={categories}
                  products={products}
                  onMoveCategory={moveProductToCategory}
                />
              }
            />
            <Route
              path="/products/:productId"
              element={
                <ProductPage
                  products={products}
                  categories={categories}
                  onSave={updateProduct}
                  onError={setError}
                />
              }
            />
          </Routes>
        )}
      </main>
    </div>
  );
}

export default App;
