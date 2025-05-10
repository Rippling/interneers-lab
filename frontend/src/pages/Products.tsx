import React, { useEffect, useState } from "react";
import ProductList from "../components/ProductList";
import UpdatePopup from "../components/UpdatePopup";

type Product = {
  product_id: number;
  name: string;
  description: string;
  brand: string;
};

const Products: React.FC = () => {
  const [products, setProducts] = useState<Product[]>([]);
  const [selectedProduct, setSelectedProduct] = useState<Product | null>(null);

  const fetchAllProducts = async () => {
    try {
      const res = await fetch(`http://127.0.0.1:8000/api/list`);
      const data = await res.json();
      setProducts(data.results || data); // adjust based on API shape
    } catch (error) {
      console.error("Error fetching products:", error);
    }
  };

  useEffect(() => {
    fetchAllProducts();
  }, []);

  return (
    <>
      <ProductList
        products={products}
        onProductClick={(product: Product) => setSelectedProduct(product)}
      />
      {selectedProduct && (
        <UpdatePopup
          product={selectedProduct}
          onClose={() => setSelectedProduct(null)}
          onUpdated={fetchAllProducts}
        />
      )}
    </>
  );
};

export default Products;
