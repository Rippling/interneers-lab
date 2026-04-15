import React, { useEffect, useState } from "react";
import { Link, useNavigate, useParams } from "react-router-dom";
import { CategoryType, ProductType } from "./Product";

interface ProductPageProps {
  products: ProductType[];
  categories: CategoryType[];
  onSave: (product: ProductType) => Promise<boolean> | boolean;
  onError: (message: string) => void;
}

function ProductPage({
  products,
  categories,
  onSave,
  onError,
}: ProductPageProps) {
  const { productId } = useParams();
  const navigate = useNavigate();

  const product = products.find((item) => item.id === productId);

  const [formData, setFormData] = useState<ProductType | null>(product ?? null);
  const [saving, setSaving] = useState(false);

  useEffect(() => {
    if (!product) {
      onError("Product page could not be loaded.");
      return;
    }

    setFormData(product);
    onError("");
  }, [product, onError]);

  if (!product || !formData) {
    return (
      <section className="mx-auto max-w-3xl">
        <h1 className="mb-4 text-3xl font-bold text-slate-900">
          Product Not Found
        </h1>
        <Link className="font-semibold text-cyan-700 hover:underline" to="/">
          Back to Product List
        </Link>
      </section>
    );
  }

  const handleChange = (
    event: React.ChangeEvent<
      HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement
    >,
  ) => {
    const { name, value } = event.target;

    setFormData((current) =>
      current
        ? {
            ...current,
            [name]:
              name === "price" || name === "quantity" ? Number(value) : value,
          }
        : current,
    );
  };

  const handleCategoryChange = (
    event: React.ChangeEvent<HTMLSelectElement>,
  ) => {
    const selectedCategory = categories.find(
      (category) => category.id === event.target.value,
    );

    setFormData((current) =>
      current
        ? {
            ...current,
            categoryId: event.target.value || null,
            categoryName: selectedCategory
              ? selectedCategory.title
              : "No Category",
          }
        : current,
    );
  };

  const handleSubmit = async (event: React.FormEvent) => {
    event.preventDefault();
    setSaving(true);

    const saved = await onSave(formData);
    setSaving(false);

    if (saved) {
      navigate("/");
    }
  };

  return (
    <section className="mx-auto max-w-3xl rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
      <h1 className="mb-4 text-3xl font-bold text-slate-900">Edit Product</h1>

      <p className="mb-5 text-sm text-slate-600">
        <strong>Current Category:</strong>{" "}
        {formData.categoryId ? (
          <Link
            className="font-semibold text-cyan-700 hover:underline"
            to={`/categories/${formData.categoryId}`}
          >
            {formData.categoryName}
          </Link>
        ) : (
          "No Category"
        )}
      </p>

      <form className="grid gap-4" onSubmit={handleSubmit}>
        <label className="grid gap-2 font-semibold text-slate-700">
          Name
          <input
            className="rounded-xl border border-slate-300 px-4 py-3 outline-none transition focus:border-cyan-500 focus:ring-2 focus:ring-cyan-200"
            name="name"
            value={formData.name}
            onChange={handleChange}
          />
        </label>

        <label className="grid gap-2 font-semibold text-slate-700">
          Brand
          <input
            className="rounded-xl border border-slate-300 px-4 py-3 outline-none transition focus:border-cyan-500 focus:ring-2 focus:ring-cyan-200"
            name="brand"
            value={formData.brand}
            onChange={handleChange}
          />
        </label>

        <label className="grid gap-2 font-semibold text-slate-700">
          Price
          <input
            className="rounded-xl border border-slate-300 px-4 py-3 outline-none transition focus:border-cyan-500 focus:ring-2 focus:ring-cyan-200"
            type="number"
            name="price"
            value={formData.price}
            onChange={handleChange}
          />
        </label>

        <label className="grid gap-2 font-semibold text-slate-700">
          Quantity
          <input
            className="rounded-xl border border-slate-300 px-4 py-3 outline-none transition focus:border-cyan-500 focus:ring-2 focus:ring-cyan-200"
            type="number"
            name="quantity"
            value={formData.quantity}
            onChange={handleChange}
          />
        </label>

        <label className="grid gap-2 font-semibold text-slate-700">
          Category
          <select
            className="rounded-xl border border-slate-300 px-4 py-3 outline-none transition focus:border-cyan-500 focus:ring-2 focus:ring-cyan-200"
            name="categoryId"
            value={formData.categoryId || ""}
            onChange={handleCategoryChange}
          >
            <option value="">No Category</option>
            {categories.map((category) => (
              <option key={category.id} value={category.id}>
                {category.title}
              </option>
            ))}
          </select>
        </label>

        <label className="grid gap-2 font-semibold text-slate-700">
          Description
          <textarea
            className="rounded-xl border border-slate-300 px-4 py-3 outline-none transition focus:border-cyan-500 focus:ring-2 focus:ring-cyan-200"
            name="description"
            value={formData.description}
            onChange={handleChange}
            rows={4}
          />
        </label>

        <label className="grid gap-2 font-semibold text-slate-700">
          Product Image URL
          <input
            className="rounded-xl border border-slate-300 px-4 py-3 outline-none transition focus:border-cyan-500 focus:ring-2 focus:ring-cyan-200"
            name="imageUrl"
            value={formData.imageUrl}
            onChange={handleChange}
          />
        </label>

        <div className="mt-2 flex items-center gap-4">
          <button
            className="rounded-xl bg-cyan-600 px-5 py-3 font-semibold text-white transition hover:bg-cyan-700 disabled:cursor-not-allowed disabled:bg-slate-400"
            type="submit"
            disabled={saving}
          >
            {saving ? "Saving..." : "Save Changes"}
          </button>
          <Link className="font-semibold text-slate-600 hover:underline" to="/">
            Cancel
          </Link>
        </div>
      </form>
    </section>
  );
}

export default ProductPage;
