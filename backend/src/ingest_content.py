"""
Content Ingestion Script for Physical AI & Humanoid Robotics Textbook

This script handles the preparation of Docusaurus textbook content for the RAG backend:
1. Reads Docusaurus Markdown files
2. Chunks the content into suitable segments
3. Embeds the chunks using Sentence Transformers
4. Stores the embeddings in Qdrant for retrieval
"""

import os
import re
from typing import List, Dict, Any
from pathlib import Path
import hashlib

from langchain_text_splitters import RecursiveCharacterTextSplitter
from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient
from qdrant_client.http import models
from qdrant_client.http.models import PointStruct
from dotenv import load_dotenv


# Load environment variables
load_dotenv()

class ContentIngestor:
    def __init__(self, qdrant_url: str = None, qdrant_api_key: str = None):
        """
        Initialize the content ingestor with Qdrant connection and embedding model.
        """
        self.qdrant_url = qdrant_url or os.getenv("QDRANT_URL", "http://localhost:6333")
        self.qdrant_api_key = qdrant_api_key or os.getenv("QDRANT_API_KEY")

        # Initialize Qdrant client
        if self.qdrant_url and "localhost" not in self.qdrant_url and "127.0.0.1" not in self.qdrant_url:
            # Using Qdrant Cloud
            self.qdrant_client = QdrantClient(
                url=self.qdrant_url,
                api_key=self.qdrant_api_key,
                prefer_grpc=False
            )
        else:
            # Using local Qdrant
            self.qdrant_client = QdrantClient(host="localhost", port=6333)

        # Initialize embedding model
        self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')

        # Initialize text splitter
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=800,
            chunk_overlap=80,
            length_function=len,
            is_separator_regex=False,
            separators=[
                "\n\n",  # Paragraph breaks
                "\n",    # Line breaks
                " ",     # Spaces
                ""       # Fallback to character-level splitting
            ]
        )

    def read_markdown_file(self, file_path: str) -> str:
        """
        Read a markdown file and return its content as a string.

        Args:
            file_path: Path to the markdown file

        Returns:
            Content of the markdown file as a string
        """
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        return content

    def extract_module_info(self, file_path: str) -> Dict[str, str]:
        """
        Extract module information from the file path.

        Args:
            file_path: Path to the markdown file

        Returns:
            Dictionary containing module information
        """
        path = Path(file_path)
        file_name = path.stem
        parent_dir = path.parent.name

        # Extract module information from file path
        module_info = {
            'source_file': str(path),
            'file_name': file_name,
            'parent_directory': parent_dir
        }

        # Try to extract module ID from the path
        if parent_dir and parent_dir.startswith('module'):
            module_info['module_id'] = parent_dir
        elif file_name.startswith('module'):
            module_info['module_id'] = file_name

        # Extract chapter title from the first H1 in the content
        try:
            content = self.read_markdown_file(file_path)
            h1_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
            if h1_match:
                module_info['chapter_title'] = h1_match.group(1).strip()
            else:
                module_info['chapter_title'] = file_name.replace('_', ' ').replace('-', ' ').title()
        except Exception:
            module_info['chapter_title'] = file_name.replace('_', ' ').replace('-', ' ').title()

        return module_info

    def chunk_text(self, text: str, source_metadata: Dict[str, str]) -> List[Dict[str, Any]]:
        """
        Split the text into chunks and prepare them with metadata.

        Args:
            text: The text to be chunked
            source_metadata: Metadata about the source document

        Returns:
            List of dictionaries containing chunk information
        """
        chunks = self.text_splitter.split_text(text)

        chunked_data = []
        for i, chunk in enumerate(chunks):
            chunk_data = {
                'text': chunk,
                'metadata': {
                    **source_metadata,
                    'chunk_id': f"{source_metadata.get('file_name', 'unknown')}_{i}",
                    'chunk_index': i,
                    'char_length': len(chunk)
                }
            }
            chunked_data.append(chunk_data)

        return chunked_data

    def embed_chunks(self, chunks: List[str]) -> List[List[float]]:
        """
        Generate embeddings for a list of text chunks.

        Args:
            chunks: List of text chunks to embed

        Returns:
            List of embedding vectors
        """
        embeddings = self.embedding_model.encode(chunks)
        return embeddings.tolist()  # Convert to Python lists

    def store_in_qdrant(self, chunked_data: List[Dict[str, Any]], collection_name: str = "humanoid_text_chunks"):
        """
        Store chunked data with embeddings in Qdrant.

        Args:
            chunked_data: List of chunk data with text and metadata
            collection_name: Name of the Qdrant collection
        """
        # Prepare points for Qdrant
        points = []
        for i, item in enumerate(chunked_data):
            # Generate embedding for the text
            embedding = self.embedding_model.encode([item['text']])[0].tolist()

            # Create a unique ID for the point
            text_hash = hashlib.md5((item['text'] + str(i)).encode()).hexdigest()

            point = PointStruct(
                id=text_hash,
                vector=embedding,
                payload={
                    "text": item['text'],
                    "metadata": item['metadata']
                }
            )
            points.append(point)

        # Upsert points to Qdrant collection
        self.qdrant_client.upsert(
            collection_name=collection_name,
            points=points
        )

        print(f"Successfully stored {len(points)} chunks in Qdrant collection '{collection_name}'")

    def process_single_file(self, file_path: str, collection_name: str = "humanoid_text_chunks") -> int:
        """
        Process a single markdown file: read, chunk, embed, and store in Qdrant.

        Args:
            file_path: Path to the markdown file
            collection_name: Name of the Qdrant collection

        Returns:
            Number of chunks processed
        """
        print(f"Processing file: {file_path}")

        # Read the file content
        content = self.read_markdown_file(file_path)

        # Extract module information
        metadata = self.extract_module_info(file_path)

        # Chunk the content
        chunked_data = self.chunk_text(content, metadata)

        # Store in Qdrant
        self.store_in_qdrant(chunked_data, collection_name)

        print(f"Completed processing {len(chunked_data)} chunks from {file_path}")
        return len(chunked_data)

    def process_directory(self, directory_path: str, collection_name: str = "humanoid_text_chunks") -> int:
        """
        Process all markdown files in a directory.

        Args:
            directory_path: Path to the directory containing markdown files
            collection_name: Name of the Qdrant collection

        Returns:
            Total number of chunks processed
        """
        directory = Path(directory_path)
        markdown_files = list(directory.rglob("*.md")) + list(directory.rglob("*.markdown"))

        total_chunks = 0
        for file_path in markdown_files:
            try:
                chunks_count = self.process_single_file(str(file_path), collection_name)
                total_chunks += chunks_count
            except Exception as e:
                print(f"Error processing {file_path}: {str(e)}")

        print(f"Completed processing directory. Total chunks: {total_chunks}")
        return total_chunks

    def process_content(self, source_path: str, collection_name: str = "humanoid_text_chunks") -> int:
        """
        Main method to process content from a file or directory.

        Args:
            source_path: Path to a markdown file or directory containing markdown files
            collection_name: Name of the Qdrant collection

        Returns:
            Total number of chunks processed
        """
        source = Path(source_path)

        if source.is_file() and source.suffix.lower() in ['.md', '.markdown']:
            return self.process_single_file(source_path, collection_name)
        elif source.is_dir():
            return self.process_directory(source_path, collection_name)
        else:
            raise ValueError(f"Invalid source path: {source_path}. Must be a markdown file or directory.")


def main():
    """
    Main function to run the content ingestion process.
    """
    import argparse

    parser = argparse.ArgumentParser(description="Ingest content into Qdrant for RAG system")
    parser.add_argument(
        "--source",
        type=str,
        required=True,
        help="Path to a markdown file or directory containing markdown files"
    )
    parser.add_argument(
        "--collection",
        type=str,
        default="humanoid_text_chunks",
        help="Qdrant collection name (default: humanoid_text_chunks)"
    )
    parser.add_argument(
        "--qdrant-url",
        type=str,
        help="Qdrant URL (optional, defaults to environment variable)"
    )
    parser.add_argument(
        "--qdrant-api-key",
        type=str,
        help="Qdrant API key (optional, defaults to environment variable)"
    )

    args = parser.parse_args()

    # Initialize the ingestor
    ingestor = ContentIngestor(
        qdrant_url=args.qdrant_url,
        qdrant_api_key=args.qdrant_api_key
    )

    # Process the content
    try:
        total_chunks = ingestor.process_content(args.source, args.collection)
        print(f"\nIngestion completed successfully! Processed {total_chunks} chunks.")
    except Exception as e:
        print(f"Error during ingestion: {str(e)}")
        return 1

    return 0


if __name__ == "__main__":
    exit(main())