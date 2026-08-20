#!/usr/bin/env bash

# Set visual aqua/cyan text (similar to Windows color 0B)
CYAN='\033[0;36m'
RED='\033[0;31m'
YELLOW='\033[0;33m'
NC='\033[0m' # No Color

# Ensure script runs in its own directory
cd "$(dirname "$0")" || exit 1

echo ""
echo -e "${CYAN}============================================================${NC}"
echo -e "${CYAN}  ExamTopics Scraper${NC}"
echo -e "${CYAN}============================================================${NC}"
echo ""

# Check for virtual environment Python binary
if [ -f ".venv/bin/python" ]; then
    PYTHON_EXE=".venv/bin/python"
else
    echo -e "${YELLOW}[WARN] Local .venv not found.${NC}"
    echo "Run install_deps.sh first for best results."
    echo ""
    
    # Check system/PATH Python
    if command -v python3 >/dev/null 2>&1; then
        PYTHON_EXE="python3"
    elif command -v python >/dev/null 2>&1; then
        PYTHON_EXE="python"
    else
        echo -e "${RED}[ERROR] Python not found.${NC}"
        echo ""
        read -p "Press [Enter] to exit..."
        exit 1
    fi
fi

# Run main script
"$PYTHON_EXE" main.py

echo ""
echo "============================================================"
echo -e "${CYAN}  Finished.${NC}"
echo "============================================================"
echo ""
read -p "Press [Enter] to exit..."
exit 0