/**
 * CategoriesPage — lists all categories from the API.
 * Clicking a category fetches and shows only that category's products.
 * No hardcoded data anywhere.
 */

import React, { useState, useEffect, useCallback } from "react";
import {
  fetchCategories,
  fetchProductsByCategory,
  createCategory,
  updateCategory,
  deleteCategory,
} from "../api/client";
import type { Category, Product } from "../types";
import ProductList from "../components/ProductList";
import "./CategoriesPage.css";

interface CategoryWithCount extends Category {
  product_count?: number;
}

export default function CategoriesPage() {
  const [categories, setCategories] = useState<CategoryWithCount[]>([]);
  const [loadingCats, setLoadingCats] = useState(true);
  const [catsError, setCatsError] = useState<string | null>(null);

  // Expanded category state
  const [expandedId, setExpandedId] = useState<string | null>(null);
  const [expandedProducts, setExpandedProducts] = useState<Product[]>([]);
  const [expandedTotal, setExpandedTotal] = useState(0);
  const [loadingProducts, setLoadingProducts] = useState(false);
  const [productsError, setProductsError] = useState<string | null>(null);

  // Inline category form state
  const [showForm, setShowForm] = useState(false);
  const [editingCat, setEditingCat] = useState<Category | null>(null);
  const [formTitle, setFormTitle] = useState("");
  const [formDesc, setFormDesc] = useState("");
  const [formError, setFormError] = useState<string | null>(null);
  const [saving, setSaving] = useState(false);

  const loadCategories = useCallback(async () => {
    setLoadingCats(true);
    setCatsError(null);
    try {
      const data = await fetchCategories(100);
      setCategories(data.categories);
    } catch (e: any) {
      setCatsError(e.message ?? "Failed to load categories");
    } finally {
      setLoadingCats(false);
    }
  }, []);

  useEffect(() => {
    loadCategories();
  }, [loadCategories]);

  async function handleToggleCategory(catId: string) {
    if (expandedId === catId) {
      setExpandedId(null);
      setExpandedProducts([]);
      return;
    }

    setExpandedId(catId);
    setExpandedProducts([]);
    setLoadingProducts(true);
    setProductsError(null);

    try {
      const data = await fetchProductsByCategory(catId);
      setExpandedProducts(data.products);
      setExpandedTotal(data.total_products);
    } catch (e: any) {
      setProductsError(e.message ?? "Failed to load products");
    } finally {
      setLoadingProducts(false);
    }
  }

  function openNewForm() {
    setEditingCat(null);
    setFormTitle("");
    setFormDesc("");
    setFormError(null);
    setShowForm(true);
  }

  function openEditForm(cat: Category) {
    setEditingCat(cat);
    setFormTitle(cat.title);
    setFormDesc(cat.description);
    setFormError(null);
    setShowForm(true);
  }

  function closeForm() {
    setShowForm(false);
    setEditingCat(null);
    setFormTitle("");
    setFormDesc("");
    setFormError(null);
  }

  async function handleSaveCategory() {
    if (!formTitle.trim()) return setFormError("Title is required");
    if (!formDesc.trim()) return setFormError("Description is required");

    setSaving(true);
    setFormError(null);
    try {
      if (editingCat) {
        await updateCategory(editingCat.id, {
          title: formTitle.trim(),
          description: formDesc.trim(),
        });
      } else {
        await createCategory({
          title: formTitle.trim(),
          description: formDesc.trim(),
        });
      }
      closeForm();
      await loadCategories();
    } catch (e: any) {
      setFormError(e.message ?? "Failed to save");
    } finally {
      setSaving(false);
    }
  }

  async function handleDeleteCategory(cat: Category) {
    if (!window.confirm(`Delete category "${cat.title}"? This cannot be undone.`)) return;
    try {
      await deleteCategory(cat.id);
      if (expandedId === cat.id) {
        setExpandedId(null);
        setExpandedProducts([]);
      }
      await loadCategories();
    } catch (e: any) {
      alert(e.message ?? "Failed to delete");
    }
  }

  return (
    <div className="cats-page">
      <div className="cats-page-header">
        <div className="cats-page-title-wrap">
          <h1 className="cats-page-title">Categories</h1>
          {!loadingCats && (
            <span className="cats-page-count">{categories.length} total</span>
          )}
        </div>
        <button className="cats-page-new-btn" onClick={openNewForm}>
          + New Category
        </button>
      </div>

      {/* Inline create/edit form */}
      {showForm && (
        <div className="cats-form-wrap">
          <h3 className="cats-form-title">
            {editingCat ? "Edit Category" : "New Category"}
          </h3>
          {formError && <div className="cats-form-error">⚠ {formError}</div>}
          <div className="cats-form-row">
            <label className="cats-form-label">
              Title *
              <input
                className="cats-form-input"
                value={formTitle}
                onChange={(e) => { setFormTitle(e.target.value); setFormError(null); }}
                placeholder="e.g. Kitchen Essentials"
              />
            </label>
            <label className="cats-form-label">
              Description *
              <input
                className="cats-form-input"
                value={formDesc}
                onChange={(e) => { setFormDesc(e.target.value); setFormError(null); }}
                placeholder="e.g. Cooking and kitchen tools"
              />
            </label>
          </div>
          <div className="cats-form-actions">
            <button className="cats-btn-secondary" onClick={closeForm} disabled={saving}>
              Cancel
            </button>
            <button className="cats-btn-primary" onClick={handleSaveCategory} disabled={saving}>
              {saving ? "Saving…" : editingCat ? "Save Changes" : "Create Category"}
            </button>
          </div>
        </div>
      )}

      {/* Error */}
      {catsError && (
        <div className="cats-error">
          Failed to load categories: {catsError}
          <button className="cats-error-retry" onClick={loadCategories}>Retry</button>
        </div>
      )}

      {/* Loading skeleton */}
      {loadingCats && (
        <div className="cats-grid">
          {Array.from({ length: 4 }).map((_, i) => (
            <div key={i} className="cat-card-skeleton" />
          ))}
        </div>
      )}

      {/* Category grid */}
      {!loadingCats && categories.length === 0 && !catsError && (
        <div className="cats-empty">
          <div className="cats-empty-icon">◈</div>
          <div className="cats-empty-text">No categories yet</div>
        </div>
      )}

      {!loadingCats && categories.length > 0 && (
        <div className="cats-grid">
          {categories.map((cat) => {
            const isExpanded = expandedId === cat.id;
            return (
              <div
                key={cat.id}
                className={`cat-card ${isExpanded ? "cat-card--expanded" : ""}`}
              >
                <div className="cat-card-body" onClick={() => handleToggleCategory(cat.id)}>
                  <div className="cat-card-title">{cat.title}</div>
                  <div className="cat-card-desc">{cat.description}</div>
                  <div className="cat-card-footer">
                    <span className="cat-card-hint">
                      {isExpanded ? "▲ hide products" : "▼ view products"}
                    </span>
                    <span className="cat-card-date">
                      {new Date(cat.created_at).toLocaleDateString()}
                    </span>
                  </div>
                </div>
                <div className="cat-card-actions">
                  <button
                    className="cat-card-action-btn"
                    onClick={(e) => { e.stopPropagation(); openEditForm(cat); }}
                    title="Edit category"
                  >
                    Edit
                  </button>
                  <button
                    className="cat-card-action-btn cat-card-action-btn--danger"
                    onClick={(e) => { e.stopPropagation(); handleDeleteCategory(cat); }}
                    title="Delete category"
                  >
                    Delete
                  </button>
                </div>
              </div>
            );
          })}
        </div>
      )}

      {/* Expanded products section */}
      {expandedId && (
        <div className="cats-products-section">
          <div className="cats-products-header">
            <span className="cats-products-label">
              PRODUCTS IN{" "}
              <span className="cats-products-cat-name">
                {categories.find((c) => c.id === expandedId)?.title?.toUpperCase()}
              </span>
            </span>
            {!loadingProducts && (
              <span className="cats-products-count">{expandedTotal} products</span>
            )}
          </div>

          {productsError && (
            <div className="cats-error">
              {productsError}
              <button
                className="cats-error-retry"
                onClick={() => handleToggleCategory(expandedId)}
              >
                Retry
              </button>
            </div>
          )}

          <ProductList
            products={expandedProducts}
            loading={loadingProducts}
            emptyMessage="No products in this category"
          />
        </div>
      )}
    </div>
  );
}