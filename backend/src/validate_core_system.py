"""
Core System Validation Script

This script validates all core functionalities of the Physical AI & Humanoid Robotics RAG system:
1. Tests ingestion functionality and Qdrant point count
2. Tests RAG backend search functionality
3. Validates system configuration and dependencies
"""

import asyncio
import sys
import subprocess
from pathlib import Path
import json
from datetime import datetime

# Add the src directory to the path so we can import modules
sys.path.insert(0, str(Path(__file__).parent))

try:
    from config import config
    from main import perform_vector_search, get_qdrant_client
    from ingest_content import ContentIngestor
except ImportError as e:
    print(f"⚠️  Import error - dependencies may not be installed: {e}")
    print("Please install the required dependencies before running validation.")
    sys.exit(1)


def validate_environment():
    """
    Validate environment variables and configuration.
    """
    print("VALIDATING ENVIRONMENT CONFIGURATION")
    print("="*50)

    validation_results = []

    # Check required configuration
    required_vars = [
        ('QDRANT_COLLECTION_NAME', config.QDRANT_COLLECTION_NAME, 'humanoid_text_chunks'),
        ('EMBEDDING_MODEL_NAME', config.EMBEDDING_MODEL_NAME, 'all-MiniLM-L6-v2'),
    ]

    for var_name, var_value, default_value in required_vars:
        if var_value and var_value != f'your-{var_name.lower()}-here' and var_value != default_value:
            print(f"✓ {var_name}: {var_value}")
            validation_results.append(True)
        else:
            print(f"⚠️  {var_name}: Using default value ({var_value})")
            validation_results.append(False)

    # Check optional but important variables
    optional_vars = [
        ('QDRANT_URL', config.QDRANT_URL),
        ('OPENAI_API_KEY', config.OPENAI_API_KEY),
        ('NEON_PG_URL', config.NEON_PG_URL),
    ]

    for var_name, var_value in optional_vars:
        if var_value and 'your-' not in var_value:
            print(f"✓ {var_name}: SET")
            validation_results.append(True)
        else:
            print(f"⚠️  {var_name}: Not set (this is OK for local testing)")
            validation_results.append(False)

    print(f"\nEnvironment validation: {sum(validation_results)}/{len(validation_results)} checks passed")
    return validation_results


def test_qdrant_connection():
    """
    Test Qdrant connection and get collection information.
    """
    print("\nTESTING QDRANT CONNECTION")
    print("="*50)

    try:
        client = get_qdrant_client()

        # Test connection by getting collections
        collections = client.get_collections()
        print(f"✓ Connected to Qdrant successfully")
        print(f"✓ Found {len(collections.collections)} collections")

        # Check if the default collection exists
        collection_names = [col.name for col in collections.collections]
        default_collection = config.QDRANT_COLLECTION_NAME
        if default_collection in collection_names:
            collection_info = client.get_collection(default_collection)
            print(f"✓ Collection '{default_collection}' exists with {collection_info.points_count} points")
        else:
            print(f"ℹ️  Collection '{default_collection}' does not exist (this is normal if no content has been ingested)")

        return True
    except Exception as e:
        print(f"✗ Qdrant connection failed: {str(e)}")
        return False


def test_ingestion_process():
    """
    Test the ingestion process with sample content.
    """
    print("\nTESTING INGESTION PROCESS")
    print("="*50)

    try:
        # Create sample content
        sample_docs_dir = Path("validation_sample_docs")
        sample_docs_dir.mkdir(exist_ok=True)

        # Create sample content about robotics concepts
        sample_content = f"""# Sample Module: Robot Kinematics and Dynamics

## Forward Kinematics

Forward kinematics is the process of determining the position and orientation of the end-effector based on the known joint angles and link parameters. This fundamental concept enables us to predict where the robot's tool or hand will be positioned in space given a specific configuration of joint angles.

## Inverse Kinematics

Inverse kinematics is the reverse process of forward kinematics, where we determine the joint angles required to achieve a desired end-effector position and orientation.

## Jacobian Matrices

The Jacobian matrix relates the joint velocities to the end-effector velocities. It is crucial for motion control and force control of robotic manipulators.

## ZMP and Bipedal Locomotion

The Zero Moment Point (ZMP) is a crucial concept in bipedal robotics that defines the point on the ground where the sum of all moments due to the ground reaction forces is zero. This concept is fundamental to understanding stable walking patterns in humanoid robots.

```
M = ∫ (r - r_zmp) × f dA = 0
```

### Key Properties:

1. **Stability Condition**: For stable walking, the ZMP must lie within the convex hull of the supporting foot/feet
2. **Support Polygon**: The area defined by the feet that constrains the ZMP position
3. **Walking Pattern Generation**: ZMP-based controllers generate stable walking gaits
"""

        sample_file = sample_docs_dir / "robotics_concepts.md"
        with open(sample_file, "w", encoding="utf-8") as f:
            f.write(sample_content)

        print(f"✓ Created sample content at {sample_file}")

        # Initialize the ingestor
        ingestor = ContentIngestor()

        # Use a test collection to avoid interfering with production data
        collection_name = "validation_test_collection"
        total_chunks = ingestor.process_content(
            source_path=str(sample_docs_dir),
            collection_name=collection_name
        )

        print(f"✓ Ingested {total_chunks} chunks into collection '{collection_name}'")

        # Verify point count in Qdrant collection
        collection_info = ingestor.qdrant_client.get_collection(collection_name)
        point_count = collection_info.points_count

        print(f"✓ Qdrant collection '{collection_name}' contains {point_count} points")

        # Clean up the test collection
        ingestor.qdrant_client.delete_collection(collection_name)
        print(f"✓ Cleaned up test collection '{collection_name}'")

        # Clean up sample files
        import shutil
        shutil.rmtree(sample_docs_dir, ignore_errors=True)
        print(f"✓ Cleaned up sample content directory")

        return total_chunks > 0

    except Exception as e:
        print(f"✗ Ingestion test failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def test_rag_search_functionality():
    """
    Test RAG search functionality with sample queries.
    """
    print("\nTESTING RAG SEARCH FUNCTIONALITY")
    print("="*50)

    sample_queries = [
        "What is forward kinematics?",
        "Explain Jacobian matrices",
        "What is the role of ZMP in bipedal locomotion?",
        "How does inverse kinematics work?"
    ]

    all_success = True

    for query in sample_queries:
        print(f"\nTesting query: '{query}'")
        try:
            # Run the vector search directly
            results = asyncio.run(perform_vector_search(query, top_k=3))

            print(f"  ✓ Found {len(results)} results")
            if len(results) > 0:
                print(f"  ✓ Top result score: {results[0]['score']:.4f}")
                print(f"  ✓ Top result preview: {results[0]['text'][:100]}...")

                # Show metadata for the top result
                metadata = results[0]['metadata']
                print(f"  ✓ Metadata: {list(metadata.keys()) if metadata else 'None'}")
            else:
                print(f"  ℹ️  No results found for this query (this may be normal if no content has been ingested)")

        except Exception as e:
            print(f"  ✗ Query failed: {str(e)}")
            all_success = False

    return all_success


def generate_validation_report():
    """
    Generate a comprehensive validation report.
    """
    print("\n" + "="*60)
    print("CORE SYSTEM VALIDATION REPORT")
    print("="*60)
    print(f"Validation Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Working Directory: {Path.cwd()}")
    print()

    # Run all validation tests
    env_results = validate_environment()
    qdrant_ok = test_qdrant_connection()
    ingestion_ok = test_ingestion_process()
    search_ok = test_rag_search_functionality()

    print("\n" + "="*60)
    print("VALIDATION SUMMARY")
    print("="*60)

    tests = [
        ("Environment Configuration", len([r for r in env_results if r]) > 0),
        ("Qdrant Connection", qdrant_ok),
        ("Ingestion Process", ingestion_ok),
        ("RAG Search Functionality", search_ok)
    ]

    for test_name, result in tests:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status}: {test_name}")

    passed = sum(1 for _, result in tests if result)
    total = len(tests)

    print(f"\nOverall: {passed}/{total} validation checks passed")

    if passed == total:
        print("\n🎉 All core system validations passed!")
        print("The RAG system is ready for use.")
    else:
        print(f"\n⚠️  {total - passed} validation checks failed.")
        print("Please review the issues above and address them before using the system.")

    return passed == total


def main():
    """
    Main function to run the validation.
    """
    print("CORE SYSTEM VALIDATION")
    print("="*60)
    print("Validating the Physical AI & Humanoid Robotics RAG system...")
    print()

    try:
        success = generate_validation_report()
        return 0 if success else 1
    except KeyboardInterrupt:
        print("\n⚠️  Validation interrupted by user.")
        return 1
    except Exception as e:
        print(f"\n✗ Validation failed with error: {str(e)}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())