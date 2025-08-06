#!/bin/bash

# JSearch Installation Script
# This script installs all required tools for JSearch

echo "🔵 JSearch Installation Script"
echo "=============================="

# Colors
BLUE='\033[94m'
GREEN='\033[92m'
YELLOW='\033[93m'
RED='\033[91m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if Go is installed
check_go() {
    if ! command -v go &> /dev/null; then
        print_error "Go is not installed. Please install Go first:"
        echo "Ubuntu/Debian: sudo apt install golang-go"
        echo "macOS: brew install go"
        echo "Or download from: https://golang.org/dl/"
        exit 1
    fi
    print_success "Go is installed: $(go version)"
}

# Check if Python 3 is installed
check_python() {
    if ! command -v python3 &> /dev/null; then
        print_error "Python 3 is not installed. Please install Python 3 first."
        exit 1
    fi
    print_success "Python 3 is installed: $(python3 --version)"
}

# Install Go tools
install_go_tools() {
    print_status "Installing Go-based tools..."
    
    tools=(
        "github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest"
        "github.com/ffuf/ffuf@latest"
        "github.com/lc/gau/v2/cmd/gau@latest"
        "github.com/projectdiscovery/httpx/cmd/httpx@latest"
        "github.com/projectdiscovery/katana/cmd/katana@latest"
        "github.com/projectdiscovery/nuclei/v2/cmd/nuclei@latest"
    )
    
    for tool in "${tools[@]}"; do
        tool_name=$(echo "$tool" | cut -d'/' -f3)
        print_status "Installing $tool_name..."
        if go install -v "$tool"; then
            print_success "$tool_name installed successfully"
        else
            print_error "Failed to install $tool_name"
        fi
    done
}

# Install Python tools
install_python_tools() {
    print_status "Installing Python-based tools..."
    
    if pip3 install mantra-cli; then
        print_success "mantra installed successfully"
    else
        print_error "Failed to install mantra"
    fi
}

# Install SecLists wordlists
install_wordlists() {
    print_status "Installing SecLists wordlists..."
    
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        # Linux
        if command -v apt &> /dev/null; then
            sudo apt update && sudo apt install -y seclists
            print_success "SecLists installed via apt"
        else
            install_seclists_manual
        fi
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        # macOS
        if command -v brew &> /dev/null; then
            brew install seclists || install_seclists_manual
        else
            install_seclists_manual
        fi
    else
        install_seclists_manual
    fi
}

# Manual SecLists installation
install_seclists_manual() {
    print_status "Installing SecLists manually..."
    
    WORDLIST_DIR="/usr/share/wordlists"
    
    if [[ ! -d "$WORDLIST_DIR" ]]; then
        print_status "Creating wordlist directory..."
        sudo mkdir -p "$WORDLIST_DIR"
    fi
    
    if [[ ! -d "$WORDLIST_DIR/seclists" ]]; then
        print_status "Cloning SecLists repository..."
        sudo git clone https://github.com/danielmiessler/SecLists.git "$WORDLIST_DIR/seclists"
        print_success "SecLists installed manually"
    else
        print_warning "SecLists already exists at $WORDLIST_DIR/seclists"
    fi
}

# Verify installations
verify_installation() {
    print_status "Verifying installations..."
    
    tools=("subfinder" "ffuf" "gau" "httpx" "katana" "nuclei" "mantra")
    all_good=true
    
    for tool in "${tools[@]}"; do
        if command -v "$tool" &> /dev/null; then
            print_success "$tool is available"
        else
            print_error "$tool is not available in PATH"
            all_good=false
        fi
    done
    
    # Check wordlist
    wordlist_path="/usr/share/wordlists/seclists/Discovery/DNS/bug-bounty-program-subdomains-trickest-inventory.txt"
    if [[ -f "$wordlist_path" ]]; then
        print_success "Required wordlist is available"
    else
        print_warning "Required wordlist not found at $wordlist_path"
        print_warning "You may need to adjust the wordlist path in jsearch.py"
    fi
    
    if $all_good; then
        print_success "All tools are properly installed!"
        echo ""
        print_status "You can now run JSearch:"
        echo "python3 jsearch.py -u example.com"
    else
        print_error "Some tools are missing. Please check your PATH and installation."
        echo ""
        print_status "Make sure Go tools are in your PATH:"
        echo "export PATH=\"\$PATH:\$HOME/go/bin\""
    fi
}

# Main installation flow
main() {
    print_status "Starting JSearch installation..."
    echo ""
    
    check_go
    check_python
    echo ""
    
    install_go_tools
    echo ""
    
    install_python_tools
    echo ""
    
    install_wordlists
    echo ""
    
    verify_installation
    
    echo ""
    print_status "Installation complete!"
    print_status "Don't forget to add Go bin to your PATH if it's not already:"
    echo "echo 'export PATH=\"\$PATH:\$HOME/go/bin\"' >> ~/.bashrc"
    echo "source ~/.bashrc"
}

# Run main function
main
