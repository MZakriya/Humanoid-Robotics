# Physical AI RAG Backend

This is the backend service for the Physical AI & Humanoid Robotics Textbook RAG system, built with FastAPI and Qdrant.

## Overview

The RAG (Retrieval-Augmented Generation) backend provides:
- Vector storage and retrieval using Qdrant
- FastAPI endpoints for content ingestion and querying
- Integration with embedding models for semantic search
- RESTful API for frontend integration

## Prerequisites

- Python 3.11+
- Docker and Docker Compose (optional, for containerized deployment)
- Qdrant Cloud account (for production) or Docker for local development

## Setup

### Local Development

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create your environment file:
```bash
cp .env.example .env
```

4. Update `.env` with your Qdrant configuration:
   - For Qdrant Cloud: Set `QDRANT_URL` and `QDRANT_API_KEY`
   - For local development: Leave empty to use default localhost settings

5. Run the application:
```bash
python -m uvicorn src.main:app --reload --port 8000
```

### Docker Setup

1. Build and run with Docker Compose:
```bash
docker-compose up --build
```

The application will be available at `http://localhost:8000`

## API Endpoints

- `GET /` - Health check and status message
- `POST /create_collection` - Create a Qdrant collection for text chunks
- `GET /health` - Detailed health check with Qdrant connection status
- `POST /admin/trigger_ingestion` - Trigger content ingestion from docs directory (admin endpoint)
- `POST /api/query/general` - General query endpoint for RAG system
- `POST /api/query/contextual` - Contextual query endpoint for RAG system (with selected text)

## Configuration

- `QDRANT_URL`: URL for Qdrant Cloud instance (leave empty for local development)
- `QDRANT_API_KEY`: API key for Qdrant Cloud (not needed for local development)
- `EMBEDDING_MODEL`: Model used for generating embeddings (default: all-MiniLM-L6-v2)
- `VECTOR_SIZE`: Size of embedding vectors (default: 768)

## Content Ingestion

The system includes a content ingestion pipeline that processes Docusaurus markdown content:

1. **Text Chunking**: Content is split into overlapping chunks (800 chars with 80 char overlap)
2. **Embedding**: Text chunks are converted to embeddings using `all-MiniLM-L6-v2`
3. **Storage**: Embeddings are stored in Qdrant with metadata for retrieval

### Ingestion Script

The `src/ingest_content.py` script handles the entire ingestion process:
- Reads markdown files from the docs directory
- Chunks content appropriately
- Generates embeddings
- Stores in Qdrant with metadata

To run manually:
```bash
python src/ingest_content.py --source docs --collection humanoid_text_chunks
```

### Admin Endpoint

The `/admin/trigger_ingestion` endpoint allows triggering ingestion via API:
```bash
curl -X POST "http://localhost:8000/admin/trigger_ingestion?source_path=docs&collection_name=humanoid_text_chunks"
```

## RAG Query Endpoints

The system includes two main endpoints for querying the RAG system:

### General Query
- **Endpoint**: `POST /api/query/general`
- **Request Body**:
```json
{
  "query": "Your question here"
}
```
- **Response**: Answer based on the knowledge base

### Contextual Query
- **Endpoint**: `POST /api/query/contextual`
- **Request Body**:
```json
{
  "user_query": "Your question about the selected text",
  "selected_text": "The text that was selected by the user"
}
```
- **Response**: Answer based on both the selected text and user query

Both endpoints return the answer along with source information for transparency.

## Development

The main application code is in `src/main.py`. To add new endpoints:

1. Define the endpoint function with appropriate decorators
2. Add proper error handling
3. Include type hints for request/response models
4. Add documentation strings

## Testing

To run the application and test the endpoints:

1. Start the server: `python -m uvicorn src.main:app --reload --port 8000`
2. Test the root endpoint: `GET http://localhost:8000`
3. Test collection creation: `POST http://localhost:8000/create_collection`
4. Check health: `GET http://localhost:8000/health`

## Deployment

For production deployment:
1. Use the provided Dockerfile
2. Set up proper environment variables
3. Configure reverse proxy (e.g., nginx) if needed
4. Set up monitoring and logging