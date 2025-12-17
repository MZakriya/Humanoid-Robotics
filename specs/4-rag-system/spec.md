# Feature Specification: Core RAG Search Logic Implementation

**Feature Branch**: `4-rag-system`
**Created**: 2025-12-07
**Status**: Draft
**Input**: User description: "Implement the core Retrieval-Augmented Generation (RAG) logic within the existing FastAPI application (`main.py`).

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

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Student Using General RAG Queries (Priority: P1)

Students need to ask general questions about Physical AI and Humanoid Robotics concepts and receive accurate, contextually relevant answers based on the educational content.

**Why this priority**: This is the core functionality that enables students to learn through interactive questioning with the AI system.

**Independent Test**: Students can submit general questions about robotics concepts and receive accurate answers with proper source attribution.

**Acceptance Scenarios**:

1. **Given** a student has a question about a robotics concept, **When** they submit a general query to the RAG system, **Then** they receive a comprehensive answer based on the relevant educational content
2. **Given** a student's query cannot be answered from the available content, **When** they submit the query, **Then** the system clearly indicates that the answer is not available in the provided context

---

### User Story 2 - Student Using Contextual RAG Queries (Priority: P1)

Students need to ask specific questions about selected text within the educational content and receive explanations that are directly related to the selected context.

**Why this priority**: This enables contextual learning where students can get immediate clarification on specific content they're reading.

**Independent Test**: Students can select text, ask related questions, and receive answers that are specifically relevant to the selected context.

**Acceptance Scenarios**:

1. **Given** a student has selected text in the educational content, **When** they submit a contextual query about that text, **Then** they receive an answer based on both the selected text and the broader knowledge base
2. **Given** a student selects text and asks a related question, **When** the system processes the query, **Then** the answer addresses the relationship between the selected text and the user's question

---

### User Story 3 - Developer Integrating RAG System (Priority: P2)

Developers need to understand and work with the implemented RAG functionality to integrate it with the frontend and maintain the backend system.

**Why this priority**: The implementation must be maintainable and well-documented for future development work.

**Independent Test**: Developers can understand the RAG implementation and extend its functionality as needed.

**Acceptance Scenarios**:

1. **Given** a developer needs to integrate the RAG endpoints with the frontend, **When** they review the API documentation, **Then** they can successfully connect the frontend components to the backend endpoints
2. **Given** a developer needs to modify the RAG functionality, **When** they examine the code, **Then** they can understand the vector search, LLM augmentation, and API endpoint implementations

---

## Edge Cases

- What happens when the vector database is temporarily unavailable?
- How does the system handle very long user queries that exceed LLM token limits?
- What happens when no relevant content is found for a user's query?
- How does the system handle concurrent requests to the RAG endpoints?
- What happens when the LLM service is temporarily unavailable?

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST provide vector search functionality using Sentence Transformer embeddings and Qdrant database
- **FR-002**: System MUST implement LLM augmentation using an expert Physical AI and Robotics instructor persona
- **FR-003**: System MUST restrict LLM responses to only use information from the retrieved context
- **FR-004**: System MUST provide a general query endpoint at `/api/query/general` that accepts user queries and returns RAG-enhanced answers
- **FR-005**: System MUST provide a contextual query endpoint at `/api/query/contextual` that accepts user queries and selected text
- **FR-006**: System MUST use the `all-MiniLM-L6-v2` Sentence Transformer model for query embedding
- **FR-007**: System MUST connect to the 'humanoid_text_chunks' Qdrant collection for vector search
- **FR-008**: System MUST return the top 5 most relevant document chunks by default in vector search
- **FR-009**: System MUST clearly indicate when an answer cannot be found in the provided context
- **FR-010**: System MUST format search results to include both raw text and metadata for LLM processing

### Key Entities *(include if feature involves data)*

- **QueryText**: User's input text to be embedded and searched in the vector database
- **RetrievedContext**: List of document chunks with text content and metadata retrieved from Qdrant
- **RAGResponse**: Final answer generated by the LLM with source attribution
- **SearchResult**: Individual result from Qdrant containing text, metadata, and similarity score
- **APIRequest**: Request object containing query parameters for the RAG endpoints

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: General query endpoint responds with relevant answers within 10 seconds for 95% of requests
- **SC-002**: Contextual query endpoint responds with contextually relevant answers within 10 seconds for 95% of requests
- **SC-003**: Vector search returns relevant content for 85% of queries based on human evaluation
- **SC-004**: LLM responses are based solely on retrieved context without hallucination for 90% of queries
- **SC-005**: System properly indicates when answers cannot be found in the provided context for 100% of such cases
- **SC-006**: API endpoints handle 50 concurrent requests without performance degradation
- **SC-007**: LLM augmentation function properly formats prompts to ensure expert instructor persona
- **SC-008**: Vector search function successfully retrieves relevant content with proper metadata for downstream processing