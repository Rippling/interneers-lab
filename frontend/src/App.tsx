import React from "react";
import { BrowserRouter as Router, Routes, Route, Link } from "react-router-dom";
import Home from "./pages/Home";
import Products from "./pages/Products";
import AddPage from "./components/AddPage";

const App: React.FC = () => {
  return (
    <>
      <div
        className="navbar"
        style={{
          display: "flex",
          justifyContent: "flex-end",
          gap: "20px",
          padding: "10px",
        }}
      >
        <Link to="/">Home</Link>
        <Link to="/products">Products</Link>
        <Link to="/add">Add</Link>
      </div>

      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/products" element={<Products />} />
        <Route path="/add" element={<AddPage />} />
      </Routes>
    </>
  );
};

export default App;
