"""
RAG Backend Search Test (Isolation)

This script tests the RAG backend search functionality in isolation by:
1. Using a sample query ('What is the role of ZMP in bipedal locomotion?')
2. Directly calling the perform_vector_search function
3. Displaying retrieved chunks with raw text and metadata
"""

import asyncio
import sys
from pathlib import Path

# Add the src directory to the path so we can import main
sys.path.insert(0, str(Path(__file__).parent))

from main import perform_vector_search


async def test_rag_search_isolation():
    """
    Test RAG backend search functionality in isolation.

    This function:
    1. Runs a sample query through the perform_vector_search function
    2. Displays retrieved chunks with raw text and metadata
    """
    print("RAG BACKEND SEARCH TEST (ISOLATION)")
    print("="*50)

    # Sample query as specified in the task
    sample_query = "What is the role of ZMP in bipedal locomotion?"
    print(f"Query: {sample_query}")
    print()

    try:
        # Run the vector search directly
        results = await perform_vector_search(sample_query, top_k=5)

        print(f"Found {len(results)} results:")
        print("-" * 50)

        for i, result in enumerate(results, 1):
            print(f"Result {i}:")
            print(f"  Score: {result['score']:.4f}")
            print(f"  Text Preview: {result['text'][:300]}...")  # First 300 chars
            print(f"  Full Text: {result['text']}")
            print(f"  Metadata: {result['metadata']}")
            print("-" * 50)

        print(f"✓ Successfully retrieved {len(results)} chunks for query: '{sample_query}'")
        return len(results) > 0

    except Exception as e:
        print(f"✗ RAG backend search test failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def test_multiple_queries():
    """
    Test multiple sample queries to validate search functionality.
    """
    print("\nTESTING MULTIPLE QUERIES")
    print("="*50)

    sample_queries = [
        "What is the role of ZMP in bipedal locomotion?",
        "Explain forward kinematics in robotics",
        "What are Jacobian matrices used for?",
        "How does inverse kinematics work?",
        "What is the Denavit-Hartenberg convention?"
    ]

    all_success = True

    for query in sample_queries:
        print(f"\nTesting query: {query}")
        try:
            results = asyncio.run(perform_vector_search(query, top_k=3))
            print(f"  Retrieved {len(results)} results")
            if len(results) > 0:
                print(f"  Top result score: {results[0]['score']:.4f}")
                print(f"  Top result preview: {results[0]['text'][:100]}...")
            else:
                print("  No results found")
        except Exception as e:
            print(f"  ✗ Failed: {str(e)}")
            all_success = False

    return all_success


if __name__ == "__main__":
    print("RAG BACKEND SEARCH VALIDATION")
    print("="*50)

    # Test single query
    single_test_success = asyncio.run(test_rag_search_isolation())

    # Test multiple queries
    multiple_test_success = test_multiple_queries()

    print("\n" + "="*50)
    print("SUMMARY")
    print("="*50)

    print(f"Single query test: {'✓ PASSED' if single_test_success else '✗ FAILED'}")
    print(f"Multiple queries test: {'✓ PASSED' if multiple_test_success else '✗ FAILED'}")

    overall_success = single_test_success and multiple_test_success
    print(f"Overall: {'✓ ALL TESTS PASSED' if overall_success else '✗ SOME TESTS FAILED'}")

    if not overall_success:
        print("\nNote: This test requires sample content to be ingested into Qdrant.")
        print("If no content exists, run the ingestion test first.")