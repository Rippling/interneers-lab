import React, { useCallback, useEffect, useMemo, useState } from "react";
import { Link, Navigate, Route, Routes, useLocation } from "react-router-dom";
import CategoryList from "./components/CategoryList";
import CategoryPage from "./components/CategoryPage";
import CreateCategoryPage from "./components/CreateCategoryPage";
import CreateProductPage from "./components/CreateProductPage";
import LoadingSpinner from "./components/LoadingSpinner";
import LoginPage from "./components/LoginPage";
import ProductList from "./components/ProductList";
import ProductPage from "./components/ProductPage";
import SignupPage from "./components/SignupPage";
import { CategoryType, ProductType } from "./components/Product";

const API_BASE = "http://127.0.0.1:8000/product-csr";
const AUTH_STORAGE_KEY = "product-csr-auth-token";

type ProductDraft = Omit<ProductType, "id" | "categoryName">;
type SortBy =
  | "name"
  | "price-low"
  | "price-high"
  | "quantity-low"
  | "quantity-high";
type StockFilter = "all" | "in-stock" | "low-stock" | "out-of-stock";

function App() {
  const [products, setProducts] = useState<ProductType[]>([]);
  const [categories, setCategories] = useState<CategoryType[]>([]);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");
  const [loading, setLoading] = useState(true);
  const [authChecking, setAuthChecking] = useState(true);
  const [authToken, setAuthToken] = useState<string | null>(null);
  const [currentUser, setCurrentUser] = useState<string | null>(null);
  const [search, setSearch] = useState("");
  const [selectedCategoryFilter, setSelectedCategoryFilter] = useState("");
  const [sortBy, setSortBy] = useState<SortBy>("name");
  const [stockFilter, setStockFilter] = useState<StockFilter>("all");
  const [authMode, setAuthMode] = useState<"login" | "signup">("login");
  const location = useLocation();

  const clearAuth = useCallback(() => {
    localStorage.removeItem(AUTH_STORAGE_KEY);
    setAuthToken(null);
    setCurrentUser(null);
    setProducts([]);
    setCategories([]);
  }, []);

  const authorizedFetch = useCallback(
    async (path: string, options: RequestInit = {}) => {
      const headers = new Headers(options.headers || {});

      if (authToken) {
        headers.set("Authorization", `Token ${authToken}`);
      }

      if (!(options.body instanceof FormData) && !headers.has("Content-Type")) {
        headers.set("Content-Type", "application/json");
      }

      const response = await fetch(`${API_BASE}${path}`, {
        ...options,
        headers,
      });

      if (response.status === 401) {
        clearAuth();
        throw new Error("Your session expired. Please log in again.");
      }

      return response;
    },
    [authToken, clearAuth],
  );

  const fetchCategories = useCallback(async () => {
    const response = await authorizedFetch("/categories/", { method: "GET" });
    if (!response.ok) {
      throw new Error("Failed to fetch categories.");
    }

    const data = await response.json();
    return data.categories as CategoryType[];
  }, [authorizedFetch]);

  const fetchProducts = useCallback(
    async (categoryList: CategoryType[]) => {
      const response = await authorizedFetch("/products/", { method: "GET" });
      if (!response.ok) {
        throw new Error("Failed to fetch products.");
      }

      const data = await response.json();

      const mappedProducts: ProductType[] = data.products.map(
        (product: any) => {
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
            categoryName: matchedCategory
              ? matchedCategory.title
              : "No Category",
            description: product.description || "",
            imageUrl: product.image_url || "",
          };
        },
      );

      return mappedProducts;
    },
    [authorizedFetch],
  );

  const loadData = useCallback(async () => {
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
  }, [fetchCategories, fetchProducts]);

  useEffect(() => {
    const bootstrapAuth = async () => {
      const storedToken = localStorage.getItem(AUTH_STORAGE_KEY);

      if (!storedToken) {
        setAuthChecking(false);
        setLoading(false);
        return;
      }

      try {
        const response = await fetch(`${API_BASE}/auth/me/`, {
          headers: {
            Authorization: `Token ${storedToken}`,
          },
        });

        if (!response.ok) {
          throw new Error("Session expired");
        }

        const data = await response.json();
        setAuthToken(storedToken);
        setCurrentUser(data.user.username);
      } catch (_error) {
        localStorage.removeItem(AUTH_STORAGE_KEY);
      } finally {
        setAuthChecking(false);
      }
    };

    bootstrapAuth();
  }, []);

  useEffect(() => {
    if (!authChecking && authToken) {
      loadData();
    }
  }, [authChecking, authToken, loadData]);

  useEffect(() => {
    setSuccess("");
    setError("");
  }, [location.pathname]);

  const handleLogin = useCallback(
    async (username: string, password: string) => {
      try {
        setLoading(true);
        setError("");

        const response = await fetch(`${API_BASE}/auth/login/`, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({ username, password }),
        });

        const data = await response.json();

        if (!response.ok) {
          throw new Error(data.error || "Login failed.");
        }

        localStorage.setItem(AUTH_STORAGE_KEY, data.token);
        setAuthToken(data.token);
        setCurrentUser(data.user.username);
        setSuccess("Login successful.");
        return true;
      } catch (err: any) {
        setError(err.message || "Login failed.");
        return false;
      } finally {
        setLoading(false);
      }
    },
    [],
  );

  const handleSignup = useCallback(
    async (username: string, email: string, password: string) => {
      try {
        setLoading(true);
        setError("");

        const response = await fetch(`${API_BASE}/auth/signup/`, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({ username, email, password }),
        });

        const data = await response.json();

        if (!response.ok) {
          throw new Error(data.error || "Signup failed.");
        }

        localStorage.setItem(AUTH_STORAGE_KEY, data.token);
        setAuthToken(data.token);
        setCurrentUser(data.user.username);
        setSuccess("Account created successfully.");
        return true;
      } catch (err: any) {
        setError(err.message || "Signup failed.");
        return false;
      } finally {
        setLoading(false);
      }
    },
    [],
  );

  const handleLogout = useCallback(() => {
    clearAuth();
    setSuccess("You have been logged out.");
  }, [clearAuth]);

  const filteredProducts = useMemo(() => {
    const filtered = products.filter((product) => {
      const matchesSearch =
        product.name.toLowerCase().includes(search.toLowerCase()) ||
        product.brand.toLowerCase().includes(search.toLowerCase());

      const matchesCategory =
        !selectedCategoryFilter ||
        product.categoryId === selectedCategoryFilter;

      const matchesStock =
        stockFilter === "all" ||
        (stockFilter === "out-of-stock" && product.quantity <= 0) ||
        (stockFilter === "low-stock" &&
          product.quantity > 0 &&
          product.quantity < 5) ||
        (stockFilter === "in-stock" && product.quantity >= 5);

      return matchesSearch && matchesCategory && matchesStock;
    });

    return [...filtered].sort((first, second) => {
      if (sortBy === "price-low") {
        return first.price - second.price;
      }

      if (sortBy === "price-high") {
        return second.price - first.price;
      }

      if (sortBy === "quantity-low") {
        return first.quantity - second.quantity;
      }

      if (sortBy === "quantity-high") {
        return second.quantity - first.quantity;
      }

      return first.name.localeCompare(second.name);
    });
  }, [products, search, selectedCategoryFilter, sortBy, stockFilter]);

  const dashboardStats = useMemo(() => {
    return {
      totalProducts: products.length,
      totalCategories: categories.length,
      lowStockProducts: products.filter(
        (product) => product.quantity > 0 && product.quantity < 5,
      ).length,
      outOfStockProducts: products.filter((product) => product.quantity <= 0)
        .length,
    };
  }, [products, categories]);

  const createCategory = useCallback(
    async (category: { title: string; description: string }) => {
      if (!category.title.trim()) {
        setError("Category title is required.");
        return false;
      }

      try {
        setLoading(true);

        const response = await authorizedFetch("/categories/", {
          method: "POST",
          body: JSON.stringify(category),
        });

        const data = await response.json();

        if (!response.ok) {
          throw new Error(data.error || "Failed to create category.");
        }

        await loadData();
        setSuccess("Category created successfully.");
        return true;
      } catch (err: any) {
        setError(err.message || "Failed to create category.");
        return false;
      } finally {
        setLoading(false);
      }
    },
    [authorizedFetch, loadData],
  );

  const createProduct = useCallback(
    async (product: ProductDraft) => {
      try {
        setLoading(true);

        const response = await authorizedFetch("/products/", {
          method: "POST",
          body: JSON.stringify({
            name: product.name,
            brand: product.brand,
            price: product.price,
            quantity: product.quantity,
            description: product.description,
            imageUrl: product.imageUrl,
            categoryId: product.categoryId,
          }),
        });

        const data = await response.json();

        if (!response.ok) {
          throw new Error(data.error || "Failed to create product.");
        }

        await loadData();
        setSuccess("Product created successfully.");
        return true;
      } catch (err: any) {
        setError(err.message || "Failed to create product.");
        return false;
      } finally {
        setLoading(false);
      }
    },
    [authorizedFetch, loadData],
  );

  const moveProductToCategory = useCallback(
    async (productId: string, newCategoryId: string) => {
      try {
        setLoading(true);

        const response = await authorizedFetch(
          `/categories/${newCategoryId}/add-product/`,
          {
            method: "POST",
            body: JSON.stringify({ product_id: productId }),
          },
        );

        const data = await response.json();

        if (!response.ok) {
          throw new Error(data.error || "Failed to move product.");
        }

        await loadData();
        setSuccess("Product moved successfully.");
      } catch (err: any) {
        setError(err.message || "Failed to move product.");
      } finally {
        setLoading(false);
      }
    },
    [authorizedFetch, loadData],
  );

  const updateProduct = useCallback(
    async (updatedProduct: ProductType) => {
      try {
        setLoading(true);

        const response = await authorizedFetch(
          `/products/${updatedProduct.id}/`,
          {
            method: "PUT",
            body: JSON.stringify({
              name: updatedProduct.name,
              brand: updatedProduct.brand,
              price: updatedProduct.price,
              quantity: updatedProduct.quantity,
              description: updatedProduct.description,
              imageUrl: updatedProduct.imageUrl,
              categoryId: updatedProduct.categoryId,
            }),
          },
        );

        const data = await response.json();

        if (!response.ok) {
          throw new Error(data.error || "Failed to update product.");
        }

        await loadData();
        setSuccess("Product updated successfully.");
        return true;
      } catch (err: any) {
        setError(err.message || "Failed to update product.");
        return false;
      } finally {
        setLoading(false);
      }
    },
    [authorizedFetch, loadData],
  );

  const deleteProduct = useCallback(
    async (productId: string) => {
      try {
        setLoading(true);

        const response = await authorizedFetch(`/products/${productId}/`, {
          method: "DELETE",
        });

        const data = await response.json();

        if (!response.ok) {
          throw new Error(data.error || "Failed to delete product.");
        }

        await loadData();
        setSuccess("Product deleted successfully.");
      } catch (err: any) {
        setError(err.message || "Failed to delete product.");
      } finally {
        setLoading(false);
      }
    },
    [authorizedFetch, loadData],
  );

  if (authChecking) {
    return <LoadingSpinner message="Checking your session..." />;
  }

  const isAuthenticated = Boolean(authToken && currentUser);

  return (
    <div className="min-h-screen bg-slate-100 text-slate-800">
      <header className="border-b border-slate-200 bg-slate-950 text-white shadow-lg">
        <div className="mx-auto flex max-w-7xl flex-col gap-4 px-6 py-5 lg:flex-row lg:items-center lg:justify-between">
          <div>
            <div className="text-2xl font-bold tracking-wide">
              Product Store
            </div>
          </div>

          {isAuthenticated ? (
            <div className="flex items-center gap-4">
              <nav className="flex gap-6 text-sm font-semibold">
                <Link to="/">Products</Link>
                <Link to="/products/new">Add Product</Link>
                <Link to="/categories">Categories</Link>
                <Link to="/categories/new">Add Category</Link>
              </nav>
              <span className="text-sm">Hi, {currentUser}</span>
              <button onClick={handleLogout}>Logout</button>
            </div>
          ) : null}
        </div>
      </header>

      <main className="mx-auto max-w-7xl px-6 py-8">
        {error && (
          <div className="mb-5 rounded-xl border border-rose-200 bg-rose-50 px-4 py-3 text-rose-700">
            {error}
          </div>
        )}
        {success && (
          <div className="mb-5 rounded-xl border border-emerald-200 bg-emerald-50 px-4 py-3 text-emerald-700">
            {success}
          </div>
        )}

        {!isAuthenticated ? (
          authMode === "login" ? (
            <LoginPage
              onLogin={handleLogin}
              onSwitchToSignup={() => setAuthMode("signup")}
            />
          ) : (
            <SignupPage
              onSignup={handleSignup}
              onSwitchToLogin={() => setAuthMode("login")}
            />
          )
        ) : loading ? (
          <LoadingSpinner message="Loading inventory data..." />
        ) : (
          <>
            <section className="mb-6 grid grid-cols-1 gap-4 sm:grid-cols-2 xl:grid-cols-4">
              <div className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm">
                <p className="text-sm font-semibold text-slate-500">Products</p>
                <p className="mt-2 text-3xl font-bold text-slate-900">
                  {dashboardStats.totalProducts}
                </p>
              </div>
              <div className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm">
                <p className="text-sm font-semibold text-slate-500">
                  Categories
                </p>
                <p className="mt-2 text-3xl font-bold text-slate-900">
                  {dashboardStats.totalCategories}
                </p>
              </div>
              <div className="rounded-2xl border border-amber-200 bg-amber-50 p-5 shadow-sm">
                <p className="text-sm font-semibold text-amber-700">
                  Low Stock
                </p>
                <p className="mt-2 text-3xl font-bold text-amber-900">
                  {dashboardStats.lowStockProducts}
                </p>
              </div>
              <div className="rounded-2xl border border-rose-200 bg-rose-50 p-5 shadow-sm">
                <p className="text-sm font-semibold text-rose-700">
                  Out of Stock
                </p>
                <p className="mt-2 text-3xl font-bold text-rose-900">
                  {dashboardStats.outOfStockProducts}
                </p>
              </div>
            </section>

            <section className="mb-6 rounded-2xl border border-slate-200 bg-white p-4 shadow-sm">
              <div className="flex flex-col gap-4 lg:flex-row lg:items-center lg:justify-between">
                <input
                  className="w-full rounded-xl border border-slate-300 px-4 py-3"
                  type="text"
                  placeholder="Search by product or brand"
                  value={search}
                  onChange={(event) => setSearch(event.target.value)}
                />

                <div className="flex gap-3">
                  <select
                    className="rounded-xl border border-slate-300 bg-white px-4 py-3"
                    value={selectedCategoryFilter}
                    onChange={(event) =>
                      setSelectedCategoryFilter(event.target.value)
                    }
                  >
                    <option value="">All Categories</option>
                    {categories.map((category) => (
                      <option key={category.id} value={category.id}>
                        {category.title}
                      </option>
                    ))}
                  </select>

                  <select
                    className="rounded-xl border border-slate-300 bg-white px-4 py-3"
                    value={stockFilter}
                    onChange={(event) =>
                      setStockFilter(event.target.value as StockFilter)
                    }
                  >
                    <option value="all">All Stock</option>
                    <option value="in-stock">In Stock</option>
                    <option value="low-stock">Low Stock</option>
                    <option value="out-of-stock">Out of Stock</option>
                  </select>

                  <select
                    className="rounded-xl border border-slate-300 bg-white px-4 py-3"
                    value={sortBy}
                    onChange={(event) =>
                      setSortBy(event.target.value as SortBy)
                    }
                  >
                    <option value="name">Sort A-Z</option>
                    <option value="price-low">Price Low to High</option>
                    <option value="price-high">Price High to Low</option>
                    <option value="quantity-low">Quantity Low to High</option>
                    <option value="quantity-high">Quantity High to Low</option>
                  </select>

                  <Link
                    className="rounded-xl bg-slate-900 px-5 py-3 text-center font-semibold text-white"
                    to="/products/new"
                  >
                    Add Product
                  </Link>

                  <Link
                    className="rounded-xl bg-cyan-600 px-5 py-3 text-center font-semibold text-white"
                    to="/categories/new"
                  >
                    Add Category
                  </Link>
                </div>
              </div>
            </section>

            <Routes>
              <Route
                path="/"
                element={
                  <ProductList
                    title="Product Inventory"
                    products={filteredProducts}
                    categories={categories}
                    onMoveCategory={moveProductToCategory}
                    onDeleteProduct={deleteProduct}
                  />
                }
              />
              <Route
                path="/products/new"
                element={
                  <CreateProductPage
                    categories={categories}
                    onCreate={createProduct}
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
              <Route
                path="/categories"
                element={
                  <CategoryList categories={categories} products={products} />
                }
              />
              <Route
                path="/categories/new"
                element={<CreateCategoryPage onCreate={createCategory} />}
              />
              <Route
                path="/categories/:categoryId"
                element={
                  <CategoryPage
                    categories={categories}
                    products={products}
                    onMoveCategory={moveProductToCategory}
                    onDeleteProduct={deleteProduct}
                  />
                }
              />
              <Route path="*" element={<Navigate to="/" replace />} />
            </Routes>
          </>
        )}
      </main>
     <footer className="mt-12 bg-slate-950 px-6 py-8 text-white">
        <div className="mx-auto flex max-w-6xl flex-col gap-4 text-center md:flex-row md:items-center md:justify-between md:text-left">
          <div>
            <h2 className="text-lg font-semibold">Product Store</h2>
            <p className="mt-1 text-sm text-slate-300">
              A simple inventory system to manage products, categories, stock,
              and product details.
            </p>
          </div>

          <div className="text-sm text-slate-300">
            <p>Built for product inventory management.</p>
            <p>Track stock, organize categories, and update products easily.</p>
            <p className="mt-2 text-slate-400">© 2026 Product Store</p>
          </div>
        </div>
      </footer>
    </div>


  );
}

export default App;
