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

    const saved = await onSave(formData);
    if (saved) {
      navigate("/");
    }
  };

  return (
    <section className="product-page">
      <h1>Edit Product</h1>

      <p className="product-page__category-link">
        <strong>Current Category:</strong>{" "}
        {formData.categoryId ? (
          <Link
            className="inline-link"
            to={`/categories/${formData.categoryId}`}
          >
            {formData.categoryName}
          </Link>
        ) : (
          "No Category"
        )}
      </p>

      <form className="product-form" onSubmit={handleSubmit}>
        <label>
          Name
          <input name="name" value={formData.name} onChange={handleChange} />
        </label>

        <label>
          Brand
          <input name="brand" value={formData.brand} onChange={handleChange} />
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
