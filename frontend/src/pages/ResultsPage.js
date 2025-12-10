import React, { useEffect, useState } from 'react';
import Table from '../components/ui/Table'; // Assuming you have this component
import { fetchQuizzes } from '../api/apiService'; // Adjust API call if needed

export default function ResultsPage({ role }) {
  const [results, setResults] = useState([]);

  useEffect(() => {
    const loadResults = async () => {
      // Your data fetching logic here...
      try {
        const res = await fetchQuizzes(); // This might need to be a different API call for results
        setResults(res.data);
      } catch (err) {
        console.error(err);
      }
    };
    loadResults();
  }, []);

  const columns = [
    { Header: 'Quiz Title', accessor: 'title' },
    { Header: 'Score', accessor: 'score' },
  ];

  const data = results.map((r) => ({
    title: r.title,
    score: role === 'student' ? r.score : `${r.studentName || 'N/A'} - ${r.score}`,
  }));

  return (
    // ✅ Use the 'main-content' class for the main container
    <main className="main-content">
      <div className="top-bar">
        <h1>{role === 'student' ? 'Your Results' : 'All Student Results'}</h1>
      </div>

      <div className="dashboard-card">
        <Table columns={columns} data={data} />
      </div>
    </main>
  );
}