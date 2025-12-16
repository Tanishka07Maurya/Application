//prii
import React from 'react';
import { useNavigate } from 'react-router-dom';
import Button from '../components/forms/Button'; 

const StudentDashboard = () => {
  const navigate = useNavigate();

  // Logout function
  const handleLogout = () => {
    // Clear user data (if using localStorage)
    localStorage.removeItem('userRole');
    localStorage.removeItem('isLoggedIn');
    // Redirect to home
    navigate('/');
  };

  return (
    <div className="dashboard-layout" style={{ display: 'flex', height: '100vh' }}>
      
      {/* --- SIDEBAR (Student Version) --- */}
      <aside className="sidebar" style={{ width: '250px', backgroundColor: '#3e2d5c', color: '#fff', padding: '20px', display: 'flex', flexDirection: 'column' }}>
        <div className="sidebar-header" style={{ marginBottom: '40px', textAlign: 'center' }}>
          <h2>Quiz Portal</h2>
        </div>

        <nav className="sidebar-nav" style={{ flexGrow: 1 }}>
          <ul style={{ listStyle: 'none', padding: 0 }}>
            <li style={{ marginBottom: '15px' }}>
              <button onClick={() => navigate('/student/dashboard')} style={styles.navLink}>Dashboard</button>
            </li>
            <li style={{ marginBottom: '15px' }}>
              <button onClick={() => navigate('/student/quizzes')} style={styles.navLink}>Available Quizzes</button>
            </li>
            <li style={{ marginBottom: '15px' }}>
              <button onClick={() => navigate('/student/results')} style={styles.navLink}>My Results</button>
            </li>
          </ul>
        </nav>

        <div className="sidebar-footer">
          <button onClick={handleLogout} style={styles.logoutBtn}>Logout</button>
        </div>
      </aside>

      {/* --- MAIN CONTENT --- */}
      <main className="main-content" style={{ flexGrow: 1, padding: '40px', backgroundColor: '#f4f7f9', overflowY: 'auto' }}>
        
        <header style={{ marginBottom: '30px' }}>
          <h1 style={{ color: '#333' }}>Student Dashboard</h1>
          <p style={{ color: '#666' }}>Welcome back! Ready to learn?</p>
        </header>

        {/* DASHBOARD CARDS */}
        <div style={styles.cardContainer}>
          
          {/* Card 1: Take Quiz */}
          <div style={styles.card}>
            <h3>Take a Quiz</h3>
            <p style={{ color: '#777', marginBottom: '20px' }}>View pending quizzes and start attempting.</p>
            <Button 
                label="View Quizzes" 
                onClick={() => navigate('/student/quizzes')} 
                className="btn btn-primary" 
            />
          </div>

          {/* Card 2: View Results */}
          <div style={styles.card}>
            <h3>My Performance</h3>
            <p style={{ color: '#777', marginBottom: '20px' }}>Check your scores and analytics.</p>
            <Button 
                label="View Results" 
                onClick={() => navigate('/student/results')} 
                className="btn btn-primary" 
            />
          </div>

        </div>
      </main>
    </div>
  );
};

// Simple internal styles
const styles = {
  navLink: {
    background: 'none', border: 'none', color: '#fff', fontSize: '1rem', cursor: 'pointer', textAlign: 'left', width: '100%'
  },
  logoutBtn: {
    backgroundColor: '#dc3545', color: '#fff', padding: '10px', width: '100%', border: 'none', borderRadius: '5px', cursor: 'pointer'
  },
  cardContainer: {
    display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))', gap: '30px'
  },
  card: {
    backgroundColor: '#fff', padding: '30px', borderRadius: '15px', boxShadow: '0 5px 15px rgba(0,0,0,0.05)'
  }
};

export default StudentDashboard;
//prii