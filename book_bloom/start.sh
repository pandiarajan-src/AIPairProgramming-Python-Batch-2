#!/bin/bash
# BookBloom Startup Script

set -e

echo "🌸 BookBloom - Books Reborn, Knowledge Renewed"
echo "=============================================="

# Get script directory and navigate to project root
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
cd "$SCRIPT_DIR"

# Check if Python 3.12+ is available
python_cmd="python3"
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed"
    exit 1
fi

# Check Python version
python_version=$(python3 -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
echo "📍 Using Python $python_version"

# Check if uv is available
if command -v uv &> /dev/null; then
    echo "📦 Using uv for dependency management"
    
    # Navigate to bookbloom directory for uv operations
    cd bookbloom
    
    # Install dependencies with uv
    echo "Installing dependencies..."
    uv sync
    
    # Run with uv
    echo "🚀 Starting BookBloom with uv..."
    uv run python ../run.py
else
    echo "📦 Using pip for dependency management"
    
    # Create virtual environment if it doesn't exist
    if [ ! -d "venv" ]; then
        echo "Creating virtual environment..."
        python3 -m venv venv
    fi
    
    # Activate virtual environment
    source venv/bin/activate
    
    # Install dependencies
    echo "Installing dependencies..."
    cd bookbloom
    pip install -e .
    cd ..
    
    # Run the application
    echo "🚀 Starting BookBloom..."
    python run.py
fi