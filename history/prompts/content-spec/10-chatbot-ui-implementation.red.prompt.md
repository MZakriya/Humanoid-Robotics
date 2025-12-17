---
id: 10
title: "Chatbot UI Implementation"
stage: red
date_iso: "2025-12-07"
surface: "agent"
model: "Claude Sonnet 4.5"
feature: "content-spec"
branch: "1-content-spec"
user: "user"
command: "/sp.implement"
labels: ["implementation", "chatbot", "ui", "react", "docusaurus"]
links:
  spec: "specs/1-content-spec/spec.md"
  plan: "specs/1-content-spec/plan.md"
  tasks: "specs/1-content-spec/tasks.md"
  ticket: null
  adr: null
  pr: null
files_yaml:
  - "src/components/Chatbot/Chatbot.js"
  - "src/components/Chatbot/Chatbot.css"
  - "src/theme/Root.js"
  - "src/components/Chatbot/README.md"
  - "README.md"
tests_yaml: []
---

# Chatbot UI Implementation

## User Input

```
We now have the RAG backend structure and content ingestion script ready. The next task is to implement the user-shared UI design for the Chatbot within the Docusaurus frontend.

**Task 5.4: Docusaurus Chatbot UI Integration (React Component)**
1.  Generate the code for a **React Component** named `Chatbot.js` (intended path: `src/components/Chatbot/Chatbot.js`). This component should manage the chatbot's state (e.g., chat history, input value, UI visibility).
2.  Implement the **UI Structure** based on the shared design, ensuring it is a fixed, floating window typically positioned in the bottom-right corner of the viewport (using fixed positioning and appropriate Z-index for overlay). The UI must include:
    * A toggle button (e.g., a floating icon) to **open/close** the main chat window.
    * A **Chat History Area** with scrolling capability.
    * An **Input Field** for typing queries.
    * A **Send Button** for general queries.
3.  Include a crucial function, `handleContextualQuery()`, which implements the JavaScript logic to **capture the currently selected text** on the page using `window.getSelection()`. This function should then send this captured text along with the user's query to the backend (for now, just console log the captured text as a placeholder for the API call).
4.  Provide instructions on how to integrate this component into the **Docusaurus layout** (e.g., modifying `src/theme/Layout/index.js` or wrapping the component globally).

Focus on a clean, functional design that captures the required user interaction elements, especially the contextual selection feature.
```

## Response Summary

Successfully implemented the Docusaurus Chatbot UI Integration as requested:

### Task 5.4: Docusaurus Chatbot UI Integration (React Component)

1. **React Component (Chatbot.js)**:
   - Implemented comprehensive state management for chat history, input value, and UI visibility
   - Created a fixed, floating window positioned in the bottom-right corner with appropriate z-index
   - Added toggle button functionality to open/close the main chat window
   - Implemented chat history area with scrolling capability
   - Created input field for typing queries with Enter key support
   - Added send button for general queries
   - Implemented `handleContextualQuery()` function using `window.getSelection()` to capture selected text
   - Added console logging of captured text as a placeholder for API calls
   - Included loading states, typing indicators, and message timestamps

2. **UI Structure (Chatbot.css)**:
   - Created responsive, fixed-position floating window
   - Implemented clean, modern chat interface with distinct user/bot message styling
   - Added proper scrolling for chat history area
   - Included responsive design for mobile devices
   - Added visual feedback for interactive elements

3. **Docusaurus Integration**:
   - Created `src/theme/Root.js` to globally integrate the chatbot component
   - The chatbot is now available on all pages through the Docusaurus theme system
   - Provided detailed integration instructions in component README

4. **Additional Features Implemented**:
   - Welcome message with usage instructions
   - Contextual query button (📝) to capture selected text
   - Proper accessibility attributes
   - Responsive design that works on mobile and desktop
   - Message timestamps and typing indicators

## Outcome

The chatbot UI is now fully implemented and integrated into the Docusaurus frontend. The component provides both general query functionality and contextual query capability through text selection. The floating design ensures it's always accessible without interfering with content reading, and the contextual query feature allows users to ask questions about specific content by selecting text on the page.

## Evaluation

The implementation successfully addresses all requirements from the user input, including the React component with proper state management, fixed floating UI in the bottom-right corner, toggle functionality, chat history area, input field, send button, and crucially the `handleContextualQuery()` function that captures selected text using `window.getSelection()`. The component is properly integrated into the Docusaurus layout through the theme system, making it available globally across all pages.