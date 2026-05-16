import React, { useState, useEffect } from "react";
import type { Product, Category, ProductPayload } from "../types";
import { createCategory } from "../api/client";
import "./ProductForm.css";

interface Props {
  product?: Product;
  categories: Category[];
  saving: boolean;
  onSave: (data: ProductPayload) => void;
  onClose: () => void;
  onCategoryCreated?: (cat: Category) => void;
}

const empty = {
  name: "", description: "", brand: "",
  price: "", quantity: "", category: "",
  image_url: "",
};

export default function ProductForm({
  product, categories, saving, onSave, onClose, onCategoryCreated,
}: Props) {
  const [form, setForm] = useState({ ...empty });
  const [validationError, setValidationError] = useState<string | null>(null);
  const [showNewCategory, setShowNewCategory] = useState(false);
  const [newCatTitle, setNewCatTitle] = useState("");
  const [newCatDesc, setNewCatDesc] = useState("");
  const [creatingCat, setCreatingCat] = useState(false);
  const [catError, setCatError] = useState<string | null>(null);

  useEffect(() => {
    if (product) {
      setForm({
        name:        product.name ?? "",
        description: product.description ?? "",
        brand:       product.brand ?? "",
        price:       String(product.price ?? ""),
        quantity:    String(product.quantity ?? ""),
        category:    product.category?.id ?? "",
        image_url:   product.image_url ?? "",
      });
    } else {
      setForm({ ...empty });
    }
  }, [product]);

  function handleChange(
    e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>
  ) {
    setForm((f) => ({ ...f, [e.target.name]: e.target.value }));
    setValidationError(null);
  }

  async function handleCreateCategory() {
    if (!newCatTitle.trim()) return setCatError("Title is required");
    if (!newCatDesc.trim())  return setCatError("Description is required");
    setCreatingCat(true);
    setCatError(null);
    try {
      const cat = await createCategory({
        title:       newCatTitle.trim(),
        description: newCatDesc.trim(),
      });
      onCategoryCreated?.(cat);
      setForm(f => ({ ...f, category: cat.id }));
      setShowNewCategory(false);
      setNewCatTitle("");
      setNewCatDesc("");
    } catch (e: any) {
      setCatError(e.message ?? "Failed to create category");
    } finally {
      setCreatingCat(false);
    }
  }

  function handleSubmit() {
    if (!form.name.trim())          return setValidationError("Name is required");
    if (!form.description.trim())   return setValidationError("Description is required");
    if (!form.brand.trim())         return setValidationError("Brand is required");
    if (Number(form.price) <= 0)    return setValidationError("Price must be greater than 0");
    if (Number(form.quantity) <= 0) return setValidationError("Quantity must be greater than 0");

    const imageUrl = form.image_url.trim() || null;
    if (
      imageUrl && !imageUrl.startsWith("http://") &&
      !imageUrl.startsWith("https://") &&
      !imageUrl.startsWith("data:") &&
      !imageUrl.startsWith("/")
    ) {
      return setValidationError("Image URL must be a valid URL (http, https, data URI) or absolute path");
    }

    onSave({
      name:        form.name.trim(),
      description: form.description.trim(),
      brand:       form.brand.trim(),
      price:       Number(form.price),
      quantity:    Number(form.quantity),
      image_url:   imageUrl,
      category_id: form.category || null,
    });
  }

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal" onClick={(e) => e.stopPropagation()}>
        <div className="modal-header">
          <h2>{product ? "Edit Product" : "New Product"}</h2>
          <button className="modal-close" onClick={onClose}>✕</button>
        </div>

        <div className="modal-body">
          {validationError && (
            <div className="form-error">⚠ {validationError}</div>
          )}

          <label>Name *
            <input name="name" value={form.name} onChange={handleChange} />
          </label>
          <label>Description *
            <textarea name="description" value={form.description}
              onChange={handleChange} rows={3} />
          </label>
          <label>Brand *
            <input name="brand" value={form.brand} onChange={handleChange} />
          </label>
          <div className="form-row">
            <label>Price *
              <input name="price" type="number" min="0.01" step="0.01"
                value={form.price} onChange={handleChange} />
            </label>
            <label>Quantity *
              <input name="quantity" type="number" min="1"
                value={form.quantity} onChange={handleChange} />
            </label>
          </div>

          {/* Image URL */}
          <label>
            Image URL
            <input
              name="image_url"
              type="url"
              value={form.image_url}
              onChange={handleChange}
              placeholder="https://example.com/product.jpg (optional)"
            />
          </label>
          {form.image_url && (
            <div className="form-image-preview-wrap">
              <img
                src={form.image_url}
                alt="preview"
                className="form-image-preview"
                onError={(e) => ((e.target as HTMLImageElement).style.display = "none")}
              />
            </div>
          )}

          {/* Category selector + inline create */}
          <label>Category
            <select name="category" value={form.category} onChange={handleChange}>
              <option value="">— None —</option>
              {categories.map((c) => (
                <option key={c.id} value={c.id}>{c.title}</option>
              ))}
            </select>
          </label>

          <button
            type="button"
            className="btn-add-category"
            onClick={() => { setShowNewCategory(v => !v); setCatError(null); }}
          >
            {showNewCategory ? "▲ Cancel new category" : "+ Create new category"}
          </button>

          {showNewCategory && (
            <div className="new-category-form">
              {catError && <div className="form-error">⚠ {catError}</div>}
              <label>Category Title *
                <input
                  value={newCatTitle}
                  onChange={e => { setNewCatTitle(e.target.value); setCatError(null); }}
                  placeholder="e.g. Kitchen Essentials"
                />
              </label>
              <label>Category Description *
                <input
                  value={newCatDesc}
                  onChange={e => { setNewCatDesc(e.target.value); setCatError(null); }}
                  placeholder="e.g. Cooking and kitchen tools"
                />
              </label>
              <button
                type="button"
                className="btn-primary"
                onClick={handleCreateCategory}
                disabled={creatingCat}
              >
                {creatingCat ? "Creating…" : "Create & Select"}
              </button>
            </div>
          )}
        </div>

        <div className="modal-footer">
          <button className="btn-secondary" onClick={onClose} disabled={saving}>
            Cancel
          </button>
          <button className="btn-primary" onClick={handleSubmit} disabled={saving}>
            {saving ? "Saving…" : product ? "Save Changes" : "Create Product"}
          </button>
        </div>
      </div>
    </div>
  );
}