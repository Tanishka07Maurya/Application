import React from 'react';
import { Link } from 'react-router-dom';
import Header from '../components/layout/Header';
import Footer from '../components/layout/Footer';
import Card from '../components/ui/Card';

export default function StudentDashboard() {
  return (
    <>
      <Header />
      {/* Use the new page container class */}
      <main className="page-container">
        {/* Pass the new card class to your Card component */}
        <Card className="dashboard-card">
          <h2>Student Dashboard</h2>
          <p>Start a quiz or check your results.</p>

          <div style={{ display: 'flex', flexDirection: 'column', gap: '15px' }}>
            {/* Apply the new, reusable button classes */}
            <Link to="/quiz/1" className="btn btn-primary">
              Take Quiz
            </Link>
            <Link to="/student/results" className="btn btn-secondary">
              View Results
            </Link>
          </div>
        </Card>
      </main>
      <Footer />
    </>
  );
}