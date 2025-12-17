# System Deployment Layout

Complete overview of the Physical AI & Humanoid Robotics RAG system deployment architecture.

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                     CLIENT SIDE (Frontend)                      │
├─────────────────────────────────────────────────────────────────┤
│ • Docusaurus Documentation Site                                 │
│ • Chatbot UI Component                                          │
│ • Authentication Context                                        │
│ • Personalization Engine                                        │
│ • React Components                                              │
│ • Static Assets (CSS, JS, Images)                              │
└─────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼ HTTP Requests
┌─────────────────────────────────────────────────────────────────┐
│                     SERVER SIDE (Backend)                       │
├─────────────────────────────────────────────────────────────────┤
│ • FastAPI Application                                           │
│ • RAG Query Endpoints (/api/query/general, /api/query/contextual)│
│ • Content Personalization (/api/content/personalize)            │
│ • User Authentication (/api/auth/*)                             │
│ • User Profile Management (/user/*)                             │
│ • Admin Tools (/admin/*)                                        │
└─────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼ API Calls
┌─────────────────────────────────────────────────────────────────┐
│                   EXTERNAL SERVICES                             │
├─────────────────────────────────────────────────────────────────┤
│ • Qdrant Vector Database                                        │
│ • OpenAI API (or Alternative LLM)                               │
│ • Neon Postgres Database (User Profiles)                        │
│ • Better Auth (User Authentication)                             │
└─────────────────────────────────────────────────────────────────┘
```

## Execution Workflow

### 1. Development Environment

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   Backend   │    │   Frontend  │    │   Browser   │
│   Server    │    │   Server    │    │   Client    │
│ (Port 8000) │◄──►│ (Port 3000) │◄──►│ (User View) │
└─────────────┘    └─────────────┘    └─────────────┘
       │                   │                   │
       ▼                   ▼                   ▼
   FastAPI App         Docusaurus         React UI
   uvicorn:8000        dev-server:3000    Components
```

### 2. Production Environment

```
┌─────────────────────────────────────────────────────────────────┐
│                    REVERSE PROXY (nginx)                        │
├─────────────────────────────────────────────────────────────────┤
│ • SSL Termination                                               │
│ • Load Balancing (if multiple instances)                        │
│ • Static File Serving                                           │
│ • Port Forwarding (443 → 8000/3000)                            │
└─────────────────────────────────────────────────────────────────┘
                                    │
┌─────────────────────────────────────────────────────────────────┐
│                   APPLICATION SERVERS                           │
├─────────────────────────────────────────────────────────────────┤
│ ┌─────────────────┐    ┌─────────────────┐                     │
│ │   Backend App   │    │  Frontend App   │                     │
│ │    (Gunicorn)   │    │  (Static NGINX) │                     │
│ │   Port 8000     │    │   Port 3000     │                     │
│ └─────────────────┘    └─────────────────┘                     │
└─────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────┐
│                   DATABASE CLUSTERS                             │
├─────────────────────────────────────────────────────────────────┤
│ • Qdrant Vector Database Cluster                                │
│ • Neon Postgres Database                                        │
│ • Redis Cache (Optional)                                        │
└─────────────────────────────────────────────────────────────────┘
```

## Launch Sequence

### 1. Backend First Approach

```mermaid
graph TD
    A[Start Backend Server] --> B[Initialize FastAPI App]
    B --> C[Load Config from .env]
    C --> D[Connect to Qdrant]
    D --> E[Initialize Embedding Model]
    E --> F[Connect to Postgres]
    F --> G[Initialize Routes]
    G --> H[Start Uvicorn Server]
    H --> I[Backend Ready]

    I --> J[Start Frontend Server]
    J --> K[Initialize Docusaurus]
    K --> L[Load React Components]
    L --> M[Connect to Backend API]
    M --> N[Frontend Ready]

    N --> O[System Operational]
```

### 2. Concurrent Launch

For production environments, both servers can be launched concurrently:

```bash
# Using concurrently package
npx concurrently \
  "cd backend && python -m uvicorn src.main:app --host 0.0.0.0 --port 8000" \
  "cd . && npm run serve"

# Using systemd services
sudo systemctl start humanoid-robotics-backend
sudo systemctl start humanoid-robotics-frontend

# Using Docker Compose
docker-compose up --build
```

## Environment Variables

### Backend (.env)
```
FASTAPI_HOST=0.0.0.0
FASTAPI_PORT=8000
QDRANT_URL=https://cluster.xxxx.us-east-1.aws.cloud.qdrant.io
QDRANT_API_KEY=your-api-key
OPENAI_API_KEY=your-openai-key
NEON_PG_URL=postgresql://user:pass@ep-xxx.us-east-1.aws.neon.tech/db
BETTER_AUTH_CLIENT_ID=your-client-id
BETTER_AUTH_SECRET=your-secret
```

### Frontend (package.json or .env)
```
REACT_APP_API_URL=http://localhost:8000
REACT_APP_BETTER_AUTH_CLIENT_ID=your-client-id
REACT_APP_DEBUG_MODE=true
```

## Health Checks

### Backend Health Endpoint
```
GET /health
Response: {
  "status": "healthy",
  "qdrant_connection": "successful",
  "total_collections": 1,
  "postgres_connection": "successful"
}
```

### Frontend Health Check
```
GET /
Response: HTTP 200 with HTML content
```

## Monitoring Points

### Backend Metrics
- API Response Times
- Qdrant Connection Status
- Database Connection Pool
- Memory Usage
- Active Connections

### Frontend Metrics
- Page Load Times
- API Request Success Rate
- User Session Duration
- Chatbot Usage Statistics
- Error Rates

## Scaling Considerations

### Horizontal Scaling
- Multiple backend instances behind load balancer
- CDN for static frontend assets
- Database read replicas
- Redis for session sharing

### Vertical Scaling
- Larger VMs for embedding computations
- More RAM for model caching
- Faster CPUs for real-time processing

## Security Considerations

### API Protection
- Rate limiting on all endpoints
- Authentication for protected routes
- Input validation and sanitization
- HTTPS enforcement

### Data Protection
- Encryption at rest for databases
- API key rotation policies
- Secure session management
- Audit logging for sensitive operations
