import React, { useState, useEffect } from "react";
import { fetchProducts, fetchCategories } from "../api/client";
import type { Product, Category } from "../types";
import "./ReportsPage.css";

interface CategoryReport {
  category: string;
  count: number;
  lowStock: number;
  totalValue: number;
}

interface PriceRangeReport {
  range: string;
  count: number;
  min: number;
  max: number;
}

export default function ReportsPage() {
  const [products, setProducts] = useState<Product[]>([]);
  const [categories, setCategories] = useState<Category[]>([]);
  const [loading, setLoading] = useState(true);
  const [activeReport, setActiveReport] = useState<"category" | "price" | "lowstock">("category");
  const [lowStockThreshold, setLowStockThreshold] = useState(10);
  const [minCategoryCount, setMinCategoryCount] = useState(0);

  useEffect(() => {
    async function load() {
      setLoading(true);
      try {
        const [pData, cData] = await Promise.all([fetchProducts(1, 200), fetchCategories(100)]);
        setProducts(pData.products);
        setCategories(cData.categories);
      } finally {
        setLoading(false);
      }
    }
    load();
  }, []);

  // ── Category Report ──────────────────────────────────────────────
  const categoryReport: CategoryReport[] = categories
    .map((cat) => {
      const catProducts = products.filter((p) => p.category?.id === cat.id);
      return {
        category: cat.title,
        count: catProducts.length,
        lowStock: catProducts.filter((p) => p.quantity <= lowStockThreshold).length,
        totalValue: catProducts.reduce((sum, p) => sum + p.price * p.quantity, 0),
      };
    })
    .filter((r) => r.count > minCategoryCount)
    .sort((a, b) => b.count - a.count);

  const uncategorized = products.filter((p) => !p.category);
  if (uncategorized.length > minCategoryCount) {
    categoryReport.push({
      category: "Uncategorized",
      count: uncategorized.length,
      lowStock: uncategorized.filter((p) => p.quantity <= lowStockThreshold).length,
      totalValue: uncategorized.reduce((sum, p) => sum + p.price * p.quantity, 0),
    });
  }

  // ── Price Range Report ───────────────────────────────────────────
  const priceRanges = [
    { label: "Under $10", min: 0, max: 10 },
    { label: "$10 – $50", min: 10, max: 50 },
    { label: "$50 – $100", min: 50, max: 100 },
    { label: "$100 – $500", min: 100, max: 500 },
    { label: "$500 – $1,000", min: 500, max: 1000 },
    { label: "Over $1,000", min: 1000, max: Infinity },
  ];

  const priceReport: PriceRangeReport[] = priceRanges
    .map((r) => ({
      range: r.label,
      count: products.filter((p) => p.price >= r.min && p.price < r.max).length,
      min: r.min,
      max: r.max,
    }))
    .filter((r) => r.count > 0);

  // ── Low Stock Report ─────────────────────────────────────────────
  const lowStockProducts = products
    .filter((p) => p.quantity <= lowStockThreshold)
    .sort((a, b) => a.quantity - b.quantity);

  const maxCount = Math.max(...categoryReport.map((r) => r.count), 1);
  const maxPriceCount = Math.max(...priceReport.map((r) => r.count), 1);

  function downloadCSV() {
    let csv = "";
    if (activeReport === "category") {
      csv =
        "Category,Products,Low Stock,Total Value\n" +
        categoryReport
          .map((r) => `"${r.category}",${r.count},${r.lowStock},$${r.totalValue.toFixed(2)}`)
          .join("\n");
    } else if (activeReport === "price") {
      csv = "Price Range,Count\n" + priceReport.map((r) => `"${r.range}",${r.count}`).join("\n");
    } else {
      csv =
        "Product,Brand,Category,Quantity,Price\n" +
        lowStockProducts
          .map(
            (p) =>
              `"${p.name}","${p.brand}","${p.category?.title ?? "None"}",${p.quantity},$${p.price}`
          )
          .join("\n");
    }
    const blob = new Blob([csv], { type: "text/csv" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = `report-${activeReport}-${Date.now()}.csv`;
    a.click();
    URL.revokeObjectURL(url);
  }

  if (loading) {
    return (
      <div className="reports-loading">
        <div className="reports-spinner" />
        <p>Generating reports…</p>
      </div>
    );
  }

  return (
    <div className="reports-page">
      <div className="reports-header">
        <div>
          <h1 className="reports-title">Reports</h1>
          <p className="reports-sub">
            {products.length} products across {categories.length} categories
          </p>
        </div>
        <button className="reports-export" onClick={downloadCSV}>
          ↓ Export CSV
        </button>
      </div>

      <div className="reports-tabs">
        {(["category", "price", "lowstock"] as const).map((tab) => (
          <button
            key={tab}
            className={`reports-tab ${activeReport === tab ? "reports-tab--active" : ""}`}
            onClick={() => setActiveReport(tab)}
          >
            {tab === "category" ? "By Category" : tab === "price" ? "By Price Range" : "Low Stock"}
          </button>
        ))}
      </div>

      {/* ── Controls ── */}
      <div className="reports-controls">
        {(activeReport === "category" || activeReport === "lowstock") && (
          <label className="reports-control">
            Low stock threshold
            <input
              type="number"
              min="1"
              max="100"
              value={lowStockThreshold}
              onChange={(e) => setLowStockThreshold(Number(e.target.value))}
            />
          </label>
        )}
        {activeReport === "category" && (
          <label className="reports-control">
            Min product count
            <input
              type="number"
              min="0"
              value={minCategoryCount}
              onChange={(e) => setMinCategoryCount(Number(e.target.value))}
            />
          </label>
        )}
      </div>

      {/* ── Category Report ── */}
      {activeReport === "category" && (
        <div className="reports-section">
          {categoryReport.length === 0 ? (
            <p className="reports-empty">No categories match the filter</p>
          ) : (
            <div className="reports-bars">
              {categoryReport.map((r, i) => (
                <div
                  key={r.category}
                  className="reports-bar-row"
                  style={{ animationDelay: `${i * 60}ms` }}
                >
                  <div className="reports-bar-label">
                    <span className="reports-bar-name">{r.category}</span>
                    <span className="reports-bar-meta">
                      {r.count} products · {r.lowStock} low · ${r.totalValue.toFixed(0)} value
                    </span>
                  </div>
                  <div className="reports-bar-track">
                    <div
                      className="reports-bar-fill"
                      style={{ width: `${(r.count / maxCount) * 100}%` }}
                    />
                    {r.lowStock > 0 && (
                      <div
                        className="reports-bar-fill reports-bar-fill--danger"
                        style={{ width: `${(r.lowStock / maxCount) * 100}%` }}
                      />
                    )}
                  </div>
                  <span className="reports-bar-count">{r.count}</span>
                </div>
              ))}
            </div>
          )}
        </div>
      )}

      {/* ── Price Range Report ── */}
      {activeReport === "price" && (
        <div className="reports-section">
          <div className="reports-bars">
            {priceReport.map((r, i) => (
              <div
                key={r.range}
                className="reports-bar-row"
                style={{ animationDelay: `${i * 60}ms` }}
              >
                <div className="reports-bar-label">
                  <span className="reports-bar-name">{r.range}</span>
                  <span className="reports-bar-meta">{r.count} products</span>
                </div>
                <div className="reports-bar-track">
                  <div
                    className="reports-bar-fill"
                    style={{ width: `${(r.count / maxPriceCount) * 100}%` }}
                  />
                </div>
                <span className="reports-bar-count">{r.count}</span>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* ── Low Stock Report ── */}
      {activeReport === "lowstock" && (
        <div className="reports-section">
          {lowStockProducts.length === 0 ? (
            <p className="reports-empty">No products below threshold of {lowStockThreshold}</p>
          ) : (
            <div className="reports-table-wrap">
              <table className="reports-table">
                <thead>
                  <tr>
                    <th>Product</th>
                    <th>Brand</th>
                    <th>Category</th>
                    <th>Qty</th>
                    <th>Price</th>
                  </tr>
                </thead>
                <tbody>
                  {lowStockProducts.map((p, i) => (
                    <tr
                      key={p.id}
                      style={{ animationDelay: `${i * 40}ms` }}
                      className="reports-table-row"
                    >
                      <td className="reports-table-name">{p.name}</td>
                      <td>{p.brand}</td>
                      <td>{p.category?.title ?? "—"}</td>
                      <td>
                        <span
                          className={`reports-qty ${p.quantity <= 5 ? "reports-qty--critical" : "reports-qty--low"}`}
                        >
                          {p.quantity}
                        </span>
                      </td>
                      <td>${p.price.toFixed(2)}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </div>
      )}
    </div>
  );
}
