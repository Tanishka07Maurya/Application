import React, { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import Header from '../components/layout/Header';
import Footer from '../components/layout/Footer';
import Button from '../components/forms/Button';
import QuestionCard from '../components/quiz/QuestionCard';
import { fetchQuizById, submitQuiz } from '../api/apiService';

export default function QuizPage() {
  const { quizId } = useParams();
  const navigate = useNavigate();
  const [quiz, setQuiz] = useState(null);
  const [answers, setAnswers] = useState({});

  useEffect(() => {
    const loadQuiz = async () => {
      try {
        const res = await fetchQuizById(quizId);
        setQuiz(res.data);
      } catch (err) {
        console.error(err);
      }
    };
    loadQuiz();
  }, [quizId]);

  const handleSelect = (questionId, option) => {
    setAnswers((prevAnswers) => ({
      ...prevAnswers,
      [questionId]: option,
    }));
  };

  const handleSubmit = async () => {
    try {
      const res = await submitQuiz(quizId, { answers });
      alert(`Quiz Submitted! Your Score: ${res.data.score}`);
      // Redirect to results page after submission
      navigate('/student/results'); 
    } catch (err) {
      alert('Error submitting quiz. Please try again.');
      console.error(err);
    }
  };
  
  // A note: For the interactive options to work, your QuestionCard component
  // will need to be updated. I will provide the code for it in the next step.

  if (!quiz) {
    return (
      <>
        <Header />
        <main className="page-container">
          <p className="loading-message">Loading quiz...</p>
        </main>
        <Footer />
      </>
    );
  }

  return (
    <>
      <Header />
      <main className="page-container">
        <div className="quiz-container">
          <h2 className="page-title">{quiz.title}</h2>
          {quiz.questions.map((q) => (
            <QuestionCard
              key={q.id}
              questionId={q.id}
              questionText={q.text}
              options={q.options}
              onSelect={handleSelect}
              selectedValue={answers[q.id]}
            />
          ))}

          <div className="submit-quiz-container">
            {/* Assuming your Button component passes down className */}
            <Button
              label="Submit Quiz"
              onClick={handleSubmit}
              className="btn btn-primary"
            />
          </div>
        </div>
      </main>
      <Footer />
    </>
  );
}