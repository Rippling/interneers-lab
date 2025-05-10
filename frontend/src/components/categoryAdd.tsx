import React, { useState } from "react";

type Category = {
  category_id: string;
  category_name: string;
  description: string;
};

function FormCategoryAdd() {
  const [formData, setFormData] = useState<Category>({
    category_id: "",
    category_name: "",
    description: "",
  });

  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setFormData({ ...formData, [name]: value });
    if (error) setError(null);
  };

  const postFormData = async () => {
    setIsLoading(true);
    setError(null);

    try {
      console.log("Sending category data:", formData);

      const response = await fetch("http://127.0.0.1:8000/api/category/list", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(formData),
      });

      const responseText = await response.text();

      try {
        const responseData = JSON.parse(responseText);
        console.log("Response:", responseData);
      } catch {
        console.log("Non-JSON response:", responseText);
      }

      if (response.ok) {
        alert("Category added successfully!");
        setFormData({ category_id: "", category_name: "", description: "" });
      } else {
        const errorMessage = `Server error ${response.status}: ${responseText}`;
        console.error(errorMessage);
        setError(errorMessage);
        alert("Failed to add category.");
      }
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : String(err);
      console.error("Network error:", errorMessage);
      setError(`Network error: ${errorMessage}`);
      alert(`Connection error: ${errorMessage}`);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="formCategoryAdd">
      <h2 style={{ textAlign: "center" }}>Add Category</h2>

      {error && (
        <div
          className="error-message"
          style={{ color: "red", margin: "10px 0" }}
        >
          Error: {error}
        </div>
      )}

      <form
        onSubmit={(e) => {
          e.preventDefault();
          postFormData();
        }}
        className="update-form"
      >
        <div className="form-group">
          <label htmlFor="category-id">Category ID:</label>
          <input
            type="text"
            id="category-id"
            name="category_id"
            value={formData.category_id}
            onChange={handleChange}
            required
          />
        </div>
        <div className="form-group">
          <label htmlFor="category-name">Name:</label>
          <input
            type="text"
            id="category-name"
            name="category_name"
            value={formData.category_name}
            onChange={handleChange}
            required
          />
        </div>
        <div className="form-group">
          <label htmlFor="category-description">Description:</label>
          <input
            type="text"
            id="category-description"
            name="description"
            value={formData.description}
            onChange={handleChange}
            required
          />
        </div>

        <button type="submit" disabled={isLoading}>
          {isLoading ? "Processing..." : "Add Category"}
        </button>
      </form>
    </div>
  );
}

export default FormCategoryAdd;
