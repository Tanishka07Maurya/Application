import React from 'react';
import { Link } from 'react-router-dom';
// The CSS is likely imported in your main App component or the HomePage,
// so you might not need to import it here again.

export default function Header() {
  return (
    <header className="site-header">
      <h1>Quiz Portal</h1>
      <nav>
        <Link to="/" className="nav-link">Home</Link>
        {/* You can add more links here and they will get the same style */}
      </nav>
    </header>
  );
}