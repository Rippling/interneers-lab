/**
 * FilterBar — search and filter controls for the product list.
 */

import React, { useState, useEffect, useRef, useCallback } from "react";
import type { Category, ProductFilters } from "../types";
import "./FilterBar.css";

interface Props {
  categories: Category[];
  onFilterChange: (filters: ProductFilters) => void;
  loading?: boolean;
}

function useDebounce<T>(value: T, delay: number): T {
  const [debounced, setDebounced] = useState(value);
  useEffect(() => {
    const t = setTimeout(() => setDebounced(value), delay);
    return () => clearTimeout(t);
  }, [value, delay]);
  return debounced;
}

export default function FilterBar({ categories, onFilterChange, loading }: Props) {
  // ── live search (debounced) ──────────────────────────────────────
  const [search, setSearch] = useState("");
  const debouncedSearch = useDebounce(search, 300);

  // ── modal state ──────────────────────────────────────────────────
  const [modalOpen, setModalOpen] = useState(false);

  // draft values inside the modal (not applied until user clicks Apply)
  const [draftMinPrice, setDraftMinPrice] = useState("");
  const [draftMaxPrice, setDraftMaxPrice] = useState("");
  const [draftCategoryId, setDraftCategoryId] = useState("");

  // applied values (sent to parent)
  const [appliedMinPrice, setAppliedMinPrice] = useState("");
  const [appliedMaxPrice, setAppliedMaxPrice] = useState("");
  const [appliedCategoryId, setAppliedCategoryId] = useState("");

  const modalRef = useRef<HTMLDivElement>(null);

  // ── how many filter groups are active ───────────────────────────
  const activeFilterCount =
    (appliedMinPrice || appliedMaxPrice ? 1 : 0) + (appliedCategoryId ? 1 : 0);

  // ── fire onFilterChange whenever search or applied filters change ─
  const currentFilters = useRef<ProductFilters>({});

  const fireChange = useCallback(
    (search: string, minPrice: string, maxPrice: string, categoryId: string) => {
      const filters: ProductFilters = {};
      if (search) filters.search = search;
      if (minPrice) filters.minPrice = minPrice;
      if (maxPrice) filters.maxPrice = maxPrice;
      if (categoryId) filters.categoryId = categoryId;
      currentFilters.current = filters;
      onFilterChange(filters);
    },
    [onFilterChange]
  );

  // Trigger on every debounced search change
  useEffect(() => {
    fireChange(debouncedSearch, appliedMinPrice, appliedMaxPrice, appliedCategoryId);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [debouncedSearch]);

  // ── modal helpers ────────────────────────────────────────────────
  function openModal() {
    // pre-fill drafts with whatever is currently applied
    setDraftMinPrice(appliedMinPrice);
    setDraftMaxPrice(appliedMaxPrice);
    setDraftCategoryId(appliedCategoryId);
    setModalOpen(true);
  }

  function handleApply() {
    setAppliedMinPrice(draftMinPrice);
    setAppliedMaxPrice(draftMaxPrice);
    setAppliedCategoryId(draftCategoryId);
    setModalOpen(false);
    fireChange(debouncedSearch, draftMinPrice, draftMaxPrice, draftCategoryId);
  }

  function handleClearModal() {
    setDraftMinPrice("");
    setDraftMaxPrice("");
    setDraftCategoryId("");
  }

  function handleCancel() {
    setModalOpen(false);
  }

  function handleClearAll() {
    setSearch("");
    setAppliedMinPrice("");
    setAppliedMaxPrice("");
    setAppliedCategoryId("");
    // fire immediately (search debounce won't catch the cleared state fast enough)
    onFilterChange({});
  }

  // close modal on backdrop click
  function handleBackdropClick(e: React.MouseEvent) {
    if (e.target === e.currentTarget) handleCancel();
  }

  // close modal on Escape
  useEffect(() => {
    if (!modalOpen) return;
    function onKey(e: KeyboardEvent) {
      if (e.key === "Escape") handleCancel();
    }
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
  }, [modalOpen]);

  const hasAnyFilter = search || appliedMinPrice || appliedMaxPrice || appliedCategoryId;

  return (
    <>
      <div className="filter-bar">
        {/* Live search */}
        <div className="filter-row filter-row--search">
          <div className="filter-search-wrap">
            <span className="filter-search-icon">⌕</span>
            <input
              type="text"
              className="filter-input filter-search"
              placeholder="Search products…"
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              disabled={loading}
            />
            {search && (
              <button
                className="filter-search-clear"
                onClick={() => setSearch("")}
                aria-label="Clear search"
              >
                ✕
              </button>
            )}
          </div>
        </div>

        {/* Row: Filters button + Clear all */}
        <div className="filter-row filter-row--controls">
          <button
            className={`filter-btn filter-btn-open ${activeFilterCount > 0 ? "has-filters" : ""}`}
            onClick={openModal}
            disabled={loading}
          >
            ⚙ Filters
            {activeFilterCount > 0 && (
              <span className="filter-badge">{activeFilterCount}</span>
            )}
          </button>

          {/* Summary chips for applied filters */}
          {appliedCategoryId && (
            <span className="filter-chip">
              {categories.find((c) => c.id === appliedCategoryId)?.title ?? "Category"}
              <button
                className="filter-chip-remove"
                onClick={() => {
                  setAppliedCategoryId("");
                  fireChange(debouncedSearch, appliedMinPrice, appliedMaxPrice, "");
                }}
              >
                ✕
              </button>
            </span>
          )}
          {(appliedMinPrice || appliedMaxPrice) && (
            <span className="filter-chip">
              {appliedMinPrice ? `$${appliedMinPrice}` : ""}
              {appliedMinPrice && appliedMaxPrice ? " – " : ""}
              {appliedMaxPrice ? `$${appliedMaxPrice}` : ""}
              <button
                className="filter-chip-remove"
                onClick={() => {
                  setAppliedMinPrice("");
                  setAppliedMaxPrice("");
                  fireChange(debouncedSearch, "", "", appliedCategoryId);
                }}
              >
                ✕
              </button>
            </span>
          )}

          {hasAnyFilter && (
            <button className="filter-btn filter-btn-clear" onClick={handleClearAll}>
              Clear all
            </button>
          )}
        </div>
      </div>

      {/* ── Filter Modal ─────────────────────────────────────────── */}
      {modalOpen && (
        <div className="filter-modal-backdrop" onClick={handleBackdropClick}>
          <div className="filter-modal" ref={modalRef} role="dialog" aria-modal="true" aria-label="Filter products">
            <div className="filter-modal-header">
              <h2 className="filter-modal-title">Filter Products</h2>
              <button className="filter-modal-close" onClick={handleCancel} aria-label="Close">✕</button>
            </div>

            <div className="filter-modal-body">
              {/* Price range */}
              <fieldset className="filter-modal-section">
                <legend className="filter-modal-section-label">Price Range</legend>
                <div className="filter-price-group">
                  <input
                    type="number"
                    className="filter-input filter-price"
                    placeholder="Min ($)"
                    value={draftMinPrice}
                    min={0}
                    onChange={(e) => setDraftMinPrice(e.target.value)}
                  />
                  <span className="filter-sep">—</span>
                  <input
                    type="number"
                    className="filter-input filter-price"
                    placeholder="Max ($)"
                    value={draftMaxPrice}
                    min={0}
                    onChange={(e) => setDraftMaxPrice(e.target.value)}
                  />
                </div>
              </fieldset>

              {/* Category */}
              <fieldset className="filter-modal-section">
                <legend className="filter-modal-section-label">Category</legend>
                <select
                  className="filter-input filter-select"
                  value={draftCategoryId}
                  onChange={(e) => setDraftCategoryId(e.target.value)}
                >
                  <option value="">All categories</option>
                  {categories.map((cat) => (
                    <option key={cat.id} value={cat.id}>
                      {cat.title}
                    </option>
                  ))}
                </select>
              </fieldset>
            </div>

            <div className="filter-modal-footer">
              <button className="filter-btn filter-btn-clear" onClick={handleClearModal}>
                Reset
              </button>
              <div className="filter-modal-footer-right">
                <button className="filter-btn filter-btn-cancel" onClick={handleCancel}>
                  Cancel
                </button>
                <button className="filter-btn filter-btn-apply" onClick={handleApply}>
                  Apply →
                </button>
              </div>
            </div>
          </div>
        </div>
      )}
    </>
  );
}
