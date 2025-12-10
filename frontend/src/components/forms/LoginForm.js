import React, { useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import FormInput from "./FormInput";
import "./FormInput.css";
import { loginUser } from "../../api/apiService"; // ✅ Import

function LoginForm() {
  const navigate = useNavigate();
  const [formData, setFormData] = useState({
    email: "",
    password: "",
  });

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      const response = await loginUser(formData); // ✅ Use apiService

      if (response.status === 200) {
        alert(response.data.message || "Login successful!");
        navigate("/dashboard");
      }
    } catch (err) {
      console.error("Login error:", err);
      alert(err.response?.data?.message || "Invalid credentials. Try again.");
    }
  };

  return (
    <div className="auth-page">
      <div className="auth-card">
        <h2>Login</h2>
        <form onSubmit={handleSubmit}>
          <FormInput
            label="Email"
            type="email"
            name="email"
            value={formData.email}
            onChange={handleChange}
            placeholder="Enter your email"
            icon="fa fa-envelope"
          />

          <FormInput
            label="Password"
            type="password"
            name="password"
            value={formData.password}
            onChange={handleChange}
            placeholder="Enter your password"
            icon="fa fa-lock"
          />

          <button type="submit" className="auth-btn">Login</button>
        </form>

        <p className="auth-text">
          Don't have an account?{" "}
          <Link to="/quiz/signup" className="auth-link">Sign up here</Link>
        </p>
      </div>
    </div>
  );
}

export default LoginForm;
// import React, { useState } from "react";
// import { useNavigate, Link } from "react-router-dom";
// import FormInput from "./FormInput";
// import "./FormInput.css";

// function LoginForm() {
//   const navigate = useNavigate();
//   const [formData, setFormData] = useState({
//     email: "",
//     password: "",
//   });

//   const handleChange = (e) => {
//     setFormData({ ...formData, [e.target.name]: e.target.value });
//   };

//   const handleSubmit = async (e) => {
//     e.preventDefault();

//     try {
//       const response = await fetch("http://localhost:8000/auth/login", {
//         method: "POST",
//         headers: { "Content-Type": "application/json" },
//         body: JSON.stringify(formData),
//       });

//       const data = await response.json();

//       if (response.ok) {
//         alert(data.message || "Login successful!");
//         navigate("/dashboard"); // redirect to dashboard/home after login
//       } else {
//         alert(data.message || "Invalid credentials. Try again.");
//       }
//     } catch (err) {
//       console.error("Login error:", err);
//       alert("An error occurred during login.");
//     }
//   };

//   return (
//     <div className="auth-page">
//       <div className="auth-card">
//         <h2>Login</h2>
//         <form onSubmit={handleSubmit}>
//           <FormInput
//             label="Email"
//             type="email"
//             name="email"
//             value={formData.email}
//             onChange={handleChange}
//             placeholder="Enter your email"
//             icon="fa fa-envelope"
//           />

//           <FormInput
//             label="Password"
//             type="password"
//             name="password"
//             value={formData.password}
//             onChange={handleChange}
//             placeholder="Enter your password"
//             icon="fa fa-lock"
//           />

//           <button type="submit" className="auth-btn">Login</button>
//         </form>

//         <p className="auth-text">
//           Don’t have an account?{" "}
//           <Link to="/quiz/signup" className="auth-link">Sign up here</Link>
//         </p>
//       </div>
//     </div>
//   );
// }

// export default LoginForm;
