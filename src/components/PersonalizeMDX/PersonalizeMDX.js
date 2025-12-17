import React, { useState } from 'react';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import PersonalizeButton from '../PersonalizeButton/PersonalizeButton';
import { useAuth } from '../../contexts/AuthContext';

// A reusable MDX component for personalizing content in Docusaurus pages
const PersonalizeMDX = ({ children, moduleId, chapterSlug }) => {
  const { isAuthenticated, profile } = useAuth();
  const [personalizedContent, setPersonalizedContent] = useState(null);

  // If user is not authenticated, show original content
  if (!isAuthenticated) {
    return <div>{children}</div>;
  }

  const handleContentUpdate = (newContent) => {
    setPersonalizedContent(newContent);
  };

  // Determine what content to display
  const contentToDisplay = personalizedContent || (typeof children === 'string' ? children : '');

  return (
    <div className="personalize-mdx-container">
      <div className="personalize-controls">
        <PersonalizeButton
          moduleId={moduleId}
          chapterSlug={chapterSlug}
          onContentUpdate={handleContentUpdate}
        />
      </div>

      <div className="content-area">
        {personalizedContent ? (
          <ReactMarkdown
            remarkPlugins={[remarkGfm]}
            className="personalized-markdown"
          >
            {personalizedContent}
          </ReactMarkdown>
        ) : (
          <div className="original-content">
            {children}
          </div>
        )}
      </div>

      {personalizedContent && (
        <div className="reset-controls">
          <button
            onClick={() => setPersonalizedContent(null)}
            className="reset-content-button"
          >
            Show Original Content
          </button>
          {profile && (
            <div className="user-profile-info">
              Personalized for: {profile.softwareBackground?.replace(/-/g, ' ')} / {profile.hardwareExperience?.replace(/-/g, ' ')}
            </div>
          )}
        </div>
      )}
    </div>
  );
};

export default PersonalizeMDX;