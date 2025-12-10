import React, { useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import FormInput from "./FormInput";
import "./FormInput.css";
import { registerUser } from "../../api/apiService"; // ✅ Import

function SignupForm() {
  const navigate = useNavigate();
  const [formData, setFormData] = useState({
    name: "",
    email: "",
    password: "",
  });

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      const response = await registerUser(formData); // ✅ Use apiService

      if (response.status === 201) {
        alert(response.data.message || "Signup successful!");
        navigate("/quiz/login");
      }
    } catch (err) {
      console.error("Signup error:", err);
      alert(err.response?.data?.message || "Signup failed. Please try again.");
    }
  };

  return (
    <div className="auth-page">
      <div className="auth-card">
        <h2>Create Account</h2>
        <form onSubmit={handleSubmit}>
          <FormInput
            label="Full Name"
            name="name"
            value={formData.name}
            onChange={handleChange}
            placeholder="Enter your name"
            icon="fa fa-user"
          />

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
            placeholder="Enter a password"
            icon="fa fa-lock"
          />

          <button type="submit" className="auth-btn">Sign Up</button>
        </form>

        <p className="auth-text">
          Already have an account?{" "}
          <Link to="/quiz/login" className="auth-link">Login here</Link>
        </p>
      </div>
    </div>
  );
}

export default SignupForm;

// import React, { useState } from "react";
// import { useNavigate, Link } from "react-router-dom";
// import FormInput from "./FormInput";
// import "./FormInput.css";

// function SignupForm() {
//   const navigate = useNavigate();
//   const [formData, setFormData] = useState({
//     name: "",
//     email: "",
//     password: "",
//   });

//   const handleChange = (e) => {
//     setFormData({ ...formData, [e.target.name]: e.target.value });
//   };

//   const handleSubmit = async (e) => {
//     e.preventDefault();

//     try {
//       const response = await fetch("http://localhost:5000/auth/signup", {
//         method: "POST",
//         headers: { "Content-Type": "application/json" },
//         body: JSON.stringify(formData),
//       });

//       const data = await response.json();

//       if (response.ok) {
//         alert(data.message || "Signup successful!");
//         navigate("/quiz/login");
//       } else {
//         alert(data.message || "Signup failed. Please try again.");
//       }
//     } catch (err) {
//       console.error("Signup error:", err);
//       alert("An error occurred during signup.");
//     }
//   };

//   return (
//     <div className="auth-page">
//       <div className="auth-card">
//         <h2>Create Account</h2>
//         <form onSubmit={handleSubmit}>
//           <FormInput
//             label="Full Name"
//             name="name"
//             value={formData.name}
//             onChange={handleChange}
//             placeholder="Enter your name"
//             icon="fa fa-user"
//           />

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
//             placeholder="Enter a password"
//             icon="fa fa-lock"
//           />

//           <button type="submit" className="auth-btn">Sign Up</button>
//         </form>

//         <p className="auth-text">
//           Already have an account?{" "}
//           <Link to="/quiz/login" className="auth-link">Login here</Link>
//         </p>
//       </div>
//     </div>
//   );
// }

// export default SignupForm;
