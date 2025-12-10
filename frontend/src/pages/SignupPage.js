import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';

// --- MODIFIED: Import reusable components from their own files ---
import FormInput from '../components/forms/FormInput';
import MessageDisplay from '../components/ui/MessageDisplay';

export default function SignupPage() {
    const navigate = useNavigate();
    const [formData, setFormData] = useState({ name: "", email: "", password: "", role: "student" });
    const [message, setMessage] = useState(null);
    const [isLoading, setIsLoading] = useState(false);

    const handleChange = (e) => setFormData({ ...formData, [e.target.name]: e.target.value });

    const handleSubmit = async (e) => {
        e.preventDefault();
        setIsLoading(true);
        setMessage(null);
        try {
            // --- MODIFIED: Use the environment variable for a flexible API URL ---
            const apiUrl = `${process.env.REACT_APP_API_URL}/auth/signup`;

            const response = await fetch(apiUrl, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(formData),
            });

            const data = await response.json();

            if (response.ok) {
                setMessage({ type: 'success', text: "Signup successful! Redirecting to login..." });
                setTimeout(() => navigate('/login'), 2000);
            } else {
                setMessage({ type: 'error', text: data.message || "Signup failed." });
            }
        } catch (err) {
            setMessage({ type: 'error', text: "An error occurred during signup." });
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <div className="page-container">
            <div className="card form-card">
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
                    Already have an account?{' '}
                    <Link to="/login">
                        <span>Login here</span>
                    </Link>
                </p>
            </div>
        </div>
    );
}