"""
Configuration module for loading environment variables securely.
This module handles the loading of environment variables from the .env file
and provides default values where appropriate.
"""
import os
from typing import Optional
from dotenv import load_dotenv


# Load environment variables from .env file
load_dotenv()


class Config:
    """
    Configuration class that loads and validates environment variables.
    """

    # FastAPI Settings
    FASTAPI_HOST: str = os.getenv("FASTAPI_HOST", "0.0.0.0")
    FASTAPI_PORT: int = int(os.getenv("FASTAPI_PORT", "8000"))
    API_SECRET_KEY: str = os.getenv("API_SECRET_KEY", "your-secret-key-here")

    # Vector Database (Qdrant)
    QDRANT_URL: Optional[str] = os.getenv("QDRANT_URL")
    QDRANT_API_KEY: Optional[str] = os.getenv("QDRANT_API_KEY")
    QDRANT_COLLECTION_NAME: str = os.getenv("QDRANT_COLLECTION_NAME", "humanoid_text_chunks")

    # LLM Service (OpenAI)
    OPENAI_API_KEY: Optional[str] = os.getenv("OPENAI_API_KEY")
    GEMINI_API_KEY: Optional[str] = os.getenv("GEMINI_API_KEY")
    EMBEDDING_MODEL_NAME: str = os.getenv("EMBEDDING_MODEL_NAME", "all-MiniLM-L6-v2")

    # Postgres (Neon) - for user profiles/auth data
    NEON_PG_URL: Optional[str] = os.getenv("NEON_PG_URL")

    # Better Auth (Bonus 4.0)
    BETTER_AUTH_CLIENT_ID: Optional[str] = os.getenv("BETTER_AUTH_CLIENT_ID")
    BETTER_AUTH_SECRET: Optional[str] = os.getenv("BETTER_AUTH_SECRET")

    # Development settings
    DEBUG: bool = os.getenv("DEBUG", "false").lower() == "true"
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")

    # Application settings
    MAX_CONTENT_LENGTH: int = int(os.getenv("MAX_CONTENT_LENGTH", "10485760"))  # 10MB in bytes

    @classmethod
    def validate_config(cls) -> bool:
        """
        Validate that required environment variables are set.
        Returns True if all required variables are present, False otherwise.
        """
        required_vars = [
            "API_SECRET_KEY",
            "QDRANT_COLLECTION_NAME",
            "EMBEDDING_MODEL_NAME"
        ]

        # For production, you might want to check for more critical variables
        missing_vars = []
        for var in required_vars:
            value = getattr(cls, var)
            if not value or value == "your-secret-key-here":
                missing_vars.append(var)

        if missing_vars:
            print(f"Warning: Missing or default configuration values for: {', '.join(missing_vars)}")
            return False

        return True

    @classmethod
    def get_qdrant_config(cls) -> dict:
        """
        Get Qdrant configuration as a dictionary.
        """
        return {
            "url": cls.QDRANT_URL,
            "api_key": cls.QDRANT_API_KEY,
            "collection_name": cls.QDRANT_COLLECTION_NAME
        }

    @classmethod
    def get_openai_config(cls) -> dict:
        """
        Get OpenAI configuration as a dictionary.
        """
        return {
            "api_key": cls.OPENAI_API_KEY
        }

    @classmethod
    def get_neon_config(cls) -> dict:
        """
        Get Neon Postgres configuration as a dictionary.
        """
        return {
            "database_url": cls.NEON_PG_URL
        }

    @classmethod
    def get_auth_config(cls) -> dict:
        """
        Get Better Auth configuration as a dictionary.
        """
        return {
            "client_id": cls.BETTER_AUTH_CLIENT_ID,
            "secret": cls.BETTER_AUTH_SECRET
        }


# Initialize configuration
config = Config()

# Validate configuration on import
if not config.validate_config():
    if not config.DEBUG:
        print("Warning: Configuration validation failed. Some required environment variables may not be set properly.")
        print("This is normal in development, but make sure to set proper values in production.")