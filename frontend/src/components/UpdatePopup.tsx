// components/UpdatePopup.tsx
import React, { useState } from "react";

type Product = {
  product_id: number;
  name: string;
  description: string;
  brand: string;
};

interface Props {
  product: Product;
  onClose: () => void;
  onUpdated: () => void;
}

const UpdatePopup: React.FC<Props> = ({ product, onClose, onUpdated }) => {
  const [form, setForm] = useState({
    name: product.name,
    description: product.description,
    brand: product.brand,
    product_id: product.product_id,
  });

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };
  console.log("form", form);
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    const res = await fetch(
      `http://127.0.0.1:8000/api/list/${product.product_id}`,
      {
        method: "PUT",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(form),
      },
    );

    if (res.ok) {
      onUpdated(); // re-fetch the list
      onClose(); // close the popup
    } else {
      alert("Failed to update. Status: " + res.status);
    }
  };

  return (
    <div
      style={{
        position: "fixed",
        top: 0,
        left: 0,
        width: "100%",
        height: "100%",
        backgroundColor: "rgba(0,0,0,0.5)",
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
      }}
    >
      <form
        onSubmit={handleSubmit}
        style={{
          backgroundColor: "#fff",
          padding: "30px",
          borderRadius: "8px",
        }}
      >
        <h3>Update Product</h3>
        <input
          name="ProductID"
          value={form.product_id}
          onChange={handleChange}
          placeholder="Name"
        />
        <br />
        <input
          name="name"
          value={form.name}
          onChange={handleChange}
          placeholder="Name"
        />
        <br />
        <input
          name="description"
          value={form.description}
          onChange={handleChange}
          placeholder="Description"
        />
        <br />
        <input
          name="brand"
          value={form.brand}
          onChange={handleChange}
          placeholder="Brand"
        />
        <br />
        <button type="submit">Update</button>
        <button type="button" onClick={onClose} style={{ marginLeft: "10px" }}>
          Cancel
        </button>
      </form>
    </div>
  );
};

export default UpdatePopup;
