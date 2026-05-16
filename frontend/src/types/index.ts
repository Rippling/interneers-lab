/**
 * Shared TypeScript types for the Inventory Management System.
 */
export interface CategoryResponse {
  message: string;
  category: Category;
}

export interface Category {
  id: string;
  title: string;
  description: string;
  created_at: string;
  updated_at: string;
}

export interface Product {
  id: string;
  name: string;
  description: string;
  price: number;
  brand: string;
  quantity: number;
  category: { id: string; title: string } | null;
  image_url: string | null;
  created_at: string;
  updated_at: string;
}

export interface PaginatedProducts {
  page: number;
  page_size: number;
  total_products: number;
  total_pages: number;
  filters_applied: Record<string, unknown>;
  products: Product[];
}

export interface PaginatedCategories {
  page: number;
  page_size: number;
  total_categories: number;
  total_pages: number;
  categories: Category[];
}

export interface ProductFilters {
  search?: string;
  minPrice?: string;
  maxPrice?: string;
  categoryId?: string;
}

export interface ProductPayload {
  name: string;
  description: string;
  brand: string;
  price: number;
  quantity: number;
  image_url?: string | null;
  category_id?: string | null;
}

export interface ProductResponse {
  message: string;
  product: Product;
}
