//priiii
// import React, { useEffect, useState } from 'react';
// import { 
//   fetchSchools, fetchPrograms, fetchDepartments, fetchCourses 
// } from '../api/apiService'; 
// import Button from '../components/forms/Button'; 

// export default function GenerateQuizPage() {
  
//   // --- STATE FOR SELECTIONS ---
//   const [selections, setSelections] = useState({
//     school: '',
//     program: '',
//     department: '',
//     semester: '',
//     course: ''
//   });

//   // --- STATE FOR DATA LISTS ---
//   const [lists, setLists] = useState({
//     schools: [],
//     programs: [],
//     departments: [],
//     semesters: [1, 2, 3, 4, 5, 6, 7, 8],
//     courses: []
//   });

//   const [generatedLink, setGeneratedLink] = useState('');
//   const [loading, setLoading] = useState(false);

//   // 1. Load Schools on Mount
//   useEffect(() => {
//     loadSchools();
//   }, []);

//   const loadSchools = async () => {
//     try {
//       const res = await fetchSchools();
//       setLists(prev => ({ ...prev, schools: res.data || [] }));
//     } catch (err) { console.error("Error loading schools:", err); }
//   };

//   // --- HANDLERS ---
//   const handleSchoolChange = async (e) => {
//     const schoolId = e.target.value;
//     setSelections({ ...selections, school: schoolId, program: '', department: '', semester: '', course: '' });
//     setLists(prev => ({ ...prev, programs: [], departments: [], courses: [] })); 

//     if (schoolId) {
//       const res = await fetchPrograms(schoolId);
//       setLists(prev => ({ ...prev, programs: res.data || [] }));
//     }
//   };

//   const handleProgramChange = async (e) => {
//     const programId = e.target.value;
//     setSelections({ ...selections, program: programId, department: '', semester: '', course: '' });
//     setLists(prev => ({ ...prev, departments: [], courses: [] }));

//     if (programId) {
//       const res = await fetchDepartments(programId);
//       setLists(prev => ({ ...prev, departments: res.data || [] }));
//     }
//   };

//   const handleDeptChange = (e) => {
//     setSelections({ ...selections, department: e.target.value, semester: '', course: '' });
//     setLists(prev => ({ ...prev, courses: [] }));
//   };

//   const handleSemesterChange = async (e) => {
//     const sem = e.target.value;
//     setSelections({ ...selections, semester: sem, course: '' });
    
//     if (selections.department && sem) {
//       const res = await fetchCourses(selections.department, sem);
//       setLists(prev => ({ ...prev, courses: res.data || [] }));
//     }
//   };

//   const handleCourseChange = (e) => {
//     setSelections({ ...selections, course: e.target.value });
//   };

//   // --- GENERATE QUIZ LOGIC ---
//   const handleGenerateQuiz = async () => {
//     if (!selections.course) {
//         alert("Please select a course first.");
//         return;
//     }
//     setLoading(true);
    
//     // Simulate generation (or call your backend API if you have one ready)
//     setTimeout(() => {
//         // Just creating a fake link for now based on the course ID
//         const fakeUniqueId = Math.random().toString(36).substring(7);
//         const link = `https://quiz-app-mccn.onrender.com/quiz/${selections.course}-${fakeUniqueId}`;
//         setGeneratedLink(link);
//         setLoading(false);
//     }, 1500);
//   };

//   return (
//     <main className="main-content" style={styles.mainContainer}>
      
//       <h2 style={styles.pageTitle}>Generate Quiz Page</h2>

//       {/* GENERATED LINK CARD (Only shows if link exists) */}
//       {generatedLink && (
//         <div style={styles.successCard}>
//             <h3>Generated Quiz Link:</h3>
//             <a href={generatedLink} target="_blank" rel="noreferrer" style={styles.link}>
//                 {generatedLink}
//             </a>
//             <p style={{marginTop: '10px', color: 'green', fontWeight: 'bold'}}>Status: Link Generated</p>
//         </div>
//       )}

//       {/* DROPDOWN FORM CARD */}
//       <div style={styles.card}>
//         <div style={styles.grid}>
            
//             {/* Row 1: School & Department (Based on your picture layout) */}
//             <div style={styles.inputGroup}>
//                 <label style={styles.label}>Select School:</label>
//                 <select style={styles.select} value={selections.school} onChange={handleSchoolChange}>
//                     <option value="">Select a school</option>
//                     {lists.schools.map(item => <option key={item.id} value={item.id}>{item.school_name}</option>)}
//                 </select>
//             </div>

//             <div style={styles.inputGroup}>
//                  <label style={styles.label}>Select Department:</label>
//                  <select style={styles.select} value={selections.department} onChange={handleDeptChange} disabled={!selections.program}>
//                     <option value="">Select a department</option>
//                     {lists.departments.map(item => <option key={item.id} value={item.id}>{item.name}</option>)}
//                 </select>
//             </div>

//             {/* Row 2: Program & Semester */}
//             <div style={styles.inputGroup}>
//                 <label style={styles.label}>Select Program:</label>
//                 <select style={styles.select} value={selections.program} onChange={handleProgramChange} disabled={!selections.school}>
//                     <option value="">Select a program</option>
//                     {lists.programs.map(item => <option key={item.id} value={item.id}>{item.program_name}</option>)}
//                 </select>
//             </div>

//             <div style={styles.inputGroup}>
//                 <label style={styles.label}>Select Semester:</label>
//                 <select style={styles.select} value={selections.semester} onChange={handleSemesterChange} disabled={!selections.department}>
//                     <option value="">Select a semester</option>
//                     {lists.semesters.map(s => <option key={s} value={s}>Semester {s}</option>)}
//                 </select>
//             </div>

//             {/* Row 3: Course (Full Width) */}
//             <div style={{...styles.inputGroup, gridColumn: '1 / -1'}}>
//                 <label style={styles.label}>Select Course:</label>
//                 <select style={styles.select} value={selections.course} onChange={handleCourseChange} disabled={!selections.semester}>
//                     <option value="">Select a course</option>
//                     {lists.courses.map(item => <option key={item.id} value={item.id}>{item.course_name}</option>)}
//                 </select>
//             </div>

//         </div>

//         {/* Generate Button */}
//         <div style={{marginTop: '30px', textAlign: 'center'}}>
//             <Button 
//                 label={loading ? "Generating..." : "Generate Quiz"} 
//                 onClick={handleGenerateQuiz} 
//                 className="btn btn-primary"
//                 style={{width: '200px', fontSize: '1.1rem'}}
//                 disabled={!selections.course || loading}
//             />
//         </div>

//       </div>
//     </main>
//   );
// }

// // --- CSS STYLES ---
// const styles = {
//   mainContainer: {
//     padding: '40px',
//     maxWidth: '1000px',
//     margin: '0 auto'
//   },
//   pageTitle: {
//     textAlign: 'center',
//     color: '#333',
//     marginBottom: '30px',
//     fontSize: '2rem',
//     fontWeight: 'bold'
//   },
//   card: {
//     backgroundColor: '#fff',
//     padding: '40px',
//     borderRadius: '15px',
//     boxShadow: '0 10px 30px rgba(0,0,0,0.05)',
//   },
//   // This creates the 2-column layout
//   grid: {
//     display: 'grid',
//     gridTemplateColumns: '1fr 1fr', // Two equal columns
//     gap: '30px', // Space between items
//   },
//   inputGroup: {
//     display: 'flex',
//     flexDirection: 'column',
//     gap: '8px'
//   },
//   label: {
//     fontWeight: 'bold',
//     color: '#555',
//     fontSize: '1rem'
//   },
//   select: {
//     padding: '12px',
//     borderRadius: '8px',
//     border: '1px solid #ccc',
//     fontSize: '1rem',
//     backgroundColor: '#fff',
//     width: '100%'
//   },
//   successCard: {
//     backgroundColor: '#e3f2fd', // Light Blue
//     padding: '20px',
//     borderRadius: '10px',
//     marginBottom: '30px',
//     textAlign: 'center',
//     border: '1px solid #bbdefb'
//   },
//   link: {
//     color: '#0d47a1',
//     fontWeight: 'bold',
//     wordBreak: 'break-all'
//   }
// };
//priiii

import React, { useEffect, useState } from 'react';
import { 
  fetchSchools, fetchPrograms, fetchDepartments, fetchCourses, generateQuiz, fetchCourseStats 
} from '../api/apiService'; 
import Button from '../components/forms/Button'; 

export default function GenerateQuizPage() {
  
  // --- STATE FOR SELECTIONS ---
  const [selections, setSelections] = useState({
    school: '',
    program: '',
    department: '',
    semester: '',
    course: ''
  });

  // --- STATE FOR DATA LISTS ---
  const [lists, setLists] = useState({
    schools: [],
    programs: [],
    departments: [],
    semesters: [1, 2, 3, 4, 5, 6, 7, 8],
    courses: []
  });

  const [generatedLink, setGeneratedLink] = useState('');
  const [loading, setLoading] = useState(false);

  // 1. Load Schools on Mount
  useEffect(() => {
    loadSchools();
  }, []);

  const loadSchools = async () => {
    try {
      const res = await fetchSchools();
      setLists(prev => ({ ...prev, schools: res.data || [] }));
    } catch (err) { console.error("Error loading schools:", err); }
  };

  // --- HANDLERS ---
  const handleSchoolChange = async (e) => {
    const schoolId = e.target.value;
    setSelections({ ...selections, school: schoolId, program: '', department: '', semester: '', course: '' });
    setLists(prev => ({ ...prev, programs: [], departments: [], courses: [] })); 

    if (schoolId) {
      const res = await fetchPrograms(schoolId);
      setLists(prev => ({ ...prev, programs: res.data || [] }));
    }
  };

  const handleProgramChange = async (e) => {
    const programId = e.target.value;
    setSelections({ ...selections, program: programId, department: '', semester: '', course: '' });
    setLists(prev => ({ ...prev, departments: [], courses: [] }));

    if (programId) {
      const res = await fetchDepartments(programId);
      setLists(prev => ({ ...prev, departments: res.data || [] }));
    }
  };

  const handleDeptChange = (e) => {
    setSelections({ ...selections, department: e.target.value, semester: '', course: '' });
    setLists(prev => ({ ...prev, courses: [] }));
  };

  const handleSemesterChange = async (e) => {
    const sem = e.target.value;
    setSelections({ ...selections, semester: sem, course: '' });
    
    if (selections.department && sem) {
      const res = await fetchCourses(selections.department, sem);
      setLists(prev => ({ ...prev, courses: res.data || [] }));
    }
  };

  const [courseStats, setCourseStats] = useState(null);

  const handleCourseChange = async (e) => {
    const course = e.target.value;
    setSelections({ ...selections, course });

    if (!course) {
      setCourseStats(null);
      return;
    }

    try {
      const statsRes = await fetchCourseStats(course);
      setCourseStats(statsRes.data || null);
    } catch (err) {
      console.error('Failed to fetch course stats:', err);
      setCourseStats(null);
    }
  };

  // --- GENERATE QUIZ LOGIC ---❤️❤️❤️❤️❤️
 // src/pages/GenerateQuizPage.js
const handleGenerateQuiz = async () => {
    if (!selections.course) {
        alert("Please select a course first.");
        return;
    }
    setLoading(true);
    try {
        // 🚀 Use the centralized API instance instead of manual fetch
        const res = await generateQuiz(selections.course);

        if (res.status === 201) {
            setGeneratedLink(res.data.quiz_link);
            const usedTeacher = res.data.used_teacher_filter;
            const count = res.data.question_count || 0;
            if (usedTeacher === false) {
                alert(`Quiz generated using course pool with ${count} questions (no teacher-specific questions found).`);
            } else {
                alert(`Quiz generated and saved successfully with ${count} questions.`);
            }
        }
    } catch (error) {
        if (error.response && error.response.status === 403) {
            alert("Session expired. Please log in again.");
        } else {
            console.error("Generation failed:", error);
            alert("Failed to generate quiz. Ensure questions exist for this course.");
        }
    } finally {
        setLoading(false);
    }
};

  return (
    <main className="main-content" style={styles.mainContainer}>
      
      <h2 style={styles.pageTitle}>Generate Quiz Form</h2>

      {/* GENERATED LINK CARD (Only shows if link exists) */}
      {generatedLink && (
        <div style={styles.successCard}>
            <h3>Generated Quiz Link:</h3>
            <a href={generatedLink} target="_blank" rel="noreferrer" style={styles.link}>
                {generatedLink}
            </a>
            <p style={{marginTop: '10px', color: 'green', fontWeight: 'bold'}}>Status: Link Generated</p>
        </div>
      )}

      {/* DROPDOWN FORM CARD */}
      <div style={styles.card}>
        
        {/* ✅ GRID CONTAINER START */}
        <div style={styles.gridContainer}>
            
            {/* Row 1, Col 1: School */}
            <div style={styles.inputGroup}>
                <label style={styles.label}>Select School:</label>
                <select style={styles.select} value={selections.school} onChange={handleSchoolChange}>
                    <option value="">Select a school</option>
                    {lists.schools.map(item => <option key={item.id} value={item.id}>{item.school_name}</option>)}
                </select>
            </div>

            {/* Row 1, Col 2: Department */}
            <div style={styles.inputGroup}>
                 <label style={styles.label}>Select Department:</label>
                 <select style={styles.select} value={selections.department} onChange={handleDeptChange} disabled={!selections.program}>
                    <option value="">Select a department</option>
                    {lists.departments.map(item => <option key={item.id} value={item.id}>{item.dept_name}</option>)}
                </select>
            </div>

            {/* Row 2, Col 1: Program */}
            <div style={styles.inputGroup}>
                <label style={styles.label}>Select Program:</label>
                <select style={styles.select} value={selections.program} onChange={handleProgramChange} disabled={!selections.school}>
                    <option value="">Select a program</option>
                    {lists.programs.map(item => <option key={item.id} value={item.id}>{item.program_name}</option>)}
                </select>
            </div>

            {/* Row 2, Col 2: Semester */}
            <div style={styles.inputGroup}>
                <label style={styles.label}>Select Semester:</label>
                <select style={styles.select} value={selections.semester} onChange={handleSemesterChange} disabled={!selections.department}>
                    <option value="">Select a semester</option>
                    {lists.semesters.map(s => <option key={s} value={s}>Semester {s}</option>)}
                </select>
            </div>

            {/* Row 3: Course (Full Width) */}
            <div style={{...styles.inputGroup, gridColumn: '1 / -1'}}>
                <label style={styles.label}>Select Course:</label>
                <select style={styles.select} value={selections.course} onChange={handleCourseChange} disabled={!selections.semester}>
                    <option value="">Select a course</option>
                    {lists.courses.map(item => <option key={item.id} value={item.id}>{item.course_name}</option>)}
                </select>
            </div>

        </div>
        {/* ✅ GRID CONTAINER END */}

        {/* Generate Button */}
        {courseStats && (
          <div style={{ marginTop: '16px', textAlign: 'center', color: '#333' }}>
            <strong>Course Questions:</strong> {courseStats.total_for_course || 0} • <strong>Your Questions:</strong> {courseStats.teacher_for_course || 0}
          </div>
        )}

        <div style={{marginTop: '30px', textAlign: 'center'}}>
            <Button 
                label={loading ? "Generating..." : "Generate Quiz"} 
                onClick={handleGenerateQuiz} 
                className="btn btn-primary"
                style={{width: '200px', fontSize: '1.1rem'}}
                disabled={!selections.course || loading}
            />
        </div>

      </div>
    </main>
  );
}

// --- CSS STYLES ---
const styles = {
  mainContainer: {
    padding: '40px',
    maxWidth: '1000px',
    margin: '0 auto',
    boxSizing: 'border-box'
  },
  pageTitle: {
    textAlign: 'center',
    color: '#333',
    marginBottom: '30px',
    fontSize: '2rem',
    fontWeight: 'bold'
  },
  card: {
    backgroundColor: '#fff',
    padding: '40px',
    borderRadius: '15px',
    boxShadow: '0 10px 30px rgba(0,0,0,0.05)',
  },
  gridContainer: {
    display: 'grid',
    gridTemplateColumns: '1fr 1fr', // 2 Columns
    gap: '25px', 
  },
  inputGroup: {
    display: 'flex',
    flexDirection: 'column',
    gap: '8px'
  },
  label: {
    fontWeight: '600',
    color: '#555',
    fontSize: '0.95rem',
    marginLeft: '4px'
  },
  select: {
    padding: '12px 15px',
    borderRadius: '8px',
    border: '1px solid #e0e0e0',
    fontSize: '1rem',
    backgroundColor: '#f9f9f9',
    width: '100%',
    outline: 'none',
    transition: 'border 0.3s ease',
    cursor: 'pointer'
  },
  successCard: {
    backgroundColor: '#e3f2fd',
    padding: '20px',
    borderRadius: '10px',
    marginBottom: '30px',
    textAlign: 'center',
    border: '1px solid #bbdefb'
  },
  link: {
    color: '#0d47a1',
    fontWeight: 'bold',
    wordBreak: 'break-all',
    textDecoration: 'none'
  }
};