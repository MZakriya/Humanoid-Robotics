import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom'; // For Docusaurus, we might need to adapt this
import './AuthForm.css';

// API base URL - configurable (can be set via environment variables in a real app)
const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

const AuthForm = ({ mode = 'signup', onAuthSuccess }) => {
  const [formData, setFormData] = useState({
    email: '',
    password: '',
    softwareBackground: '',
    hardwareExperience: ''
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [showCustomFields, setShowCustomFields] = useState(mode === 'signup');

  const softwareBackgroundOptions = [
    { value: 'python-ros', label: 'Python/ROS Focused' },
    { value: 'cpp-low-level', label: 'C++/Low-Level Focused' },
    { value: 'data-science-ml', label: 'Data Science/ML Focused' }
  ];

  const hardwareExperienceOptions = [
    { value: 'beginner', label: 'Beginner/Theoretical' },
    { value: 'intermediate-jetson', label: 'Intermediate/Edge Devices (Jetson)' },
    { value: 'expert-fullstack', label: 'Expert/Full Stack Robotics' }
  ];

  const navigate = useNavigate || (() => {}); // Fallback if useNavigate is not available

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      if (mode === 'signup') {
        // First, perform the authentication signup (placeholder for Better Auth)
        const authResponse = await fetch(`${API_BASE_URL}/api/auth/signup`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            email: formData.email,
            password: formData.password
          })
        });

        if (!authResponse.ok) {
          throw new Error('Authentication signup failed');
        }

        const authResult = await authResponse.json();
        const userId = authResult.userId || 'mock-user-id'; // In a real implementation, this would come from Better Auth

        // After successful auth signup, register the profile data
        const profileResponse = await fetch(`${API_BASE_URL}/user/register_profile`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            userId: userId,
            softwareBackground: formData.softwareBackground,
            hardwareExperience: formData.hardwareExperience
          })
        });

        if (!profileResponse.ok) {
          throw new Error('Profile registration failed');
        }

        const profileResult = await profileResponse.json();
        console.log('Profile registered:', profileResult);
      } else {
        // Login flow
        const response = await fetch(`${API_BASE_URL}/api/auth/login`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            email: formData.email,
            password: formData.password
          })
        });

        if (!response.ok) {
          throw new Error('Login failed');
        }

        const result = await response.json();
        console.log('Login successful:', result);
      }

      // Redirect to home page after successful auth
      window.location.href = '/';

      if (onAuthSuccess) {
        onAuthSuccess({ ...formData, userId: 'mock-user-id' });
      }
    } catch (err) {
      setError(err.message);
      console.error('Auth error:', err);
    } finally {
      setLoading(false);
    }
  };

  const toggleMode = () => {
    const newMode = mode === 'signup' ? 'login' : 'signup';
    setShowCustomFields(newMode === 'signup');
    setFormData({
      email: '',
      password: '',
      softwareBackground: '',
      hardwareExperience: ''
    });
    setError('');
  };

  return (
    <div className="auth-form-container">
      <div className="auth-form-header">
        <h2>{mode === 'signup' ? 'Create Account' : 'Sign In'}</h2>
        <p className="auth-form-subtitle">
          {mode === 'signup'
            ? 'Join the Physical AI & Robotics community'
            : 'Access your personalized content'}
        </p>
      </div>

      {error && <div className="error-message">{error}</div>}

      <form onSubmit={handleSubmit} className="auth-form">
        <div className="form-group">
          <label htmlFor="email">Email:</label>
          <input
            type="email"
            id="email"
            name="email"
            value={formData.email}
            onChange={handleChange}
            required
            disabled={loading}
          />
        </div>

        <div className="form-group">
          <label htmlFor="password">Password:</label>
          <input
            type="password"
            id="password"
            name="password"
            value={formData.password}
            onChange={handleChange}
            required
            minLength="6"
            disabled={loading}
          />
        </div>

        {showCustomFields && (
          <>
            <div className="form-group">
              <label htmlFor="softwareBackground">Software Background:</label>
              <select
                id="softwareBackground"
                name="softwareBackground"
                value={formData.softwareBackground}
                onChange={handleChange}
                required
                disabled={loading}
              >
                <option value="">Select your software background</option>
                {softwareBackgroundOptions.map(option => (
                  <option key={option.value} value={option.value}>
                    {option.label}
                  </option>
                ))}
              </select>
            </div>

            <div className="form-group">
              <label htmlFor="hardwareExperience">Hardware Experience:</label>
              <select
                id="hardwareExperience"
                name="hardwareExperience"
                value={formData.hardwareExperience}
                onChange={handleChange}
                required
                disabled={loading}
              >
                <option value="">Select your hardware experience</option>
                {hardwareExperienceOptions.map(option => (
                  <option key={option.value} value={option.value}>
                    {option.label}
                  </option>
                ))}
              </select>
            </div>
          </>
        )}

        <button type="submit" disabled={loading} className="auth-button">
          {loading ? (mode === 'signup' ? 'Creating Account...' : 'Signing In...') : (mode === 'signup' ? 'Create Account' : 'Sign In')}
        </button>
      </form>

      <div className="auth-form-footer">
        <p>
          {mode === 'signup'
            ? 'Already have an account?'
            : 'Don\'t have an account?'}
          <button
            type="button"
            onClick={toggleMode}
            className="auth-toggle-button"
          >
            {mode === 'signup' ? 'Sign In' : 'Sign Up'}
          </button>
        </p>
      </div>
    </div>
  );
};

export default AuthForm;