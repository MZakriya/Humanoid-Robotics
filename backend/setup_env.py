#!/usr/bin/env python3
"""
Setup script for the Physical AI RAG Backend environment.
This script helps create a virtual environment and install dependencies.
"""

import os
import sys
import subprocess
import platform

def create_virtual_environment():
    """Create a Python virtual environment for the project."""
    print("Creating virtual environment...")

    venv_path = os.path.join(os.getcwd(), "venv")

    # Determine the Python executable to use
    python_executable = sys.executable

    # Create virtual environment
    result = subprocess.run([python_executable, "-m", "venv", "venv"],
                          capture_output=True, text=True)

    if result.returncode != 0:
        print(f"Error creating virtual environment: {result.stderr}")
        return False

    print("Virtual environment created successfully.")
    return True

def install_dependencies():
    """Install project dependencies from requirements.txt."""
    print("Installing dependencies...")

    # Determine the path to pip based on the platform
    if platform.system() == "Windows":
        pip_path = os.path.join("venv", "Scripts", "pip")
    else:
        pip_path = os.path.join("venv", "bin", "pip")

    # Install dependencies
    result = subprocess.run([pip_path, "install", "-r", "requirements.txt"],
                          capture_output=True, text=True)

    if result.returncode != 0:
        print(f"Error installing dependencies: {result.stderr}")
        return False

    print("Dependencies installed successfully.")
    return True

def show_activation_instructions():
    """Display instructions for activating the virtual environment."""
    print("\nVirtual environment setup complete!")
    print("\nTo activate the virtual environment:")

    if platform.system() == "Windows":
        print("  venv\\Scripts\\activate")
    else:
        print("  source venv/bin/activate")

    print("\nTo run the application:")
    print("  uvicorn src.main:app --reload --port 8000")

    print("\nTo deactivate the virtual environment:")
    print("  deactivate")

def main():
    """Main setup function."""
    print("Physical AI RAG Backend Environment Setup")
    print("=" * 50)

    # Check if we're in the correct directory
    required_files = ["requirements.txt", "src"]
    missing_files = [f for f in required_files if not os.path.exists(f)]

    if missing_files:
        print(f"Error: Missing required files/directories: {missing_files}")
        print("Please run this script from the backend directory.")
        return 1

    # Check if virtual environment already exists
    if os.path.exists("venv"):
        response = input("Virtual environment already exists. Recreate? (y/N): ")
        if response.lower() != 'y':
            print("Setup cancelled.")
            return 0

    # Create virtual environment
    if not create_virtual_environment():
        return 1

    # Install dependencies
    if not install_dependencies():
        return 1

    # Show activation instructions
    show_activation_instructions()

    return 0

if __name__ == "__main__":
    sys.exit(main())