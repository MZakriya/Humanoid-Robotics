# Project Launch Instructions

Complete guide to launching the Physical AI & Humanoid Robotics RAG system.

## Prerequisites

- Python 3.8+ installed
- Node.js and npm/yarn installed
- Git installed
- Access to Qdrant Cloud (or local instance running)
- Access to OpenAI API (or alternative LLM service)

## Directory Structure

```
physical-ai-humanoid-robotics/
├── backend/
│   ├── src/
│   │   ├── main.py
│   │   ├── ingest_content.py
│   │   └── config.py
│   └── requirements.txt
├── docs/
│   ├── module1-embodied-intelligence/
│   ├── module2-ros2-fundamentals/
│   └── ...
├── src/
│   ├── components/
│   ├── contexts/
│   └── theme/
├── .env
└── package.json
```

## 1. Backend Environment Setup

### Create and Activate Virtual Environment

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Upgrade pip
python -m pip install --upgrade pip
```

### Install Dependencies

```bash
# Install required Python packages
pip install -r requirements.txt

# If requirements.txt doesn't exist, install the core dependencies:
pip install fastapi uvicorn qdrant-client python-dotenv sentence-transformers openai pydantic transformers torch psycopg2-binary sqlalchemy asyncpg
```

### Set Up Environment Variables

Create or update the `.env` file in the project root with the following variables:

```env
# FastAPI Settings
FASTAPI_HOST=0.0.0.0
FASTAPI_PORT=8000
API_SECRET_KEY=your-secret-key-here

# Vector Database (Qdrant)
QDRANT_URL=https://your-cluster.xxxx.us-east-1.aws.cloud.qdrant.io
QDRANT_API_KEY=your-qdrant-api-key
QDRANT_COLLECTION_NAME=humanoid_text_chunks

# LLM Service (OpenAI)
OPENAI_API_KEY=your-openai-api-key
EMBEDDING_MODEL_NAME=all-MiniLM-L6-v2

# Postgres (Neon) - for user profiles/auth data
NEON_PG_URL=postgresql://username:password@ep-xxx.us-east-1.aws.neon.tech/dbname?sslmode=require

# Better Auth (Bonus 4.0)
BETTER_AUTH_CLIENT_ID=your-better-auth-client-id
BETTER_AUTH_SECRET=your-better-auth-secret

# Development settings
DEBUG=true
LOG_LEVEL=INFO

# Application settings
MAX_CONTENT_LENGTH=10485760  # 10MB in bytes
```

### Run the FastAPI Application

```bash
# From the backend directory
cd src
python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

Or using the config values:

```bash
# From the backend directory
cd src
python -c "
from main import app
import uvicorn
from config import config
uvicorn.run(app, host=config.FASTAPI_HOST, port=config.FASTAPI_PORT)
"
```

## 2. Frontend Start-up

### Install Frontend Dependencies

```bash
# From the project root
npm install
# or
yarn install
```

### Launch Docusaurus Development Server

```bash
# From the project root
npm run start
# or
yarn start
```

This will start the Docusaurus development server at `http://localhost:3000`.

## 3. Content Ingestion (Pre-Requisite)

Before testing the RAG chatbot, you must populate the Qdrant database with textbook content:

### Method 1: Using Admin Endpoint

```bash
# After starting the backend server, call the admin endpoint:
curl -X POST "http://localhost:8000/admin/trigger_ingestion?source_path=docs&collection_name=humanoid_text_chunks"
```

### Method 2: Direct Script Execution

```bash
# From the backend/src directory
cd backend/src

# Run the ingestion script directly
python ingest_content.py --source ../docs --collection humanoid_text_chunks
```

### Method 3: Using the FastAPI Endpoint

You can also trigger ingestion through the admin endpoint programmatically:

```bash
# Trigger ingestion via POST request
curl -X POST "http://localhost:8000/admin/trigger_ingestion" \
  -H "Content-Type: application/json" \
  -d '{
    "source_path": "docs",
    "collection_name": "humanoid_text_chunks"
  }'
```

## 4. Final Execution Layout

### Concurrent Terminal Setup

You need to run the backend and frontend servers concurrently in separate terminals:

**Terminal 1 - Backend Server:**
```bash
cd backend
source venv/bin/activate  # or venv\Scripts\activate on Windows
cd src
python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

**Terminal 2 - Frontend Server:**
```bash
# From project root
npm run start
```

### Alternative: Using a Process Manager

You can use tools like `tmux`, `screen`, or a process manager like `concurrently`:

#### Using concurrently:

```bash
# Install concurrently globally (if not already installed)
npm install -g concurrently

# From project root, run both servers:
concurrently "cd backend && source venv/bin/activate && cd src && python -m uvicorn main:app --host 0.0.0.0 --port 8000" "npm run start"
```

#### Using a script file:

Create a `launch.sh` script:

```bash
#!/bin/bash

# Start backend in background
echo "Starting backend server..."
cd backend
source venv/bin/activate
cd src &
python -m uvicorn main:app --host 0.0.0.0 --port 8000 > backend.log 2>&1 &

BACKEND_PID=$!

# Start frontend in background
echo "Starting frontend server..."
cd ../..  # Back to project root
npm run start > frontend.log 2>&1 &

FRONTEND_PID=$!

# Cleanup function
cleanup() {
    echo "Shutting down servers..."
    kill $BACKEND_PID $FRONTEND_PID
    exit 0
}

trap cleanup SIGINT

# Wait for processes
wait $BACKEND_PID $FRONTEND_PID
```

## 5. Testing the Full Stack

### Before Testing

1. Ensure both backend and frontend servers are running
2. Verify content has been ingested into Qdrant
3. Confirm API endpoints are accessible

### Testing Steps

1. **Backend Health Check:**
   - Visit `http://localhost:8000/health` to verify backend status
   - Check Qdrant connection and collection status

2. **Content Availability:**
   - Verify that the Qdrant collection has content
   - Test the ingestion endpoint if needed

3. **Frontend Functionality:**
   - Visit `http://localhost:3000` to access the Docusaurus site
   - Test the RAG chatbot functionality
   - Verify personalization features if authenticated

4. **API Integration:**
   - Test the `/api/query/general` endpoint
   - Test the `/api/query/contextual` endpoint
   - Verify the `/api/content/personalize` endpoint

## 6. Troubleshooting

### Common Issues

1. **Port Already in Use:**
   - Change the port in `.env` file
   - Kill existing processes using the port

2. **Dependency Installation Issues:**
   - Ensure Python version is compatible
   - Check for OS-specific installation requirements

3. **Qdrant Connection Issues:**
   - Verify QDRANT_URL and QDRANT_API_KEY in `.env`
   - Ensure Qdrant server is running

4. **OpenAI API Issues:**
   - Verify OPENAI_API_KEY in `.env`
   - Check API quota and permissions

### Useful Commands

```bash
# Check if backend is running
curl http://localhost:8000/health

# Check if frontend is running
curl http://localhost:3000

# View backend logs
tail -f backend.log

# View frontend logs
tail -f frontend.log

# Kill processes on specific ports
# Windows: netstat -ano | findstr :8000, then taskkill /PID <pid> /F
# Linux/Mac: lsof -i :8000, then kill -9 <pid>
```

## 7. Production Deployment Notes

For production deployment:

1. Use environment variables for sensitive data
2. Implement proper SSL certificates
3. Set up a reverse proxy (nginx, Apache)
4. Configure proper logging and monitoring
5. Set DEBUG=false in production
6. Use a proper WSGI server like Gunicorn for production
