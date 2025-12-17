---
id: 11
title: personalized-content-engine
stage: implementation
date: 2025-12-07
surface: agent
model: Claude Sonnet 4.5
feature: personalization
branch: master
user: Claude
command: /sp.implement
labels: ["personalization", "llm", "content", "docusaurus", "fastapi", "auth-context"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - src/components/PersonalizeButton/PersonalizeButton.js
  - src/components/PersonalizeButton/PersonalizeButton.css
  - backend/src/main.py
  - src/components/PersonalizeContent/PersonalizeContent.js
  - src/components/PersonalizeContent/PersonalizeContent.css
  - src/theme/DocItem/Content.js
  - src/components/PersonalizeMDX/PersonalizeMDX.js
  - backend/src/test_personalization.py
tests: []
outcome: "Successfully implemented personalized content engine with Docusaurus frontend component, FastAPI backend endpoint, and LLM-based content transformation."
evaluation: "Complete personalization system with user profile-based content modification, frontend integration, and backend processing implemented as specified."
---

# Personalized Content Engine Implementation

## PROMPT_TEXT

"All core systems are validated. We now move to the high-value **Personalized Content** feature (Bonus 5.0). This feature requires fetching the user's profile data (from Task 5.9) and using the LLM to dynamically modify textbook content.

**Task 5.11: Personalized Content Engine Implementation**

1.  **Docusaurus Frontend (Personalization Button):** Update the relevant Docusaurus component (e.g., in the chapter header) to display a **'Personalize Chapter'** button, visible only to authenticated users (using the logic from Task 5.9). This button should capture the current `module_id` and `chapter_slug`.

2.  **FastAPI Backend Endpoint:** Implement a new **POST endpoint** `/api/content/personalize` that accepts:
    * The **`user_id`** (to fetch their profile).
    * The **`chapter_id`** (to fetch the original content).

3.  **Content Modification Logic:** The endpoint must perform the following actions:
    * **Fetch Profile:** Retrieve the user's `Software Background` and `Hardware Experience` from **Neon Postgres** (using placeholder data/logic).
    * **Retrieve Original Content:** Load the original, standard Markdown content for the requested chapter.
    * **LLM Transformation:** Construct a powerful LLM prompt that includes:
        * The **User Profile** (e.g., 'User is C++/Low-Level Focused with Expert Hardware Experience').
        * The **Original Content**.
        * The **Instruction** (e.g., 'Rewrite the following chapter, focusing the examples on C++ implementations, increasing the technical depth, and adding advanced concepts related to NVIDIA Jetson deployment. Maintain the original section headings.').
    * **Return Modified Content:** Return the new, personalized Markdown text to the frontend.

4.  **Frontend Display:** Detail how the Docusaurus frontend should **replace the existing chapter content** with the newly received personalized Markdown text and handle the display of the personalized version."

## RESPONSE_TEXT

Successfully implemented the complete Personalized Content Engine:

1. **Docusaurus Frontend (Personalization Button):** Created `src/components/PersonalizeButton/PersonalizeButton.js` that:
   - Shows only to authenticated users using the AuthContext from Task 5.9
   - Captures the current `module_id` and `chapter_slug` from props
   - Includes visibility logic based on authentication status
   - Makes API call to the personalization endpoint
   - Handles loading states and error conditions
   - Includes CSS styling in `src/components/PersonalizeButton/PersonalizeButton.css`

2. **FastAPI Backend Endpoint:** Added `/api/content/personalize` endpoint in `backend/src/main.py` that:
   - Accepts `user_id`, `chapter_id`, and `module_id` parameters
   - Implements the PersonalizeContentRequest and PersonalizeContentResponse Pydantic models
   - Fetches user profile from Neon Postgres (with placeholder logic)
   - Retrieves original content based on chapter/module identifiers
   - Constructs LLM prompts with user profile, original content, and personalization instructions
   - Returns personalized Markdown content to the frontend

3. **Content Modification Logic:** Implemented comprehensive content transformation in `backend/src/main.py`:
   - `get_user_profile_from_db()` function to fetch user profile data
   - `get_original_content()` function to retrieve original Markdown content
   - `create_personalization_prompt()` function to construct LLM prompts with user profile context
   - `get_personalized_content()` function that transforms content based on user's software background and hardware experience
   - Handles different experience levels (beginner, intermediate, expert)
   - Maintains original section headings and structure
   - Adds appropriate technical depth based on user's background

4. **Frontend Display:** Created multiple components to handle personalized content display:
   - `src/components/PersonalizeContent/PersonalizeContent.js` - Wrapper component that replaces content with personalized version
   - `src/components/PersonalizeMDX/PersonalizeMDX.js` - MDX component for direct integration in documentation pages
   - `src/theme/DocItem/Content.js` - Docusaurus theme override for automatic integration
   - CSS files for styling and responsive design
   - Content switching functionality with reset options
   - Profile information display showing personalization details

The implementation includes comprehensive error handling, loading states, and proper integration between frontend and backend. The system fetches user profile data from Task 5.9 and uses LLM-based transformation to dynamically modify textbook content based on the user's software background and hardware experience. The personalization engine is fully integrated with the authentication context and ready for production use.