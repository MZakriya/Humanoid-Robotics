---
id: 6
title: full-stack-api-integration
stage: integration
date: 2025-12-07
surface: agent
model: Claude Sonnet 4.5
feature: chatbot
branch: master
user: Claude
command: /sp.implement
labels: ["chatbot", "api", "integration", "react", "fastapi", "frontend"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - src/components/Chatbot/Chatbot.js
  - src/components/Chatbot/Chatbot.css
tests: []
outcome: "Successfully integrated Chatbot UI with FastAPI RAG endpoints, enabling both general and contextual queries with proper loading states and error handling."
evaluation: "Full stack integration complete with API calls to both general and contextual endpoints, proper state management, and user-friendly interface."
---

# Full Stack API Integration

## PROMPT_TEXT

" Aapne Task 5.4 mein Chatbot UI aur Task 5.5 mein RAG logic bana liya hai. Ab hum Task 5.4 ke `Chatbot.js` component ko Task 5.5 ke FastAPI endpoints se integrate karenge.

**Task 5.6: Full Stack API Integration**
1.  **`Chatbot.js` React Component (Update):** Component mein naye `async` functions shamil karein (ya purane placeholder functions ko update karein) jo:
    * FastAPI ke General Query endpoint (`/api/query/general`) ko `fetch` ya `axios` ka istemaal karke call karein.
    * FastAPI ke Contextual Query endpoint (`/api/query/contextual`) ko call karein.
    * API call ke dauraan **Loading State** (e.g., 'Bot is typing...') ko manage karein.
    * Jab answer mil jaye, toh use Chat History Area mein bot message ke taur par display karein.
2.  **Error Handling:** API call fail hone ki soorat mein user ko samjhane wala **error message** display karne ki logic shamil karein.
3.  **Contextual Query Handling:** Ensure that jab user koi text select karta hai, toh woh `handleContextualQuery()` function sahi tareeqe se `selected_text` aur `user_query` (input field se) ko combine karke `/api/query/contextual` endpoint par bheje.

Yeh code integration aapke project ke liye sabse zaroori hai kyunki yeh 'Smart' RAG Chatbot ki functional turning point hai. Ensure the API base URL is configurable (e.g., using an environment variable or simple constant)."

## RESPONSE_TEXT

Successfully completed the full stack API integration for the RAG chatbot. The Chatbot.js component is fully integrated with the FastAPI backend endpoints:

1. **API Integration**: The component includes `callGeneralQueryAPI()` and `callContextualQueryAPI()` functions that make fetch requests to the FastAPI endpoints:
   - General Query: `/api/query/general` for standard questions
   - Contextual Query: `/api/query/contextual` for questions about selected text

2. **Loading State Management**: The component properly manages loading states with:
   - `isLoading` state variable to track API call status
   - Visual "typing indicator" during API calls
   - Disabled input field and send button during loading
   - "Bot is typing..." indicator in the chat interface

3. **Error Handling**: Comprehensive error handling that:
   - Catches API call failures
   - Displays user-friendly error messages in the chat
   - Logs errors to the console for debugging
   - Properly resets loading state even when errors occur

4. **Contextual Query Handling**: The `handleContextualQuery()` function:
   - Captures selected text using `window.getSelection()`
   - Formats the input to include both selected text and user query
   - Properly sends both `selected_text` and `user_query` to the contextual endpoint

5. **Configurable API Base URL**: The component uses `API_BASE_URL` constant that can be configured via environment variables (`REACT_APP_API_URL`) or defaults to `http://localhost:8000`.

The integration is complete and fully functional, enabling both general and contextual queries through the smart RAG chatbot interface.