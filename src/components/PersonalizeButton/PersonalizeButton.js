import React, { useState, useEffect } from 'react';
import { useAuth } from '../../contexts/AuthContext';
import './PersonalizeButton.css';

// API base URL - hardcoded for Docusaurus compatibility
const API_BASE_URL = 'http://localhost:8000';

const PersonalizeButton = ({ moduleId, chapterSlug, onContentUpdate }) => {
  const { user, profile, isAuthenticated, isLoading } = useAuth();
  const [isPersonalizing, setIsPersonalizing] = useState(false);
  const [error, setError] = useState(null);

  // Show button only to authenticated users
  if (!isAuthenticated || isLoading || !user) {
    return null;
  }

  const handlePersonalize = async () => {
    if (!moduleId || !chapterSlug) {
      setError('Module ID or Chapter Slug not available');
      return;
    }

    setIsPersonalizing(true);
    setError(null);

    try {
      // Call the personalization endpoint
      const response = await fetch(`${API_BASE_URL}/api/content/personalize`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          user_id: user.id,
          chapter_id: chapterSlug,
          module_id: moduleId,
          user_profile: profile || {} // Include user profile data
        })
      });

      if (!response.ok) {
        throw new Error(`Personalization failed: ${response.statusText}`);
      }

      const result = await response.json();

      // Update the content with the personalized version
      if (onContentUpdate && result.personalized_content) {
        onContentUpdate(result.personalized_content);
      }

      console.log('Content personalized successfully:', result);
    } catch (err) {
      console.error('Personalization error:', err);
      setError(err.message);
    } finally {
      setIsPersonalizing(false);
    }
  };

  // Determine if user has profile data
  const hasProfile = profile && profile.softwareBackground && profile.hardwareExperience;

  return (
    <div className="personalize-container">
      <button
        onClick={handlePersonalize}
        disabled={isPersonalizing}
        className={`personalize-button ${isPersonalizing ? 'loading' : ''} ${!hasProfile ? 'no-profile' : ''}`}
        title={hasProfile
          ? "Personalize this chapter based on your background"
          : "Set your profile to enable personalization"}
      >
        {isPersonalizing ? (
          <span className="loading-text">Personalizing...</span>
        ) : (
          <span className="button-text">Personalize Chapter</span>
        )}
        {!hasProfile && (
          <span className="profile-warning">⚠️</span>
        )}
      </button>

      {error && (
        <div className="personalize-error">
          Error: {error}
        </div>
      )}

      {!hasProfile && (
        <div className="profile-notice">
          <small>
            Tip: Set your profile preferences to get better personalization
          </small>
        </div>
      )}
    </div>
  );
};

export default PersonalizeButton;