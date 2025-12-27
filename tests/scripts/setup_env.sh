#!/bin/bash

# Enhanced Budget Pro Environment Setup Script

set -e  # Exit on error

echo "🎬 Enhanced Budget Pro - Environment Setup"
echo "=========================================="

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Check Python version
echo -e "${BLUE}Checking Python version...${NC}"
python_version=$(python3 -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')
required_version="3.10"

if [[ $(echo "$python_version >= $required_version" | bc -l) -eq 1 ]]; then
    echo -e "${GREEN}✓ Python $python_version detected${NC}"
else
    echo -e "${RED}✗ Python $required_version+ required, found $python_version${NC}"
    exit 1
fi

# Check for virtualenv/venv
echo -e "${BLUE}Checking for virtual environment tool...${NC}"
if command -v virtualenv &> /dev/null; then
    echo -e "${GREEN}✓ virtualenv found${NC}"
    VENV_TOOL="virtualenv"
elif python3 -m venv --help &> /dev/null; then
    echo -e "${GREEN}✓ venv module found${NC}"
    VENV_TOOL="venv"
else
    echo -e "${YELLOW}⚠ No virtual environment tool found. Installing virtualenv...${NC}"
    pip3 install virtualenv
    VENV_TOOL="virtualenv"
fi

# Create virtual environment
echo -e "${BLUE}Creating virtual environment...${NC}"
if [[ "$VENV_TOOL" == "venv" ]]; then
    python3 -m venv .venv
else
    virtualenv .venv
fi

echo -e "${GREEN}✓ Virtual environment created${NC}"

# Activate virtual environment
echo -e "${BLUE}Activating virtual environment...${NC}"
source .venv/bin/activate

# Upgrade pip
echo -e "${BLUE}Upgrading pip...${NC}"
pip install --upgrade pip setuptools wheel

# Install requirements
echo -e "${BLUE}Installing requirements...${NC}"
if [[ "$1" == "--minimal" ]]; then
    echo -e "${YELLOW}Installing minimal requirements...${NC}"
    pip install -r requirements-minimal.txt
elif [[ "$1" == "--dev" ]]; then
    echo -e "${YELLOW}Installing development requirements...${NC}"
    pip install -r requirements-dev.txt
elif [[ "$1" == "--full" ]]; then
    echo -e "${YELLOW}Installing all requirements...${NC}"
    pip install -r requirements.txt
    pip install -r requirements-dev.txt
else
    echo -e "${YELLOW}Installing production requirements...${NC}"
    pip install -r requirements.txt
fi

# Install package in development mode
echo -e "${BLUE}Installing package in development mode...${NC}"
pip install -e .

# Install pre-commit hooks if dev mode
if [[ "$1" == "--dev" ]] || [[ "$1" == "--full" ]]; then
    echo -e "${BLUE}Setting up pre-commit hooks...${NC}"
    pre-commit install
fi

# Create necessary directories
echo -e "${BLUE}Creating directories...${NC}"
mkdir -p data/exports data/uploads logs config

# Create .env file if it doesn't exist
if [[ ! -f .env ]]; then
    echo -e "${BLUE}Creating .env file...${NC}"
    cat > .env << EOF
# Enhanced Budget Pro Environment Variables
ENVIRONMENT=development
LOG_LEVEL=INFO
DATABASE_URL=sqlite:///data/budget.db
REDIS_URL=redis://localhost:6379/0
SECRET_KEY=$(python3 -c "import secrets; print(secrets.token_urlsafe(32))")
API_TIMEOUT=30
UPLOAD_FOLDER=data/uploads
EXPORT_FOLDER=data/exports
MAX_UPLOAD_SIZE=104857600  # 100MB

# Optional API Keys (uncomment and add your keys)
# STUDIOBINDER_API_KEY=your_key_here
# MONDAY_API_KEY=your_key_here
# AIRTABLE_API_KEY=your_key_here
# GOOGLE_API_KEY=your_key_here
EOF
    echo -e "${GREEN}✓ .env file created${NC}"
fi

# Run initial checks
echo -e "${BLUE}Running initial checks...${NC}"
python -c "import pandas; print(f'✓ pandas {pandas.__version__}')"
python -c "import streamlit; print(f'✓ streamlit {streamlit.__version__}')"
python -c "import plotly; print(f'✓ plotly {plotly.__version__}')"

echo ""
echo -e "${GREEN}==========================================${NC}"
echo -e "${GREEN}🎉 Setup Complete!${NC}"
echo ""
echo -e "${YELLOW}To activate the virtual environment:${NC}"
echo "  source .venv/bin/activate"
echo ""
echo -e "${YELLOW}To run the application:${NC}"
echo "  make run"
echo "  or"
echo "  streamlit run ui_app.py"
echo ""
echo -e "${YELLOW}For development:${NC}"
echo "  make test      # Run tests"
echo "  make lint      # Run linters"
echo "  make format    # Format code"
echo ""
echo -e "${GREEN}==========================================${NC}"