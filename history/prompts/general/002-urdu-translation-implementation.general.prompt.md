---
id: 2
title: "Urdu Translation Feature Implementation"
stage: "general"
date: "2025-12-08"
model: "Claude Sonnet 4.5"
surface: "agent"
feature: "none"
branch: "master"
user: "user"
command: "/sp.implement"
labels: ["translation", "urdu", "frontend", "backend", "llm"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - "src/components/TranslateButton/TranslateButton.js"
  - "src/components/TranslateButton/TranslateButton.css"
  - "backend/src/main.py"
  - "src/theme/DocItem/Content.js"
  - "src/css/custom.css"
tests: []
---

# Urdu Translation Feature Implementation

## User Input
```
"All core system implementation and startup procedures (Task 5.12) are now complete. We will proceed with the final high-value bonus feature: Urdu Translation.

**Task 5.13: Urdu Translation Feature Implementation (Bonus 6.0)**

1.  **Docusaurus Frontend (Translation Button):** Create a **'Translate to Urdu'** button (similar to the personalization button) that is visible only to logged-in users. This button must capture the current `chapter_content` (either in Markdown or HTML) and the `chapter_slug`.

2.  **FastAPI Backend Endpoint:** Implement a new **POST endpoint** `/api/content/translate_urdu` that accepts the `chapter_slug` and the `original_content`.

3.  **LLM/Translation Logic:** The endpoint must perform the following actions:
    * **LLM Prompt Construction:** Create an LLM prompt that instructs the model (or use a dedicated translation API like Google Translate if available, but LLM preferred for this hackathon) to accurately translate the provided **Markdown** content into **standard, modern Urdu**. The prompt must emphasize maintaining the original Markdown structure (headings, lists, code blocks).
    * **Return Translated Content:** Return the new, fully translated Urdu Markdown text to the frontend.

4.  **Frontend Display:** Detail how the Docusaurus frontend will **replace the existing chapter content** with the translated Urdu Markdown text and provide a **'Revert to English'** button."
```

## Implementation Summary

Successfully implemented the Urdu Translation feature with the following components:

### 1. Frontend Translation Button
- Created `TranslateButton` component similar to the existing personalization button
- Button is visible only to authenticated users
- Captures chapter content and slug for translation
- Includes both "Translate to Urdu" and "Revert to English" functionality
- Proper error handling and loading states

### 2. Backend API Endpoint
- Added `/api/content/translate_urdu` POST endpoint to main.py
- Created `UrduTranslationRequest` and `UrduTranslationResponse` Pydantic models
- Implemented LLM-based translation using OpenAI API
- Added comprehensive prompt engineering to preserve Markdown structure during translation

### 3. LLM Translation Logic
- Created detailed prompt that instructs the LLM to translate content to Urdu
- Emphasizes preserving all Markdown formatting (headings, lists, code blocks, etc.)
- Uses appropriate temperature setting for consistent translations
- Includes error handling to return original content if translation fails

### 4. Frontend Content Replacement
- Updated `src/theme/DocItem/Content.js` to integrate translation functionality
- Added CSS styling for Urdu text (RTL direction, appropriate font)
- Implemented content state management for translation/reversion
- Added visual prompt for unauthenticated users to login for translation features

## Files Modified/Added
- `src/components/TranslateButton/TranslateButton.js` - Translation button component
- `src/components/TranslateButton/TranslateButton.css` - Styling for translation button
- `backend/src/main.py` - Added Urdu translation endpoint and logic
- `src/theme/DocItem/Content.js` - Integrated translation into document display
- `src/css/custom.css` - Added Urdu text styling

## Outcome
The Urdu translation feature is now fully implemented and integrated into the Docusaurus frontend. Authenticated users can translate chapter content to Urdu while preserving all Markdown formatting, and revert back to English when needed.