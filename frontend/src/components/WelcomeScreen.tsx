import React, { useState, useEffect } from "react";
import "./WelcomeScreen.css";

interface Props {
  onEnter: () => void;
}

export default function WelcomeScreen({ onEnter }: Props) {
  const [visible, setVisible] = useState(false);

  useEffect(() => {
    const t = setTimeout(() => setVisible(true), 100);
    return () => clearTimeout(t);
  }, []);

  return (
    <div className={`welcome ${visible ? "welcome--visible" : ""}`}>
      <div className="welcome__bg">
        {Array.from({ length: 20 }).map((_, i) => (
          <div
            key={i}
            className="welcome__particle"
            style={{
              left: `${Math.random() * 100}%`,
              animationDelay: `${Math.random() * 4}s`,
              animationDuration: `${3 + Math.random() * 4}s`,
            }}
          />
        ))}
      </div>

      <div className="welcome__content">
        <div className="welcome__badge">RIPPLING INTERNEERS LAB 2026</div>
        <h1 className="welcome__title">
          <span className="welcome__title-line">Inventory</span>
          <span className="welcome__title-line welcome__title-line--accent">Management</span>
          <span className="welcome__title-line">System</span>
        </h1>
        <p className="welcome__sub">A fullstack Django + React implementation</p>
        <button className="welcome__cta" onClick={onEnter}>
          <span>Enter System</span>
          <svg
            width="18"
            height="18"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            strokeWidth="2"
          >
            <path d="M5 12h14M12 5l7 7-7 7" />
          </svg>
        </button>
        <div className="welcome__hint">Click the button to continue</div>
      </div>

      <div className="welcome__grid" />
    </div>
  );
}
