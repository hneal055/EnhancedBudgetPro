#!/bin/bash
# Enhanced Budget Pro - Automated Daily Startup Script
# Version: 1.0.0
# Last Updated: December 14, 2025

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}================================================${NC}"
echo -e "${BLUE}   Enhanced Budget Pro - Daily Startup${NC}"
echo -e "${BLUE}================================================${NC}"
echo ""

# Get project directory
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$PROJECT_DIR"

# Step 1: Check Git status
echo -e "${YELLOW}📦 Checking Git status...${NC}"
git fetch origin main --quiet
BEHIND=$(git rev-list --count HEAD..origin/main 2>/dev/null || echo "0")
if [ "$BEHIND" -gt 0 ]; then
    echo -e "${YELLOW}⚠️  You are $BEHIND commits behind origin/main${NC}"
    read -p "Pull latest changes? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        git pull origin main
        echo -e "${GREEN}✅ Updated to latest version${NC}"
    fi
else
    echo -e "${GREEN}✅ Up to date with origin/main${NC}"
fi
echo ""

# Step 2: Check Python version
echo -e "${YELLOW}�� Checking Python environment...${NC}"
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
    echo -e "${GREEN}✅ Python $PYTHON_VERSION found${NC}"
else
    echo -e "${RED}❌ Python 3 not found. Please install Python 3.12+${NC}"
    exit 1
fi
echo ""

# Step 3: Check/activate virtual environment
echo -e "${YELLOW}🔧 Setting up virtual environment...${NC}"
if [ -d ".venv" ]; then
    echo -e "${GREEN}✅ Virtual environment exists${NC}"
    source .venv/bin/activate || source .venv/Scripts/activate
    echo -e "${GREEN}✅ Virtual environment activated${NC}"
else
    echo -e "${YELLOW}⚠️  No virtual environment found. Creating one...${NC}"
    python3 -m venv .venv
    source .venv/bin/activate || source .venv/Scripts/activate
    echo -e "${GREEN}✅ Virtual environment created and activated${NC}"
fi
echo ""

# Step 4: Install/update dependencies
echo -e "${YELLOW}📚 Checking dependencies...${NC}"
if [ -f "requirements.txt" ]; then
    pip install -q --upgrade pip
    pip install -q -r requirements.txt
    echo -e "${GREEN}✅ Dependencies up to date${NC}"
else
    echo -e "${RED}❌ requirements.txt not found${NC}"
    exit 1
fi
echo ""

# Step 5: Clear Python cache
echo -e "${YELLOW}🧹 Clearing Python cache...${NC}"
find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
find . -type f -name "*.pyc" -delete 2>/dev/null || true
echo -e "${GREEN}✅ Cache cleared${NC}"
echo ""

# Step 6: Kill any existing Streamlit processes
echo -e "${YELLOW}🔪 Checking for existing Streamlit processes...${NC}"
if pgrep -f "streamlit" > /dev/null; then
    pkill -f "streamlit" 2>/dev/null || true
    sleep 2
    echo -e "${GREEN}✅ Stopped existing Streamlit processes${NC}"
else
    echo -e "${GREEN}✅ No existing processes found${NC}"
fi
echo ""

# Step 7: Check for port availability
echo -e "${YELLOW}🔌 Checking port 8501...${NC}"
if lsof -Pi :8501 -sTCP:LISTEN -t >/dev/null 2>&1; then
    echo -e "${YELLOW}⚠️  Port 8501 is in use. Killing process...${NC}"
    kill $(lsof -t -i:8501) 2>/dev/null || true
    sleep 2
fi
echo -e "${GREEN}✅ Port 8501 available${NC}"
echo ""

# Step 8: Display project status
echo -e "${BLUE}================================================${NC}"
echo -e "${BLUE}   Project Status${NC}"
echo -e "${BLUE}================================================${NC}"
echo -e "${GREEN}📁 Project Directory:${NC} $PROJECT_DIR"
echo -e "${GREEN}🎯 Current Branch:${NC} $(git branch --show-current)"
echo -e "${GREEN}📝 Latest Commit:${NC} $(git log -1 --pretty=format:'%h - %s')"
echo -e "${GREEN}🐍 Python Version:${NC} $PYTHON_VERSION"
echo -e "${GREEN}🔧 Virtual Env:${NC} Activated (.venv)"
echo ""

# Step 9: Prompt for startup mode
echo -e "${BLUE}================================================${NC}"
echo -e "${BLUE}   Launch Options${NC}"
echo -e "${BLUE}================================================${NC}"
echo "1) Start Streamlit UI (Recommended)"
echo "2) Start Flask Web App"
echo "3) Run Tests"
echo "4) Exit (manual start)"
echo ""
read -p "Select option (1-4): " -n 1 -r OPTION
echo ""
echo ""

case $OPTION in
    1)
        echo -e "${GREEN}🚀 Starting Streamlit UI...${NC}"
        echo ""
        echo -e "${BLUE}================================================${NC}"
        echo -e "${GREEN}   Streamlit will be available at:${NC}"
        echo -e "${GREEN}   http://localhost:8501${NC}"
        echo -e "${BLUE}================================================${NC}"
        echo ""
        sleep 2
        streamlit run ui_app.py
        ;;
    2)
        echo -e "${GREEN}🚀 Starting Flask Web App...${NC}"
        echo ""
        echo -e "${BLUE}================================================${NC}"
        echo -e "${GREEN}   Flask will be available at:${NC}"
        echo -e "${GREEN}   http://localhost:5000${NC}"
        echo -e "${BLUE}================================================${NC}"
        echo ""
        sleep 2
        python web_app.py
        ;;
    3)
        echo -e "${GREEN}🧪 Running test suite...${NC}"
        echo ""
        pytest tests/ -v
        echo ""
        echo -e "${GREEN}✅ Tests complete${NC}"
        echo ""
        read -p "Start Streamlit UI? (y/n) " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            streamlit run ui_app.py
        fi
        ;;
    4)
        echo -e "${YELLOW}Manual mode selected.${NC}"
        echo ""
        echo -e "${GREEN}To start manually:${NC}"
        echo "  - Streamlit: ${BLUE}streamlit run ui_app.py${NC}"
        echo "  - Flask:     ${BLUE}python web_app.py${NC}"
        echo "  - CLI:       ${BLUE}python -m src.cli analyze --input script.fdx${NC}"
        echo ""
        ;;
    *)
        echo -e "${RED}Invalid option. Exiting.${NC}"
        exit 1
        ;;
esac

# Exit
exit 0
