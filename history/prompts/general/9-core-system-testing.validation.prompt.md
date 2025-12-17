---
id: 9
title: core-system-testing
stage: validation
date: 2025-12-07
surface: agent
model: Claude Sonnet 4.5
feature: testing
branch: master
user: Claude
command: /sp.implement
labels: ["testing", "validation", "rag", "qdrant", "full-stack"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - backend/src/core_system_test.py
  - backend/src/rag_search_test.py
  - docs/test-instructions/full-stack-connectivity-test.md
  - backend/src/validate_core_system.py
tests: []
outcome: "Successfully implemented comprehensive testing suite for RAG system including ingestion, search, and full-stack validation."
evaluation: "Complete test suite with ingestion verification, isolated search testing, and full-stack connectivity instructions implemented as specified."
---

# Core System Testing and Validation

## PROMPT_TEXT

Task 5.10: Core System Testing and Validation**

1.  **Ingestion Test Utility:** Provide the necessary shell commands aur Python snippet (using the Qdrant client) to run **`ingest_content.py`** (Task 5.3) aur uske baad Qdrant collection mein **point count** (kitne chunks store hue) ko verify karein. Yeh confirm karega ke data ingestion successfull hai.

2.  **RAG Backend Search Test (Isolation):** Provide a Python snippet ya FastAPI test client code. Is code mein:
    * Ek sample query (maslan, 'What is the role of ZMP in bipedal locomotion?') ko hardcode karein.
    * **Directly** `perform_vector_search` function (Task 5.5 se) ko call karein.
    * Output mein **retrieved chunks ka raw text aur metadata** display karein. (Humein sirf retrieval test karna hai, LLM answer abhi zaroori nahi.) Yeh confirm karega ke search sahi context la raha hai.

3.  **Full Stack Connectivity Test (Browser Console):** Docusaurus frontend mein console log check karne ke liye **step-by-step instructions** generate karein. Jab user Chatbot UI (Task 5.4) se general ya contextual query karta hai, toh browser ke **Network tab** mein kya check karna chahiye:
    * Sahi FastAPI endpoint (`/api/query/general` or `/api/query/contextual`) call ho raha hai ya nahi?
    * Request body mein data (user query, selected text) sahi format mein bheja ja raha hai ya nahi?
    * Response status code (e.g., 200 OK) kya hai?

In testing steps aur code se hum project ke core functionalities ko validate kar saken ge."

## RESPONSE_TEXT

Successfully implemented comprehensive testing suite for the Physical AI & Humanoid Robotics RAG system:

1. **Ingestion Test Utility**: Created `backend/src/core_system_test.py` and `backend/src/validate_core_system.py` that:
   - Run the `ingest_content.py` script with sample content
   - Verify Qdrant collection point count after ingestion
   - Test the complete ingestion pipeline with verification
   - Clean up test data after validation
   - Include proper error handling and reporting

2. **RAG Backend Search Test (Isolation)**: Created `backend/src/rag_search_test.py` that:
   - Tests the sample query "What is the role of ZMP in bipedal locomotion?" directly against the `perform_vector_search` function
   - Displays retrieved chunks with raw text and metadata as requested
   - Includes multiple sample queries for comprehensive testing
   - Provides detailed output of search results including scores and content
   - Tests both single and multiple query scenarios

3. **Full Stack Connectivity Test**: Created `docs/test-instructions/full-stack-connectivity-test.md` with:
   - Step-by-step instructions for testing general query functionality
   - Step-by-step instructions for testing contextual query functionality
   - Details on checking the Network tab for proper endpoint calls
   - Information on verifying request bodies and response formats
   - Expected status codes (200 OK) and troubleshooting steps
   - Console error checking and common issue resolution

The implementation includes a comprehensive validation script (`backend/src/validate_core_system.py`) that tests all core system functionalities in sequence, providing a complete validation report. The test suite ensures that data ingestion, search functionality, and full-stack connectivity all work as expected, with proper error handling and cleanup procedures.