import React, { useState, useEffect } from 'react';
import OriginalDocItemContent from '@theme-original/DocItem/Content';
import { useLocation } from '@docusaurus/router';
import TranslateButton from '../../components/TranslateButton/TranslateButton';
import PersonalizeButton from '../../components/PersonalizeButton/PersonalizeButton';
import { useAuth } from '../../contexts/AuthContext';

// This component wraps the default DocContent to add translation and personalization functionality
function DocContent(props) {
  const location = useLocation();
  const { isAuthenticated } = useAuth();

  const [currentContent, setCurrentContent] = useState(null); // For translation/personalization
  const [hasMounted, setHasMounted] = useState(false);

  useEffect(() => {
    setHasMounted(true);
  }, []);

  // Extract module and chapter info from the URL
  const pathParts = location.pathname.split('/').filter(part => part);
  const moduleId = pathParts[1] || 'unknown-module';
  const chapterSlug = pathParts[2] || 'unknown-chapter';

  // Function to update content (for translation/personalization)
  const handleContentUpdate = (newContent) => {
    setCurrentContent(newContent);
  };

  // Safe rendering wrapper for the original content
  const renderOriginalContent = () => {
    try {
      return <OriginalDocItemContent {...props} />;
    } catch (error) {
      console.error('Error rendering original content:', error);
      return <div>Content temporarily unavailable</div>;
    }
  };

  // For authenticated users, show both translation and personalization options
  if (isAuthenticated && hasMounted) {
    return (
      <div className="doc-content-wrapper">
        {/* Personalization button - visible to authenticated users */}
        <PersonalizeButton
          moduleId={moduleId}
          chapterSlug={chapterSlug}
          onContentUpdate={handleContentUpdate}
        />

        {/* Translation button - visible to authenticated users */}
        <TranslateButton
          moduleId={moduleId}
          chapterSlug={chapterSlug}
          chapterContent={currentContent || 'Default Content'} // Use current content if available, otherwise default
          onContentUpdate={handleContentUpdate}
        />

        {/* Original content or translated/personalized content */}
        <div className={`doc-content ${currentContent ? 'custom-content' : ''}`}>
          {currentContent ? (
            <div
              className="custom-content-display"
              dangerouslySetInnerHTML={{ __html: currentContent }}
            />
          ) : (
            renderOriginalContent()
          )}
        </div>
      </div>
    );
  }

  // For unauthenticated users, show original content with login prompts for features
  return (
    <div className="doc-content-wrapper">
      <div className="feature-prompt">
        <small>
          Login to access personalization and translation features
        </small>
      </div>
      <div className="doc-content">
        {renderOriginalContent()}
      </div>
    </div>
  );
}

export default DocContent;