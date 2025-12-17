# Implementation Plan: Core RAG Search Logic

**Branch**: `4-rag-system` | **Date**: 2025-12-07 | **Spec**: [specs/4-rag-system/spec.md](../spec.md)
**Input**: Feature specification from `/specs/4-rag-system/spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Implementation of the core Retrieval-Augmented Generation (RAG) logic within the existing FastAPI application. This includes vector search functionality using Sentence Transformers and Qdrant, LLM augmentation with OpenAI, and both general and contextual query API endpoints for the Physical AI & Humanoid Robotics educational platform.

## Technical Context

**Language/Version**: Python 3.11, FastAPI framework
**Primary Dependencies**: FastAPI, Qdrant Client, Sentence Transformers, OpenAI, LangChain
**Storage**: Qdrant Cloud for vector storage, OpenAI for LLM responses
**Testing**: Manual testing and validation of RAG functionality
**Target Platform**: Web-based RAG system integrated with Docusaurus frontend
**Performance Goals**: <10s response time for 95% of RAG queries, high accuracy in context retrieval
**Constraints**: Must use only retrieved context for answers, clearly indicate when answer is not available
**Scale/Scope**: Educational platform for students, educators, and practitioners in Physical AI and Robotics

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- **Docusaurus-First Documentation**: Ensure RAG system properly integrates with Docusaurus educational content
- **RAG-Based Intelligence Integration**: Verify that the backend services use FastAPI, Qdrant, and OpenAI as specified
- **Test-Driven Content Development**: Confirm that RAG functionality will work with educational content structure
- **Multi-Module Educational Coherence**: Ensure the RAG system maintains pedagogical consistency across all modules
- **Open Source Accessibility**: Verify that the RAG implementation is open source and properly documented
- **Technology Stack Compliance**: Confirm adherence to the mandated technology stack (FastAPI, Qdrant, OpenAI)

## Project Structure

### Documentation (this feature)

```text
specs/4-rag-system/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (/sp.plan command)
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
# Backend API
backend/src/
├── main.py              # FastAPI application with RAG endpoints
├── ingest_content.py    # Content ingestion script for Qdrant
├── models/              # Pydantic models for API requests
├── services/            # RAG service functions
└── api/                 # API route definitions

# Dependencies
backend/
├── requirements.txt     # Python dependencies
└── .env                 # Environment variables
```

**Structure Decision**: Single FastAPI application containing all RAG functionality with separate ingestion script for content processing.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| [e.g., 4th project] | [current need] | [why 3 projects insufficient] |
| [e.g., Repository pattern] | [specific problem] | [why direct DB access insufficient] |

## Project Roadmap

### Phase 1: Foundation & Structure
**Time Allocation**: 5 hours (1 day)

**Purpose**: Ensure all dependencies and infrastructure are properly configured

- [X] Verify Qdrant connection and 'humanoid_text_chunks' collection exists
- [X] Confirm OpenAI API key is properly configured
- [X] Verify Sentence Transformer model 'all-MiniLM-L6-v2' is available
- [X] Test basic FastAPI endpoints and health check

### Phase 2: Core RAG Implementation
**Time Allocation**: 15 hours (3 days)

**Purpose**: Implement the complete RAG pipeline functionality

- [X] Implement vector search function using Sentence Transformers and Qdrant
- [X] Implement LLM augmentation function with proper prompt engineering
- [X] Create general query endpoint `/api/query/general`
- [X] Create contextual query endpoint `/api/query/contextual`
- [X] Implement proper error handling and context validation
- [X] Add logging and monitoring for RAG operations
- [X] Test vector search accuracy and relevance

### Phase 3: Integration & Testing
**Time Allocation**: 10 hours (2 days)

**Purpose**: Validate the complete RAG system functionality

- [X] Test general query functionality with various robotics concepts
- [X] Test contextual query functionality with selected text
- [X] Validate that LLM only uses provided context for answers
- [X] Verify proper error handling when no context is found
- [X] Performance testing for response times
- [X] Integration testing with potential frontend components

### Phase 4: Documentation & Deployment
**Time Allocation**: 5 hours (1 day)

**Purpose**: Document and prepare for deployment

- [X] Document API endpoints with request/response examples
- [X] Create environment variable configuration guide
- [X] Document ingestion process for content updates
- [X] Prepare deployment configuration for production

**Total Time Allocation**: 35 hours (7 days) - focused on RAG implementation

## Dependencies & Execution Order

### Phase Dependencies
- **Phase 1** (Foundation): No dependencies - can start immediately
- **Phase 2** (Core RAG): Depends on Phase 1 completion - BLOCKS functionality
- **Phase 3** (Integration): Depends on Phase 2 completion - BLOCKS validation
- **Phase 4** (Documentation): Depends on all previous phases completion

### Parallel Opportunities
- API endpoint development can happen in parallel with service function implementation
- Testing can begin as soon as individual components are implemented
- Documentation can be created in parallel with implementation