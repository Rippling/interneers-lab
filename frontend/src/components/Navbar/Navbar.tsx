import React from "react";
import "./Navbar.css";

const Navbar = () => {
  return (
    <nav className="navbar">
      <div className="navbar-links">
        <a>Home</a>
        <a>Products</a>
        <a>About</a>
      </div>
    </nav>
  );
};

export default Navbar;
