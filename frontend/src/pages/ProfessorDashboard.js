import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import Card from '../components/ui/Card'; 
import { fetchQuestions } from '../api/apiService';


export default function ProfessorDashboard() {
  const [questionCount, setQuestionCount] = useState(0);

  useEffect(() => {
    const loadQuestions = async () => {
      try {
        const res = await fetchQuestions();

        if (res.data && typeof res.data === 'object') {
          setQuestionCount(Object.keys(res.data).length);
        } else {
          setQuestionCount(0);
        }
      } catch (err) {
        console.error("Error loading questions on dashboard:", err);
        setQuestionCount(0);
      }
    };
    loadQuestions();
  }, []);

  return (
    <main className="main-content">
      <div className="top-bar">
        <h1>Professor Dashboard</h1>
      </div>

      <div className="dashboard-grid">
        <Card className="card card-left-align">
          <h3>Manage Questions</h3>
          {/*  */}
          <p>Total Questions: {questionCount}</p>
          <Link to="/professor/questions" className="btn btn-primary">
            View Questions
          </Link>
        </Card>

        <Card className="card card-left-align">
          <h3>View Quizzes</h3>
          <p>See all quizzes and get shareable links.</p>
          <Link to="/professor/quizzes" className="btn btn-primary">
            View Quizzes
          </Link>
        </Card>

        <Card className="card card-left-align">
          <h3>View Results</h3>
          <p>See all student quiz performance.</p>
          <Link to="/professor/results" className="btn btn-accent">
            View Results
          </Link>
        </Card>
      </div>
    </main>
  );
}