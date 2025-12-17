"""
Test script for content ingestion functionality.
This script tests the ingestion process with sample content.
"""

import os
import sys
from pathlib import Path

# Add the src directory to the path so we can import ingest_content
sys.path.insert(0, str(Path(__file__).parent))

from ingest_content import ContentIngestor


def create_sample_content():
    """
    Create sample markdown content for testing the ingestion process.
    """
    sample_docs_dir = Path("sample_docs")
    sample_docs_dir.mkdir(exist_ok=True)

    # Create a sample module file
    sample_content = """# Module 3: Kinematics and Dynamics

## Forward Kinematics

Forward kinematics is the process of determining the position and orientation of the end-effector based on the known joint angles and link parameters. This fundamental concept enables us to predict where the robot's tool or hand will be positioned in space given a specific configuration of joint angles.

### Mathematical Foundation

Forward kinematics relies on homogeneous transformation matrices to represent position and orientation in 3D space:

```
T = [R  p]
    [0  1]
```

Where:
- R is a 3×3 rotation matrix
- p is a 3×1 position vector
- The bottom row [0 0 0 1] maintains homogeneity

### Denavit-Hartenberg (DH) Convention

The DH convention provides a systematic method for assigning coordinate frames to each joint in a kinematic chain:

1. **Z-axis**: Along the joint axis of rotation or translation
2. **X-axis**: Along the common normal between current and next joint axes
3. **Y-axis**: Completes the right-handed coordinate system (Y = Z × X)

## Inverse Kinematics

Inverse kinematics is the reverse process of forward kinematics, where we determine the joint angles required to achieve a desired end-effector position and orientation.

### Analytical Solutions

For simple manipulators, analytical solutions to inverse kinematics can be derived using geometric or algebraic methods.

### Numerical Solutions

For complex manipulators, numerical methods such as the Jacobian-based methods are often used.

## Jacobian Matrices

The Jacobian matrix relates the joint velocities to the end-effector velocities. It is crucial for motion control and force control of robotic manipulators.

### Differential Kinematics

Differential kinematics describes the relationship between joint space velocities and Cartesian space velocities:

```
ẋ = J(q)q̇
```

Where:
- ẋ is the end-effector velocity vector
- J(q) is the Jacobian matrix
- q̇ is the joint velocity vector
"""

    with open(sample_docs_dir / "module3-kinematics-dynamics.md", "w", encoding="utf-8") as f:
        f.write(sample_content)

    print(f"Created sample content at {sample_docs_dir / 'module3-kinematics-dynamics.md'}")
    return str(sample_docs_dir)


def test_ingestion():
    """
    Test the content ingestion process with sample content.
    """
    print("Testing content ingestion process...")

    # Create sample content
    sample_dir = create_sample_content()

    # Initialize the ingestor
    ingestor = ContentIngestor()

    try:
        # Process the sample content
        total_chunks = ingestor.process_content(
            source_path=sample_dir,
            collection_name="test_humanoid_text_chunks"
        )

        print(f"Ingestion test completed successfully! Processed {total_chunks} chunks.")
        return True

    except Exception as e:
        print(f"Error during ingestion test: {str(e)}")
        return False


def test_qdrant_connection():
    """
    Test the Qdrant connection.
    """
    print("Testing Qdrant connection...")

    try:
        ingestor = ContentIngestor()
        client = ingestor.qdrant_client

        # Try to get collections to verify connection
        collections = client.get_collections()
        print(f"Qdrant connection successful! Found {len(collections.collections)} collections.")
        return True

    except Exception as e:
        print(f"Error connecting to Qdrant: {str(e)}")
        return False


def main():
    """
    Main function to run the tests.
    """
    print("Running content ingestion tests...\n")

    # Test Qdrant connection first
    if not test_qdrant_connection():
        print("Qdrant connection test failed. Please check your Qdrant configuration.")
        return 1

    # Test ingestion process
    if not test_ingestion():
        print("Ingestion test failed.")
        return 1

    print("\nAll tests passed successfully!")
    return 0


if __name__ == "__main__":
    exit(main())