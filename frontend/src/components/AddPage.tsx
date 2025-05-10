import React from "react";
import FormUpdate from "../components/formUpdate";
import FormCategoryAdd from "../components/categoryAdd";
import "./add.css"; // optional for styling layout

function AddPage() {
  return (
    <div className="add-page">
      <h1 style={{ textAlign: "center" }}>Add Items</h1>
      <div className="form-container">
        <div className="form-section">
          <FormUpdate />
        </div>
        <div className="form-section">
          <FormCategoryAdd />
        </div>
      </div>
    </div>
  );
}

export default AddPage;
