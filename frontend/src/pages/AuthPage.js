import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { loginUser, registerUser } from '../api/apiService'; // ✅ Import apiService

// --- Reusable FormInput Component (Now using custom CSS classes) ---
const FormInput = ({ label, type, name, value, onChange, placeholder, icon }) => (
  <div className="form-input-group">
    <label htmlFor={name}>{label}</label>
    <div className="form-input-icon">
      <svg fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
        {icon === 'user' && <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />}
        {icon === 'email' && <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />}
        {icon === 'password' && <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />}
      </svg>
    </div>
    <input
      id={name}
      type={type}
      name={name}
      value={value}
      onChange={onChange}
      placeholder={placeholder}
      required
    />
  </div>
);

// --- Message Display Component (Now using custom CSS classes) ---
const MessageDisplay = ({ message, type }) => {
  if (!message) return null;
  return <div className={`message-display ${type}`}>{message}</div>;
};

// --- LoginForm Component ---
function LoginForm({ onToggle }) {
  const navigate = useNavigate();
  const [formData, setFormData] = useState({ email: "", password: "" });
  const [message, setMessage] = useState(null);
  const [isLoading, setIsLoading] = useState(false);

  const handleChange = (e) => setFormData({ ...formData, [e.target.name]: e.target.value });

  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsLoading(true);
    setMessage(null);
    try {
      // ✅ Use apiService instead of fetch
      const response = await loginUser(formData);
      
      if (response.status === 200) {
        setMessage({ type: 'success', text: "Login successful! Redirecting..." });
        setTimeout(() => {
          if (response.data.user?.role === 'professor') {
            navigate('/professor/dashboard');
          } else {
            navigate('/student/dashboard');
          }
        }, 1500);
      }
    } catch (err) {
      console.error("Login error:", err);
      const errorMessage = err.response?.data?.message || "Invalid credentials. Try again.";
      setMessage({ type: 'error', text: errorMessage });
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <>
      <h2>Login</h2>
      <MessageDisplay message={message?.text} type={message?.type} />
      <form onSubmit={handleSubmit} noValidate>
        <FormInput label="Email" type="email" name="email" value={formData.email} onChange={handleChange} placeholder="Enter your email" icon="email" />
        <FormInput label="Password" type="password" name="password" value={formData.password} onChange={handleChange} placeholder="Enter your password" icon="password" />
        <button type="submit" className="btn btn-primary" style={{ width: '100%' }} disabled={isLoading}>
          {isLoading ? 'Logging in...' : 'Login'}
        </button>
      </form>
      <p className="form-toggle-text">
        Don't have an account? <span onClick={onToggle}>Sign up here</span>
      </p>
    </>
  );
}

// --- SignupForm Component ---
function SignupForm({ onToggle }) {
  const [formData, setFormData] = useState({ name: "", email: "", password: "", role: "student" });
  const [message, setMessage] = useState(null);
  const [isLoading, setIsLoading] = useState(false);

  const handleChange = (e) => setFormData({ ...formData, [e.target.name]: e.target.value });

  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsLoading(true);
    setMessage(null);
    try {
      // ✅ Use apiService instead of fetch
      const response = await registerUser(formData);
      
      if (response.status === 201) {
        setMessage({ type: 'success', text: "Signup successful! Redirecting to login..." });
        setTimeout(() => onToggle(), 2000);
      }
    } catch (err) {
      console.error("Signup error:", err);
      const errorMessage = err.response?.data?.message || "Signup failed. Try again.";
      setMessage({ type: 'error', text: errorMessage });
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <>
      <h2>Create Account</h2>
      <MessageDisplay message={message?.text} type={message?.type} />
      <form onSubmit={handleSubmit} noValidate>
        <FormInput label="Full Name" name="name" type="text" value={formData.name} onChange={handleChange} placeholder="Enter your name" icon="user" />
        <FormInput label="Email" type="email" name="email" value={formData.email} onChange={handleChange} placeholder="Enter your email" icon="email" />
        <FormInput label="Password" type="password" name="password" value={formData.password} onChange={handleChange} placeholder="Create a password" icon="password" />
        
        <div className="role-selector-group">
          <p>I am a:</p>
          <div className="role-selector">
            <label>
              <input type="radio" name="role" value="student" checked={formData.role === 'student'} onChange={handleChange} />
              <span>Student</span>
            </label>
            <label>
              <input type="radio" name="role" value="professor" checked={formData.role === 'professor'} onChange={handleChange} />
              <span>Professor</span>
            </label>
          </div>
        </div>

        <button type="submit" className="btn btn-primary" style={{ width: '100%' }} disabled={isLoading}>
          {isLoading ? 'Creating Account...' : 'Sign Up'}
        </button>
      </form>
      <p className="form-toggle-text">
        Already have an account? <span onClick={onToggle}>Login here</span>
      </p>
    </>
  );
}

// --- Main AuthPage Component ---
export default function AuthPage() {
  const [isLoginView, setIsLoginView] = useState(true);
  const handleToggle = () => setIsLoginView(!isLoginView);

  return (
    <div className="page-container">
      <div className="card form-card">
        {isLoginView ? <LoginForm onToggle={handleToggle} /> : <SignupForm onToggle={handleToggle} />}
      </div>
    </div>
  );
}
// import React, { useState } from 'react';
// import { useNavigate } from 'react-router-dom';

// // --- Reusable FormInput Component (Now using custom CSS classes) ---
// const FormInput = ({ label, type, name, value, onChange, placeholder, icon }) => (
//   <div className="form-input-group">
//     <label htmlFor={name}>{label}</label>
//     <div className="form-input-icon">
//       <svg fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
//         {icon === 'user' && <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />}
//         {icon === 'email' && <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />}
//         {icon === 'password' && <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />}
//       </svg>
//     </div>
//     <input
//       id={name}
//       type={type}
//       name={name}
//       value={value}
//       onChange={onChange}
//       placeholder={placeholder}
//       required
//     />
//   </div>
// );

// // --- Message Display Component (Now using custom CSS classes) ---
// const MessageDisplay = ({ message, type }) => {
//   if (!message) return null;
//   return <div className={`message-display ${type}`}>{message}</div>;
// };

// // --- LoginForm Component ---
// function LoginForm({ onToggle }) {
//   const navigate = useNavigate();
//   const [formData, setFormData] = useState({ email: "", password: "" });
//   const [message, setMessage] = useState(null);
//   const [isLoading, setIsLoading] = useState(false);

//   const handleChange = (e) => setFormData({ ...formData, [e.target.name]: e.target.value });

//   const handleSubmit = async (e) => {
//     e.preventDefault();
//     setIsLoading(true);
//     setMessage(null);
//     try {
//       const response = await fetch("http://localhost:5000/auth/login", {
//         method: "POST",
//         headers: { "Content-Type": "application/json" },
//         body: JSON.stringify(formData),
//       });
//       const data = await response.json();
//       if (response.ok) {
//         setMessage({ type: 'success', text: "Login successful! Redirecting..." });
//         setTimeout(() => {
//           if (data.user?.role === 'professor') {
//             navigate('/professor/dashboard');
//           } else {
//             navigate('/student/dashboard');
//           }
//         }, 1500);
//       } else {
//         setMessage({ type: 'error', text: data.message || "Invalid credentials." });
//       }
//     } catch (err) {
//       setMessage({ type: 'error', text: "An error occurred during login." });
//     } finally {
//       setIsLoading(false);
//     }
//   };

//   return (
//     <>
//       <h2>Login</h2>
//       <MessageDisplay message={message?.text} type={message?.type} />
//       <form onSubmit={handleSubmit} noValidate>
//         <FormInput label="Email" type="email" name="email" value={formData.email} onChange={handleChange} placeholder="Enter your email" icon="email" />
//         <FormInput label="Password" type="password" name="password" value={formData.password} onChange={handleChange} placeholder="Enter your password" icon="password" />
//         <button type="submit" className="btn btn-primary" style={{ width: '100%' }} disabled={isLoading}>
//           {isLoading ? 'Logging in...' : 'Login'}
//         </button>
//       </form>
//       <p className="form-toggle-text">
//         Don’t have an account? <span onClick={onToggle}>Sign up here</span>
//       </p>
//     </>
//   );
// }

// // --- SignupForm Component ---
// function SignupForm({ onToggle }) {
//   const [formData, setFormData] = useState({ name: "", email: "", password: "", role: "student" });
//   const [message, setMessage] = useState(null);
//   const [isLoading, setIsLoading] = useState(false);

//   const handleChange = (e) => setFormData({ ...formData, [e.target.name]: e.target.value });

//   const handleSubmit = async (e) => {
//     e.preventDefault();
//     setIsLoading(true);
//     setMessage(null);
//     try {
//       const response = await fetch("http://localhost:5000/auth/signup", {
//         method: "POST",
//         headers: { "Content-Type": "application/json" },
//         body: JSON.stringify(formData),
//       });
//       const data = await response.json();
//       if (response.ok) {
//         setMessage({ type: 'success', text: "Signup successful! Redirecting to login..." });
//         setTimeout(() => onToggle(), 2000);
//       } else {
//         setMessage({ type: 'error', text: data.message || "Signup failed." });
//       }
//     } catch (err) {
//       setMessage({ type: 'error', text: "An error occurred during signup." });
//     } finally {
//       setIsLoading(false);
//     }
//   };

//   return (
//     <>
//       <h2>Create Account</h2>
//       <MessageDisplay message={message?.text} type={message?.type} />
//       <form onSubmit={handleSubmit} noValidate>
//         <FormInput label="Full Name" name="name" type="text" value={formData.name} onChange={handleChange} placeholder="Enter your name" icon="user" />
//         <FormInput label="Email" type="email" name="email" value={formData.email} onChange={handleChange} placeholder="Enter your email" icon="email" />
//         <FormInput label="Password" type="password" name="password" value={formData.password} onChange={handleChange} placeholder="Create a password" icon="password" />
        
//         <div className="role-selector-group">
//           <p>I am a:</p>
//           <div className="role-selector">
//             <label>
//               <input type="radio" name="role" value="student" checked={formData.role === 'student'} onChange={handleChange} />
//               <span>Student</span>
//             </label>
//             <label>
//               <input type="radio" name="role" value="professor" checked={formData.role === 'professor'} onChange={handleChange} />
//               <span>Professor</span>
//             </label>
//           </div>
//         </div>

//         <button type="submit" className="btn btn-primary" style={{ width: '100%' }} disabled={isLoading}>
//           {isLoading ? 'Creating Account...' : 'Sign Up'}
//         </button>
//       </form>
//       <p className="form-toggle-text">
//         Already have an account? <span onClick={onToggle}>Login here</span>
//       </p>
//     </>
//   );
// }

// // --- Main AuthPage Component ---
// export default function AuthPage() {
//   const [isLoginView, setIsLoginView] = useState(true);
//   const handleToggle = () => setIsLoginView(!isLoginView);

//   return (
//     // Use the page-container for the consistent background
//     <div className="page-container">
//       {/* Use the card and form-card classes for the container */}
//       <div className="card form-card">
//         {isLoginView ? <LoginForm onToggle={handleToggle} /> : <SignupForm onToggle={handleToggle} />}
//       </div>
//     </div>
//   );
// }