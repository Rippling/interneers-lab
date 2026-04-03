import React, { useEffect, useState } from "react";
import { Link, useNavigate, useParams } from "react-router-dom";
import { ProductType } from "./Product";

interface ProductPageProps {
  products: ProductType[];
  categories: string[];
  onSave: (product: ProductType) => boolean;
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

  const product = products.find((item) => item.id === Number(productId));

  const [formData, setFormData] = useState<ProductType | null>(product ?? null);

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
      <section className="product-page">
        <h1>Product Not Found</h1>
        <Link className="inline-link" to="/">
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

  const handleSubmit = (event: React.FormEvent) => {
    event.preventDefault();

    const saved = onSave(formData);
    if (saved) {
      navigate("/");
    }
  };

  return (
    <section className="product-page">
      <h1>Edit Product</h1>

      <p className="product-page__category-link">
        <strong>Current Category:</strong>{" "}
        <Link className="inline-link" to={`/categories/${formData.category}`}>
          {formData.category}
        </Link>
      </p>

      <form className="product-form" onSubmit={handleSubmit}>
        <label>
          Name
          <input
            name="name"
            value={formData.name}
            onChange={handleChange}
          />
        </label>

        <label>
          Brand
          <input
            name="brand"
            value={formData.brand}
            onChange={handleChange}
          />
        </label>

        <label>
          Price
          <input
            type="number"
            name="price"
            value={formData.price}
            onChange={handleChange}
          />
        </label>

        <label>
          Quantity
          <input
            type="number"
            name="quantity"
            value={formData.quantity}
            onChange={handleChange}
          />
        </label>

        <label>
          Category
          <select
            name="category"
            value={formData.category}
            onChange={handleChange}
          >
            {categories.map((category) => (
              <option key={category} value={category}>
                {category}
              </option>
            ))}
          </select>
        </label>

        <label>
          Description
          <textarea
            name="description"
            value={formData.description}
            onChange={handleChange}
            rows={4}
          />
        </label>

        <div className="product-form__actions">
          <button type="submit">Save Changes</button>
          <Link className="inline-link" to="/">
            Cancel
          </Link>
        </div>
      </form>
    </section>
  );
}

export default ProductPage;

