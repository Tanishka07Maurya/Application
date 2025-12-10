import React from 'react';
import { Routes, Route } from 'react-router-dom';
import './App.css';

// --- Components ---
import HomePage from './pages/HomePage';
import LoginPage from './pages/LoginPage'; 
import SignupPage from './pages/SignupPage';
import ProfessorDashboard from './pages/ProfessorDashboard';
import StudentDashboard from './pages/StudentDashboard';
import QuizPage from './pages/QuizPage';
import ViewQuizzesPage from './pages/ViewQuizzesPage';
import ViewQuestionsPage from './pages/ViewQuestionsPage';
import EditQuestionsPage from './pages/EditQuestionsPage';
import ResultsPage from './pages/ResultsPage';

// ✅ 1. IMPORT THE NEW LAYOUT COMPONENT
import ProfessorLayout from './components/layout/ProfessorLayout';

function App() {
  return (
    <div className="App">
      <Routes>
        {/* --- Public & Student Routes (remain the same) --- */}
        <Route path="/" element={<HomePage />} />
        <Route path="/login" element={<LoginPage />} />
        <Route path="/signup" element={<SignupPage />} />
        <Route path="/student/dashboard" element={<StudentDashboard />} />
        <Route path="/quiz/:quizId" element={<QuizPage />} />
        <Route path="/student/results" element={<ResultsPage role="student" />} />

        {/* --- Professor Routes (Now wrapped in the new layout) --- */}
        {/* ✅ 2. WRAP all professor pages inside the ProfessorLayout route */}
        <Route path="/professor" element={<ProfessorLayout />}>
          <Route path="dashboard" element={<ProfessorDashboard />} />
          <Route path="quizzes" element={<ViewQuizzesPage />} />
          <Route path="questions" element={<ViewQuestionsPage />} />
          <Route path="questions/add" element={<EditQuestionsPage isNew />} />
          <Route path="questions/edit/:questionId" element={<EditQuestionsPage />} />
          <Route path="results" element={<ResultsPage role="professor" />} />

          <Route path="generate-quiz" element={<h1>Generate Quiz Page</h1>} />

          {/* You will need to create components for these new pages */}
          <Route path="students" element={<h1>Manage Students Page</h1>} />
          <Route path="analytics" element={<h1>Analytics Page</h1>} />
        </Route>

        <Route path="*" element={<h1>404: Page Not Found</h1>} />
      </Routes>
    </div>
  );
}

export default App;