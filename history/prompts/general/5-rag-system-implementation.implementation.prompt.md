---
id: 5
title: rag-system-implementation
stage: implementation
date: 2025-12-07
surface: agent
model: Claude Sonnet 4.5
feature: rag-system
branch: master
user: Claude
command: /sp.implement
labels: ["rag", "ai", "fastapi", "qdrant", "openai", "implementation"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - backend/src/main.py
  - specs/4-rag-system/spec.md
  - specs/4-rag-system/plan.md
  - specs/4-rag-system/tasks.md
  - backend/src/ingest_content.py
  - backend/requirements.txt
tests: []
outcome: "Successfully implemented core RAG search logic in FastAPI application with vector search, LLM augmentation, and both general and contextual query endpoints."
evaluation: "Implementation meets all requirements from the original task specification, including dependencies, vector search function, LLM augmentation function, and both API endpoints."
---

# RAG System Implementation

## PROMPT_TEXT

"This is the most critical task: implementing the core Retrieval-Augmented Generation (RAG) logic within the existing FastAPI application (`main.py`).

**Task 5.5: Implement Core RAG Search Logic**

1.  **Dependencies:** Ensure the necessary libraries for interacting with the chosen LLM (e.g., OpenAI, Claude API, or a locally run model) are defined and initialized in `main.py` (use placeholder API key variables).

2.  **Vector Search Function:** Create a reusable asynchronous function, `perform_vector_search(query_text: str, top_k: int = 5)`, that handles:
    * **Embedding the Query:** Uses the same Sentence Transformer model (`all-MiniLM-L6-v2`) used in Task 5.3 to embed the incoming `query_text`.
    * **Qdrant Search:** Connects to the 'humanoid\_text\_chunks' collection and performs a vector search to retrieve the top `top_k` similar document chunks.
    * **Result Formatting:** Extracts the raw text and metadata from the search results.

3.  **LLM Augmentation Function:** Create an asynchronous function, `generate_rag_answer(user_query: str, retrieved_context: list)`, that takes the user's query and the list of retrieved text chunks, constructs a high-quality, augmented prompt, and sends it to the LLM to get the final answer. The prompt must instruct the LLM to:
    * Act as an expert Physical AI and Robotics instructor.
    * Use **ONLY** the provided `retrieved_context` to answer the question.
    * Clearly state if the answer cannot be found in the provided context.

4.  **API Endpoint - General Query:** Implement a **POST endpoint** `/api/query/general` that:
    * Accepts the user's plain text query.
    * Calls `perform_vector_search` to find relevant context.
    * Calls `generate_rag_answer` to provide the response.

5.  **API Endpoint - Contextual Query:** Implement a **POST endpoint** `/api/query/contextual` that:
    * Accepts both the `user_query` (e.g., "Explain this concept") AND the `selected_text` (the text the user highlighted).
    * Combines the two inputs into a single search query (e.g., "Explain the selected text: [selected\_text] in the context of: [user\_query]").
    * Calls `perform_vector_search` and `generate_rag_answer`.

This task finalizes the RAG system, making it ready to be fully integrated with the Docusaurus frontend."

## RESPONSE_TEXT

Successfully implemented the core RAG search logic in the FastAPI application. The implementation includes:

1. **Dependencies**: All required libraries (FastAPI, Qdrant Client, Sentence Transformers, OpenAI) are properly defined in requirements.txt and initialized in main.py with placeholder API keys.

2. **Vector Search Function**: The `perform_vector_search(query_text: str, top_k: int = 5)` function successfully:
   - Embeds queries using the 'all-MiniLM-L6-v2' Sentence Transformer model
   - Connects to the 'humanoid_text_chunks' collection in Qdrant
   - Performs vector search to retrieve top-k similar document chunks
   - Formats results with raw text and metadata

3. **LLM Augmentation Function**: The `generate_rag_answer(user_query: str, retrieved_context: list)` function:
   - Constructs high-quality prompts for the LLM
   - Instructs the LLM to act as an expert Physical AI and Robotics instructor
   - Ensures the LLM uses ONLY the provided context
   - Clearly states when answers cannot be found in the context

4. **General Query API Endpoint**: The `/api/query/general` endpoint:
   - Accepts plain text queries from users
   - Calls vector search to find relevant context
   - Uses LLM augmentation to generate responses

5. **Contextual Query API Endpoint**: The `/api/query/contextual` endpoint:
   - Accepts both user queries and selected text
   - Combines inputs into a single search query
   - Processes with vector search and LLM augmentation

The implementation is complete and ready for integration with the Docusaurus frontend.