---
id: 5
title: "Urdu Translation with Gemini API"
stage: "general"
date: "2025-12-08"
model: "Claude Sonnet 4.5"
surface: "agent"
feature: "none"
branch: "master"
user: "user"
command: "/sp.implement"
labels: ["translation", "urdu", "gemini", "api", "frontend", "backend"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - "backend/requirements.txt"
  - "backend/src/main.py"
  - "backend/src/config.py"
  - "src/components/TranslateButton/TranslateButton.js"
  - "src/theme/DocItem/Content.js"
tests: []
---

# Urdu Translation Feature Implementation with Gemini API

## User Input
```
"The Docusaurus content structure is now complete and verified. We will proceed with the final content modification bonus feature: Urdu Translation (Bonus 6.0). This feature must use the configured Gemini API for translation.

**Task 5.13: Urdu Translation Feature Implementation (Using Gemini)**

1.  **Docusaurus Frontend (Translation Button):** Generate the React code for a **'Translate to Urdu'** button. This button must be placed in the chapter header (similar to the Personalization button from Task 5.11) and only be visible if the user is authenticated. The button should capture the current **original_markdown_content** and the **chapter_slug**.

2.  **FastAPI Backend Endpoint:** Implement a new **POST endpoint** `/api/content/translate_urdu` in `main.py`. This endpoint will accept the `original_content` (Markdown string).

3.  **Gemini Translation Logic:** The endpoint must perform the following actions:
    * **Gemini Client Initialization:** Use the `GEMINI_API_KEY` (from .env) to initialize the Gemini client.
    * **LLM Prompt Construction:** Construct a specific prompt for the Gemini model (`gemini-2.5-flash` or similar) that strictly instructs it to:
        * Translate the entire provided **Markdown text** into **standard, modern Urdu**.
        * **CRITICALLY: Maintain the original Markdown structure**, including headings (`#`), lists (`*`), links (`[]()`), and code blocks (``). The integrity of the Markdown syntax is paramount.
    * **Return Translated Content:** Return the new, fully translated Urdu Markdown text to the frontend.

4.  **Frontend Display & Revert:** Detail the JavaScript/React logic for the frontend that will temporarily **replace the English chapter content** with the translated Urdu content. Also, include a **'Revert to English'** button/logic to restore the original text."
```

## Implementation Summary

Successfully implemented the Urdu Translation feature using the Google Gemini API with the following components:

### 1. Backend Implementation
- Added `google-generativeai==0.4.1` to requirements.txt
- Updated config.py to include GEMINI_API_KEY configuration
- Modified main.py to use Gemini API instead of OpenAI:
  - Added import for google.generativeai
  - Configured Gemini API with the API key from config
  - Updated the `get_urdu_translated_content` function to use `genai.GenerativeModel('gemini-2.5-flash')`
  - Created proper generation configuration with temperature control

### 2. Translation Prompt Engineering
- Maintained comprehensive prompt that instructs Gemini to preserve Markdown structure
- Ensures headings, lists, code blocks, links, and other Markdown elements remain intact
- Focuses on translating only human-readable text while preserving formatting

### 3. Frontend Components
- Enhanced existing TranslateButton component to work with the Gemini-powered backend
- Translation button appears only for authenticated users
- Includes revert functionality to restore original content
- Proper error handling and loading states

### 4. Frontend Content Management
- Updated Content.js to manage content state for translation/reversion
- Added proper content replacement logic
- Included Urdu text styling (RTL direction, appropriate font)

## Files Modified
- `backend/requirements.txt` - Added Google Generative AI library
- `backend/src/main.py` - Updated to use Gemini API for translation
- `backend/src/config.py` - Added GEMINI_API_KEY configuration
- `src/components/TranslateButton/TranslateButton.js` - Enhanced with revert functionality
- `src/theme/DocItem/Content.js` - Updated content management for translation

## Outcome
The Urdu translation feature is now fully implemented using the Gemini API, allowing authenticated users to translate documentation content to Urdu while preserving all Markdown formatting, with the ability to revert back to English.