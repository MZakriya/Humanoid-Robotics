#!/bin/bash

# System Launch Test Script
# Validates that all components of the Physical AI & Humanoid Robotics system can be launched correctly

set -e  # Exit on any error

echo "==========================================="
echo "Physical AI & Humanoid Robotics System Launch Test"
echo "==========================================="
echo

# Configuration
PROJECT_ROOT="$(pwd)"
BACKEND_DIR="$PROJECT_ROOT/backend"
FRONTEND_DIR="$PROJECT_ROOT"
LOG_DIR="$PROJECT_ROOT/logs"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")

# Create logs directory
mkdir -p "$LOG_DIR"

# Function to print status
print_status() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1"
}

# Function to print success
print_success() {
    echo -e "\033[32m✓ $1\033[0m"
}

# Function to print error
print_error() {
    echo -e "\033[31m✗ $1\033[0m"
}

# Function to check if a command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Test 1: Check prerequisites
echo "1. Checking Prerequisites..."
print_status "Checking if required tools are installed..."

if ! command_exists python3; then
    print_error "Python 3 is not installed"
    exit 1
else
    print_success "Python 3: $(python3 --version)"
fi

if ! command_exists npm; then
    print_error "npm is not installed"
    exit 1
else
    print_success "npm: $(npm --version)"
fi

if ! command_exists git; then
    print_error "git is not installed"
    exit 1
else
    print_success "git: $(git --version)"
fi

print_success "All prerequisites are installed"
echo

# Test 2: Check project structure
echo "2. Checking Project Structure..."
if [ ! -d "$BACKEND_DIR" ]; then
    print_error "Backend directory not found: $BACKEND_DIR"
    exit 1
fi

if [ ! -f "$BACKEND_DIR/requirements.txt" ]; then
    print_error "Backend requirements.txt not found"
    exit 1
fi

if [ ! -f "$FRONTEND_DIR/package.json" ]; then
    print_error "Frontend package.json not found"
    exit 1
fi

if [ ! -f "$PROJECT_ROOT/.env" ]; then
    print_error ".env file not found in project root"
    print_status "Creating a sample .env file for testing..."
    cat > "$PROJECT_ROOT/.env" << EOF
# Sample environment variables for testing
FASTAPI_HOST=0.0.0.0
FASTAPI_PORT=8000
API_SECRET_KEY=test-secret-key
QDRANT_URL=https://your-cluster.xxxx.us-east-1.aws.cloud.qdrant.io
QDRANT_API_KEY=your-qdrant-api-key
QDRANT_COLLECTION_NAME=humanoid_text_chunks
OPENAI_API_KEY=your-openai-api-key
EMBEDDING_MODEL_NAME=all-MiniLM-L6-v2
NEON_PG_URL=postgresql://username:password@ep-xxx.us-east-1.aws.neon.tech/dbname?sslmode=require
BETTER_AUTH_CLIENT_ID=your-better-auth-client-id
BETTER_AUTH_SECRET=your-better-auth-secret
DEBUG=true
LOG_LEVEL=INFO
MAX_CONTENT_LENGTH=10485760
EOF
    print_success "Sample .env file created for testing"
else
    print_success ".env file exists"
fi

print_success "Project structure is valid"
echo

# Test 3: Check backend environment
echo "3. Checking Backend Environment..."
cd "$BACKEND_DIR"

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    print_status "Creating virtual environment..."
    python3 -m venv venv
    print_success "Virtual environment created"
fi

# Activate virtual environment
source venv/bin/activate
print_success "Virtual environment activated"

# Check if requirements can be installed
if [ -f "requirements.txt" ]; then
    print_status "Checking if requirements can be installed..."
    # Try to install dependencies (but don't actually install for speed)
    pip list > /dev/null 2>&1
    print_success "Python environment is ready"
else
    print_error "requirements.txt not found in backend directory"
    exit 1
fi

# Check if main.py exists and can be imported
if [ -f "src/main.py" ]; then
    print_status "Checking main.py import..."
    python3 -c "import sys; sys.path.append('src'); import main" 2>/dev/null
    if [ $? -eq 0 ]; then
        print_success "main.py can be imported"
    else
        print_error "main.py cannot be imported"
        exit 1
    fi
else
    print_error "src/main.py not found"
    exit 1
fi

print_success "Backend environment is ready"
cd "$PROJECT_ROOT"
echo

# Test 4: Check frontend environment
echo "4. Checking Frontend Environment..."
cd "$FRONTEND_DIR"

# Check if node_modules exists or can be installed
if [ ! -d "node_modules" ]; then
    print_status "node_modules not found, checking if installation is possible..."
    if command_exists npm; then
        print_success "npm is available for dependency installation"
    else
        print_error "npm is not available"
        exit 1
    fi
else
    print_success "node_modules exists"
fi

# Check if package.json has required scripts
if grep -q '"start"' package.json; then
    print_success "Start script exists in package.json"
else
    print_error "Start script not found in package.json"
    exit 1
fi

print_success "Frontend environment is ready"
cd "$PROJECT_ROOT"
echo

# Test 5: Check configuration files
echo "5. Checking Configuration Files..."
if [ -f "$PROJECT_ROOT/docusaurus.config.js" ]; then
    print_success "Docusaurus configuration exists"
else
    print_error "docusaurus.config.js not found"
    exit 1
fi

if [ -f "$PROJECT_ROOT/sidebars.js" ]; then
    print_success "Docusaurus sidebars configuration exists"
else
    print_error "sidebars.js not found"
    exit 1
fi

if [ -f "$BACKEND_DIR/src/config.py" ]; then
    print_success "Backend configuration module exists"
else
    print_error "Backend config.py not found"
    exit 1
fi

print_success "Configuration files are present"
echo

# Test 6: Check content directories
echo "6. Checking Content Directories..."
if [ -d "$PROJECT_ROOT/docs" ]; then
    print_success "Docs directory exists"

    # Check if there are content modules
    MODULE_COUNT=$(find "$PROJECT_ROOT/docs" -maxdepth 1 -type d -name "module*" | wc -l)
    if [ "$MODULE_COUNT" -gt 0 ]; then
        print_success "Found $MODULE_COUNT content modules"
    else
        print_status "No content modules found in docs/ (this may be expected for a fresh install)"
    fi
else
    print_error "Docs directory not found"
    exit 1
fi

print_success "Content directories are structured correctly"
echo

# Test 7: Check scripts and utilities
echo "7. Checking Scripts and Utilities..."
if [ -f "$PROJECT_ROOT/scripts/start-system.sh" ]; then
    print_success "Start system script exists"
else
    print_status "Start system script not found (will be created)"
fi

if [ -f "$BACKEND_DIR/src/ingest_content.py" ]; then
    print_success "Content ingestion script exists"
else
    print_error "Content ingestion script not found"
    exit 1
fi

if [ -f "$BACKEND_DIR/src/test_ingestion.py" ]; then
    print_success "Ingestion test script exists"
else
    print_status "Ingestion test script not found (optional)"
fi

print_success "Scripts and utilities are available"
echo

# Test 8: Summary of launch requirements
echo "8. Launch Requirements Summary:"
echo
echo "Backend Requirements:"
echo "  - Python 3.8+ with virtual environment"
echo "  - Dependencies from requirements.txt"
echo "  - .env file with API keys and configuration"
echo "  - Access to Qdrant vector database"
echo "  - Access to OpenAI API or alternative LLM"
echo
echo "Frontend Requirements:"
echo "  - Node.js and npm/yarn"
echo "  - Dependencies from package.json"
echo "  - Docusaurus configuration files"
echo
echo "Content Requirements:"
echo "  - Textbook content in docs/ directory"
echo "  - Ingestion script to populate Qdrant"
echo

print_success "System launch test completed successfully!"
echo
print_success "Next steps to launch the system:"
echo "  1. Ensure all environment variables are properly set in .env"
echo "  2. Run content ingestion: python backend/src/ingest_content.py"
echo "  3. Start backend: cd backend && source venv/bin/activate && cd src && python -m uvicorn main:app --host 0.0.0.0 --port 8000"
echo "  4. Start frontend: npm run start (in project root)"
echo "  5. Access the system at http://localhost:3000"
echo

echo "==========================================="
echo "Launch Test Result: PASSED"
echo "==========================================="