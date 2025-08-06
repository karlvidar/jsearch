#!/bin/bash

# JSearch Alias Verification Script
# This script helps verify that jsearch aliases are working correctly

echo "🔍 JSearch Alias Verification"
echo "============================="

# Color codes
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print status
print_status() {
    if [ $1 -eq 0 ]; then
        echo -e "${GREEN}✅ $2${NC}"
    else
        echo -e "${RED}❌ $2${NC}"
    fi
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

# Detect shell config file
if [[ "$SHELL" == *"zsh"* ]]; then
    SHELL_CONFIG="$HOME/.zshrc"
    SHELL_NAME="zsh"
elif [[ "$SHELL" == *"bash"* ]]; then
    SHELL_CONFIG="$HOME/.bashrc"
    SHELL_NAME="bash"
else
    SHELL_CONFIG="unknown"
    SHELL_NAME="unknown"
fi

echo "Shell: $SHELL_NAME"
echo "Config file: $SHELL_CONFIG"
echo ""

# Test 1: Check if aliases exist in config file
echo "Test 1: Checking if aliases exist in shell config..."
if [[ "$SHELL_CONFIG" != "unknown" ]] && grep -q "alias jsearch=" "$SHELL_CONFIG" 2>/dev/null; then
    print_status 0 "Aliases found in $SHELL_CONFIG"
    echo "   Found aliases:"
    grep "alias jsearch" "$SHELL_CONFIG" | sed 's/^/   /'
else
    print_status 1 "Aliases not found in $SHELL_CONFIG"
    print_warning "Run ./setup-alias.sh to add aliases"
fi

echo ""

# Test 2: Check if jsearch command is available
echo "Test 2: Checking if jsearch command is available..."
if command -v jsearch >/dev/null 2>&1; then
    print_status 0 "jsearch command is available"
else
    print_status 1 "jsearch command not found"
    print_warning "Try running: source $SHELL_CONFIG"
fi

echo ""

# Test 3: Check if jsearch-cli command is available
echo "Test 3: Checking if jsearch-cli command is available..."
if command -v jsearch-cli >/dev/null 2>&1; then
    print_status 0 "jsearch-cli command is available"
else
    print_status 1 "jsearch-cli command not found"
    print_warning "Try running: source $SHELL_CONFIG"
fi

echo ""

# Test 4: Check if Python 3 is available
echo "Test 4: Checking Python 3 availability..."
if command -v python3 >/dev/null 2>&1; then
    PYTHON_VERSION=$(python3 --version 2>&1)
    print_status 0 "Python 3 is available: $PYTHON_VERSION"
else
    print_status 1 "Python 3 not found"
    print_warning "Install Python 3 first"
fi

echo ""

# Test 5: Check if jsearch.py exists and is executable
echo "Test 5: Checking jsearch.py file..."
CURRENT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
if [[ -f "$CURRENT_DIR/jsearch.py" ]]; then
    print_status 0 "jsearch.py found at $CURRENT_DIR/jsearch.py"
    
    if [[ -x "$CURRENT_DIR/jsearch.py" ]]; then
        print_status 0 "jsearch.py is executable"
    else
        print_status 1 "jsearch.py is not executable"
        print_warning "Run: chmod +x jsearch.py"
    fi
else
    print_status 1 "jsearch.py not found in current directory"
fi

echo ""

# Test 6: Try to run jsearch help
echo "Test 6: Testing jsearch execution..."
if command -v jsearch >/dev/null 2>&1; then
    if jsearch --help >/dev/null 2>&1; then
        print_status 0 "jsearch --help works correctly"
    else
        print_status 1 "jsearch command exists but execution failed"
        print_warning "There might be a Python or script error"
    fi
elif [[ -f "$CURRENT_DIR/jsearch.py" ]]; then
    if python3 "$CURRENT_DIR/jsearch.py" --help >/dev/null 2>&1; then
        print_status 0 "Direct execution works: python3 jsearch.py --help"
        print_warning "Alias not working, but direct execution is fine"
    else
        print_status 1 "Direct execution failed"
        print_warning "Check Python dependencies or script errors"
    fi
fi

echo ""
echo "=== Summary ==="

# Provide recommendations based on test results
if command -v jsearch >/dev/null 2>&1 && command -v jsearch-cli >/dev/null 2>&1; then
    echo -e "${GREEN}🎉 All tests passed! JSearch aliases are working correctly.${NC}"
    echo ""
    echo "You can now use:"
    echo "  jsearch -u example.com"
    echo "  jsearch-cli --check-tools"
elif grep -q "alias jsearch=" "$SHELL_CONFIG" 2>/dev/null; then
    echo -e "${YELLOW}🔄 Aliases are configured but not active in current session.${NC}"
    echo ""
    echo "Solutions:"
    echo "  1. Run: source $SHELL_CONFIG"
    echo "  2. Open a new terminal window"
    echo "  3. Restart your terminal"
else
    echo -e "${RED}❌ Aliases are not set up.${NC}"
    echo ""
    echo "Solutions:"
    echo "  1. Run: ./setup-alias.sh"
    echo "  2. Or manually add aliases to $SHELL_CONFIG"
fi

echo ""
print_info "For more help, check the README.md troubleshooting section"
