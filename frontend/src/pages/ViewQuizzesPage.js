import React, { useEffect, useState } from 'react';
import { fetchQuizzes } from '../api/apiService';
// Vaidehi Changes
export default function ViewQuizzesPage() {
  const [quizzes, setQuizzes] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    loadQuizzes();
  }, []);

  const loadQuizzes = async () => {
    setLoading(true);
    setError(null);
    try {
      const res = await fetchQuizzes();
      console.log('Fetched quizzes:', res.data); // Debug log
      setQuizzes(res.data || []);
    } catch (err) {
      console.error("Failed to fetch quizzes:", err);
      setError('Failed to load quizzes. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async (quizId) => {
    if (!window.confirm('Are you sure you want to delete this quiz?')) {
      return;
    }

    try {
      const response = await fetch(`http://localhost:5000/api/quizzes/${quizId}`, {
        method: 'DELETE',
        headers: {
          'Content-Type': 'application/json',
        },
      });

      if (response.ok) {
        setQuizzes(quizzes.filter(quiz => quiz.id !== quizId));
        alert('Quiz deleted successfully!');
      } else {
        alert('Failed to delete quiz');
      }
    } catch (err) {
      console.error('Error deleting quiz:', err);
      alert('Error deleting quiz');
    }
  };

  const handleReviewEdit = (quizId, quizLink) => {
    // Navigate to quiz review/edit page
    window.location.href = `/quiz/${quizLink || quizId}`;
  };

  const formatDate = (dateString) => {
    if (!dateString) return 'N/A';
    const date = new Date(dateString);
    return date.toLocaleString('en-US', {
      year: 'numeric',
      month: '2-digit',
      day: '2-digit',
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  if (loading) {
    return (
      <main className="main-content">
        <div style={{ 
          display: 'flex', 
          justifyContent: 'center', 
          alignItems: 'center', 
          minHeight: '400px' 
        }}>
          <p style={{ fontSize: '18px', color: '#666' }}>Loading quizzes...</p>
        </div>
      </main>
    );
  }

  return (
    <main className="main-content" style={{ padding: '20px', backgroundColor: '#f5f5f5' }}>
      <div style={{ maxWidth: '1400px', margin: '0 auto' }}>
        {/* Header */}
        <h1 style={{ 
          textAlign: 'center', 
          fontSize: '32px', 
          fontWeight: 'bold',
          marginBottom: '30px',
          color: '#333'
        }}>
          All Your Generated Quizzes
        </h1>

        {error && (
          <div style={{
            padding: '15px',
            backgroundColor: '#fee',
            border: '1px solid #fcc',
            borderRadius: '8px',
            marginBottom: '20px',
            color: '#c33'
          }}>
            {error}
          </div>
        )}

        {quizzes.length === 0 ? (
          <div style={{
            backgroundColor: 'white',
            borderRadius: '8px',
            padding: '60px',
            textAlign: 'center',
            boxShadow: '0 2px 4px rgba(0,0,0,0.1)'
          }}>
            <p style={{ fontSize: '18px', color: '#666', marginBottom: '20px' }}>
              No quizzes found
            </p>
            <button
              onClick={() => window.location.href = '/professor/generate-quiz'}
              style={{
                padding: '12px 24px',
                backgroundColor: '#22c55e',
                color: 'white',
                border: 'none',
                borderRadius: '8px',
                fontSize: '16px',
                fontWeight: '500',
                cursor: 'pointer'
              }}
            >
              Generate New Quiz
            </button>
          </div>
        ) : (
          <>
            {/* Table */}
            <div style={{
              backgroundColor: 'white',
              borderRadius: '8px',
              overflow: 'hidden',
              boxShadow: '0 2px 4px rgba(0,0,0,0.1)'
            }}>
              <div style={{ overflowX: 'auto' }}>
                <table style={{ 
                  width: '100%', 
                  borderCollapse: 'collapse',
                  fontSize: '14px'
                }}>
                  <thead>
                    <tr style={{ backgroundColor: '#f3f4f6', borderBottom: '2px solid #e5e7eb' }}>
                      <th style={headerStyle}>Quiz Title</th>
                      <th style={headerStyle}>Teacher</th>
                      <th style={headerStyle}>School</th>
                      <th style={headerStyle}>Department</th>
                      <th style={headerStyle}>Program</th>
                      <th style={headerStyle}>Semester</th>
                      <th style={headerStyle}>Course</th>
                      <th style={headerStyle}>Total Questions</th>
                      <th style={headerStyle}>Duration</th>
                      <th style={headerStyle}>Status</th>
                      <th style={headerStyle}>Quiz Link</th>
                      <th style={headerStyle}>Generated On</th>
                      <th style={headerStyle}>Actions</th>
                    </tr>
                  </thead>
                  <tbody>
                    {quizzes.map((quiz, index) => (
                      <tr 
                        key={quiz.id} 
                        style={{ 
                          backgroundColor: index % 2 === 0 ? 'white' : '#f9fafb',
                          borderBottom: '1px solid #e5e7eb'
                        }}
                      >
                        <td style={cellStyle}>{quiz.title || quiz.quiz_title || 'Untitled'}</td>
                        <td style={cellStyle}>{quiz.teacher || 'yoothikapatol'}</td>
                        <td style={cellStyle}>{quiz.school || 'School of Technology'}</td>
                        <td style={cellStyle}>{quiz.department || 'Computer Science & Engineering'}</td>
                        <td style={cellStyle}>{quiz.program || '03 - B Tech Computer Science and Engineering'}</td>
                        <td style={cellStyle}>{quiz.semester || 'SEMESTER 3'}</td>
                        <td style={cellStyle}>{quiz.course || 'Specialized track elective-python programming'}</td>
                        <td style={{ ...cellStyle, textAlign: 'center' }}>
                          {quiz.total_questions || quiz.totalQuestions || 5}
                        </td>
                        <td style={cellStyle}>{quiz.duration || 10} minutes</td>
                        <td style={cellStyle}>
                          <span style={{
                            padding: '4px 12px',
                            borderRadius: '9999px',
                            fontSize: '12px',
                            fontWeight: '500',
                            backgroundColor: quiz.status === 'Published' ? '#d1fae5' : '#fef3c7',
                            color: quiz.status === 'Published' ? '#065f46' : '#92400e'
                          }}>
                            {quiz.status || 'Published'}
                          </span>
                        </td>
                        <td style={cellStyle}>
                          <a 
                            href={`/quiz/${quiz.quiz_link || quiz.id}`}
                            target="_blank"
                            rel="noopener noreferrer"
                            style={{ 
                              color: '#2563eb',
                              textDecoration: 'underline',
                              cursor: 'pointer'
                            }}
                          >
                            {quiz.quiz_link ? quiz.quiz_link.substring(0, 30) + '...' : 'View Link'}
                          </a>
                        </td>
                        <td style={cellStyle}>{formatDate(quiz.created_at || quiz.createdAt)}</td>
                        <td style={cellStyle}>
                          <div style={{ display: 'flex', gap: '8px' }}>
                            <button
                              onClick={() => handleReviewEdit(quiz.id, quiz.quiz_link)}
                              style={{
                                padding: '6px 12px',
                                backgroundColor: '#3b82f6',
                                color: 'white',
                                border: 'none',
                                borderRadius: '4px',
                                cursor: 'pointer',
                                fontSize: '12px',
                                fontWeight: '500'
                              }}
                              title="Review/Edit"
                            >
                              Review/Edit
                            </button>
                            <button
                              onClick={() => handleDelete(quiz.id)}
                              style={{
                                padding: '6px 12px',
                                backgroundColor: '#ef4444',
                                color: 'white',
                                border: 'none',
                                borderRadius: '4px',
                                cursor: 'pointer',
                                fontSize: '12px',
                                fontWeight: '500'
                              }}
                              title="Discard"
                            >
                              Discard
                            </button>
                          </div>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>

            {/* Action Buttons */}
            <div style={{ 
              marginTop: '30px', 
              display: 'flex', 
              justifyContent: 'center', 
              gap: '16px' 
            }}>
              <button
                onClick={() => window.location.href = '/professor/generate-quiz'}
                style={{
                  padding: '12px 24px',
                  backgroundColor: '#22c55e',
                  color: 'white',
                  border: 'none',
                  borderRadius: '8px',
                  fontSize: '16px',
                  fontWeight: '500',
                  cursor: 'pointer'
                }}
              >
                Generate New Quiz
              </button>
              <button
                onClick={() => window.location.href = '/professor/dashboard'}
                style={{
                  padding: '12px 24px',
                  backgroundColor: '#6b7280',
                  color: 'white',
                  border: 'none',
                  borderRadius: '8px',
                  fontSize: '16px',
                  fontWeight: '500',
                  cursor: 'pointer'
                }}
              >
                Back to Home
              </button>
            </div>
          </>
        )}
      </div>
    </main>
  );
}

// Styles
const headerStyle = {
  padding: '12px 16px',
  textAlign: 'left',
  fontSize: '13px',
  fontWeight: '600',
  color: '#374151'
};

const cellStyle = {
  padding: '12px 16px',
  fontSize: '13px',
  color: '#4b5563'
};
// import React, { useEffect, useState } from 'react';
// // 💡 FIXED: 'Header' and 'Footer' imports have been removed
// import { fetchQuizzes } from '../api/apiService';

// export default function ViewQuizzesPage() {
//   const [quizzes, setQuizzes] = useState([]);

//   useEffect(() => {
//     const loadQuizzes = async () => {
//       try {
//         const res = await fetchQuizzes();
//         setQuizzes(res.data);
//       } catch (err) {
//         console.error("Failed to fetch quizzes:", err);
//       }
//     };
//     loadQuizzes();
//   }, []);

//   const copyLinkToClipboard = (quizId) => {
//     const link = `${window.location.origin}/quiz/${quizId}`;
//     navigator.clipboard.writeText(link);
//     alert('Quiz link copied to clipboard!');
//   };

//   return (
//     // This component no longer needs <Header /> or <Footer />
//     <main className="main-content">
//       <div className="top-bar">
//         <h1>Available Quizzes</h1>
//       </div>

//       <div className="quiz-list">
//         {quizzes.length > 0 ? (
//           quizzes.map((quiz) => (
//             <div key={quiz.id} className="quiz-list-item">
//               <p className="quiz-list-title">{quiz.title}</p>
//               <button onClick={() => copyLinkToClipboard(quiz.id)} className="btn-like-link">
//                 Copy Link
//               </button>
//             </div>
//           ))
//         ) : (
//           <p>No quizzes found.</p>
//         )}
//       </div>
//     </main>
//   );
// }