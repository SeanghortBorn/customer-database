#!/bin/bash
# Automatic Conda Environment Activation Script
# This script activates the 'cds' conda environment for this project

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}🔧 Customer Database System - Conda Setup${NC}"
echo ""

# Check if conda is installed
if ! command -v conda &> /dev/null; then
    echo -e "${YELLOW}⚠️  Conda is not installed or not in PATH${NC}"
    echo "Please install Miniconda or Anaconda first:"
    echo "  https://docs.conda.io/en/latest/miniconda.html"
    exit 1
fi

# Check if environment exists
if conda env list | grep -q "^cds "; then
    echo "✅ Conda environment 'cds' found"
    echo ""
    echo "To activate the environment, run:"
    echo -e "  ${GREEN}conda activate cds${NC}"
    echo ""
else
    echo -e "${YELLOW}⚠️  Conda environment 'cds' not found${NC}"
    echo ""
    echo "Creating environment from environment.yml..."
    conda env create -f environment.yml
    echo ""
    echo "✅ Environment created successfully!"
    echo ""
    echo "To activate the environment, run:"
    echo -e "  ${GREEN}conda activate cds${NC}"
    echo ""
fi

# Optional: Setup direnv for auto-activation
if ! command -v direnv &> /dev/null; then
    echo -e "${YELLOW}💡 Tip: Install 'direnv' for automatic environment activation${NC}"
    echo ""
    echo "With direnv, the conda environment activates automatically when you cd into this directory."
    echo ""
    echo "To install direnv:"
    echo "  Ubuntu/Debian: sudo apt install direnv"
    echo "  macOS: brew install direnv"
    echo ""
    echo "After installing, add to your shell rc file (~/.bashrc or ~/.zshrc):"
    echo "  eval \"\$(direnv hook bash)\"  # for bash"
    echo "  eval \"\$(direnv hook zsh)\"   # for zsh"
    echo ""
    echo "Then run: direnv allow ."
    echo ""
else
    echo "✅ direnv is installed"
    echo ""
    if [ -f .envrc ]; then
        echo "To enable auto-activation, run:"
        echo -e "  ${GREEN}direnv allow .${NC}"
        echo ""
    fi
fi

echo "================================================"
echo ""
echo "📚 For more information, see:"
echo "  docs/00-getting-started/QUICK_START.md"
echo ""
