import React from "react";
import { Link, useLocation } from "react-router-dom";
import "./Header.css";

interface Props {
  onSettingsClick?: () => void;
}

export default function Header({ onSettingsClick }: Props) {
  const location = useLocation();

  const navLinks = [
    { to: "/",           label: "Home" },
    { to: "/categories", label: "Categories" },
    { to: "/reports",    label: "Reports" },
  ];

  return (
    <header className="header">
      <div className="header-inner">
        <Link to="/" className="header-logo">
          <span className="header-logo-mark">▣</span>
          <span className="header-logo-text">WAREHOUSE</span>
        </Link>

        <nav className="header-nav">
          {navLinks.map(link => (
            <Link
              key={link.to}
              to={link.to}
              className={
                "header-nav-link" +
                (location.pathname === link.to ? " active" : "")
              }
            >
              {link.label}
            </Link>
          ))}
        </nav>

        <button className="header-settings-btn" onClick={onSettingsClick}>
          ⚙
        </button>
      </div>
    </header>
  );
}