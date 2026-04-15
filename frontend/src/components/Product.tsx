import React, { useState } from "react";
import { Link } from "react-router-dom";

export interface CategoryType {
  id: string;
  title: string;
  description: string;
}

export interface ProductType {
  id: string;
  name: string;
  brand: string;
  price: number;
  quantity: number;
  categoryId: string | null;
  categoryName: string;
  description: string;
  imageUrl: string;
}

interface ProductProps {
  product: ProductType;
  categories: CategoryType[];
  onMoveCategory: (productId: string, newCategoryId: string) => void;
  onDeleteProduct: (productId: string) => void;
}

function Product({
  product,
  categories,
  onMoveCategory,
  onDeleteProduct,
}: ProductProps) {
  const [selectedCategory, setSelectedCategory] = useState(
    product.categoryId || "",
  );

  const stockLabel =
    product.quantity <= 0
      ? "Out of Stock"
      : product.quantity < 5
        ? "Low Stock"
        : "In Stock";

  const stockBadgeClass =
    product.quantity <= 0
      ? "bg-rose-100 text-rose-700"
      : product.quantity < 5
        ? "bg-amber-100 text-amber-700"
        : "bg-cyan-100 text-cyan-700";

  const handleDelete = () => {
    const confirmed = window.confirm(
      `Are you sure you want to delete "${product.name}"?`,
    );

    if (confirmed) {
      onDeleteProduct(product.id);
    }
  };

  return (
    <article className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm transition hover:-translate-y-1 hover:shadow-lg">
      {product.imageUrl ? (
        <img
          className="mb-4 h-48 w-full rounded-2xl object-cover"
          src={product.imageUrl}
          alt={product.name}
        />
      ) : (
        <div className="mb-4 flex h-48 w-full items-center justify-center rounded-2xl bg-slate-100 text-sm font-semibold text-slate-400">
          No image
        </div>
      )}

      <div className="mb-3 flex justify-end">
        <span
          className={`rounded-full px-3 py-1 text-xs font-bold ${stockBadgeClass}`}
        >
          {stockLabel}
        </span>
      </div>

      <h2 className="mb-3 text-xl font-bold text-slate-900">{product.name}</h2>

      <p className="mb-4 min-h-[48px] text-sm leading-6 text-slate-500">
        {product.description}
      </p>

      <div className="space-y-2 text-sm text-slate-700">
        <p>
          <strong>Brand:</strong> {product.brand}
        </p>
        <p>
          <strong>Price:</strong> Rs. {product.price}
        </p>
        <p>
          <strong>Quantity:</strong> {product.quantity}
        </p>
        <p>
          <strong>Category:</strong>{" "}
          {product.categoryId ? (
            <Link
              className="font-semibold text-cyan-700 hover:underline"
              to={`/categories/${product.categoryId}`}
            >
              {product.categoryName}
            </Link>
          ) : (
            "No Category"
          )}
        </p>
      </div>

      <div className="mt-5 flex gap-3">
        <select
          className="flex-1 rounded-xl border border-slate-300 px-3 py-2 text-sm outline-none transition focus:border-cyan-500 focus:ring-2 focus:ring-cyan-200"
          value={selectedCategory}
          onChange={(event) => setSelectedCategory(event.target.value)}
        >
          <option value="">No Category</option>
          {categories.map((category) => (
            <option key={category.id} value={category.id}>
              {category.title}
            </option>
          ))}
        </select>

        <button
          className="rounded-xl bg-cyan-600 px-4 py-2 text-sm font-semibold text-white transition hover:bg-cyan-700"
          onClick={() => onMoveCategory(product.id, selectedCategory)}
        >
          Move
        </button>
      </div>

      <div className="mt-5 flex items-center justify-between">
        <Link
          className="font-semibold text-cyan-700 hover:underline"
          to={`/products/${product.id}`}
        >
          Edit Product
        </Link>

        <button
          className="rounded-xl bg-rose-600 px-4 py-2 text-sm font-semibold text-white transition hover:bg-rose-700"
          onClick={handleDelete}
        >
          Delete
        </button>
      </div>
    </article>
  );
}

export default Product;
