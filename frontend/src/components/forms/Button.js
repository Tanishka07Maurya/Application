
import React from 'react';

export default function Button({ label, onClick, type = "button", className = "" }) {
  return (
    <button
      type={type}
      onClick={onClick}
      className={`bg-blue-600 text-white py-2 px-4 rounded hover:bg-blue-700 ${className}`}
    >
      {label}
    </button>
  );
}
