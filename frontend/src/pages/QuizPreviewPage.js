// src/pages/QuizPreviewPage.js
import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import { fetchQuizPreview } from '../api/apiService';

export default function QuizPreviewPage() {
    const { token } = useParams(); // Get token from URL
    const [quiz, setQuiz] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState('');

    useEffect(() => {
        const loadPreview = async () => {
            try {
                const res = await fetchQuizPreview(token);
                setQuiz(res.data);
            } catch (err) {
                setError("Failed to load quiz. The link may be invalid.");
            } finally {
                setLoading(false);
            }
        };
        loadPreview();
    }, [token]);

    if (loading) return <div style={{padding: '40px', textAlign: 'center'}}>Loading Preview...</div>;
    if (error) return <div style={{padding: '40px', color: 'red', textAlign: 'center'}}>{error}</div>;

    return (
        <div style={styles.container}>
            <h2 style={styles.title}>Preview: {quiz.title}</h2>
            <div style={styles.banner}>
                This is a preview. Correct answers are highlighted in <span style={{color:'green', fontWeight:'bold'}}>Green</span>.
            </div>

            {quiz.questions.map((q, index) => (
                <div key={q.id} style={styles.card}>
                    <h4 style={styles.qText}>Q{index + 1}: {q.text}</h4>
                    <ul style={styles.optionsList}>
                        {q.options.map((opt, i) => (
                            <li key={i} style={{
                                ...styles.option,
                                border: opt.is_correct ? '2px solid #4CAF50' : '1px solid #ddd',
                                backgroundColor: opt.is_correct ? '#e8f5e9' : 'white'
                            }}>
                                {opt.text}
                                {opt.is_correct && <span style={styles.check}> ✓ Correct</span>}
                            </li>
                        ))}
                    </ul>
                </div>
            ))}
        </div>
    );
}

const styles = {
    container: { maxWidth: '800px', margin: '0 auto', padding: '20px' },
    title: { textAlign: 'center', marginBottom: '20px', color: '#333' },
    banner: { backgroundColor: '#fff3cd', padding: '10px', borderRadius: '5px', marginBottom: '20px', textAlign: 'center', border: '1px solid #ffeeba' },
    card: { backgroundColor: 'white', padding: '20px', borderRadius: '10px', boxShadow: '0 2px 5px rgba(0,0,0,0.1)', marginBottom: '20px' },
    qText: { marginTop: 0, marginBottom: '15px' },
    optionsList: { listStyle: 'none', padding: 0 },
    option: { padding: '10px', borderRadius: '5px', marginBottom: '8px', display: 'flex', justifyContent: 'space-between' },
    check: { color: 'green', fontWeight: 'bold' }
};