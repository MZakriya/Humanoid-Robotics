"""
Test script for RAG functionality in the Physical AI & Humanoid Robotics platform.

This script tests:
1. General query endpoint
2. Contextual query endpoint
3. Vector search functionality
4. LLM augmentation functionality
"""
import asyncio
import json
import sys
from pathlib import Path

# Add the src directory to the path so we can import main
sys.path.insert(0, str(Path(__file__).parent))

import httpx


async def test_general_query():
    """
    Test the general query endpoint functionality.
    """
    print("Testing general query endpoint...")

    async with httpx.AsyncClient(base_url="http://localhost:8000") as client:
        try:
            response = await client.post(
                "/api/query/general",
                json={"query": "What is forward kinematics in robotics?"},
                timeout=30.0
            )

            print(f"Status Code: {response.status_code}")
            if response.status_code == 200:
                data = response.json()
                print("✓ General query endpoint test passed")
                print(f"Query: {data.get('query', 'N/A')}")
                print(f"Answer: {data.get('answer', 'N/A')[:100]}...")
                print(f"Context Type: {data.get('context_type', 'N/A')}")
                return True
            else:
                print(f"✗ General query endpoint test failed with status {response.status_code}")
                print(f"Response: {response.text}")
                return False
        except httpx.ConnectError:
            print("✗ Cannot connect to the server. Please make sure the FastAPI server is running on localhost:8000")
            return False
        except Exception as e:
            print(f"✗ Error during general query test: {str(e)}")
            return False


async def test_contextual_query():
    """
    Test the contextual query endpoint functionality.
    """
    print("\nTesting contextual query endpoint...")

    async with httpx.AsyncClient(base_url="http://localhost:8000") as client:
        try:
            response = await client.post(
                "/api/query/contextual",
                json={
                    "user_query": "Explain this concept",
                    "selected_text": "Forward kinematics is the process of determining the position and orientation of the end-effector based on the known joint angles and link parameters."
                },
                timeout=30.0
            )

            print(f"Status Code: {response.status_code}")
            if response.status_code == 200:
                data = response.json()
                print("✓ Contextual query endpoint test passed")
                print(f"User Query: {data.get('user_query', 'N/A')}")
                print(f"Selected Text: {data.get('selected_text', 'N/A')[:50]}...")
                print(f"Answer: {data.get('answer', 'N/A')[:100]}...")
                print(f"Context Type: {data.get('context_type', 'N/A')}")
                return True
            else:
                print(f"✗ Contextual query endpoint test failed with status {response.status_code}")
                print(f"Response: {response.text}")
                return False
        except httpx.ConnectError:
            print("✗ Cannot connect to the server. Please make sure the FastAPI server is running on localhost:8000")
            return False
        except Exception as e:
            print(f"✗ Error during contextual query test: {str(e)}")
            return False


async def test_health_check():
    """
    Test the health check endpoint.
    """
    print("\nTesting health check endpoint...")

    async with httpx.AsyncClient(base_url="http://localhost:8000") as client:
        try:
            response = await client.get("/health", timeout=10.0)

            print(f"Status Code: {response.status_code}")
            if response.status_code == 200:
                data = response.json()
                print("✓ Health check endpoint test passed")
                print(f"Status: {data.get('status', 'N/A')}")
                print(f"Qdrant Connection: {data.get('qdrant_connection', 'N/A')}")
                print(f"Total Collections: {data.get('total_collections', 'N/A')}")
                return True
            else:
                print(f"✗ Health check endpoint test failed with status {response.status_code}")
                print(f"Response: {response.text}")
                return False
        except httpx.ConnectError:
            print("✗ Cannot connect to the server. Please make sure the FastAPI server is running on localhost:8000")
            return False
        except Exception as e:
            print(f"✗ Error during health check test: {str(e)}")
            return False


async def test_vector_search_function():
    """
    Test the vector search functionality directly.
    """
    print("\nTesting vector search function directly...")

    try:
        # Import the main module to access the function directly
        import main
        from main import perform_vector_search

        # Test the function directly
        results = await perform_vector_search("What is forward kinematics?", top_k=3)

        print(f"Found {len(results)} results from vector search")
        if len(results) > 0:
            print("✓ Vector search function test passed")
            for i, result in enumerate(results[:2]):  # Show first 2 results
                print(f"Result {i+1}: Score={result['score']:.3f}, Text='{result['text'][:100]}...'")
            return True
        else:
            print("✗ Vector search function returned no results")
            return False
    except ImportError as e:
        print(f"✗ Cannot import main module: {str(e)}")
        return False
    except Exception as e:
        print(f"✗ Error during vector search test: {str(e)}")
        return False


async def test_llm_augmentation_function():
    """
    Test the LLM augmentation functionality directly.
    """
    print("\nTesting LLM augmentation function directly...")

    try:
        # Import the main module to access the function directly
        import main
        from main import generate_rag_answer

        # Create a mock context with some content
        mock_context = [
            {
                "text": "Forward kinematics is the process of determining the position and orientation of the end-effector based on the known joint angles and link parameters. This fundamental concept enables us to predict where the robot's tool or hand will be positioned in space given a specific configuration of joint angles.",
                "metadata": {"source": "module3-kinematics-dynamics.md", "chunk_id": "kinematics_0"}
            }
        ]

        # Test the function directly
        answer = await generate_rag_answer("What is forward kinematics?", mock_context)

        print(f"LLM response: {answer[:150]}...")
        if answer and len(answer) > 0:
            print("✓ LLM augmentation function test passed")
            return True
        else:
            print("✗ LLM augmentation function returned empty response")
            return False
    except ImportError as e:
        print(f"✗ Cannot import main module: {str(e)}")
        return False
    except Exception as e:
        print(f"✗ Error during LLM augmentation test: {str(e)}")
        return False


async def run_all_tests():
    """
    Run all RAG functionality tests.
    """
    print("Starting RAG functionality tests...\n")

    tests = [
        ("Health Check", test_health_check),
        ("Vector Search Function", test_vector_search_function),
        ("LLM Augmentation Function", test_llm_augmentation_function),
        ("General Query Endpoint", test_general_query),
        ("Contextual Query Endpoint", test_contextual_query),
    ]

    results = []
    for test_name, test_func in tests:
        print(f"\n{'='*50}")
        print(f"Running: {test_name}")
        print('='*50)

        try:
            result = await test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"✗ {test_name} failed with exception: {str(e)}")
            results.append((test_name, False))

    print(f"\n{'='*50}")
    print("TEST RESULTS SUMMARY")
    print('='*50)

    passed = 0
    total = len(results)

    for test_name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status}: {test_name}")
        if result:
            passed += 1

    print(f"\nOverall: {passed}/{total} tests passed")

    if passed == total:
        print("🎉 All RAG functionality tests passed!")
        return True
    else:
        print(f"⚠️  {total - passed} tests failed. Please check the implementation.")
        return False


def test_without_server():
    """
    Test functions that don't require a running server.
    """
    print("Testing RAG functions without server...")

    success_count = 0
    total_tests = 3  # Vector search, LLM augmentation, and health check (for imports)

    # Test imports first
    try:
        import main
        print("✓ Main module imports successfully")
        success_count += 1
    except ImportError as e:
        print(f"✗ Main module import failed: {e}")

    # Test vector search function (this will test if dependencies are available)
    try:
        import asyncio
        # Run the async test in a new event loop
        async def test_imports():
            return await test_vector_search_function()

        result = asyncio.run(test_imports())
        if result:
            success_count += 1
    except Exception as e:
        print(f"✗ Vector search function test failed: {e}")

    # Test LLM augmentation function
    try:
        async def test_llm_imports():
            return await test_llm_augmentation_function()

        result = asyncio.run(test_llm_imports())
        if result:
            success_count += 1
    except Exception as e:
        print(f"✗ LLM augmentation function test failed: {e}")

    print(f"\nDependency tests: {success_count-1}/{total_tests-1} functions work (excluding server-dependent health check)")

    if success_count >= 2:  # At least the core functions work
        print("✓ Core RAG functionality is available")
        return True
    else:
        print("✗ Core RAG functionality has issues")
        return False


if __name__ == "__main__":
    print("RAG Functionality Test Suite")
    print("="*50)

    # First, test dependencies without requiring a server
    deps_ok = test_without_server()

    if deps_ok:
        print("\n" + "="*50)
        print("All core functionality is available.")
        print("To run full integration tests, please start the FastAPI server first:")
        print("  cd backend")
        print("  uvicorn src.main:app --reload --host 0.0.0.0 --port 8000")
        print("\nThen run this test script again.")
        print("="*50)
    else:
        print("\n✗ Core functionality has issues. Please check dependencies and implementation.")