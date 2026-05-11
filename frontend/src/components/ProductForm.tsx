import React, { useState, useEffect } from "react";
import type { Product, Category, ProductPayload } from "../types";
import "./ProductForm.css";

interface Props {
  product?: Product;
  categories: Category[];
  saving: boolean;
  onSave: (data: ProductPayload) => void;
  onClose: () => void;
}

const empty = {
  name: "", description: "", brand: "",
  price: "", quantity: "", category: "",
};

export default function ProductForm({
  product, categories, saving, onSave, onClose,
}: Props) {
  const [form, setForm] = useState({ ...empty });
  const [validationError, setValidationError] = useState<string | null>(null);

  useEffect(() => {
    if (product) {
      setForm({
        name:        product.name ?? "",
        description: product.description ?? "",
        brand:       product.brand ?? "",
        price:       String(product.price ?? ""),
        quantity:    String(product.quantity ?? ""),
        category:    product.category?.id ?? "",
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

  function handleSubmit() {
    if (!form.name.trim())         return setValidationError("Name is required");
    if (!form.brand.trim())        return setValidationError("Brand is required");
    if (Number(form.price) <= 0)   return setValidationError("Price must be greater than 0");
    if (Number(form.quantity) <= 0) return setValidationError("Quantity must be greater than 0");

    onSave({
      name:        form.name.trim(),
      description: form.description.trim(),
      brand:       form.brand.trim(),
      price:       Number(form.price),
      quantity:    Number(form.quantity),
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
          <label>Brand *
            <input name="brand" value={form.brand} onChange={handleChange} />
          </label>
          <label>Description
            <textarea name="description" value={form.description} onChange={handleChange} rows={3} />
          </label>
          <div className="form-row">
            <label>Price *
              <input name="price" type="number" min="0" step="0.01"
                value={form.price} onChange={handleChange} />
            </label>
            <label>Quantity *
              <input name="quantity" type="number" min="0"
                value={form.quantity} onChange={handleChange} />
            </label>
          </div>
          <label>Category
            <select name="category" value={form.category} onChange={handleChange}>
              <option value="">— None —</option>
              {categories.map((c) => (
                <option key={c.id} value={c.id}>{c.title}</option>
              ))}
            </select>
          </label>
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