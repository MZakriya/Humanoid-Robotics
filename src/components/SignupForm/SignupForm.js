import React, { useState } from 'react';
import './SignupForm.css'; // Optional CSS file for styling

const SignupForm = ({ onSignupSuccess }) => {
  const [formData, setFormData] = useState({
    email: '',
    password: '',
    softwareBackground: '',
    hardwareExperience: ''
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

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
      // This is a placeholder for Better Auth signup
      // In a real implementation, this would call the Better Auth SDK
      const response = await fetch('/api/auth/signup', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          email: formData.email,
          password: formData.password,
          // Custom fields that will be sent to the profile registration endpoint
          profileData: {
            softwareBackground: formData.softwareBackground,
            hardwareExperience: formData.hardwareExperience
          }
        })
      });

      if (!response.ok) {
        throw new Error('Signup failed');
      }

      const result = await response.json();

      // After successful auth signup, register the profile data
      await registerUserProfile(result.userId, {
        softwareBackground: formData.softwareBackground,
        hardwareExperience: formData.hardwareExperience
      });

      if (onSignupSuccess) {
        onSignupSuccess(result);
      }
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const registerUserProfile = async (userId, profileData) => {
    // Placeholder for profile registration after successful auth
    try {
      const response = await fetch('/api/user/register_profile', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          userId,
          ...profileData
        })
      });

      if (!response.ok) {
        throw new Error('Profile registration failed');
      }

      return await response.json();
    } catch (err) {
      console.error('Error registering user profile:', err);
      throw err;
    }
  };

  return (
    <div className="signup-form-container">
      <h2>Sign Up for Physical AI & Robotics Platform</h2>

      {error && <div className="error-message">{error}</div>}

      <form onSubmit={handleSubmit} className="signup-form">
        <div className="form-group">
          <label htmlFor="email">Email:</label>
          <input
            type="email"
            id="email"
            name="email"
            value={formData.email}
            onChange={handleChange}
            required
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
          />
        </div>

        <div className="form-group">
          <label htmlFor="softwareBackground">Software Background:</label>
          <select
            id="softwareBackground"
            name="softwareBackground"
            value={formData.softwareBackground}
            onChange={handleChange}
            required
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
          >
            <option value="">Select your hardware experience</option>
            {hardwareExperienceOptions.map(option => (
              <option key={option.value} value={option.value}>
                {option.label}
              </option>
            ))}
          </select>
        </div>

        <button type="submit" disabled={loading} className="signup-button">
          {loading ? 'Signing up...' : 'Sign Up'}
        </button>
      </form>
    </div>
  );
};

export default SignupForm;