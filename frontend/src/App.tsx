import React from "react";
import "./App.css";
import ProductList from "./components/ProductList";

function App() {
  return (
    <div className="app-shell">
      <header className="app-header">
        <div className="brand">Product Store</div>
        <nav className="app-nav">
          <a href="/">Home</a>
          <a href="/">Products</a>
          <a href="/">Categories</a>
          <a href="/">About</a>
        </nav>
      </header>

      <main className="app-main">
        <ProductList />
      </main>
    </div>
  );
}

export default App;
