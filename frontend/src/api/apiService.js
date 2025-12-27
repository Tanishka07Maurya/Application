import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000/';

const API_URL = 'http://localhost:5000/api/questions'; //Vaidehi Changes

export const api = axios.create({
  baseURL: API_BASE_URL,
  withCredentials: true,
});

// Auth endpoints
export const loginUser = (data) => api.post('/auth/login', data);
export const registerUser = (data) => api.post('/auth/signup', data); 

// Quiz endpoints
export const fetchQuizzes = () => api.get('/prof/quizzes');
export const fetchQuizById = (id) => api.get(`/quizzes/${id}`);
export const submitQuiz = (id, data) => api.post(`/quizzes/${id}/submit`, data);

// Professor endpoints
export const fetchQuestions = () => api.get('/prof/questions');
export const addQuestion = (data) => api.post('/prof/add_questions', data);
export const updateQuestion = (id, data) => api.put(`/prof/questions/${id}`, data);
export const deleteQuestion = (id) => api.delete(`/prof/questions/${id}`);
export const fetchQuestionById = (id) => api.get(`/prof/questions/${id}`);//Vaidehi Changes

// --- Dropdown API Calls (Add these to the bottom of apiService.js) ---

// 1. Get schools
export const fetchSchools = () => api.get('/prof/schools');

// 2. Get Programs (linked to schools)
export const fetchPrograms = (schoolId) => api.get(`/prof/programs?school_id=${schoolId}`);

// 3. Get Departments (linked to Program)
export const fetchDepartments = (programId) => api.get(`/prof/departments?program_id=${programId}`);

// 4. Get Courses (linked to Dept & Semester)
export const fetchCourses = (deptId, semester) => api.get(`/prof/courses?dept_id=${deptId}&semester=${semester}`);

// 5. Get Questions (linked to Course)
export const fetchQuestionsByCourse = (courseId) => api.get(`/prof/questions/by_course/${courseId}`);

// 6. Generate Quiz for selected Course
export const generateQuiz = (courseId) => api.post('/prof/generate', { course_id: courseId });

// 7. Fetch Quiz details by token for preview
export const fetchQuizPreview = (token) => api.get(`/prof/quiz-preview/${token}`);

// 8. Fetch courses specifically for the logged-in teacher
export const fetchTeacherCourses = () => api.get('/prof/my-courses');

// 9. Course stats (useful for debugging why generation fails)
export const fetchCourseStats = (courseId) => api.get(`/prof/course-stats?course_id=${courseId}`);