# JSearch - Bug Bounty Reconnaissance Tool

<div align="center">

```
     ╦╔═╗╔═╗╔═╗╦═╗╔═╗╦ ╦
     ║╚═╗║╣ ╠═╣╠╦╝║  ╠═╣
    ╚╝╚═╝╚═╝╩ ╩╩╚═╚═╝╩ ╩
```

**A comprehensive subdomain discovery and JavaScript analysis tool for bug bounty hunters**

[![Python 3.6+](https://img.shields.io/badge/python-3.6+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)

</div>

## 🔍 Overview

JSearch is an automated reconnaissance tool designed for bug bounty hunters and penetration testers. It combines multiple powerful tools to perform comprehensive subdomain discovery, live domain verification, JavaScript file extraction, and secret analysis in a streamlined workflow.

## ✨ Features

- **Subdomain Discovery**: Uses subfinder and ffuf with comprehensive wordlists
- **Live Domain Verification**: Validates discovered subdomains using httpx
- **JavaScript File Discovery**: Extracts JS files using gau and katana
- **Secret Analysis**: Analyzes JavaScript files for potential secrets using mantra
- **Vulnerability Scanning**: Optional nuclei integration for vulnerability detection
- **Duplicate Prevention**: Automatically removes duplicates across different tools
- **Blue-themed Output**: Clean, colored terminal output for better readability
- **Comprehensive Reporting**: JSON output with detailed results

## 🛠️ Required Tools

Before using JSearch, you need to install the following tools:

### Core Tools (Required)
- [subfinder](https://github.com/projectdiscovery/subfinder)
- [ffuf](https://github.com/ffuf/ffuf)
- [gau](https://github.com/lc/gau)
- [httpx](https://github.com/projectdiscovery/httpx)
- [mantra](https://github.com/MrEmpy/mantra)

### Optional Tools
- [katana](https://github.com/projectdiscovery/katana) - Additional JS file discovery
- [nuclei](https://github.com/projectdiscovery/nuclei) - Vulnerability scanning

## 📦 Installation

### 1. Clone the Repository
```bash
git clone https://github.com/karlvidar/jsearch.git
cd jsearch
```

### 2. Install Required Tools

#### Using Go (Recommended)
```bash
# Install Go tools
go install -v github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest
go install github.com/ffuf/ffuf@latest
go install github.com/lc/gau/v2/cmd/gau@latest
go install -v github.com/projectdiscovery/httpx/cmd/httpx@latest
go install -v github.com/projectdiscovery/katana/cmd/katana@latest
go install -v github.com/projectdiscovery/nuclei/v2/cmd/nuclei@latest
```

#### Install mantra
```bash
pip install mantra-cli
```

#### Alternative: Using Package Managers

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install golang-go
# Then install Go tools as shown above
```

**macOS:**
```bash
brew install go
# Then install Go tools as shown above
```

### 3. Install Wordlists (Required for ffuf)
```bash
# Install SecLists
sudo apt install seclists
# Or manually:
git clone https://github.com/danielmiessler/SecLists.git /usr/share/wordlists/seclists
```

### 4. Make JSearch Executable
```bash
chmod +x jsearch.py
```

### 5. Optional: Add to PATH
```bash
# Add to your ~/.bashrc or ~/.zshrc
export PATH="$PATH:/path/to/jsearch"
```

## 🚀 Usage

### Basic Usage
```bash
python3 jsearch.py -u example.com
```

### Advanced Usage
```bash
# Specify custom output directory
python3 jsearch.py -u example.com -p /tmp/bug_bounty_results

# Save results to specific file
python3 jsearch.py -u example.com -o results.json

# Combine options
python3 jsearch.py -u example.com -p /custom/path -o final_results.json
```

### Command Line Options

| Option | Description | Example |
|--------|-------------|---------|
| `-u, --url` | Target domain (required) | `-u example.com` |
| `-p, --path` | Custom output directory | `-p /tmp/results` |
| `-o, --output` | Output file for results | `-o results.json` |
| `-h, --help` | Show help message | `-h` |

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
By default, JSearch uses:
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

### Common Issues

**1. Tools not found**
```bash
# Check if tools are in PATH
which subfinder httpx ffuf gau

# Add Go bin to PATH if needed
export PATH="$PATH:$HOME/go/bin"
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

**4. Timeout issues**
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

---

<div align="center">
Made with ❤️ for the bug bounty community
</div>
