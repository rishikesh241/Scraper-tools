#!/usr/bin/env bash

# Set visual green text (similar to Windows color 0A)
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Ensure script runs in its own directory
cd "$(dirname "$0")" || exit 1

echo ""
echo "============================================================"
echo -e "${GREEN}  ExamTopics Scraper - Dependency Installer${NC}"
echo "============================================================"
echo ""

# Helper function for failure
failed() {
    echo ""
    echo "============================================================"
    echo -e "${RED}  Install failed. Check error above.${NC}"
    echo "============================================================"
    echo ""
    read -p "Press [Enter] to exit..."
    exit 1
}

# Check if requirements.txt exists
if [ ! -f "requirements.txt" ]; then
    echo -e "${RED}[ERROR] requirements.txt not found.${NC}"
    echo "Run this file from the project folder."
    echo ""
    read -p "Press [Enter] to exit..."
    exit 1
fi

# Detect Python 3 command on macOS
if command -v python3 >/dev/null 2>&1; then
    PY_CMD="python3"
elif command -v python >/dev/null 2>&1; then
    PY_CMD="python"
else
    echo -e "${RED}[ERROR] Python not found in PATH.${NC}"
    echo "Install Python 3, then run this file again."
    echo ""
    read -p "Press [Enter] to exit..."
    exit 1
fi

# [1/4] Create local virtual environment
if [ ! -f ".venv/bin/python" ]; then
    echo "[1/4] Creating local virtual environment..."
    $PY_CMD -m venv .venv || failed
else
    echo "[1/4] Local virtual environment already exists."
fi

# [2/4] Activate virtual environment
echo "[2/4] Activating virtual environment..."
if [ -f ".venv/bin/activate" ]; then
    source .venv/bin/activate || failed
else
    echo -e "${RED}[ERROR] Activation script not found in .venv/bin/activate${NC}"
    failed
fi

# [3/4] Install Python packages
echo "[3/4] Installing Python packages..."
python -m pip install --upgrade pip setuptools wheel || failed
python -m pip install -r requirements.txt || failed

# [4/4] Fetch Camoufox browser files
echo "[4/4] Fetching Camoufox browser files..."
python -m camoufox fetch || failed

echo ""
echo "============================================================"
echo -e "${GREEN}  Install complete.${NC}"
echo "  Next: run your run_scraper.sh script"
echo "============================================================"
echo ""
read -p "Press [Enter] to exit..."
exit 0