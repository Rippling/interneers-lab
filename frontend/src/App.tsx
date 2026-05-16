import React, { useState, useEffect } from "react";
import { Routes, Route } from "react-router-dom";
import Header from "./components/Header";
import ProductsPage from "./pages/ProductsPage";
import CategoriesPage from "./pages/CategoriesPage";
import ReportsPage from "./pages/ReportsPage";
import WelcomeScreen from "./components/WelcomeScreen";
import SettingsPanel, {
  defaultSettings,
  applySettings,
  type Settings,
} from "./components/SettingsPanel";
import "./App.css";

function NotFound() {
  return (
    <div
      style={{
        maxWidth: 1400,
        margin: "0 auto",
        padding: "80px 32px",
        textAlign: "center",
        fontFamily: "'Syne', sans-serif",
      }}
    >
      <div style={{ fontSize: 48, color: "#2a2a2a", marginBottom: 16 }}>◈</div>
      <h2 style={{ fontSize: 24, color: "#3d3d3d", marginBottom: 8 }}>
        404 — Page not found
      </h2>
      <a
        href="/"
        style={{
          color: "#1a1a1a",
          fontSize: 13,
          fontFamily: "'DM Mono', monospace",
        }}
      >
        ← Back to products
      </a>
    </div>
  );
}

export default function App() {
  const [entered, setEntered] = useState(false);
  const [showSettings, setShowSettings] = useState(false);
  const [settings, setSettings] = useState<Settings>(() => {
    try {
      const saved = localStorage.getItem("wh-settings");
      return saved ? { ...defaultSettings, ...JSON.parse(saved) } : defaultSettings;
    } catch {
      return defaultSettings;
    }
  });

  // Apply ALL settings (theme, font size, density, animations) on every change
  // and on first mount — this covers page refresh so no preferences are lost
  useEffect(() => {
    applySettings(settings);
  }, [settings]);

  // Persist settings to localStorage whenever they change
  useEffect(() => {
    localStorage.setItem("wh-settings", JSON.stringify(settings));
  }, [settings]);

  function handleSettingsChange(newSettings: Settings) {
    setSettings(newSettings);
  }

  if (!entered) {
    return <WelcomeScreen onEnter={() => setEntered(true)} />;
  }

  return (
    <div className="app app--entered">
      <Header onSettingsClick={() => setShowSettings(true)} />
      <main className="app-main">
        <Routes>
          <Route path="/" element={<ProductsPage pageSize={settings.pageSize} />} />
          <Route path="/categories" element={<CategoriesPage />} />
          <Route path="/reports" element={<ReportsPage />} />
          <Route path="*" element={<NotFound />} />
        </Routes>
      </main>

      {showSettings && (
        <SettingsPanel
          settings={settings}
          onChange={handleSettingsChange}
          onClose={() => setShowSettings(false)}
        />
      )}
    </div>
  );
}