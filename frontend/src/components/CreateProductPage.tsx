import React, { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { CategoryType, ProductType } from "./Product";

interface CreateProductPageProps {
  categories: CategoryType[];
  onCreate: (
    product: Omit<ProductType, "id" | "categoryName">,
  ) => Promise<boolean>;
}

function CreateProductPage({ categories, onCreate }: CreateProductPageProps) {
  const navigate = useNavigate();
  const [saving, setSaving] = useState(false);
  const [formData, setFormData] = useState<
    Omit<ProductType, "id" | "categoryName">
  >({
    name: "",
    brand: "",
    price: 0,
    quantity: 0,
    categoryId: "",
    description: "",
    imageUrl: "",
  });

  const handleChange = (
    event: React.ChangeEvent<
      HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement
    >,
  ) => {
    const { name, value } = event.target;

    setFormData((current) => ({
      ...current,
      [name]: name === "price" || name === "quantity" ? Number(value) : value,
    }));
  };

  const handleSubmit = async (event: React.FormEvent) => {
    event.preventDefault();
    setSaving(true);

    const created = await onCreate({
      ...formData,
      categoryId: formData.categoryId || null,
    });

    setSaving(false);

    if (created) {
      navigate("/");
    }
  };

  return (
    <section className="mx-auto max-w-3xl rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
      <h1 className="mb-4 text-3xl font-bold text-slate-900">Add Product</h1>

      <form className="grid gap-4" onSubmit={handleSubmit}>
        <input
          className="rounded-xl border border-slate-300 px-4 py-3"
          name="name"
          placeholder="Name"
          value={formData.name}
          onChange={handleChange}
        />
        <input
          className="rounded-xl border border-slate-300 px-4 py-3"
          name="brand"
          placeholder="Brand"
          value={formData.brand}
          onChange={handleChange}
        />
        <input
          className="rounded-xl border border-slate-300 px-4 py-3"
          type="number"
          name="price"
          placeholder="Price"
          value={formData.price}
          onChange={handleChange}
        />
        <input
          className="rounded-xl border border-slate-300 px-4 py-3"
          type="number"
          name="quantity"
          placeholder="Quantity"
          value={formData.quantity}
          onChange={handleChange}
        />
        <select
          className="rounded-xl border border-slate-300 px-4 py-3"
          name="categoryId"
          value={formData.categoryId || ""}
          onChange={handleChange}
        >
          <option value="">No Category</option>
          {categories.map((category) => (
            <option key={category.id} value={category.id}>
              {category.title}
            </option>
          ))}
        </select>
        <textarea
          className="rounded-xl border border-slate-300 px-4 py-3"
          name="description"
          rows={4}
          placeholder="Description"
          value={formData.description}
          onChange={handleChange}
        />
        <input
          className="rounded-xl border border-slate-300 px-4 py-3"
          name="imageUrl"
          placeholder="Product image URL"
          value={formData.imageUrl}
          onChange={handleChange}
        />

        <div className="flex items-center gap-4">
          <button
            className="rounded-xl bg-cyan-600 px-5 py-3 font-semibold text-white"
            type="submit"
            disabled={saving}
          >
            {saving ? "Creating..." : "Create Product"}
          </button>
          <Link className="font-semibold text-slate-600 hover:underline" to="/">
            Cancel
          </Link>
        </div>
      </form>
    </section>
  );
}

export default CreateProductPage;
