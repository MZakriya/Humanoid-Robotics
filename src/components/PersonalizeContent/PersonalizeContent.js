import React, { useState, useEffect } from 'react';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import PersonalizeButton from '../PersonalizeButton/PersonalizeButton';
import { useAuth } from '../../contexts/AuthContext';
import './PersonalizeContent.css';

const PersonalizeContent = ({ moduleId, chapterSlug, originalContent, children }) => {
  const { user, profile, isAuthenticated } = useAuth();
  const [personalizedContent, setPersonalizedContent] = useState(null);
  const [isLoading, setIsLoading] = useState(false);

  // Reset to original content when user changes or logs out
  useEffect(() => {
    if (!isAuthenticated || !user) {
      setPersonalizedContent(null);
    }
  }, [isAuthenticated, user]);

  const handleContentUpdate = (newContent) => {
    setPersonalizedContent(newContent);
  };

  const displayContent = personalizedContent || originalContent || children;

  return (
    <div className="personalize-content-wrapper">
      <div className="personalize-header">
        <PersonalizeButton
          moduleId={moduleId}
          chapterSlug={chapterSlug}
          onContentUpdate={handleContentUpdate}
        />
      </div>

      <div className="content-display">
        {isLoading ? (
          <div className="loading-indicator">Loading personalized content...</div>
        ) : (
          <ReactMarkdown
            remarkPlugins={[remarkGfm]}
            className="markdown-content"
          >
            {displayContent}
          </ReactMarkdown>
        )}
      </div>

      {personalizedContent && (
        <div className="content-controls">
          <button
            className="reset-button"
            onClick={() => setPersonalizedContent(null)}
          >
            Show Original Content
          </button>
          <div className="profile-badge">
            Personalized for: {profile?.softwareBackground?.replace('-', ' ').replace('-', ' ')} / {profile?.hardwareExperience?.replace('-', ' ')}
          </div>
        </div>
      )}
    </div>
  );
};

export default PersonalizeContent;