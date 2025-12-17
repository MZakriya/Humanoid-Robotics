from fastapi import FastAPI, HTTPException, BackgroundTasks, Request
from qdrant_client import QdrantClient
from qdrant_client.http import models
from qdrant_client.http.models import Distance, VectorParams
import os
import subprocess
import sys
import logging
from typing import List, Dict, Any
# Import configuration
from .config import config

# Optional database imports for Neon Postgres (placeholder)
try:
    import asyncpg
    from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
    from sqlalchemy.orm import sessionmaker
    from sqlalchemy import Column, String, DateTime, create_engine
    from sqlalchemy.ext.declarative import declarative_base
    from sqlalchemy.sql import func
    DB_AVAILABLE = True
except ImportError:
    # If database libraries are not available, use placeholder functionality
    DB_AVAILABLE = False
    logging.warning("Database libraries not available. Using placeholder functionality for user profiles.")

# Initialize global components
# Using a mock instead of SentenceTransformer
class MockEmbeddingModel:
    def encode(self, texts):
        # Return mock embeddings - a simple list of zeros for each text
        return [[0.0] * 768 for _ in texts]

embedding_model = MockEmbeddingModel()

# Mock Google Generative AI
class MockGenerativeModel:
    def __init__(self, model_name):
        self.model_name = model_name

    def generate_content(self, prompt, generation_config=None):
        class MockResponse:
            def __init__(self):
                self.text = "This is a mock response from the AI model based on the provided context."

        return MockResponse()

class MockGenai:
    @staticmethod
    def configure(api_key):
        pass

    @staticmethod
    def GenerativeModel(model_name):
        return MockGenerativeModel(model_name)

# Use mock instead of actual google.generativeai
import sys
class MockGenaiModule:
    @staticmethod
    def configure(api_key):
        pass

    @staticmethod
    def GenerativeModel(model_name):
        return MockGenerativeModel(model_name)

# Add the mock to sys.modules to prevent import errors
sys.modules['google.generativeai'] = MockGenaiModule()
import google.generativeai as genai

# Configure Google Generative AI (mock)
genai.configure(api_key=config.GEMINI_API_KEY)

# Data models for API requests
from pydantic import BaseModel
import json
import uuid
from datetime import datetime

class GeneralQueryRequest(BaseModel):
    query: str

class ContextualQueryRequest(BaseModel):
    user_query: str
    selected_text: str

# Data models for user authentication and profile
class UserRegistrationRequest(BaseModel):
    userId: str
    softwareBackground: str
    hardwareExperience: str

class UserProfileResponse(BaseModel):
    message: str
    userId: str
    profileId: str

class UserAuthRequest(BaseModel):
    email: str
    password: str

class UserAuthResponse(BaseModel):
    message: str
    userId: str
    sessionId: str

app = FastAPI(
    title="Physical AI RAG Backend",
    description="Backend API for the Physical AI & Humanoid Robotics Textbook RAG system",
    version="1.0.0"
)

def get_qdrant_client():
    """
    Initialize and return Qdrant client using configuration
    """
    qdrant_url = config.QDRANT_URL
    qdrant_api_key = config.QDRANT_API_KEY

    if not qdrant_url or "your-cluster" in qdrant_url:
        # For local development, use local Qdrant instance
        client = QdrantClient(host="localhost", port=6333)
    else:
        # For production, use Qdrant Cloud
        client = QdrantClient(
            url=qdrant_url,
            api_key=qdrant_api_key,
            prefer_grpc=False  # Set to True in production for better performance
        )

    return client

async def perform_vector_search(query_text: str, top_k: int = 5):
    """
    Perform vector search in Qdrant to find relevant document chunks.
    This is a mock implementation that returns mock results.
    """
    try:
        # Mock results since we don't have actual embeddings
        mock_results = [
            {
                "text": f"Mock result for query: {query_text} - This is a simulated search result.",
                "metadata": {"source": "mock_document.md", "page": 1},
                "score": 0.9
            }
        ]
        return mock_results

    except Exception as e:
        logging.error(f"Error performing vector search: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Vector search failed: {str(e)}")

async def generate_rag_answer(user_query: str, retrieved_context: list):
    """
    Generate an answer using the retrieved context and LLM.
    This is a mock implementation that returns a simulated response.
    """
    try:
        # Construct the context string from retrieved chunks
        context_text = "\n\n".join([chunk["text"] for chunk in retrieved_context])

        # If no context is found, inform the user
        if not context_text.strip():
            return "I couldn't find any relevant information in the provided context to answer your question."

        # Construct the prompt for the LLM
        prompt = f"""
        You are an expert instructor in Physical AI and Robotics. Answer the user's question based ONLY on the provided context.

        Context:
        {context_text}

        User's question: {user_query}

        Instructions:
        - Use ONLY the provided context to answer the question
        - If the answer cannot be found in the provided context, clearly state this
        - Provide a comprehensive, well-structured response
        - Reference the relevant parts of the context where appropriate
        """

        # Initialize the mock model
        model = genai.GenerativeModel('gemini-2.5-flash')

        # Generate content using mock
        response = model.generate_content(
            prompt,
            generation_config={
                "temperature": 0.3,  # Lower temperature for more consistent answers
            }
        )

        # Extract and return the answer
        answer = response.text.strip()
        return answer

    except Exception as e:
        logging.error(f"Error generating RAG answer: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Answer generation failed: {str(e)}")

@app.post("/api/query/general")
async def query_general(request: GeneralQueryRequest):
    """
    Handle general queries without specific context.
    """
    try:
        # Perform vector search to find relevant context
        retrieved_context = await perform_vector_search(request.query)

        # Generate answer using the retrieved context
        answer = await generate_rag_answer(request.query, retrieved_context)

        return {
            "query": request.query,
            "answer": answer,
            "sources": [chunk["metadata"] for chunk in retrieved_context],
            "context_type": "general"
        }

    except Exception as e:
        logging.error(f"Error processing general query: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Query processing failed: {str(e)}")

@app.post("/api/query/contextual")
async def query_contextual(request: ContextualQueryRequest):
    """
    Handle contextual queries where the user has selected specific text.
    """
    try:
        # Combine the selected text with the user query to form the search query
        combined_query = f"Explain the selected text: '{request.selected_text}' in the context of: {request.user_query}"

        # Perform vector search to find relevant context
        retrieved_context = await perform_vector_search(combined_query)

        # Generate answer using the retrieved context
        answer = await generate_rag_answer(combined_query, retrieved_context)

        return {
            "user_query": request.user_query,
            "selected_text": request.selected_text,
            "combined_query": combined_query,
            "answer": answer,
            "sources": [chunk["metadata"] for chunk in retrieved_context],
            "context_type": "contextual"
        }

    except Exception as e:
        logging.error(f"Error processing contextual query: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Contextual query processing failed: {str(e)}")

@app.get("/")
async def root():
    """
    Root endpoint to check if the backend is operational
    """
    return {"message": "Physical AI RAG Backend Operational - Using Mock Implementation"}

@app.post("/create_collection")
async def create_collection(collection_name: str = "humanoid_text_chunks", vector_size: int = 768):
    """
    Create a placeholder Qdrant collection for storing text chunks
    with a standard vector size (768 for all-MiniLM-L6-v2 embedding model)
    """
    try:
        client = get_qdrant_client()

        # Check if collection already exists
        collections = client.get_collections()
        existing_collection_names = [collection.name for collection in collections.collections]

        if collection_name in existing_collection_names:
            return {
                "message": f"Collection '{collection_name}' already exists",
                "collection_name": collection_name,
                "vector_size": vector_size
            }

        # Create the collection with specified vector size
        client.create_collection(
            collection_name=collection_name,
            vectors_config=VectorParams(size=vector_size, distance=Distance.COSINE)
        )

        return {
            "message": f"Collection '{collection_name}' created successfully",
            "collection_name": collection_name,
            "vector_size": vector_size
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating collection: {str(e)}")

@app.get("/health")
async def health_check():
    """
    Health check endpoint to verify the backend and Qdrant connection
    """
    try:
        client = get_qdrant_client()
        # Try to get collections to verify connection
        collections = client.get_collections()
        return {
            "status": "healthy",
            "qdrant_connection": "successful",
            "total_collections": len(collections.collections)
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "qdrant_connection": "failed",
            "error": str(e)
        }

# Session handling endpoints (placeholder for Better Auth integration)
@app.get("/api/auth/session")
async def get_session(request: Request):
    """
    Check if user is authenticated and return session data.
    This is a placeholder for Better Auth session management.
    """
    # In a real implementation, this would verify the Better Auth session
    # For now, we'll simulate a mock session if a specific header is present
    auth_header = request.headers.get("authorization")

    if auth_header and auth_header.startswith("Bearer "):
        # In a real implementation, this would validate the JWT token with Better Auth
        # For now, we'll return mock user data
        return {
            "user": {
                "id": "mock-user-id",
                "email": "user@example.com",
                "name": "Test User"
            },
            "expiresAt": "2025-12-08T00:00:00Z"
        }
    else:
        # Return 401 if not authenticated
        raise HTTPException(
            status_code=401,
            detail="Not authenticated"
        )

@app.post("/api/auth/login")
async def login():
    """
    Login endpoint - placeholder for Better Auth integration.
    In a real implementation, this would redirect to Better Auth login page.
    """
    # This would normally redirect to Better Auth's login page
    # For now, we'll return a mock response
    return {
        "message": "Redirecting to login page",
        "loginUrl": "/login"  # This would be the Better Auth login URL
    }

@app.post("/api/auth/logout")
async def logout():
    """
    Logout endpoint - placeholder for Better Auth integration.
    """
    # In a real implementation, this would call Better Auth's logout API
    # For now, we'll just return a success message
    return {
        "message": "Logged out successfully"
    }

@app.get("/api/auth/me")
async def get_user_info(request: Request):
    """
    Get current user information if authenticated.
    """
    # Similar to session check, verify the user is authenticated
    auth_header = request.headers.get("authorization")

    if auth_header and auth_header.startswith("Bearer "):
        # In a real implementation, this would validate the JWT token with Better Auth
        # For now, we'll return mock user data
        return {
            "id": "mock-user-id",
            "email": "user@example.com",
            "name": "Test User",
            "isLoggedIn": True
        }
    else:
        raise HTTPException(
            status_code=401,
            detail="Not authenticated"
        )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=config.FASTAPI_HOST, port=config.FASTAPI_PORT)