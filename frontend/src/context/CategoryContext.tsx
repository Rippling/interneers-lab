import React, {
  createContext,
  useContext,
  useEffect,
  useMemo,
  useState,
} from "react";
import { Category } from "../types/Category";

type CategoryContextType = {
  categories: Category[];
  categoryMap: Map<string, Category>;
  loading: boolean;
  refreshCategories: () => void;
};

const CategoryContext = createContext<CategoryContextType | undefined>(
  undefined,
);

const CATEGORY_URL = "http://127.0.0.1:8001/api/categories/";

export const CategoryProvider = ({
  children,
}: {
  children: React.ReactNode;
}) => {
  const [categories, setCategories] = useState<Category[]>([]);
  const [loading, setLoading] = useState(true);

  const fetchCategories = async () => {
    setLoading(true);
    try {
      const res = await fetch(CATEGORY_URL);
      const data = await res.json();

      const normalized = (data.results || data).map((c: any) => ({
        id: c.id || c._id,
        title: c.title,
        description: c.description,
        author: c.author,
      }));

      setCategories(normalized);
    } catch (err) {
      console.error("Error fetching categories", err);
    }
    setLoading(false);
  };

  useEffect(() => {
    fetchCategories();
  }, []);

  const categoryMap = useMemo(
    () => new Map(categories.map((c) => [c.id, c])),
    [categories],
  );

  return (
    <CategoryContext.Provider
      value={{
        categories,
        categoryMap,
        loading,
        refreshCategories: fetchCategories,
      }}
    >
      {children}
    </CategoryContext.Provider>
  );
};

export const useCategories = () => {
  const context = useContext(CategoryContext);
  if (!context) {
    throw new Error("useCategories must be used within CategoryProvider");
  }
  return context;
};
