---
id: 11
title: "RAG Implementation"
stage: red
date_iso: "2025-12-07"
surface: "agent"
model: "Claude Sonnet 4.5"
feature: "content-spec"
branch: "1-content-spec"
user: "user"
command: "/sp.implement"
labels: ["implementation", "rag", "retrieval", "generation", "qdrant", "openai"]
links:
  spec: "specs/1-content-spec/spec.md"
  plan: "specs/1-content-spec/plan.md"
  tasks: "specs/1-content-spec/tasks.md"
  ticket: null
  adr: null
  pr: null
files_yaml:
  - "backend/requirements.txt"
  - "backend/src/main.py"
  - "backend/.env.example"
  - "backend/README.md"
tests_yaml: []
---

# RAG Implementation

## User Input

```
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
```

## Response Summary

Successfully implemented the core Retrieval-Augmented Generation (RAG) logic as requested:

### Task 5.5: Implement Core RAG Search Logic

1. **Dependencies:**
   - Added OpenAI library to requirements.txt
   - Initialized SentenceTransformer model globally in main.py
   - Configured OpenAI API with environment variable for API key
   - Added Pydantic models for API request validation

2. **Vector Search Function (`perform_vector_search`):**
   - Implemented asynchronous function to handle vector search
   - Uses the same SentenceTransformer model (`all-MiniLM-L6-v2`) as ingestion
   - Embeds query text and performs search in 'humanoid_text_chunks' collection
   - Retrieves top 5 results by default with text and metadata
   - Includes proper error handling and logging

3. **LLM Augmentation Function (`generate_rag_answer`):**
   - Implemented asynchronous function to generate answers from retrieved context
   - Constructs expert instructor prompt with specific instructions
   - Instructs LLM to use ONLY the provided context and state if answer is not found
   - Uses OpenAI's ChatCompletion API with gpt-3.5-turbo model
   - Includes temperature and token limits for consistent responses

4. **API Endpoint - General Query (`/api/query/general`):**
   - POST endpoint accepting GeneralQueryRequest with query text
   - Calls perform_vector_search to find relevant context
   - Calls generate_rag_answer to provide the response
   - Returns answer with sources and context type

5. **API Endpoint - Contextual Query (`/api/query/contextual`):**
   - POST endpoint accepting ContextualQueryRequest with user query and selected text
   - Combines inputs into a single search query
   - Calls perform_vector_search and generate_rag_answer
   - Returns answer with original inputs, combined query, sources, and context type

6. **Additional Features Implemented:**
   - Proper error handling with HTTPException for API failures
   - Logging for debugging and monitoring
   - Comprehensive documentation and type hints
   - Updated environment configuration with OpenAI API key
   - Updated documentation in README.md

## Outcome

The core RAG system is now fully implemented and ready for integration with the Docusaurus frontend. The system can handle both general queries and contextual queries where users can select text and ask questions about it. The implementation follows best practices for API development and includes proper error handling, logging, and documentation.

## Evaluation

The implementation successfully addresses all requirements from the user input, including the dependencies, vector search function with embedding and Qdrant search, LLM augmentation function with proper prompting, and both API endpoints for general and contextual queries. The RAG system is now complete and ready for frontend integration.