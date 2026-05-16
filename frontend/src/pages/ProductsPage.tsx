/**
 * ProductsPage — the main products listing page at route "/".
 *
 * Week 8: connects FilterBar, ProductList, and Pagination together
 * using the useProducts and useCategories hooks for real API data.
 * Handles loading state, error state, loading spinners, and full CRUD.
 */

import React, { useState, useEffect } from "react";
import FilterBar from "../components/FilterBar";
import ProductList from "../components/ProductList";
import Pagination from "../components/Pagination";
import ProductForm from "../components/ProductForm";
import { useProducts } from "../hooks/useProducts";
import { useCategories } from "../hooks/useCategories";
import { createProduct, updateProduct, deleteProduct } from "../api/client";
import type { Category, Product, ProductPayload } from "../types";
import "./ProductsPage.css";

interface Props {
  pageSize?: number;
}

export default function ProductsPage({ pageSize = 9 }: Props) {
  const {
    products,
    loading,
    error,
    page,
    totalPages,
    totalProducts,
    setPage,
    setFilters,
    refresh,
  } = useProducts(pageSize);

  const { categories, loading: categoriesLoading, refresh: refreshCategories } = useCategories();

  // null = form closed | undefined = creating new | Product = editing existing
  const [formProduct, setFormProduct] = useState<Product | undefined | null>(null);
  const [saving, setSaving] = useState(false);
  const [actionError, setActionError] = useState<string | null>(null);
  const [extraCategories, setExtraCategories] = useState<Category[]>([]);

  // Once the categories hook finishes re-fetching (loading flips false),
  // the new category is already in `categories`, so clear extraCategories
  // to prevent it appearing twice in allCategories.
  useEffect(() => {
    if (!categoriesLoading) setExtraCategories([]);
  }, [categoriesLoading]);

  const allCategories = [...categories, ...extraCategories];

  async function handleSave(data: ProductPayload) {
    setSaving(true);
    setActionError(null);
    try {
      if (formProduct?.id) {
        await updateProduct(formProduct.id, data);
      } else {
        await createProduct(data);
      }
      setFormProduct(null);
      refresh();
    } catch (e: any) {
      setActionError(e.message ?? "Save failed");
    } finally {
      setSaving(false);
    }
  }

  async function handleDelete(product: Product) {
    if (!window.confirm(`Delete "${product.name}"?`)) return;
    setActionError(null);
    try {
      await deleteProduct(product.id);
      refresh();
    } catch (e: any) {
      setActionError(e.message ?? "Delete failed");
    }
  }

  function handleCategoryCreated(cat: Category) {
    // Optimistically show the new category immediately while the API re-fetches.
    // The useEffect above clears extraCategories once categoriesLoading settles,
    // at which point `categories` from the hook already contains it.
    setExtraCategories((prev) => [...prev, cat]);
    refreshCategories?.();
  }

  return (
    <div className="products-page">
      <div className="products-page-title-row">
        <h1 className="products-page-title">Products</h1>
        {!loading && (
          <span className="products-page-count">{totalProducts} total</span>
        )}
        <button
          className="btn-primary"
          onClick={() => setFormProduct(undefined)}
        >
          + New Product
        </button>
      </div>

      <FilterBar
        categories={allCategories}
        onFilterChange={setFilters}
        loading={loading}
      />

      {(error || actionError) && (
        <div className="products-page-error">
          <span className="error-icon">⚠</span>
          {error === "Failed to fetch"
            ? "Could not reach the API — make sure Django is running on localhost:8000"
            : error ?? actionError}
        </div>
      )}

      <ProductList
        products={products}
        loading={loading}
        emptyMessage="No products match your filters"
        onEdit={(p) => setFormProduct(p)}
        onDelete={handleDelete}
      />

      <Pagination
        page={page}
        totalPages={totalPages}
        totalProducts={totalProducts}
        onPageChange={setPage}
      />

      {formProduct !== null && (
        <ProductForm
          product={formProduct}
          categories={allCategories}
          saving={saving}
          onSave={handleSave}
          onClose={() => setFormProduct(null)}
          onCategoryCreated={handleCategoryCreated}
        />
      )}
    </div>
  );
}