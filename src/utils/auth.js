// Authentication utilities for the Docusaurus frontend
// This handles session checking and provides auth context to components

// API base URL - should match the backend URL
const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

// Check if user is authenticated
export const isAuthenticated = async () => {
  try {
    const response = await fetch(`${API_BASE_URL}/api/auth/session`, {
      method: 'GET',
      credentials: 'include', // Include cookies if using session cookies
      headers: {
        'Content-Type': 'application/json',
      },
    });

    return response.ok;
  } catch (error) {
    console.error('Error checking authentication:', error);
    return false;
  }
};

// Get current user info
export const getCurrentUser = async () => {
  try {
    const response = await fetch(`${API_BASE_URL}/api/auth/me`, {
      method: 'GET',
      credentials: 'include',
      headers: {
        'Content-Type': 'application/json',
      },
    });

    if (response.ok) {
      return await response.json();
    } else {
      return null;
    }
  } catch (error) {
    console.error('Error getting user info:', error);
    return null;
  }
};

// Login function (redirects to auth provider)
export const login = () => {
  // In a real implementation, this would redirect to Better Auth login
  window.location.href = `${API_BASE_URL}/api/auth/login`;
};

// Logout function
export const logout = async () => {
  try {
    await fetch(`${API_BASE_URL}/api/auth/logout`, {
      method: 'POST',
      credentials: 'include',
      headers: {
        'Content-Type': 'application/json',
      },
    });

    // Clear any local storage or cookies if needed
    localStorage.clear();

    // Redirect to home page after logout
    window.location.href = '/';
  } catch (error) {
    console.error('Error logging out:', error);
  }
};

// Register user profile after successful auth
export const registerUserProfile = async (userId, profileData) => {
  try {
    const response = await fetch(`${API_BASE_URL}/user/register_profile`, {
      method: 'POST',
      credentials: 'include',
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
  } catch (error) {
    console.error('Error registering user profile:', error);
    throw error;
  }
};

// Get user profile
export const getUserProfile = async (userId) => {
  try {
    const response = await fetch(`${API_BASE_URL}/user/profile/${userId}`, {
      method: 'GET',
      credentials: 'include',
      headers: {
        'Content-Type': 'application/json',
      },
    });

    if (!response.ok) {
      throw new Error('Failed to get user profile');
    }

    return await response.json();
  } catch (error) {
    console.error('Error getting user profile:', error);
    throw error;
  }
};

// Default export for easy import
export default {
  isAuthenticated,
  getCurrentUser,
  login,
  logout,
  registerUserProfile,
  getUserProfile
};