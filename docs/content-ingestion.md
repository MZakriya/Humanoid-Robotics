# Content Ingestion Guide

Instructions for populating the Qdrant vector database with textbook content.

## Prerequisites

- Backend server running
- Qdrant database accessible
- Textbook content in `docs/` directory

## Methods to Run Content Ingestion

### Method 1: Admin Endpoint (Recommended)

Once the backend server is running, trigger content ingestion via the admin endpoint:

```bash
# Using curl
curl -X POST "http://localhost:8000/admin/trigger_ingestion?source_path=docs&collection_name=humanoid_text_chunks"

# Using Python requests
import requests

response = requests.post(
    "http://localhost:8000/admin/trigger_ingestion",
    json={
        "source_path": "docs",
        "collection_name": "humanoid_text_chunks"
    }
)

print(response.json())
```

### Method 2: Direct Script Execution

Run the ingestion script directly from the command line:

```bash
# From backend/src directory
cd backend/src

# Basic usage
python ingest_content.py --source ../docs --collection humanoid_text_chunks

# With specific options
python ingest_content.py \
  --source ../docs \
  --collection humanoid_text_chunks \
  --qdrant-url "https://your-cluster.xxxx.us-east-1.aws.cloud.qdrant.io" \
  --qdrant-api-key "your-qdrant-api-key"
```

### Method 3: Using Python API

Import and use the ContentIngestor class directly in Python:

```python
from backend.src.ingest_content import ContentIngestor

# Initialize the ingestor
ingestor = ContentIngestor()

# Process content from docs directory
total_chunks = ingestor.process_content(
    source_path="../docs",
    collection_name="humanoid_text_chunks"
)

print(f"Ingested {total_chunks} chunks into Qdrant")
```

## Ingestion Process

The content ingestion process includes:

1. **File Discovery**: Recursively finds all Markdown files in the source directory
2. **Text Extraction**: Reads content from each Markdown file
3. **Content Chunking**: Splits content into semantically meaningful chunks
4. **Embedding**: Converts each chunk to vector embeddings using Sentence Transformers
5. **Storage**: Stores embeddings in Qdrant with metadata

## Configuration Options

The ingestion process can be customized with:

- **Chunk Size**: Default 800 characters
- **Chunk Overlap**: Default 80 characters
- **Embedding Model**: Default `all-MiniLM-L6-v2`
- **Qdrant Collection**: Default `humanoid_text_chunks`

## Verification

After ingestion, verify the content is available:

```bash
# Check collection status
curl http://localhost:8000/health

# Test vector search with a sample query
curl -X POST "http://localhost:8000/api/query/general" \
  -H "Content-Type: application/json" \
  -d '{"query": "What is forward kinematics?"}'
```

## Troubleshooting

### Common Issues

1. **Qdrant Connection Failure**:
   - Verify QDRANT_URL and QDRANT_API_KEY in `.env`
   - Check that Qdrant server is accessible

2. **File Not Found Errors**:
   - Verify the source path exists
   - Check that the directory contains Markdown files

3. **Memory Issues**:
   - Reduce chunk size for large documents
   - Process content in smaller batches

### Monitoring

- Monitor the ingestion process for progress updates
- Check Qdrant dashboard for collection statistics
- Review application logs for errors
