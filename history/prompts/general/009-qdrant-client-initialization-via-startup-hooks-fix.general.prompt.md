---
id: "009"
title: "Qdrant Client Initialization via Startup Hooks Fix"
stage: "general"
date_iso: "2025-12-14"
surface: "agent"
model: "claude-sonnet-4-5-20250929"
feature: "none"
branch: "001-robotics-textbook"
user: "user"
command: "Task 5.46: Implement Qdrant Client Initialization via Startup/Shutdown Hooks"
labels:
  - "backend"
  - "qdrant"
  - "api"
  - "startup-hooks"
  - "fix"
links:
  SPEC: "null"
  TICKET: "null"
  ADR: "null"
  PR: "null"
files_yaml:
  - "D:\\humanoid_robotics_ai\\backend\\src\\main.py"
tests_yaml:
  - "None run yet"
---

# Qdrant Client Initialization via Startup Hooks Fix

## Summary
Implemented Qdrant client initialization via FastAPI startup/shutdown hooks to move heavy initialization outside of request handling and prevent blocking operations during requests.

## Changes Made
1. Removed global Qdrant client variable
2. Added @app.on_event("startup") hook to initialize QdrantClient and store in app.state.qdrant_client
3. Added @app.on_event("shutdown") hook to cleanup Qdrant client
4. Updated perform_vector_search function to accept Request object and fetch client from app.state
5. Modified all API endpoints to accept Request object and pass it to perform_vector_search
6. Updated create_collection and health_check endpoints to use app.state.qdrant_client
7. Removed dependency injection approach in favor of app state approach

## Technical Details
- Qdrant client now initialized during app startup via startup_event()
- Client stored in app.state.qdrant_client for request-time access
- All Qdrant operations fetch client from request.app.state.qdrant_client
- Maintained run_in_threadpool for synchronous operations
- Removed Depends(get_qdrant_client) dependency injection

## Outcome
Qdrant client initialization moved to startup phase, preventing blocking operations during request handling.

## Original Prompt
The FastAPI server is hanging silently on the first RAG request without generating an error log, indicating a hidden, persistent synchronous blocking operation, most likely related to the final initialization or access of the Qdrant Client or the Embedding Model.

**Task 5.46: Implement Qdrant Client Initialization via Startup/Shutdown Hooks**

1.  **Goal:** Generate the corrected content for `D:\humanoid_robotics_ai\backend\src\main.py`.
2.  **Fix Strategy:**
    * Remove the global declaration of the Qdrant Client.
    * Use FastAPI's **`@app.on_event("startup")`** hook to initialize the synchronous `QdrantClient` and store it in the app's state (`app.state.qdrant_client`).
    * Use **`@app.on_event("shutdown")`** hook to close the client.
    * Update the RAG endpoint (`/api/rag/chat`) to fetch the client from `request.app.state.qdrant_client`.
3.  **Output:** Provide the **full, corrected Python code** for `main.py` that moves the heavy client initialization into the dedicated FastAPI startup lifecycle, forcing the blocking operation to happen before the server accepts requests.

## Response Summary
Successfully implemented startup/shutdown hooks for Qdrant client, moving initialization outside of request handling to prevent blocking operations during requests.