import React, { useEffect, useState } from "react";
import "./categories.css";

type props = {
  onclick: (category_id: number) => void;
};

type Category = {
  category_id: number;
  category_name: string;
  description: string;
};

const Categories: React.FC<props> = ({ onclick }) => {
  const [dataFinal, setData] = useState<Category[]>([]);

  const fetchCategories = async () => {
    try {
      const response = await fetch("http://127.0.0.1:8000/api/category/list");
      const data: Category[] = await response.json();
      console.log("Categories data:", data);
      setData(data);
    } catch (error) {
      console.error("Error fetching categories:", error);
    }
  };

  useEffect(() => {
    fetchCategories();
  }, []);

  // const categories = data.map((category: { name: string }) => {category: {category.category_name}, description : {category.description}});
  return (
    <>
      <h2 className="categories-header">Categories</h2>

      <div className="categories">
        {dataFinal.map((item) => (
          <div className="category-item" key={item.category_id}>
            <h3>{item.category_name}</h3>
            <p>{item.category_id}</p>
            <p>{item.description}</p>
            <button
              className="category-button"
              onClick={() => onclick(item.category_id)}
            >
              View Products
            </button>
          </div>
        ))}
      </div>
    </>
  );
};

export default Categories;
