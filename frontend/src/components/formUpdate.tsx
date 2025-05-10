import "./formUpdate.css";
import React, { useState } from "react";

type Product = {
  product_id: string;
  name: string;
  description: string;
  brand: string;
  category_Id: string;
};

function FormUpdate() {
  const [formData, setFormData] = useState<Product>({
    product_id: "",
    name: "",
    description: "",
    brand: "",
    category_Id: "",
  });

  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  function handleChange(event: React.ChangeEvent<HTMLInputElement>) {
    const { name, value } = event.target;
    setFormData({
      ...formData,
      [name]: value,
    });

    // Clear any previous error when user makes changes
    if (error) {
      setError(null);
    }
  }

  const postFormData = async () => {
    setIsLoading(true);
    setError(null);

    try {
      // Log the data being sent
      console.log("Sending data to server:", formData);

      // API URL - Make sure this matches your actual API endpoint
      const apiUrl = "http://127.0.0.1:8000/api/list";
      console.log("Sending request to:", apiUrl);

      const response = await fetch(apiUrl, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          // Add any authentication headers if needed
          // "Authorization": "Bearer yourTokenHere"
        },
        body: JSON.stringify(formData),
      });

      console.log("Response status:", response.status);

      // Attempt to parse response regardless of status code for debugging
      let responseData;
      const responseText = await response.text();

      try {
        responseData = JSON.parse(responseText);
        console.log("Response data:", responseData);
      } catch (e) {
        console.log("Response is not JSON:", responseText);
      }

      if (response.ok) {
        alert("Product added successfully!");
        // Reset form
        setFormData({
          product_id: "",
          name: "",
          description: "",
          brand: "",
          category_Id: "",
        });
      } else {
        // Create a descriptive error message
        const errorMessage = `Server returned ${response.status} ${response.statusText}. ${responseText || ""}`;
        console.error(errorMessage);
        setError(errorMessage);
        alert(
          `Failed to add product: ${response.status} ${response.statusText}`,
        );
      }
    } catch (error) {
      // This catches network errors
      const errorMessage =
        error instanceof Error ? error.message : String(error);
      console.error("Network error:", errorMessage);
      setError(`Network error: ${errorMessage}`);
      alert(`Connection error: ${errorMessage}`);
    } finally {
      setIsLoading(false);
    }
  };

  // Convert input IDs for better CSS and avoid potential ID conflicts
  const formatInputId = (name: string) =>
    `product-${name.toLowerCase().replace("_", "-")}`;

  return (
    <div className="formUpdate">
      <h2 style={{ textAlign: "center" }}>Add Product</h2>

      {error && (
        <div
          className="error-message"
          style={{ color: "red", margin: "10px 0" }}
        >
          Error: {error}
        </div>
      )}

      <form
        className="update-form"
        onSubmit={(e) => {
          e.preventDefault();
          postFormData();
        }}
      >
        <div className="form-group">
          <label htmlFor={formatInputId("product_id")}>Product ID:</label>
          <input
            type="text"
            id={formatInputId("product_id")}
            name="product_id"
            value={formData.product_id}
            onChange={handleChange}
            required
          />
        </div>
        <div className="form-group">
          <label htmlFor={formatInputId("name")}>Name:</label>
          <input
            type="text"
            id={formatInputId("name")}
            name="name"
            value={formData.name}
            onChange={handleChange}
            required
          />
        </div>
        <div className="form-group">
          <label htmlFor={formatInputId("description")}>Description:</label>
          <input
            type="text"
            id={formatInputId("description")}
            name="description"
            value={formData.description}
            onChange={handleChange}
            required
          />
        </div>
        <div className="form-group">
          <label htmlFor={formatInputId("brand")}>Brand:</label>
          <input
            type="text"
            id={formatInputId("brand")}
            name="brand"
            value={formData.brand}
            onChange={handleChange}
            required
          />
        </div>
        <div className="form-group">
          <label htmlFor={formatInputId("category_Id")}>Category ID:</label>
          <input
            type="text"
            id={formatInputId("category_Id")}
            name="category_Id"
            value={formData.category_Id}
            onChange={handleChange}
            required
          />
        </div>

        <button type="submit" disabled={isLoading}>
          {isLoading ? "Processing..." : "Update Product"}
        </button>
      </form>
    </div>
  );
}

export default FormUpdate;
