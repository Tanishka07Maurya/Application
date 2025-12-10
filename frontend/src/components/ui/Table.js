import React from 'react';

export default function Table({ columns, data }) {
  return (
    <table className="w-full border">
      <thead>
        <tr className="bg-gray-200">
          {columns.map((col) => (
            <th key={col.accessor} className="border px-3 py-2 text-left">{col.Header}</th>
          ))}
        </tr>
      </thead>
      <tbody>
        {data.length > 0 ? (
          data.map((row, idx) => (
            <tr key={idx}>
              {columns.map((col) => (
                <td key={col.accessor} className="border px-3 py-2">{row[col.accessor]}</td>
              ))}
            </tr>
          ))
        ) : (
          <tr><td colSpan={columns.length} className="text-center py-3">No data found</td></tr>
        )}
      </tbody>
    </table>
  );
}
