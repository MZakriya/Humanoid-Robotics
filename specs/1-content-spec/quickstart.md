# Quickstart Guide: Physical AI & Humanoid Robotics Textbook & Platform

**Feature**: 1-content-spec
**Date**: 2025-12-07

## Getting Started

This guide will help you set up and run the Physical AI & Humanoid Robotics educational platform locally.

### Prerequisites

- Node.js (v18 or higher)
- Python (v3.11 or higher)
- Git
- Access to Neon Serverless Postgres (for backend)
- Access to Qdrant Cloud (for vector database)

### Setup Instructions

#### 1. Clone the Repository

```bash
git clone https://github.com/your-org/physical-ai-humanoid-robotics.git
cd physical-ai-humanoid-robotics
```

#### 2. Set up the Frontend (Docusaurus)

```bash
# Navigate to the project root
cd frontend  # or directly in the root if Docusaurus is in the root

# Install dependencies
npm install

# Create environment file
cp .env.example .env

# Update .env with your configuration
# (For frontend, this may include API endpoints)
```

#### 3. Set up the Backend (FastAPI)

```bash
# Navigate to the backend directory
cd backend

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create environment file
cp .env.example .env

# Update .env with your database configurations:
# NEON_DATABASE_URL=your_neon_connection_string
# QDRANT_URL=your_qdrant_cloud_url
# QDRANT_API_KEY=your_qdrant_api_key
```

#### 4. Environment Variables

Create `.env` files in both frontend and backend with the following variables:

**Backend (.env):**
```
NEON_DATABASE_URL=postgresql://username:password@ep-xxx.us-east-1.aws.neon.tech/dbname
QDRANT_URL=https://your-cluster.xxxx.us-east-1.aws.cloud.qdrant.io
QDRANT_API_KEY=your_qdrant_api_key
OPENAI_API_KEY=your_openai_api_key  # or other LLM provider key
```

#### 5. Run the Applications

**Frontend:**
```bash
cd frontend  # or project root if Docusaurus is there
npm start
```

**Backend:**
```bash
cd backend
uvicorn src.main:app --reload --port 8000
```

The frontend will be available at `http://localhost:3000` and the backend API at `http://localhost:8000`.

### Running the RAG System

1. First, ensure your backend is running
2. Ingest the educational content:
   ```bash
   # From backend directory
   python -m src.scripts.ingest_content
   ```
3. The RAG chatbot will be accessible through the frontend UI

### Development Workflow

1. **Content Development**: Add/edit content in the `docs/` directory following the module structure
2. **Backend Development**: Work in the `backend/` directory for RAG functionality
3. **Frontend Development**: Work in the `frontend/` directory for UI components
4. **Testing**: Run tests in both frontend and backend directories

### Deployment to GitHub Pages

1. Build the Docusaurus site:
   ```bash
   npm run build
   ```

2. The site will be built to the `build/` directory and automatically deployed via GitHub Actions when pushed to the main branch.

### API Endpoints

- `POST /api/chat/query` - Submit queries to the RAG chatbot
- `POST /api/chat/session` - Create a new chat session
- `POST /api/content/ingest` - Ingest content for RAG indexing

### Troubleshooting

- If you encounter issues with the vector database, ensure your Qdrant Cloud instance is properly configured
- For database connection issues, verify your Neon connection string is correct
- If the RAG queries are slow, check your embedding model and vector search configuration