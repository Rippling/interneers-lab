/**
 * Pagination — prev/next controls with page indicator.
 */

import React from "react";
import "./Pagination.css";

interface Props {
  page: number;
  totalPages: number;
  totalProducts: number;
  onPageChange: (page: number) => void;
}

export default function Pagination({ page, totalPages, totalProducts, onPageChange }: Props) {
  if (totalPages <= 1) return null;

  return (
    <div className="pagination">
      <span className="pagination-info">
        {totalProducts} products · page {page} of {totalPages}
      </span>
      <div className="pagination-controls">
        <button
          className="pagination-btn"
          disabled={page <= 1}
          onClick={() => onPageChange(page - 1)}
        >
          ← Prev
        </button>
        <span className="pagination-current">{page}</span>
        <button
          className="pagination-btn"
          disabled={page >= totalPages}
          onClick={() => onPageChange(page + 1)}
        >
          Next →
        </button>
      </div>
    </div>
  );
}
