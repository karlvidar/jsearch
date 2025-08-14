# JSearch - JavaScript Search Tool

<div align="center">

![jsearch Banner](assets/Banner.png)

**A comprehensive subdomain discovery and JavaScript analysis tool for bug bounty reconnaissance**

[![Python 3.6+](https://img.shields.io/badge/python-3.6+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)

</div>

## 🔍 Overview

JSearch is an automated reconnaissance tool designed for bug bounty hunters and penetration testers. It combines multiple powerful tools to perform comprehensive subdomain discovery, live domain verification, JavaScript file extraction, and secret analysis in a streamlined workflow.

## ✨ Features

### 🌐 Subdomain Discovery
- **Subfinder**: Comprehensive subdomain enumeration from various sources
- **FFUF**: DNS fuzzing with wordlists for additional subdomain discovery
- **Live Validation**: HTTPx verification of discovered subdomains

### 📄 JavaScript File Discovery
- **GAU (GetAllUrls)**: Historical URL discovery from web archives
- **LinkFinder**: Extract JavaScript files and endpoints from live sites
- **Katana**: Advanced web crawling for JavaScript file discovery

### 🔒 Security Analysis
- **Mantra**: Secret analysis of JavaScript files (API keys, tokens, etc.)
- **Nuclei**: Vulnerability scanning with customizable templates

### 🎨 User Experience
- Real-time output with color-coded results
- Comprehensive logging and progress tracking
- Organized output directory structure
- JSON export for automation and integration

## 📦 Installation

### Prerequisites

Install the required tools:

```bash
# Install Go tools
go install -v github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest
go install github.com/ffuf/ffuf@latest
go install github.com/lc/gau/v2/cmd/gau@latest
go install github.com/projectdiscovery/httpx/cmd/httpx@latest
go install github.com/projectdiscovery/katana/cmd/katana@latest
go install github.com/projectdiscovery/nuclei/v2/cmd/nuclei@latest

# Install Python dependencies
pip3 install requests

# Install Mantra (JavaScript secret analysis)
git clone https://github.com/brosck/mantra
cd mantra
# Follow installation instructions from the repository

# Install LinkFinder
git clone https://github.com/GerbenJavado/LinkFinder
cd LinkFinder
pip3 install -r requirements.txt

# Note: LinkFinder will be automatically detected in ~/LinkFinder/
```

### Install JSearch

#### Linux / macOS
```bash
# 1. Clone the repository
git clone https://github.com/karlvidar/jsearch.git
cd jsearch

# 2. Make executable
chmod +x jsearch.py

# 3. Create global alias
cd ..
echo "alias jsearch='python3 $(pwd)/jsearch/jsearch.py'" >> ~/.bashrc
source ~/.bashrc

# 4. Test the installation
jsearch --help
```

### macOS
```bash
# 1. Clone the repository
git clone https://github.com/karlvidar/jsearch.git
cd jsearch

# 2. Make executable
chmod +x jsearch.py

# 3. Create global alias (for bash)
cd ..
echo "alias jsearch='python3 $(pwd)/jsearch/jsearch.py'" >> ~/.bash_profile
source ~/.bash_profile

# For zsh users (default on newer macOS)
echo "alias jsearch='python3 $(pwd)/jsearch/jsearch.py'" >> ~/.zshrc
source ~/.zshrc

# 4. Test the installation
jsearch --help
```

### Windows
```powershell
# 1. Clone the repository
git clone https://github.com/karlvidar/jsearch.git
cd jsearch

# 2. Run directly
python jsearch.py -u example.com
```

## 🛠️ Install Required Tools

After installing jsearch, you need to install the reconnaissance tools:

### Kali Linux / Ubuntu / Debian
```bash
# Install Go
sudo apt update
sudo apt install golang-go

# Install Go tools
go install -v github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest
go install github.com/ffuf/ffuf@latest
go install github.com/lc/gau/v2/cmd/gau@latest
go install -v github.com/projectdiscovery/httpx/cmd/httpx@latest
go install -v github.com/projectdiscovery/katana/cmd/katana@latest
go install -v github.com/projectdiscovery/nuclei/v2/cmd/nuclei@latest

# Install mantra (brosck version)
git clone https://github.com/brosck/mantra.git
cd mantra
pip install -r requirements.txt
sudo cp mantra /usr/local/bin/
cd ..

# Install wordlists
sudo apt install seclists
```

### macOS
```bash
# Install Go
brew install go

# Install Go tools (same as above)
go install -v github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest
go install github.com/ffuf/ffuf@latest
go install github.com/lc/gau/v2/cmd/gau@latest
go install -v github.com/projectdiscovery/httpx/cmd/httpx@latest
go install -v github.com/projectdiscovery/katana/cmd/katana@latest
go install -v github.com/projectdiscovery/nuclei/v2/cmd/nuclei@latest

# Install mantra (brosck version)
git clone https://github.com/brosck/mantra.git
cd mantra
pip install -r requirements.txt
sudo cp mantra /usr/local/bin/
cd ..

# Install wordlists manually
git clone https://github.com/danielmiessler/SecLists.git /usr/local/share/wordlists/seclists
```

## 🚀 Usage

### Basic Usage

```bash
# Basic scan
jsearch -u example.com

# Specify output directory
jsearch -u example.com -p /tmp/example_scan

# Export results to JSON
jsearch -u example.com -o results.json
```

### Advanced Options

```bash
# Skip specific tools
jsearch -u example.com --skip-ffuf --skip-nuclei

# Use custom LinkFinder path
jsearch -u example.com --linkfinder-path /opt/LinkFinder/linkfinder.py

# Skip JavaScript file discovery tools
jsearch -u example.com --skip-gau --skip-katana --skip-linkfinder

# Skip secret analysis
jsearch -u example.com --skip-mantra
```

### Command Line Options

```
Required:
-u, --url           Target URL/domain

Output:
-p, --path          Output directory path
-o, --output        Output file for results (JSON format)

Configuration:
--linkfinder-path   Custom path to LinkFinder script

Tool Control:
--skip-ffuf         Skip FFUF subdomain discovery
--skip-gau          Skip GAU JavaScript file discovery
--skip-linkfinder   Skip LinkFinder JavaScript file discovery
--skip-katana       Skip Katana JavaScript file discovery
--skip-mantra       Skip Mantra secret analysis
--skip-nuclei       Skip Nuclei vulnerability scanning
```

## 🔄 Workflow

JSearch follows a systematic 5-step process:

1. **Gathering Subdomains**
   - Subfinder discovers subdomains from various sources
   - FFUF performs DNS fuzzing for additional discovery

2. **Checking Live Domains**
   - HTTPx validates which subdomains are live and accessible

3. **Discovering JavaScript Files**
   - GAU searches web archives for historical JavaScript URLs
   - LinkFinder crawls live sites for JavaScript files and endpoints
   - Katana performs advanced web crawling

4. **Analyzing for Secrets**
   - Mantra analyzes all discovered JavaScript files for secrets
   - Displays API keys, tokens, and sensitive information

5. **Scanning for Vulnerabilities**
   - Nuclei runs vulnerability scans on live domains
   - Focuses on medium, high, and critical severity issues

## 📂 Output Structure

JSearch creates an organized output directory:

```
jsearch_example_com/
├── subfinder_results.txt      # Subdomain discovery results
├── ffuf_results.txt           # FFUF fuzzing results
├── live_domains.txt           # Live domain validation
├── katana_js_files.txt        # Katana JavaScript discovery
├── mantra_secrets.txt         # Secret analysis results
├── nuclei_results.txt         # Vulnerability scan results
└── jsearch_summary.json       # Complete results summary
```

## 📋 Example Output

```
[14:25:33] [INFO] Checking tool availability...
[14:25:33] [SUCCESS] All required tools are available

[1/5] Gathering Subdomains
[SUBDOMAIN] api.example.com
[SUBDOMAIN] admin.example.com
[SUBDOMAIN] www.example.com (NEW)

[2/5] Checking Live Domains
[LIVE] https://api.example.com
[LIVE] https://www.example.com

[3/5] Discovering JavaScript Files
[JS FILE] https://www.example.com/assets/app.js
[JS FILE] https://api.example.com/static/main.js

[4/5] Analyzing for Secrets
███╗   ███╗ █████╗ ███╗   ██╗████████╗██████╗  █████╗
████╗ ████║██╔══██╗████╗  ██║╚══██╔══╝██╔══██╗██╔══██╗
██╔████╔██║███████║██╔██╗ ██║   ██║   ██████╔╝███████║
██║╚██╔╝██║██╔══██║██║╚██╗██║   ██║   ██╔══██╗██╔══██║
██║ ╚═╝ ██║██║  ██║██║ ╚████║   ██║   ██║  ██║██║  ██║
╚═╝     ╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝   ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═╝
[+] https://www.example.com/app.js [AIzaSyDxVxKt8B2nGfH7X9cL4mP5qR8sT3uY6vW]

=== JSEARCH SUMMARY ===
Target: example.com
Subdomains found: 15
Live domains: 8
JS files found: 47
Output directory: jsearch_example_com
```

## 🔧 Dependencies

### Required Tools
- **subfinder**: Subdomain discovery
- **ffuf**: DNS fuzzing
- **gau**: Historical URL discovery
- **httpx**: HTTP toolkit
- **katana**: Web crawling
- **nuclei**: Vulnerability scanning
- **mantra**: JavaScript secret analysis
- **LinkFinder**: JavaScript file discovery

### System Requirements
- Python 3.6+
- Go 1.19+
- Internet connection for subdomain discovery
- Sufficient disk space for results

## 🛠️ Troubleshooting

### Tool Not Found Errors
```bash
# Ensure Go bin is in PATH
export PATH=$PATH:$(go env GOPATH)/bin

# Verify tool installation
subfinder -h
ffuf -h
```

### LinkFinder Issues
```bash
# Install in home directory (automatically detected)
cd ~
git clone https://github.com/GerbenJavado/LinkFinder
cd LinkFinder
pip3 install -r requirements.txt

# Install in common system location
git clone https://github.com/GerbenJavado/LinkFinder /opt/LinkFinder
pip3 install -r /opt/LinkFinder/requirements.txt

# Or specify custom path
jsearch -u example.com --linkfinder-path /custom/path/linkfinder.py
```

### Permission Issues
```bash
chmod +x jsearch.py
```

## 📊 Output Structure

JSearch creates a structured output directory containing:

```
jsearch_example_com/
├── subfinder_results.txt      # Subfinder discoveries
├── ffuf_results.json         # Ffuf fuzzing results
├── live_domains.txt          # Live domain verification
├── gau_js_files.txt          # JS files from gau
├── katana_js_files.txt       # JS files from katana (if available)
├── mantra_secrets.txt        # Secret analysis results
├── nuclei_results.txt        # Vulnerability scan results (if available)
└── jsearch_summary.json      # Consolidated summary
```

### Summary JSON Format
```json
{
  "target": "example.com",
  "timestamp": "2025-08-06T10:30:00",
  "subdomains_found": 150,
  "live_domains_found": 75,
  "js_files_found": 230,
  "subdomains": [...],
  "live_domains": [...],
  "js_files": [...]
}
```

## 🔧 Configuration

### Wordlist Configuration
By default, jsearch uses:
```
/usr/share/wordlists/seclists/Discovery/DNS/bug-bounty-program-subdomains-trickest-inventory.txt
```

To use a custom wordlist, modify the `wordlist_path` variable in `jsearch.py`.

### Tool Timeouts and Threads
You can adjust the following parameters in the script:
- `timeout`: Command timeout (default: 300 seconds)
- `httpx threads`: Concurrent threads for httpx (default: 50)
- `ffuf threads`: Concurrent threads for ffuf (default: 50)

## 🎨 Features in Detail

### 1. Subdomain Discovery
- **Subfinder**: Passive subdomain enumeration using multiple sources
- **Ffuf**: Active subdomain fuzzing with comprehensive wordlists
- **Duplicate Removal**: Automatically merges results without duplicates

### 2. Live Domain Verification
- **Httpx**: Fast HTTP probe to verify live subdomains
- **Timeout Management**: Configurable timeouts for reliability
- **Status Code Filtering**: Focuses on responsive domains

### 3. JavaScript File Discovery
- **Gau**: GetAllUrls for historical JS file discovery
- **Katana**: Modern web crawler for additional JS files
- **Filtering**: Automatically filters for .js files only

### 4. Secret Analysis
- **Mantra**: Analyzes JS files for API keys, tokens, and secrets
- **Pattern Matching**: Uses advanced regex patterns for detection
- **Reporting**: Clear output of potential security issues

### 5. Vulnerability Scanning (Optional)
- **Nuclei**: Community-powered vulnerability scanner
- **Template-based**: Uses extensive vulnerability templates
- **Severity Filtering**: Focuses on medium, high, and critical issues

## 🔍 Troubleshooting

### Alias Issues

**1. Aliases not working:**
```bash
# Check if aliases were added
grep "jsearch" ~/.bashrc  # For bash users
grep "jsearch" ~/.zshrc   # For zsh users (macOS)

# Reload configuration
source ~/.bashrc  # or source ~/.zshrc

# Or start a new terminal session
```

**2. "Command not found" error:**
```bash
# Test direct execution first
python3 /full/path/to/jsearch/jsearch.py --help

# Check if the path in your alias is correct
which python3

# Re-add the alias with correct path
echo "alias jsearch='python3 $(pwd)/jsearch/jsearch.py'" >> ~/.bashrc
source ~/.bashrc
```

### Tool Issues

**1. Tools not found**
```bash
# Check if tools are in PATH
which subfinder httpx ffuf gau

# Add Go bin to PATH if needed
echo 'export PATH="$PATH:$HOME/go/bin"' >> ~/.bashrc
source ~/.bashrc
```

**2. Permission denied**
```bash
chmod +x jsearch.py
```

**3. Wordlist not found**
```bash
# Install SecLists
sudo apt install seclists
# Or download manually
git clone https://github.com/danielmiessler/SecLists.git /usr/share/wordlists/seclists
```

**4. Mantra installation issues**
```bash
# If you get permission errors with mantra:
# Make sure you cloned the correct mantra repository
git clone https://github.com/brosck/mantra.git
cd mantra

# Install requirements
pip install -r requirements.txt

# Make mantra executable and copy to system PATH
chmod +x mantra
sudo cp mantra /usr/local/bin/

# Test mantra installation
mantra -h

# If still having issues, try adding to local bin
mkdir -p ~/.local/bin
cp mantra ~/.local/bin/
echo 'export PATH="$PATH:$HOME/.local/bin"' >> ~/.bashrc
source ~/.bashrc
```

**5. Timeout issues**
- Increase timeout values in the script for slow networks
- Reduce thread counts for stability

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

### Development Setup
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## ⚠️ Disclaimer

This tool is for educational and authorized testing purposes only. Users are responsible for complying with applicable laws and regulations. The authors are not responsible for any misuse of this tool.

## 🙏 Acknowledgments

- [ProjectDiscovery](https://github.com/projectdiscovery) for amazing reconnaissance tools
- [Ffuf team](https://github.com/ffuf/ffuf) for the powerful fuzzer
- [SecLists](https://github.com/danielmiessler/SecLists) for comprehensive wordlists
- [Bug bounty community](https://bugcrowd.com) for inspiration and feedback

## 📞 Support

If you have any questions or need help, please:
1. Check the [Issues](https://github.com/karlvidar/jsearch/issues) page
2. Create a new issue if your problem isn't already reported
3. Provide detailed information about your environment and the issue
