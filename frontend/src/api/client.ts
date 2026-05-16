/**
 * API client — all fetch calls to the Django backend live here.
 */

import type {
  PaginatedProducts,
  PaginatedCategories,
  Product,
  ProductResponse,
  Category,
  CategoryResponse,
  ProductFilters,
  ProductPayload,
} from "../types";

const API_BASE = process.env.REACT_APP_API_BASE ?? "http://localhost:8000";

// ── helpers ──────────────────────────────────────────────────────────

async function apiFetch<T>(path: string, options?: RequestInit): Promise<T> {
  const response = await fetch(`${API_BASE}${path}`, options);
  if (!response.ok) {
    const body = await response.json().catch(() => ({}));
    throw new Error(body.error ?? `HTTP ${response.status}`);
  }
  if (response.status === 204) return undefined as T;
  return response.json() as Promise<T>;
}

const jsonOptions = (method: string, body: unknown): RequestInit => ({
  method,
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify(body),
});

// ── Products ─────────────────────────────────────────────────────────

export async function fetchProducts(
  page = 1,
  pageSize = 9,
  filters: ProductFilters = {}
): Promise<PaginatedProducts> {
  const params = new URLSearchParams();
  params.set("page", String(page));
  params.set("page_size", String(pageSize));
  if (filters.search) params.set("search", filters.search);
  if (filters.minPrice) params.set("min_price", filters.minPrice);
  if (filters.maxPrice) params.set("max_price", filters.maxPrice);
  if (filters.categoryId) params.set("category_ids", filters.categoryId);
  return apiFetch<PaginatedProducts>(`/products/?${params}`);
}

export async function fetchProduct(id: string): Promise<Product> {
  return apiFetch<Product>(`/products/${id}/`);
}

export async function createProduct(data: ProductPayload): Promise<Product> {
  const res = await apiFetch<ProductResponse>("/products/", jsonOptions("POST", data));
  return res.product;
}

export async function updateProduct(
  id: string,
  data: ProductPayload // ← was Partial<ProductPayload>, PUT requires all fields
): Promise<Product> {
  const res = await apiFetch<ProductResponse>(`/products/${id}/`, jsonOptions("PUT", data));
  return res.product;
}

export async function deleteProduct(id: string): Promise<void> {
  return apiFetch<void>(`/products/${id}/`, { method: "DELETE" });
}

export async function moveProductCategory(productId: string, categoryId: string): Promise<Product> {
  const res = await apiFetch<ProductResponse>(
    `/products/${productId}/category/`,
    jsonOptions("PUT", { category_id: categoryId })
  );
  return res.product;
}

export async function fetchProductsByCategory(
  categoryId: string
): Promise<{ category: Category; total_products: number; products: Product[] }> {
  return apiFetch(`/categories/${categoryId}/products/`);
}

// ── Categories ───────────────────────────────────────────────────────

export async function fetchCategories(pageSize = 50): Promise<PaginatedCategories> {
  return apiFetch<PaginatedCategories>(`/categories/?page_size=${pageSize}`);
}

export async function fetchCategory(id: string): Promise<Category> {
  return apiFetch<Category>(`/categories/${id}/`);
}

export async function createCategory(
  data: Omit<Category, "id" | "created_at" | "updated_at">
): Promise<Category> {
  const res = await apiFetch<CategoryResponse>("/categories/", jsonOptions("POST", data));
  return res.category;
}

export async function updateCategory(
  id: string,
  data: Omit<Category, "id" | "created_at" | "updated_at">
): Promise<Category> {
  const res = await apiFetch<CategoryResponse>(`/categories/${id}/`, jsonOptions("PUT", data));
  return res.category;
}

export async function deleteCategory(id: string): Promise<void> {
  return apiFetch<void>(`/categories/${id}/`, { method: "DELETE" });
}
