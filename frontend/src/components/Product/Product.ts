export type Product = {
  id: string; 
  name: string;
  description?: string;
  category?: string | null; 
  price?: number;
  brand: string;
  quantity?: number;
  created_at: string; 
  updated_at: string;
};