import React, { useState, useEffect, useRef } from 'react';
import './Chatbot.css';

// API base URL - configured for Docusaurus client-side usage
// This avoids the 'process is not defined' error in the browser
const API_BASE_URL = 'http://localhost:8000';  // Hardcoded for simplicity

const Chatbot = () => {
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState([]);
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef(null);
  const inputRef = useRef(null);

  // Scroll to bottom of chat history when messages change
  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  const toggleChat = () => {
    setIsOpen(!isOpen);
    if (!isOpen && inputRef.current) {
      setTimeout(() => inputRef.current.focus(), 100);
    }
  };

  // Function to call the RAG chat endpoint
  const callRagChatAPI = async (query) => {
    try {
      const response = await fetch(`${API_BASE_URL}/api/rag/chat`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          query: query,
          top_k: 5  // Number of context chunks to retrieve (default: 5)
        }),
      });

      if (!response.ok) {
        throw new Error(`API request failed with status ${response.status}`);
      }

      const data = await response.json();
      return data.response; // Return the generated response from the RAG system
    } catch (error) {
      console.error('Error calling RAG chat API:', error);
      throw error;
    }
  };

  // Function to call the general query endpoint (kept for compatibility)
  const callGeneralQueryAPI = async (query) => {
    try {
      const response = await fetch(`${API_BASE_URL}/api/query/general`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ query }),
      });

      if (!response.ok) {
        throw new Error(`API request failed with status ${response.status}`);
      }

      const data = await response.json();
      return data.answer;
    } catch (error) {
      console.error('Error calling general query API:', error);
      throw error;
    }
  };

  // Function to call the contextual query endpoint (kept for compatibility)
  const callContextualQueryAPI = async (user_query, selected_text) => {
    try {
      const response = await fetch(`${API_BASE_URL}/api/query/contextual`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          user_query,
          selected_text
        }),
      });

      if (!response.ok) {
        throw new Error(`API request failed with status ${response.status}`);
      }

      const data = await response.json();
      return data.answer;
    } catch (error) {
      console.error('Error calling contextual query API:', error);
      throw error;
    }
  };

  const handleSend = async () => {
    if (!inputValue.trim() || isLoading) return;

    // Add user message to chat
    const userMessage = {
      id: Date.now(),
      text: inputValue,
      sender: 'user',
      timestamp: new Date()
    };

    setMessages(prev => [...prev, userMessage]);
    setInputValue('');
    setIsLoading(true);

    try {
      // Determine if this is a contextual query based on whether the input contains context
      // For contextual queries, the input format is "Context: "[selected text]". Question: [user question]"
      const contextualMatch = inputValue.match(/Context: "([^"]*)"\. Question: (.+)/);

      let botResponse;
      if (contextualMatch) {
        // This is a contextual query
        const selectedText = contextualMatch[1];
        const userQuestion = contextualMatch[2];
        botResponse = await callContextualQueryAPI(userQuestion, selectedText);
      } else {
        // Use the RAG chat endpoint for all queries (this is the main fix)
        botResponse = await callRagChatAPI(inputValue);
      }

      // Add bot response to chat
      const botMessage = {
        id: Date.now() + 1,
        text: botResponse,
        sender: 'bot',
        timestamp: new Date()
      };
      setMessages(prev => [...prev, botMessage]);
    } catch (error) {
      // Add error message to chat
      const errorMessage = {
        id: Date.now() + 1,
        text: `Sorry, I encountered an error processing your request. Please try again.`,
        sender: 'bot',
        timestamp: new Date()
      };
      setMessages(prev => [...prev, errorMessage]);
      console.error('Error in handleSend:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const handleContextualQuery = () => {
    // Capture selected text using window.getSelection()
    const selectedText = window.getSelection().toString().trim();

    if (!selectedText) {
      alert('Please select some text on the page first.');
      return;
    }

    // Add user contextual query to chat
    const contextualQuery = `Context: "${selectedText}". Question: `;
    setInputValue(contextualQuery);

    // Focus the input field so user can complete the question
    setTimeout(() => {
      if (inputRef.current) {
        inputRef.current.focus();
        // Move cursor to end of input
        inputRef.current.setSelectionRange(inputRef.current.value.length, inputRef.current.value.length);
      }
    }, 100);
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  const formatTime = (date) => {
    return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
  };

  return (
    <>
      {/* Chatbot toggle button */}
      <button
        className="chatbot-toggle"
        onClick={toggleChat}
        aria-label={isOpen ? "Close chat" : "Open chat"}
      >
        {isOpen ? '×' : '💬'}
      </button>

      {/* Chatbot window - only render if open */}
      {isOpen && (
        <div className="chatbot-container">
          <div className="chatbot-header">
            <h3>AI Assistant</h3>
            <div className="header-controls">
              <button
                className="contextual-query-btn"
                onClick={handleContextualQuery}
                title="Ask about selected text"
              >
                📝
              </button>
              <button
                className="close-btn"
                onClick={toggleChat}
                aria-label="Close chat"
              >
                ×
              </button>
            </div>
          </div>

          <div className="chatbot-messages">
            {messages.length === 0 ? (
              <div className="welcome-message">
                <p>Hello! I'm your AI assistant for the Physical AI & Humanoid Robotics textbook.</p>
                <p>You can:</p>
                <ul>
                  <li>Ask general questions about robotics topics</li>
                  <li>Select text on the page and click the 📝 button to ask context-specific questions</li>
                </ul>
              </div>
            ) : (
              messages.map((message) => (
                <div
                  key={message.id}
                  className={`message ${message.sender}-message`}
                >
                  <div className="message-content">
                    <div className="message-text">{message.text}</div>
                    <div className="message-time">{formatTime(message.timestamp)}</div>
                  </div>
                </div>
              ))
            )}
            {isLoading && (
              <div className="message bot-message">
                <div className="message-content">
                  <div className="typing-indicator">
                    <div></div>
                    <div></div>
                    <div></div>
                  </div>
                </div>
              </div>
            )}
            <div ref={messagesEndRef} />
          </div>

          <div className="chatbot-input-area">
            <textarea
              ref={inputRef}
              value={inputValue}
              onChange={(e) => setInputValue(e.target.value)}
              onKeyDown={handleKeyPress}
              placeholder="Ask a question about the content..."
              rows="1"
              disabled={isLoading}
            />
            <button
              onClick={handleSend}
              disabled={!inputValue.trim() || isLoading}
              className="send-button"
            >
              {isLoading ? '...' : '➤'}
            </button>
          </div>
        </div>
      )}
    </>
  );
};

export default Chatbot;