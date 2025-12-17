# Chatbot Component

A floating AI assistant component for the Physical AI & Humanoid Robotics Textbook, built with React.

## Features

- **Floating UI**: Fixed position chat window in the bottom-right corner
- **Toggle Button**: Open/close the chat interface
- **Chat History**: Scrollable message history display
- **Text Input**: Text area for typing queries
- **Contextual Queries**: Capture selected text from the page and use it as context for queries
- **Responsive Design**: Works on mobile and desktop devices

## How It Works

1. **General Queries**: Type your question in the input field and click send or press Enter
2. **Contextual Queries**: Select text on the page, click the 📝 button, then complete your question
3. **Message History**: Previous conversations are displayed in the chat window

## Integration with Docusaurus

The chatbot is integrated globally through the `src/theme/Root.js` file, which wraps the entire application. This ensures the chatbot is available on all pages.

## Component Structure

- `Chatbot.js`: Main React component with state management and UI logic
- `Chatbot.css`: Styles for the chatbot interface
- `Root.js`: Docusaurus theme wrapper that includes the chatbot

## API Integration

Currently, the component simulates API responses. To connect to the backend:

1. Replace the `setTimeout` in `handleSend` with an actual API call to your backend
2. Update `handleContextualQuery` to send both the selected text and user query to the backend
3. The backend endpoints would be:
   - General query: `POST /api/chat/general`
   - Contextual query: `POST /api/chat/contextual`

## Usage

The component is automatically included in all pages through the Docusaurus theme system. No additional setup is required after installation.

## Customization

- Modify `Chatbot.css` to change colors, sizes, and positioning
- Update the placeholder text in the welcome message
- Adjust the contextual query behavior in `handleContextualQuery`