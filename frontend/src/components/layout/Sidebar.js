import React from 'react';
import { NavLink, useNavigate } from 'react-router-dom';

export default function Sidebar() {
  const navigate = useNavigate();

  const handleLogout = () => {
    // Here you would clear user session/token
    console.log("User logged out");
    navigate('/login');
  };

  return (
    <aside className="sidebar">
      <div className="sidebar-header">
        <h2 className="sidebar-logo">Quiz Portal</h2>
      </div>

      <div className="sidebar-nav-section">
        <h3>Navigation</h3>
        <nav className="sidebar-nav-links">
          {/* NavLink adds an "active" class to the current page's link */}
          <NavLink to="/professor/dashboard" className="sidebar-nav-link">Home Page</NavLink>
          <NavLink to="/professor/quizzes" className="sidebar-nav-link">View Quiz</NavLink>
          {/* <NavLink to="/professor/questions/add" className="sidebar-nav-link">Generate Quiz</NavLink> */}
          <NavLink to="/professor/generate-quiz" className="sidebar-nav-link">Generate Quiz</NavLink>
          {/* <Link to="/professor/generate-quiz">Generate Quiz</Link> */}
          <NavLink to="/professor/results" className="sidebar-nav-link">Results</NavLink>
        </nav>
      </div>

      <div className="sidebar-nav-section">
        <h3>Quick Actions</h3>
        <nav className="sidebar-nav-links">
          {/* Note: You will need to create pages for these new routes */}
          <NavLink to="/professor/students" className="sidebar-nav-link">Manage Students</NavLink>
          <NavLink to="/professor/analytics" className="sidebar-nav-link">Analytics</NavLink>
        </nav>
      </div>

      <div className="sidebar-footer">
        <button onClick={handleLogout} className="logout-button">Logout</button>
      </div>
    </aside>
  );
}