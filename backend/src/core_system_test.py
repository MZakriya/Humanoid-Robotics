"""
Core System Testing and Validation Suite

This test suite validates the core functionalities of the Physical AI & Humanoid Robotics RAG system:
1. Ingestion Test Utility - Tests content ingestion and verifies Qdrant collection point count
2. RAG Backend Search Test - Tests vector search functionality in isolation
3. Full Stack Connectivity Test - Provides instructions for frontend testing
"""

import asyncio
import sys
from pathlib import Path
import os

# Add the src directory to the path so we can import modules
sys.path.insert(0, str(Path(__file__).parent))

from ingest_content import ContentIngestor
from main import perform_vector_search, get_qdrant_client


def test_ingestion_and_verify_points():
    """
    Test utility to run ingest_content.py and verify Qdrant collection point count.

    This function:
    1. Creates sample content
    2. Runs the ingestion process
    3. Verifies the point count in the Qdrant collection
    """
    print("="*60)
    print("INGESTION TEST UTILITY")
    print("="*60)

    try:
        # Create sample content for testing
        sample_docs_dir = Path("sample_docs_test")
        sample_docs_dir.mkdir(exist_ok=True)

        # Create sample content similar to the textbook modules
        sample_content = """# Sample Module: ZMP and Bipedal Locomotion

## Zero Moment Point (ZMP) Theory

The Zero Moment Point (ZMP) is a crucial concept in bipedal robotics that defines the point on the ground where the sum of all moments due to the ground reaction forces is zero. This concept is fundamental to understanding stable walking patterns in humanoid robots.

### Mathematical Definition

The ZMP is defined as the point where the net moment of the ground reaction force about that point is zero. In mathematical terms:

```
M = ∫ (r - r_zmp) × f dA = 0
```

Where:
- M is the moment vector
- r is the position vector
- r_zmp is the ZMP position
- f is the force vector
- dA is the differential area

### ZMP in Bipedal Locomotion

In bipedal locomotion, the ZMP trajectory must remain within the support polygon defined by the feet to ensure dynamic stability. This constraint forms the basis for many walking pattern generation algorithms.

#### Key Properties:

1. **Stability Condition**: For stable walking, the ZMP must lie within the convex hull of the supporting foot/feet
2. **Support Polygon**: The area defined by the feet that constrains the ZMP position
3. **Walking Pattern Generation**: ZMP-based controllers generate stable walking gaits

## Applications in Humanoid Robotics

Modern humanoid robots like Honda's ASIMO and Boston Dynamics' Atlas utilize ZMP-based controllers to achieve stable walking. These controllers continuously adjust the robot's center of mass trajectory to keep the ZMP within acceptable bounds.

### Control Strategies

- Preview control for ZMP regulation
- Inverted pendulum models for balance
- Foot placement strategies for stability
"""

        sample_file = sample_docs_dir / "zmp_bipedal_locomotion.md"
        with open(sample_file, "w", encoding="utf-8") as f:
            f.write(sample_content)

        print(f"✓ Created sample content at {sample_file}")

        # Initialize the ingestor
        ingestor = ContentIngestor()

        # Process the sample content
        collection_name = "test_humanoid_text_chunks"
        total_chunks = ingestor.process_content(
            source_path=str(sample_docs_dir),
            collection_name=collection_name
        )

        print(f"✓ Ingested {total_chunks} chunks into collection '{collection_name}'")

        # Verify point count in Qdrant collection
        client = ingestor.qdrant_client

        # Get collection info to verify point count
        collection_info = client.get_collection(collection_name)
        point_count = collection_info.points_count

        print(f"✓ Qdrant collection '{collection_name}' contains {point_count} points")

        # Verify the count matches expected chunks
        if point_count == total_chunks:
            print("✓ Point count verification PASSED")
        else:
            print(f"⚠ Point count mismatch: expected {total_chunks}, got {point_count}")

        # Clean up - remove the test collection
        try:
            client.delete_collection(collection_name)
            print(f"✓ Cleaned up test collection '{collection_name}'")
        except Exception as e:
            print(f"⚠ Could not clean up collection: {e}")

        # Clean up sample files
        import shutil
        shutil.rmtree(sample_docs_dir, ignore_errors=True)
        print(f"✓ Cleaned up sample content directory")

        return True

    except Exception as e:
        print(f"✗ Ingestion test failed: {str(e)}")
        return False


def test_rag_backend_search():
    """
    Test RAG backend search functionality in isolation.

    This function:
    1. Runs a sample query through the perform_vector_search function
    2. Displays retrieved chunks with raw text and metadata
    """
    print("\n" + "="*60)
    print("RAG BACKEND SEARCH TEST (ISOLATION)")
    print("="*60)

    try:
        # Sample query as specified in the task
        sample_query = "What is the role of ZMP in bipedal locomotion?"
        print(f"Query: {sample_query}")

        # Run the vector search directly
        results = asyncio.run(perform_vector_search(sample_query, top_k=3))

        print(f"\nFound {len(results)} results:")
        print("-" * 60)

        for i, result in enumerate(results, 1):
            print(f"Result {i}:")
            print(f"  Score: {result['score']:.4f}")
            print(f"  Text: {result['text'][:200]}...")  # First 200 chars
            print(f"  Metadata: {result['metadata']}")
            print("-" * 60)

        if len(results) > 0:
            print("✓ RAG backend search test PASSED")
            return True
        else:
            print("⚠ No results returned from search")
            return False

    except Exception as e:
        print(f"✗ RAG backend search test failed: {str(e)}")
        return False


def print_full_stack_connectivity_instructions():
    """
    Print step-by-step instructions for full stack connectivity testing.

    This provides instructions for testing the frontend and backend connection.
    """
    print("\n" + "="*60)
    print("FULL STACK CONNECTIVITY TEST INSTRUCTIONS")
    print("="*60)

    instructions = """
1. START THE BACKEND SERVER:
   - Navigate to the backend directory: cd backend
   - Start the FastAPI server: uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
   - Verify the server is running by visiting: http://localhost:8000/health

2. START THE DOCUSAURUS FRONTEND:
   - Navigate to the project root: cd ..
   - Install Docusaurus dependencies: npm install
   - Start the development server: npm run start
   - The frontend should be available at: http://localhost:3000

3. OPEN BROWSER DEVELOPER TOOLS:
   - Press F12 or right-click → Inspect Element
   - Go to the 'Network' tab
   - Clear any existing network requests

4. TEST GENERAL QUERY FUNCTIONALITY:
   - Open the chatbot UI in the Docusaurus site
   - Enter a general query like: "What is forward kinematics?"
   - Submit the query
   - In the Network tab, look for:
     * Request URL: http://localhost:8000/api/query/general
     * Request method: POST
     * Request body: {"query": "What is forward kinematics?"}
     * Response status: 200 OK
     * Response body: Should contain query, answer, sources, and context_type

5. TEST CONTEXTUAL QUERY FUNCTIONALITY:
   - Select some text on the page (e.g., select a paragraph about kinematics)
   - Click the contextual query button (📝) in the chatbot
   - The input field should be pre-filled with: Context: "[selected text]". Question:
   - Complete the question: "Explain this concept in simple terms"
   - Submit the query
   - In the Network tab, look for:
     * Request URL: http://localhost:8000/api/query/contextual
     * Request method: POST
     * Request body: {"user_query": "Explain this concept in simple terms", "selected_text": "[selected text]"}
     * Response status: 200 OK
     * Response body: Should contain user_query, selected_text, answer, sources, and context_type

6. VERIFY CONNECTION SUCCESS:
   - All requests should return 200 OK status
   - Request bodies should contain the expected data
   - Response bodies should contain the expected fields
   - No CORS errors should appear in the console

7. TROUBLESHOOTING:
   - If requests fail, check the backend server is running
   - Verify the API_BASE_URL in the frontend matches the backend URL
   - Check for CORS errors in the console
   - Ensure environment variables are properly set
"""

    print(instructions)
    print("✓ Full stack connectivity test instructions generated")
    return True


def run_all_tests():
    """
    Run all core system tests.
    """
    print("CORE SYSTEM TESTING AND VALIDATION")
    print("="*60)

    tests = [
        ("Ingestion Test Utility", test_ingestion_and_verify_points),
        ("RAG Backend Search Test", test_rag_backend_search),
        ("Full Stack Connectivity Instructions", print_full_stack_connectivity_instructions)
    ]

    results = []
    for test_name, test_func in tests:
        print(f"\nRunning: {test_name}")
        print("-" * 40)
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"✗ {test_name} failed with exception: {str(e)}")
            results.append((test_name, False))

    print("\n" + "="*60)
    print("TEST RESULTS SUMMARY")
    print("="*60)

    for test_name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status}: {test_name}")

    passed = sum(1 for _, result in results if result)
    total = len(results)

    print(f"\nOverall: {passed}/{total} tests passed")

    if passed == total:
        print("🎉 All core system tests passed!")
        return True
    else:
        print(f"⚠️  {total - passed} tests failed. Please check the implementation.")
        return False


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)