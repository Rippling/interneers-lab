import React from "react";

interface LoadingSpinnerProps {
  message?: string;
}

function LoadingSpinner({ message = "Loading data..." }: LoadingSpinnerProps) {
  return (
    <div className="flex flex-col items-center gap-4 py-12">
      <div className="h-11 w-11 animate-spin rounded-full border-4 border-slate-300 border-t-cyan-600" />
      <p className="text-sm font-semibold text-slate-500">{message}</p>
    </div>
  );
}

export default LoadingSpinner;
