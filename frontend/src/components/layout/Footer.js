import React from 'react';
// The CSS is likely imported in your main App component or the HomePage,
// so you might not need to import it here again.

export default function Footer() {
  return (
    <footer className="site-footer">
      © {new Date().getFullYear()} Quiz Portal. All rights reserved.
    </footer>
  );
}