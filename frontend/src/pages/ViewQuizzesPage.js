import React, { useEffect, useState } from 'react';
// 💡 FIXED: 'Header' and 'Footer' imports have been removed
import { fetchQuizzes } from '../api/apiService';

export default function ViewQuizzesPage() {
  const [quizzes, setQuizzes] = useState([]);

  useEffect(() => {
    const loadQuizzes = async () => {
      try {
        const res = await fetchQuizzes();
        setQuizzes(res.data);
      } catch (err) {
        console.error("Failed to fetch quizzes:", err);
      }
    };
    loadQuizzes();
  }, []);

  const copyLinkToClipboard = (quizId) => {
    const link = `${window.location.origin}/quiz/${quizId}`;
    navigator.clipboard.writeText(link);
    alert('Quiz link copied to clipboard!');
  };

  return (
    // This component no longer needs <Header /> or <Footer />
    <main className="main-content">
      <div className="top-bar">
        <h1>Available Quizzes</h1>
      </div>

      <div className="quiz-list">
        {quizzes.length > 0 ? (
          quizzes.map((quiz) => (
            <div key={quiz.id} className="quiz-list-item">
              <p className="quiz-list-title">{quiz.title}</p>
              <button onClick={() => copyLinkToClipboard(quiz.id)} className="btn-like-link">
                Copy Link
              </button>
            </div>
          ))
        ) : (
          <p>No quizzes found.</p>
        )}
      </div>
    </main>
  );
}