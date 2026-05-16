/**
 * Custom hook: useCategories
 * Fetches all categories once on mount — used to populate filter dropdowns.
 */

import { useState, useEffect, useCallback } from "react";
import { fetchCategories } from "../api/client";
import type { Category } from "../types";

interface UseCategoriesResult {
  categories: Category[];
  loading: boolean;
  error: string | null;
  refresh: () => void;
}

export function useCategories(): UseCategoriesResult {
  const [categories, setCategories] = useState<Category[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [tick, setTick] = useState(0);

  const refresh = useCallback(() => setTick((t) => t + 1), []);

  useEffect(() => {
    let cancelled = false;
    setLoading(true);
    setError(null);
    fetchCategories()
      .then((data) => {
        if (cancelled) return;
        setCategories(data.categories);
      })
      .catch((err) => {
        if (cancelled) return;
        setError(err.message);
      })
      .finally(() => {
        if (cancelled) return;
        setLoading(false);
      });
    return () => { cancelled = true; };
  }, [tick]);

  return { categories, loading, error, refresh };
}