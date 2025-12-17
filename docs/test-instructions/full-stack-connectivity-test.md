# Full Stack Connectivity Test Instructions

This document provides step-by-step instructions for testing the connection between the Docusaurus frontend and FastAPI backend for the Physical AI & Humanoid Robotics RAG system.

## Prerequisites

- Backend server running on `http://localhost:8000`
- Docusaurus frontend running on `http://localhost:3000`
- Browser with developer tools (F12)

## Testing General Query Functionality

### 1. Preparation
1. Open your browser and navigate to the Docusaurus site (e.g., `http://localhost:3000`)
2. Open browser developer tools by pressing `F12`
3. Go to the **Network** tab
4. Clear any existing network requests by clicking the "Clear" button (🗑️)

### 2. Execute General Query
1. Open the chatbot UI (click the chat icon 💬 in the bottom right)
2. Enter a general query like: "What is forward kinematics?"
3. Click the send button or press Enter
4. Wait for the response

### 3. Verify in Network Tab
Look for the following in the Network tab:

- **Request URL**: `http://localhost:8000/api/query/general`
- **Method**: `POST`
- **Request Payload**:
  ```json
  {
    "query": "What is forward kinematics?"
  }
  ```
- **Status Code**: `200 OK`
- **Response**: Should contain:
  ```json
  {
    "query": "What is forward kinematics?",
    "answer": "...",
    "sources": [...],
    "context_type": "general"
  }
  ```

## Testing Contextual Query Functionality

### 1. Preparation
1. Navigate to any documentation page in the Docusaurus site
2. Open browser developer tools and go to the **Network** tab
3. Clear any existing network requests

### 2. Execute Contextual Query
1. Select a paragraph or text on the page (e.g., a paragraph about kinematics)
2. Open the chatbot UI if not already open
3. Click the contextual query button (📝) in the chatbot header
4. The input field should be pre-filled with: `Context: "[selected text]". Question:`
5. Complete the question: "Explain this concept in simple terms"
6. Click the send button

### 3. Verify in Network Tab
Look for the following in the Network tab:

- **Request URL**: `http://localhost:8000/api/query/contextual`
- **Method**: `POST`
- **Request Payload**:
  ```json
  {
    "user_query": "Explain this concept in simple terms",
    "selected_text": "[the text you selected]"
  }
  ```
- **Status Code**: `200 OK`
- **Response**: Should contain:
  ```json
  {
    "user_query": "Explain this concept in simple terms",
    "selected_text": "[the text you selected]",
    "combined_query": "Explain the selected text: '[selected text]' in the context of: Explain this concept in simple terms",
    "answer": "...",
    "sources": [...],
    "context_type": "contextual"
  }
  ```

## Expected Results

### Successful Connection Indicators
- ✅ All requests return `200 OK` status
- ✅ Request payloads contain the expected data structure
- ✅ Response payloads contain the expected data structure
- ✅ No CORS (Cross-Origin Resource Sharing) errors in the console
- ✅ Response times are reasonable (< 10 seconds for most queries)

### Common Issues to Check
- ❌ `404 Not Found` - Backend server not running or wrong URL
- ❌ `405 Method Not Allowed` - Wrong HTTP method or endpoint
- ❌ CORS errors - Backend not configured to accept requests from frontend origin
- ❌ `500 Internal Server Error` - Backend server error
- ❌ Request timeout - Backend server not responding

## Console Error Checking

In addition to the Network tab, check the **Console** tab for any error messages:

1. Look for JavaScript errors that might prevent the request from being sent
2. Check for network-related errors
3. Verify that no CORS policy violations are reported

## Troubleshooting Steps

If tests fail:

1. **Verify Backend Status**:
   - Visit `http://localhost:8000/health` to check if backend is running
   - Check backend console for any error messages

2. **Check API Base URL**:
   - Verify that the frontend is configured with the correct backend URL
   - Check environment variables or configuration files

3. **Verify Content Ingestion**:
   - Ensure that content has been properly ingested into Qdrant
   - Test the `/api/query/general` endpoint directly using curl or Postman

4. **Check Network Connectivity**:
   - Verify both frontend and backend are running
   - Check firewall settings if applicable

## Test Completion Checklist

- [ ] General query endpoint called successfully
- [ ] Contextual query endpoint called successfully
- [ ] Request bodies contain correct data format
- [ ] Response status codes are 200 OK
- [ ] Response bodies contain expected fields
- [ ] No CORS errors in console
- [ ] No JavaScript errors in console
- [ ] Response times are acceptable
