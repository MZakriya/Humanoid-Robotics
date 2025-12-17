import React, { useState } from 'react';
import { useAuth } from '../../contexts/AuthContext';
import './TranslateButton.css';

// API base URL - configured for Docusaurus client-side usage
// This avoids the 'process is not defined' error in the browser
const API_URL = 'http://localhost:8000';  // Hardcoded for simplicity

const TranslateButton = ({ moduleId, chapterSlug, chapterContent, onContentUpdate }) => {
  const { isAuthenticated, isLoading } = useAuth();
  const [isTranslating, setIsTranslating] = useState(false);
  const [error, setError] = useState(null);
  const [originalContent, setOriginalContent] = useState(null); // To store original content for revert

  // Show button only to authenticated users
  if (!isAuthenticated || isLoading) {
    return null;
  }

  const handleTranslate = async () => {
    if (!moduleId || !chapterSlug || !chapterContent) {
      setError('Module ID, Chapter Slug, or Chapter Content not available');
      return;
    }

    setIsTranslating(true);
    setError(null);

    try {
      // Store original content for revert functionality
      setOriginalContent(chapterContent);

      // Call the Urdu translation endpoint
      const response = await fetch(`${API_URL}/api/content/translate_urdu`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          chapter_slug: chapterSlug,
          original_content: chapterContent
        })
      });

      if (!response.ok) {
        throw new Error(`Translation failed: ${response.statusText}`);
      }

      const result = await response.json();

      // Update the content with the translated version
      if (onContentUpdate && result.translated_content) {
        onContentUpdate(result.translated_content);
      }

      console.log('Content translated successfully:', result);
    } catch (err) {
      console.error('Translation error:', err);
      setError(err.message);
    } finally {
      setIsTranslating(false);
    }
  };

  const handleRevert = () => {
    if (originalContent && onContentUpdate) {
      onContentUpdate(originalContent);
      setOriginalContent(null); // Reset original content after revert
    }
  };

  return (
    <div className="translate-container">
      <div className="translate-buttons">
        <button
          onClick={handleTranslate}
          disabled={isTranslating}
          className={`translate-button ${isTranslating ? 'loading' : ''}`}
          title="Translate this chapter to Urdu"
        >
          {isTranslating ? (
            <span className="loading-text">Translating to Urdu...</span>
          ) : (
            <span className="button-text">.Translate to Urdu</span>
          )}
        </button>

        {originalContent && (
          <button
            onClick={handleRevert}
            className="revert-button"
            title="Revert to original English content"
          >
            <span className="button-text">Revert to English</span>
          </button>
        )}
      </div>

      {error && (
        <div className="translate-error">
          Error: {error}
        </div>
      )}

      <div className="translate-notice">
        <small>
          This feature translates content to standard, modern Urdu while preserving Markdown structure
        </small>
      </div>
    </div>
  );
};

export default TranslateButton;