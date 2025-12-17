---
id: 1
title: "System Startup Instructions"
stage: "general"
date: "2025-12-08"
model: "Claude Sonnet 4.5"
surface: "agent"
feature: "none"
branch: "master"
user: "user"
command: "/sp.implement"
labels: ["startup", "instructions", "deployment"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files: []
tests: []
---

# System Startup Instructions for Physical AI & Humanoid Robotics RAG System

## User Input
```
"The core project is implemented. We need the final set of instructions and commands to launch the entire system for testing (Task 5.10).

**Task 5.12: Project Start-up and Environment Initialization**

1.  **Backend Environment Setup (Consolidated):** Provide the full sequence of shell commands necessary to set up the Python environment and launch the FastAPI backend. This must include:
    * Creating and activating a virtual environment (e.g., using `python -m venv`).
    * Installing all necessary Python dependencies (e.g., `pip install -r requirements.txt`, assuming this file contains `fastapi`, `uvicorn`, `qdrant-client`, `python-dotenv`, `sentence-transformers`, etc.).
    * The command to run the FastAPI application using Uvicorn, referencing the host and port defined in the `.env` file (Task 5.8), ensuring the application starts correctly.

2.  **Frontend Start-up:** Provide the necessary NPM/Yarn command to launch the Docusaurus frontend development server.

3.  **Ingestion Command (Pre-Requisite):** Explicitly provide the command needed to run **`ingest_content.py`** (from Task 5.3) *before* testing the RAG chatbot, ensuring the Qdrant database is populated with the textbook content.

4.  **Final Execution Layout:** Present the necessary steps and commands clearly, indicating that the Backend and Frontend commands must run **concurrently** in separate terminal windows for the full stack to function."
```

## Response Summary
Provided comprehensive startup instructions for the Physical AI & Humanoid Robotics RAG system, including:

1. Backend environment setup with virtual environment creation and dependency installation
2. Environment variable configuration for OpenAI and Qdrant
3. Commands to run the FastAPI application with Uvicorn
4. Frontend startup instructions for Docusaurus
5. Content ingestion command to populate the Qdrant database
6. Final execution layout showing concurrent terminal requirements
7. Available API endpoints and testing instructions

The system requires concurrent operation of backend (FastAPI) and frontend (Docusaurus) servers, with content ingestion completed before testing RAG functionality.

## Outcome
Successfully provided complete system startup instructions for the RAG system implementation, enabling full-stack operation with both backend API and frontend documentation site.