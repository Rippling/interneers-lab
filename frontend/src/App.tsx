import React, { useEffect, useState } from "react";
import { Link, Route, Routes, useLocation } from "react-router-dom";
import "./App.css";
import ProductList from "./components/ProductList";
import ProductPage from "./components/ProductPage";
import CategoryList from "./components/CategoryList";
import CategoryPage from "./components/CategoryPage";
import LoadingSpinner from "./components/LoadingSpinner";
import { CategoryType, ProductType } from "./components/Product";

function App() {
  const [products, setProducts] = useState<ProductType[]>([]);
  const [categories, setCategories] = useState<CategoryType[]>([]);
  const [error, setError] = useState<string>("");
  const [loading, setLoading] = useState<boolean>(true);
  const location = useLocation();

  const fetchCategories = async () => {
    const response = await fetch(
      "http://127.0.0.1:8000/product-csr/categories/",
    );

    if (!response.ok) {
      throw new Error("Failed to fetch categories.");
    }

    const data = await response.json();
    return data.categories as CategoryType[];
  };

  const fetchProducts = async (categoryList: CategoryType[]) => {
    const response = await fetch("http://127.0.0.1:8000/product-csr/products/");

    if (!response.ok) {
      throw new Error("Failed to fetch products.");
    }

    const data = await response.json();

    const mappedProducts: ProductType[] = data.products.map((product: any) => {
      const matchedCategory = categoryList.find(
        (category) => category.id === product.category,
      );

      return {
        id: product.id,
        name: product.name,
        brand: product.brand,
        price: Number(product.price),
        quantity: Number(product.quantity),
        categoryId: product.category || null,
        categoryName: matchedCategory ? matchedCategory.title : "No Category",
        description: product.description || "No description available.",
      };
    });

    return mappedProducts;
  };

  const loadData = async () => {
    try {
      setLoading(true);
      setError("");

      const fetchedCategories = await fetchCategories();
      const fetchedProducts = await fetchProducts(fetchedCategories);

      setCategories(fetchedCategories);
      setProducts(fetchedProducts);
    } catch (err: any) {
      setError(err.message || "Something went wrong while loading data.");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadData();
  }, []);

  useEffect(() => {
    setLoading(true);

    const timer = setTimeout(() => {
      setLoading(false);
    }, 300);

    return () => clearTimeout(timer);
  }, [location.pathname]);

  const moveProductToCategory = async (
    productId: string,
    newCategoryId: string,
  ) => {
    const product = products.find((item) => item.id === productId);

    if (!product) {
      setError("Product could not be found.");
      return;
    }

    if (!newCategoryId) {
      setError("Please select a category.");
      return;
    }

    if (product.categoryId === newCategoryId) {
      setError("Product is already in that category.");
      return;
    }

    try {
      setLoading(true);

      const response = await fetch(
        `http://127.0.0.1:8000/product-csr/categories/${newCategoryId}/add-product/`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({ product_id: productId }),
        },
      );

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.error || "Failed to move product.");
      }

      await loadData();
      setError("");
    } catch (err: any) {
      setError(err.message || "Failed to move product.");
    } finally {
      setLoading(false);
    }
  };

  const updateProduct = async (updatedProduct: ProductType) => {
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

    try {
      setLoading(true);

      const response = await fetch(
        `http://127.0.0.1:8000/product-csr/products/${updatedProduct.id}/`,
        {
          method: "PUT",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            name: updatedProduct.name,
            brand: updatedProduct.brand,
            price: updatedProduct.price,
            quantity: updatedProduct.quantity,
          }),
        },
      );

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.error || "Failed to update product.");
      }

      await loadData();
      setError("");
      return true;
    } catch (err: any) {
      setError(err.message || "Failed to update product.");
      return false;
    } finally {
      setLoading(false);
    }
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
                <CategoryList categories={categories} products={products} />
              }
            />
            <Route
              path="/categories/:categoryId"
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
