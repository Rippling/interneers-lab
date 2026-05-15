/**
 * Custom hook: useProducts
 *
 * Encapsulates all state and fetching logic for the products list.
 * Components that need products just call this hook — they don't care
 * about fetch(), loading state, or error handling.
 *
 * This is the React pattern for separating data-fetching from rendering.
 */

import { useState, useEffect, useCallback } from "react";
import { fetchProducts } from "../api/client";
import type { Product, ProductFilters } from "../types";

export function useProducts(pageSize = 9) {
  const [products, setProducts] = useState<Product[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [page, setPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);
  const [totalProducts, setTotalProducts] = useState(0);
  const [filters, setFilters] = useState<ProductFilters>({});
  const [tick, setTick] = useState(0);

  const refresh = useCallback(() => setTick((t) => t + 1), []);
  const updateFilters = useCallback((nextFilters: ProductFilters) => {
    setFilters(nextFilters);
    setPage(1);
  }, []);

  useEffect(() => {
    let cancelled = false;
    setLoading(true);
    setError(null);
    fetchProducts(page, pageSize, filters)
      .then((data) => {
        if (cancelled) return;
        setProducts(data.products);
        setTotalPages(data.total_pages);
        setTotalProducts(data.total_products); // ← was total_count
      })
      .catch((e) => {
        if (cancelled) return;
        setError(e.message ?? "Unknown error");
      })
      .finally(() => {
        if (cancelled) return;
        setLoading(false);
      });
    return () => {
      cancelled = true;
    };
  }, [page, pageSize, filters, tick]);

  return {
    products,
    loading,
    error,
    page,
    totalPages,
    totalProducts,
    setPage,
    setFilters: updateFilters,
    refresh,
  };
}
