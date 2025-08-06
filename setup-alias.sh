#!/bin/bash

# JSearch Alias Setup Script
# This script helps set up global aliases for jsearch

echo "🔵 JSearch Alias Setup"
echo "======================"

# Get the current directory (jsearch project directory)
JSEARCH_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "JSearch directory: $JSEARCH_DIR"

# Detect shell
if [[ "$SHELL" == *"zsh"* ]]; then
    SHELL_CONFIG="$HOME/.zshrc"
    SHELL_NAME="zsh"
elif [[ "$SHELL" == *"bash"* ]]; then
    SHELL_CONFIG="$HOME/.bashrc"
    SHELL_NAME="bash"
else
    echo "⚠️  Could not detect shell type. Please manually add aliases."
    echo "Add these lines to your shell configuration:"
    echo "alias jsearch=\"python3 $JSEARCH_DIR/jsearch.py\""
    echo "alias jsearch-cli=\"python3 $JSEARCH_DIR/cli.py\""
    exit 1
fi

echo "Detected shell: $SHELL_NAME"
echo "Configuration file: $SHELL_CONFIG"

# Check if aliases already exist
if grep -q "alias jsearch=" "$SHELL_CONFIG" 2>/dev/null; then
    echo "⚠️  JSearch aliases already exist in $SHELL_CONFIG"
    echo "Please remove existing aliases before running this script."
    exit 1
fi

# Add aliases
echo ""
echo "Adding aliases to $SHELL_CONFIG..."

cat >> "$SHELL_CONFIG" << EOF

# JSearch aliases (added by setup-alias.sh)
alias jsearch="python3 $JSEARCH_DIR/jsearch.py"
alias jsearch-cli="python3 $JSEARCH_DIR/cli.py"
EOF

echo "✅ Aliases added successfully!"
echo ""
echo "🔄 To activate the aliases in your current session, run:"
echo "source $SHELL_CONFIG"
echo ""
echo "🚀 After that, you can use jsearch from anywhere:"
echo "jsearch -u example.com"
echo "jsearch-cli --check-tools"
echo ""

# Ask if user wants to reload now
read -p "Would you like to reload your shell configuration now? (y/N): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "🔄 Reloading shell configuration..."
    
    # Try to source the config file
    if source "$SHELL_CONFIG" 2>/dev/null; then
        echo "✅ Configuration reloaded!"
        echo ""
        echo "🎉 JSearch is now available globally!"
        echo "Try: jsearch --help"
        
        # Test if alias works
        if command -v jsearch >/dev/null 2>&1; then
            echo "✅ Alias verification: jsearch command is available"
        else
            echo "⚠️  Alias verification failed. You may need to:"
            echo "   1. Open a new terminal window"
            echo "   2. Or run: source $SHELL_CONFIG"
        fi
    else
        echo "⚠️  Could not reload configuration automatically."
        echo "Please run: source $SHELL_CONFIG"
        echo "Or open a new terminal window."
    fi
else
    echo "💡 To activate the aliases, either:"
    echo "   1. Run: source $SHELL_CONFIG"
    echo "   2. Open a new terminal window"
    echo ""
    echo "Then test with: jsearch --help"
fi

echo ""
echo "🔧 If aliases still don't work, try:"
echo "   • Check aliases: grep jsearch $SHELL_CONFIG"
echo "   • Verify Python path: which python3"
echo "   • Test direct execution: python3 $JSEARCH_DIR/jsearch.py --help"
