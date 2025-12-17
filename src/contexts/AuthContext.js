import React, { createContext, useContext, useReducer, useEffect } from 'react';

// API base URL - configured for Docusaurus client-side usage
// This avoids the 'process is not defined' error in the browser
const API_URL = 'http://localhost:8000';  // Hardcoded for simplicity

// Initial state for the authentication context
const initialState = {
  user: null,
  profile: null,
  isAuthenticated: false,
  isLoading: true,
  error: null
};

// Auth context
const AuthContext = createContext();

// Auth reducer to handle state changes
const authReducer = (state, action) => {
  switch (action.type) {
    case 'AUTH_START':
      return {
        ...state,
        isLoading: true,
        error: null
      };
    case 'AUTH_SUCCESS':
      return {
        ...state,
        user: action.payload.user,
        profile: action.payload.profile,
        isAuthenticated: true,
        isLoading: false,
        error: null
      };
    case 'AUTH_FAILURE':
      return {
        ...state,
        user: null,
        profile: null,
        isAuthenticated: false,
        isLoading: false,
        error: action.payload.error
      };
    case 'SET_USER_PROFILE':
      return {
        ...state,
        profile: action.payload.profile
      };
    case 'LOGOUT':
      return {
        ...state,
        user: null,
        profile: null,
        isAuthenticated: false,
        isLoading: false,
        error: null
      };
    case 'SET_LOADING':
      return {
        ...state,
        isLoading: action.payload.isLoading
      };
    default:
      return state;
  }
};

// Auth provider component
export const AuthProvider = ({ children }) => {
  const [state, dispatch] = useReducer(authReducer, initialState);

  // Check authentication status on app load
  useEffect(() => {
    checkAuthStatus();
  }, []);

  // Function to check if user is authenticated
  const checkAuthStatus = async () => {
    try {
      dispatch({ type: 'AUTH_START' });

      const response = await fetch(`${API_URL}/api/auth/me`, {
        method: 'GET',
        credentials: 'include', // Include cookies if using session cookies
        headers: {
          'Content-Type': 'application/json',
        },
      });

      if (response.ok) {
        const userData = await response.json();

        // Get user profile if user is authenticated
        const profile = await getUserProfile(userData.id);

        dispatch({
          type: 'AUTH_SUCCESS',
          payload: {
            user: userData,
            profile: profile
          }
        });
      } else {
        dispatch({ type: 'AUTH_FAILURE', payload: { error: 'Not authenticated' } });
      }
    } catch (error) {
      dispatch({
        type: 'AUTH_FAILURE',
        payload: { error: error.message || 'Authentication check failed' }
      });
    }
  };

  // Function to get user profile
  const getUserProfile = async (userId) => {
    try {
      const response = await fetch(`${API_URL}/user/profile/${userId}`, {
        method: 'GET',
        credentials: 'include',
        headers: {
          'Content-Type': 'application/json',
        },
      });

      if (response.ok) {
        return await response.json();
      } else {
        console.warn('User profile not found, returning null');
        return null;
      }
    } catch (error) {
      console.error('Error getting user profile:', error);
      return null;
    }
  };

  // Function to register user profile
  const registerUserProfile = async (userId, profileData) => {
    try {
      dispatch({ type: 'AUTH_START' });

      const response = await fetch(`${API_URL}/user/register_profile`, {
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

      const result = await response.json();

      // Update the profile in state
      dispatch({
        type: 'SET_USER_PROFILE',
        payload: { profile: profileData }
      });

      return result;
    } catch (error) {
      dispatch({
        type: 'AUTH_FAILURE',
        payload: { error: error.message || 'Profile registration failed' }
      });
      throw error;
    }
  };

  // Function to login
  const login = async (email, password) => {
    try {
      dispatch({ type: 'AUTH_START' });

      const response = await fetch(`${API_URL}/api/auth/login`, {
        method: 'POST',
        credentials: 'include',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email, password })
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Login failed');
      }

      const result = await response.json();

      // Get user profile after login
      const profile = await getUserProfile(result.userId);

      dispatch({
        type: 'AUTH_SUCCESS',
        payload: {
          user: { id: result.userId, email },
          profile: profile
        }
      });

      return result;
    } catch (error) {
      dispatch({
        type: 'AUTH_FAILURE',
        payload: { error: error.message || 'Login failed' }
      });
      throw error;
    }
  };

  // Function to signup
  const signup = async (email, password, profileData) => {
    try {
      dispatch({ type: 'AUTH_START' });

      // First, register the user
      const response = await fetch(`${API_URL}/api/auth/signup`, {
        method: 'POST',
        credentials: 'include',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email, password })
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Signup failed');
      }

      const result = await response.json();
      const userId = result.userId;

      // Then register the profile with custom fields
      await registerUserProfile(userId, {
        softwareBackground: profileData.softwareBackground,
        hardwareExperience: profileData.hardwareExperience
      });

      // Get updated user profile
      const profile = await getUserProfile(userId);

      dispatch({
        type: 'AUTH_SUCCESS',
        payload: {
          user: { id: userId, email },
          profile: profile
        }
      });

      return result;
    } catch (error) {
      dispatch({
        type: 'AUTH_FAILURE',
        payload: { error: error.message || 'Signup failed' }
      });
      throw error;
    }
  };

  // Function to logout
  const logout = async () => {
    try {
      await fetch(`${API_URL}/api/auth/logout`, {
        method: 'POST',
        credentials: 'include',
        headers: {
          'Content-Type': 'application/json',
        },
      });

      // Clear any local storage or cookies if needed
      localStorage.clear();

      dispatch({ type: 'LOGOUT' });
    } catch (error) {
      console.error('Logout error:', error);
      dispatch({ type: 'LOGOUT' });
    }
  };

  // Value to be provided to consumers
  const value = {
    ...state,
    login,
    signup,
    logout,
    registerUserProfile,
    getUserProfile,
    checkAuthStatus
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};

// Custom hook to use the auth context
export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};

export default AuthContext;