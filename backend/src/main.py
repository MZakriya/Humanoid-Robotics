from fastapi import FastAPI, HTTPException, BackgroundTasks, Request
from fastapi.middleware.cors import CORSMiddleware
from qdrant_client import QdrantClient
from starlette.concurrency import run_in_threadpool
from qdrant_client.http import models
from qdrant_client.http.models import Distance, VectorParams
import os
import subprocess
import sys
import logging
from typing import List, Dict, Any
from sentence_transformers import SentenceTransformer
from pydantic import BaseModel
import json
import uuid
from datetime import datetime
import google.generativeai as genai
import threading
import asyncio

# Import configuration
try:
    from .config import config
except ImportError:
    # Fallback for when running directly
    from config import config

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

# Global variables to hold the embedding model and qdrant client with thread safety
_embedding_model = None
_qdrant_client = None
_initialization_lock = threading.Lock()

# Configure Google Generative AI
genai.configure(api_key=config.GEMINI_API_KEY)

# Data models for API requests
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

# Add CORS middleware to allow cross-origin requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001", "http://localhost:3002", "http://localhost:3003", "http://127.0.0.1:3000", "http://127.0.0.1:3001", "http://127.0.0.1:3002", "http://127.0.0.1:3003", "*"],  # Allow Docusaurus and other local development origins
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],  # Explicitly include OPTIONS and other methods
    allow_headers=["*"],  # Allow all headers
)


def get_qdrant_client():
    """
    Thread-safe lazy initialization function for Qdrant client.
    Initializes the client only when first accessed, preventing blocking during startup.
    """
    global _qdrant_client
    if _qdrant_client is None:
        with _initialization_lock:
            if _qdrant_client is None:  # Double-check locking
                logging.info("Initializing Qdrant client (lazy initialization)...")
                qdrant_url = config.QDRANT_URL
                qdrant_api_key = config.QDRANT_API_KEY

                logging.info(f"Qdrant URL: {qdrant_url}")
                logging.info(f"Qdrant API Key present: {qdrant_api_key is not None}")

                if not qdrant_url or "your-cluster" in qdrant_url:
                    # For local development, use local Qdrant instance
                    logging.info("Using local Qdrant instance")
                    _qdrant_client = QdrantClient(host="localhost", port=6333)
                else:
                    # For production, use Qdrant Cloud
                    logging.info("Using Qdrant Cloud")
                    _qdrant_client = QdrantClient(
                        url=qdrant_url,
                        api_key=qdrant_api_key,
                        prefer_grpc=False  # Set to True in production for better performance
                    )
                logging.info("Qdrant client initialized successfully")
    return _qdrant_client

def get_embedding_model():
    """
    Get the embedding model instance (lazy initialization with thread safety)
    """
    global _embedding_model
    if _embedding_model is None:
        with _initialization_lock:
            if _embedding_model is None:  # Double-check locking
                logging.info("Initializing embedding model...")
                try:
                    _embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
                    logging.info("Embedding model initialized successfully")
                except Exception as e:
                    logging.error(f"Error initializing embedding model: {str(e)}", exc_info=True)
                    raise
    return _embedding_model

async def perform_vector_search(query_text: str, top_k: int = 5):
    """
    Perform vector search in Qdrant to find relevant document chunks.

    Args:
        query_text: The text to search for
        top_k: Number of top results to return (default: 5)

    Returns:
        List of search results with text and metadata
    """
    try:
        # Get the Qdrant client using thread-safe lazy initialization
        logging.info("Getting Qdrant client for vector search...")
        client = get_qdrant_client()
        logging.info("Qdrant client retrieved successfully")

        # Embed the query text using the same model used during ingestion
        logging.info("Getting embedding model...")
        embedding_model = get_embedding_model()
        logging.info("Encoding query text...")
        query_embedding = embedding_model.encode([query_text])[0].tolist()
        logging.info(f"Query embedding created with length: {len(query_embedding)}")

        # Perform the search in the 'humanoid_text_chunks' collection
        # Using the synchronous QdrantClient with run_in_threadpool to avoid blocking
        logging.info(f"Performing search in 'humanoid_text_chunks' collection with top_k={top_k}...")
        search_results = await run_in_threadpool(
            lambda: client.query_points(
                collection_name="humanoid_text_chunks",
                query=query_embedding,
                limit=top_k,
                with_payload=True  # Include the payload (text and metadata)
            )
        )
        logging.info(f"Search completed, found {len(search_results)} results")

        # Format the results - query_points returns QueryResponse with points
        # Extract the actual scored points from the response
        points = search_results.points if hasattr(search_results, 'points') else search_results
        formatted_results = []

        for point in points:
            # Each point should have id, payload, vector, and score
            text = ""
            metadata = {}
            score = 0

            # Extract payload data
            if hasattr(point, 'payload') and point.payload:
                text = point.payload.get("text", "")
                metadata = point.payload.get("metadata", {})
            elif hasattr(point, 'payload') and isinstance(point.payload, dict):
                text = point.payload.get("text", "")
                metadata = point.payload.get("metadata", {})

            # Extract score
            if hasattr(point, 'score'):
                score = point.score

            formatted_results.append({
                "text": text,
                "metadata": metadata,
                "score": score
            })

        logging.info(f"Formatted {len(formatted_results)} search results")
        return formatted_results

    except AttributeError as e:
        logging.error(f"AttributeError in vector search: {str(e)}")
        # This could happen if the method doesn't exist - provide a more specific error
        raise HTTPException(status_code=500, detail=f"Qdrant client method error: {str(e)}")
    except Exception as e:
        logging.error(f"Error performing vector search: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Vector search failed: {str(e)}")

async def generate_rag_answer(user_query: str, retrieved_context: list):
    """
    Generate an answer using the retrieved context and LLM.

    Args:
        user_query: The user's original query
        retrieved_context: List of retrieved text chunks with metadata

    Returns:
        Generated answer from the LLM
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

        # Initialize the Gemini model
        model = genai.GenerativeModel('gemini-2.5-flash')

        # Generate content using Gemini
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
        logging.error(f"Error processing general query: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Query processing failed: {str(e)}")


@app.post("/api/query/general")
async def query_general(request: GeneralQueryRequest):
    """
    Handle general queries by searching the knowledge base and generating answers.

    Args:
        request: GeneralQueryRequest containing the user query

    Returns:
        Generated answer based on the knowledge base
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
        raise HTTPException(status_code=500, detail=f"General query processing failed: {str(e)}")


@app.post("/api/query/contextual")
async def query_contextual(request: ContextualQueryRequest):
    """
    Handle contextual queries where the user has selected specific text.

    Args:
        request: ContextualQueryRequest containing user query and selected text

    Returns:
        Generated answer based on the selected text and user query
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
    return {"message": "Physical AI RAG Backend Operational"}

@app.post("/create_collection")
async def create_collection(collection_name: str = "humanoid_text_chunks", vector_size: int = 768):
    """
    Create a placeholder Qdrant collection for storing text chunks
    with a standard vector size (768 for all-MiniLM-L6-v2 embedding model)
    """
    try:
        # Get the Qdrant client using thread-safe lazy initialization
        client = get_qdrant_client()

        # Check if collection already exists
        collections = await run_in_threadpool(lambda: client.get_collections())
        existing_collection_names = [collection.name for collection in collections.collections]

        if collection_name in existing_collection_names:
            return {
                "message": f"Collection '{collection_name}' already exists",
                "collection_name": collection_name,
                "vector_size": vector_size
            }

        # Create the collection with specified vector size
        await run_in_threadpool(
            lambda: client.create_collection(
                collection_name=collection_name,
                vectors_config=VectorParams(size=vector_size, distance=Distance.COSINE)
            )
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
        # Get the Qdrant client using thread-safe lazy initialization
        client = get_qdrant_client()

        # Try to get collections to verify connection
        collections = await run_in_threadpool(lambda: client.get_collections())
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

@app.post("/admin/trigger_ingestion")
async def trigger_ingestion(
    source_path: str = "docs",
    collection_name: str = "humanoid_text_chunks",
    background_tasks: BackgroundTasks = None
):
    """
    Administration endpoint to trigger content ingestion.
    This endpoint executes the ingest_content.py script to refresh the vector database.

    Args:
        source_path: Path to the content to be ingested (default: 'docs')
        collection_name: Name of the Qdrant collection (default: 'humanoid_text_chunks')
        background_tasks: FastAPI background tasks for async execution

    Returns:
        Status message indicating the ingestion process has started
    """
    try:
        # Validate that the ingest script exists
        script_path = os.path.join(os.path.dirname(__file__), "ingest_content.py")
        if not os.path.exists(script_path):
            raise HTTPException(status_code=500, detail="Ingestion script not found")

        # Prepare the command to run the ingestion script
        cmd = [
            sys.executable,  # Use the same Python interpreter
            script_path,
            "--source", source_path,
            "--collection", collection_name
        ]

        # Run the ingestion process
        # Note: In a production environment, you might want to run this as a background task
        # or use a proper task queue like Celery
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=300  # 5 minute timeout
        )

        if result.returncode != 0:
            raise HTTPException(
                status_code=500,
                detail=f"Ingestion failed: {result.stderr}"
            )

        return {
            "message": "Content ingestion completed successfully",
            "source_path": source_path,
            "collection_name": collection_name,
            "output": result.stdout
        }

    except subprocess.TimeoutExpired:
        raise HTTPException(
            status_code=408,
            detail="Ingestion process timed out after 5 minutes"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error during ingestion: {str(e)}"
        )


@app.post("/user/register_profile", response_model=UserProfileResponse)
async def register_user_profile(request: UserRegistrationRequest):
    """
    Register user profile with custom background data in Neon Postgres.
    This is a placeholder implementation - in a real system, this would connect to Neon Postgres.

    Args:
        request: UserRegistrationRequest containing userId and background data

    Returns:
        UserProfileResponse with success message and profile ID
    """
    try:
        # In a real implementation, this would connect to Neon Postgres and store the user profile
        # For this placeholder, we'll simulate the database operation
        import uuid
        profile_id = str(uuid.uuid4())

        # Placeholder for Neon Postgres database interaction
        # This would normally use an async database driver like asyncpg or SQLAlchemy with async support
        print(f"Registering profile for user {request.userId}")
        print(f"Software Background: {request.softwareBackground}")
        print(f"Hardware Experience: {request.hardwareExperience}")

        # Simulate database operation
        # In a real implementation, you would:
        # 1. Connect to Neon Postgres using asyncpg or SQLAlchemy
        # 2. Insert the user profile data into the appropriate table
        # 3. Handle potential errors and return appropriate responses

        return {
            "message": "User profile registered successfully",
            "userId": request.userId,
            "profileId": profile_id
        }
    except Exception as e:
        logging.error(f"Error registering user profile: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error registering user profile: {str(e)}"
        )


@app.get("/user/profile/{user_id}")
async def get_user_profile(user_id: str):
    """
    Get user profile data from Neon Postgres.
    This is a placeholder implementation.

    Args:
        user_id: The ID of the user whose profile to retrieve

    Returns:
        User profile data
    """
    try:
        # Placeholder for Neon Postgres database interaction
        # In a real implementation, this would query the database for user profile
        print(f"Retrieving profile for user {user_id}")

        # Simulate retrieving user profile data
        # In a real implementation, you would query the Neon Postgres database
        mock_profile = {
            "userId": user_id,
            "softwareBackground": "python-ros",  # Would come from DB
            "hardwareExperience": "intermediate-jetson",  # Would come from DB
            "createdAt": "2025-12-07T00:00:00Z"  # Would come from DB
        }

        return mock_profile
    except Exception as e:
        logging.error(f"Error retrieving user profile: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error retrieving user profile: {str(e)}"
        )


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


# Database models for user profiles (placeholder implementation)
if DB_AVAILABLE:
    # Define the database model using SQLAlchemy
    Base = declarative_base()

    class UserProfile(Base):
        __tablename__ = 'user_profiles'

        id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
        user_id = Column(String, nullable=False, unique=True)
        software_background = Column(String, nullable=False)
        hardware_experience = Column(String, nullable=False)
        created_at = Column(DateTime, server_default=func.now())
        updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    # Initialize database engine (placeholder)
    DATABASE_URL = config.NEON_PG_URL
    if DATABASE_URL:
        engine = create_async_engine(DATABASE_URL)
        async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    else:
        logging.warning("Neon Postgres URL not configured. Database functionality will use placeholder.")


async def save_user_profile_to_db(user_id: str, software_background: str, hardware_experience: str):
    """
    Save user profile to Neon Postgres database.
    This is a placeholder implementation that uses a mock database operation.
    """
    if not DB_AVAILABLE or not config.NEON_PG_URL:
        # Placeholder implementation - in a real system, this would save to the database
        profile_id = str(uuid.uuid4())
        print(f"Saving profile for user {user_id}")
        print(f"Software Background: {software_background}")
        print(f"Hardware Experience: {hardware_experience}")
        return profile_id

    # Real implementation would use SQLAlchemy async operations
    # This is commented out since the database libraries may not be available
    """
    async with async_session() as session:
        try:
            new_profile = UserProfile(
                user_id=user_id,
                software_background=software_background,
                hardware_experience=hardware_experience
            )
            session.add(new_profile)
            await session.commit()
            await session.refresh(new_profile)
            return new_profile.id
        except Exception as e:
            await session.rollback()
            logging.error(f"Error saving user profile: {str(e)}")
            raise
    """


@app.post("/api/auth/signup", response_model=UserAuthResponse)
async def signup(request: UserAuthRequest):
    """
    Signup endpoint - placeholder for Better Auth integration.
    In a real implementation, this would integrate with Better Auth.
    """
    # This would normally call Better Auth's signup API
    # For now, we'll return mock data
    user_id = str(uuid.uuid4())
    session_id = str(uuid.uuid4())

    return {
        "message": "Signup successful",
        "userId": user_id,
        "sessionId": session_id
    }




# Pydantic model for personalization request
class PersonalizeContentRequest(BaseModel):
    user_id: str
    chapter_id: str
    module_id: str
    user_profile: Dict[str, str]  # Contains softwareBackground and hardwareExperience


class PersonalizeContentResponse(BaseModel):
    message: str
    original_content: str
    personalized_content: str
    user_profile_used: Dict[str, str]


async def get_user_profile_from_db(user_id: str) -> Dict[str, str]:
    """
    Get user profile from Neon Postgres database.
    This is a placeholder implementation.
    """
    if not DB_AVAILABLE or not config.NEON_PG_URL:
        # Placeholder implementation - return mock profile data
        # In a real implementation, this would query the database
        mock_profiles = {
            "test-user-id-12345": {
                "softwareBackground": "python-ros",
                "hardwareExperience": "intermediate-jetson"
            },
            "expert-user": {
                "softwareBackground": "cpp-low-level",
                "hardwareExperience": "expert-fullstack"
            },
            "beginner-user": {
                "softwareBackground": "data-science-ml",
                "hardwareExperience": "beginner"
            }
        }
        return mock_profiles.get(user_id, {
            "softwareBackground": "python-ros",
            "hardwareExperience": "intermediate-jetson"
        })

    # Real implementation would query the database
    # This is commented out since the database libraries may not be available
    """
    async with async_session() as session:
        try:
            result = await session.execute(
                select(UserProfile).where(UserProfile.user_id == user_id)
            )
            profile = result.scalars().first()
            if profile:
                return {
                    "softwareBackground": profile.software_background,
                    "hardwareExperience": profile.hardware_experience
                }
            return None
        except Exception as e:
            logging.error(f"Error fetching user profile: {str(e)}")
            raise
    """


def get_original_content(chapter_id: str, module_id: str) -> str:
    """
    Retrieve the original Markdown content for the requested chapter.
    This is a placeholder implementation that returns sample content.
    In a real implementation, this would read from the docs directory.
    """
    # In a real implementation, this would read the actual Markdown file
    # For now, we'll return sample content based on the chapter/module
    sample_content = f"""# Sample Chapter Content for {module_id}/{chapter_id}

## Introduction

This is a sample chapter about robotics concepts. The content would normally be more detailed and comprehensive.

### Section 1: Basic Concepts

Robotic systems involve complex interactions between hardware and software components. The implementation approach can vary significantly based on the target platform and experience level.

### Section 2: Implementation Details

Different programming languages and hardware platforms require different approaches to achieve the same goals.

## Conclusion

This chapter covered the fundamental concepts of robotics implementation.
"""
    return sample_content


def create_personalization_prompt(original_content: str, user_profile: Dict[str, str]) -> str:
    """
    Create a prompt for the LLM to personalize content based on user profile.
    """
    software_background = user_profile.get('softwareBackground', 'python-ros')
    hardware_experience = user_profile.get('hardwareExperience', 'intermediate-jetson')

    # Map the profile values to human-readable descriptions
    background_descriptions = {
        'python-ros': 'Python/ROS Focused',
        'cpp-low-level': 'C++/Low-Level Focused',
        'data-science-ml': 'Data Science/ML Focused'
    }

    experience_descriptions = {
        'beginner': 'Beginner/Theoretical',
        'intermediate-jetson': 'Intermediate/Edge Devices (Jetson)',
        'expert-fullstack': 'Expert/Full Stack Robotics'
    }

    background_desc = background_descriptions.get(software_background, software_background)
    experience_desc = experience_descriptions.get(hardware_experience, hardware_experience)

    prompt = f"""You are an expert instructor in Physical AI and Robotics. Rewrite the following chapter content to match the user's background and experience level.

User Profile:
- Software Background: {background_desc}
- Hardware Experience: {experience_desc}

Original Content:
{original_content}

Instructions:
1. Adjust the technical depth based on the user's experience level (beginner, intermediate, expert)
2. Focus examples and code snippets on the user's preferred software background (Python/ROS, C++/Low-Level, Data Science/ML)
3. Include relevant hardware-specific examples based on their experience (e.g., Jetson for intermediate, full-stack concepts for expert)
4. Maintain the original section headings and structure
5. Add appropriate technical details, code examples, or theoretical explanations based on their background
6. For beginners, add more foundational explanations and simpler examples
7. For experts, add advanced concepts and deeper technical insights
8. For intermediate users, provide balanced explanations with practical examples

Return only the personalized content with the same structure as the original."""

    return prompt


async def get_personalized_content(original_content: str, user_profile: Dict[str, str]) -> str:
    """
    Use the LLM to transform the content based on the user's profile.
    This is a placeholder implementation that returns modified content.
    """
    try:
        # Create the prompt for personalization
        prompt = create_personalization_prompt(original_content, user_profile)

        # In a real implementation, this would call the LLM API
        # For now, we'll return a placeholder personalized version
        software_background = user_profile.get('softwareBackground', 'python-ros')
        hardware_experience = user_profile.get('hardwareExperience', 'intermediate-jetson')

        # Generate personalized content based on profile
        if hardware_experience == 'beginner':
            personalized_content = f"""# Personalized Chapter Content for {software_background.replace('-', ' ').title()} Focus

## Introduction

This chapter has been adapted for a beginner level with a focus on {software_background.replace('-', ' ').title()} concepts.

### Section 1: Basic Concepts

Robotic systems involve interactions between hardware and software. As a beginner, you'll start with fundamental concepts:

- Basic programming approaches
- Simple control systems
- Introduction to sensors and actuators

### Section 2: Implementation Details

For {software_background.replace('-', ' ').title()} users, we focus on:

- Beginner-friendly code examples
- Basic setup and configuration
- Simple implementation patterns

## Conclusion

This chapter introduced fundamental robotics concepts appropriate for your experience level.
"""
        elif hardware_experience == 'expert-fullstack':
            personalized_content = f"""# Advanced Chapter Content for {software_background.replace('-', ' ').title()} Focus

## Advanced Introduction

This chapter provides expert-level content for {software_background.replace('-', ' ').title()} with full-stack robotics experience.

### Section 1: Advanced Concepts

Robotic systems require sophisticated integration across multiple layers. As an expert, we'll dive deep into:

- Low-level system optimizations
- Advanced control algorithms
- Hardware-software co-design principles

### Section 2: Implementation Details

For {software_background.replace('-', ' ').title()} experts, we explore:

- Performance-critical implementations
- Real-time system considerations
- Advanced debugging and optimization techniques

## Advanced Conclusion

This chapter covered expert-level robotics concepts for full-stack implementation.
"""
        else:  # intermediate-jetson
            personalized_content = f"""# Intermediate Chapter Content for {software_background.replace('-', ' ').title()} Focus

## Intermediate Introduction

This chapter provides intermediate content for {software_background.replace('-', ' ').title()} with focus on edge devices like Jetson.

### Section 1: Intermediate Concepts

Robotic systems on edge devices require careful balance of performance and efficiency:

- Resource optimization techniques
- Edge computing considerations
- Power and thermal management

### Section 2: Implementation Details

For {software_background.replace('-', ' ').title()} on Jetson platforms:

- GPU-accelerated processing
- Optimized deployment strategies
- Edge-specific development patterns

## Intermediate Conclusion

This chapter covered intermediate robotics concepts for edge device implementation.
"""

        return personalized_content

    except Exception as e:
        logging.error(f"Error generating personalized content: {str(e)}")
        # Return original content if personalization fails
        return original_content


@app.post("/api/content/personalize", response_model=PersonalizeContentResponse)
async def personalize_content(request: PersonalizeContentRequest):
    """
    Personalize chapter content based on user profile.

    Args:
        request: PersonalizeContentRequest containing user_id, chapter_id, module_id, and user_profile

    Returns:
        PersonalizeContentResponse with original and personalized content
    """
    try:
        # Get user profile (fetch from database if not provided in request)
        user_profile = request.user_profile
        if not user_profile or not user_profile.get('softwareBackground'):
            # Fetch from database if not provided
            user_profile = await get_user_profile_from_db(request.user_id)

        # Retrieve original content
        original_content = get_original_content(request.chapter_id, request.module_id)

        # Generate personalized content using LLM
        personalized_content = await get_personalized_content(original_content, user_profile)

        return {
            "message": "Content personalized successfully",
            "original_content": original_content,
            "personalized_content": personalized_content,
            "user_profile_used": user_profile
        }

    except Exception as e:
        logging.error(f"Error in personalize_content: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error personalizing content: {str(e)}"
        )


# Pydantic model for Urdu translation request
class UrduTranslationRequest(BaseModel):
    chapter_slug: str
    original_content: str


class UrduTranslationResponse(BaseModel):
    message: str
    chapter_slug: str
    original_content: str
    translated_content: str


def create_urdu_translation_prompt(original_content: str) -> str:
    """
    Create a prompt for the LLM to translate Markdown content to Urdu.
    """
    prompt = f"""You are an expert translator specializing in technical content. Translate the following Markdown content to standard, modern Urdu while preserving the original Markdown structure exactly.

Original Content:
{original_content}

Instructions:
1. Translate ALL text content to Urdu
2. Preserve ALL Markdown formatting exactly:
   - Headings (#, ##, ###) should remain unchanged
   - Lists (-, *, 1., 2.) should remain unchanged
   - Code blocks (```language ... ```) should remain unchanged
   - Inline code (`code`) should remain unchanged
   - Bold (**text**) and italic (*text*) formatting should remain unchanged
   - Links ([text](url)) should remain unchanged
   - Blockquotes (>) should remain unchanged
   - Tables should maintain their structure
3. Only translate human-readable text, NOT formatting elements
4. Maintain the same document structure and hierarchy
5. Use standard, modern Urdu that is easily readable
6. Do NOT translate technical terms that don't have standard Urdu equivalents
7. Preserve the meaning and context of the original content

Return only the translated content with the same structure as the original."""
    return prompt


async def get_urdu_translated_content(original_content: str) -> str:
    """
    Use the Gemini API to translate content to Urdu while preserving Markdown structure.
    """
    try:
        # Create the prompt for Urdu translation
        prompt = create_urdu_translation_prompt(original_content)

        # Initialize the Gemini model
        model = genai.GenerativeModel('gemini-2.5-flash')

        # Generate content using Gemini
        response = model.generate_content(
            prompt,
            generation_config={
                "temperature": 0.3,  # Lower temperature for more consistent translations
            }
        )

        # Extract and return the translated content
        translated_content = response.text.strip()
        return translated_content

    except Exception as e:
        logging.error(f"Error generating Urdu translation with Gemini: {str(e)}")
        # Return original content if translation fails
        return original_content


@app.post("/api/content/translate_urdu", response_model=UrduTranslationResponse)
async def translate_urdu(request: UrduTranslationRequest):
    """
    Translate chapter content to Urdu while preserving Markdown structure.

    Args:
        request: UrduTranslationRequest containing chapter_slug and original_content

    Returns:
        UrduTranslationResponse with original and translated content
    """
    try:
        # Generate Urdu translated content using LLM
        translated_content = await get_urdu_translated_content(request.original_content)

        return {
            "message": "Content translated to Urdu successfully",
            "chapter_slug": request.chapter_slug,
            "original_content": request.original_content,
            "translated_content": translated_content
        }

    except Exception as e:
        logging.error(f"Error in translate_urdu: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error translating content to Urdu: {str(e)}"
        )


# Pydantic model for the RAG chat endpoint
class RAGChatRequest(BaseModel):
    query: str
    top_k: int = 5  # Number of context chunks to retrieve (default: 5)


class RAGChatResponse(BaseModel):
    query: str
    response: str
    sources: List[Dict[str, Any]]
    context_used: str


@app.post("/api/rag/chat", response_model=RAGChatResponse)
async def rag_chat_endpoint(request: RAGChatRequest):
    """
    RAG Chat endpoint that processes user queries using the RAG pipeline.

    Args:
        request: RAGChatRequest containing the user query

    Returns:
        RAGChatResponse with the answer, sources, and context used
    """
    try:
        # Log the incoming request
        logging.info(f"Processing RAG chat request: {request.query[:50]}...")
        print(f"DEBUG: Processing RAG chat request: {request.query}")

        # Perform vector search to find relevant context
        retrieved_context = await perform_vector_search(request.query, request.top_k)
        logging.info(f"Retrieved {len(retrieved_context)} context chunks")

        # Generate RAG answer using the retrieved context
        answer = await generate_rag_answer(request.query, retrieved_context)
        logging.info("Successfully generated RAG answer")

        # Prepare response
        context_used = "\n\n".join([chunk["text"] for chunk in retrieved_context])
        sources = [chunk["metadata"] for chunk in retrieved_context]

        response = RAGChatResponse(
            query=request.query,
            response=answer,
            sources=sources,
            context_used=context_used
        )

        logging.info("RAG chat request completed successfully")
        return response

    except Exception as e:
        # Detailed error logging for debugging
        import traceback
        error_msg = f"Error in RAG chat endpoint: {str(e)}"
        error_traceback = traceback.format_exc()

        logging.error(error_msg)
        logging.error(f"Full traceback: {error_traceback}")
        print(f"ERROR: {error_msg}")
        print(f"TRACEBACK: {error_traceback}")

        # Raise HTTP exception with detailed error for client
        raise HTTPException(
            status_code=500,
            detail=f"RAG chat processing failed: {str(e)}"
        )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=config.FASTAPI_HOST, port=config.FASTAPI_PORT)