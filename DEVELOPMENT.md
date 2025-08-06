# JSearch Developer Documentation

## Project Structure

```
jsearch/
├── jsearch.py              # Main application logic
├── cli.py                  # Enhanced CLI interface
├── config.py               # Configuration management
├── setup.py                # Setup script
├── test_jsearch.py         # Test suite
├── install.sh              # Tool installation script
├── setup-alias.sh          # Alias setup script (Linux/macOS)
├── setup-alias.ps1         # Alias setup script (Windows)
├── verify-alias.sh         # Alias verification script
├── jsearch.bat             # Windows batch launcher
├── jsearch-cli.bat         # Windows enhanced CLI launcher
├── requirements.txt        # Python dependencies
├── config_example.py       # Example configuration
├── quickstart.py           # Interactive quick start guide
├── wordlists/              # Local wordlists
│   └── subdomains.txt     # Sample subdomain wordlist
├── README.md               # User documentation
├── LICENSE                 # MIT license
├── .gitignore             # Git ignore rules
├── DEVELOPMENT.md         # This file
└── PROJECT_SUMMARY.md     # Project overview
```

## Core Components

### 1. JSearch Class (`jsearch.py`)

The main application class that orchestrates the reconnaissance workflow.

#### Key Methods:
- `__init__()`: Initialize with target URL and configuration
- `run()`: Main execution flow
- `discover_subdomains_*()`: Subdomain discovery methods
- `check_live_domains()`: Verify live domains with httpx
- `discover_js_files_*()`: JavaScript file discovery
- `analyze_secrets_mantra()`: Secret analysis
- `analyze_with_nuclei()`: Vulnerability scanning

#### Configuration Options:
- `custom_wordlist`: Custom wordlist path
- `timeout`: Command timeout
- `threads`: Number of threads
- `quiet_mode`: Reduce output
- `skip_*`: Skip specific tools

### 2. CLI Interface (`cli.py`)

Enhanced command-line interface with comprehensive options.

#### Features:
- Argument parsing with argparse
- Tool availability checking
- Configuration validation
- Error handling and user feedback

### 3. Configuration (`config.py`)

Centralized configuration management.

#### Key Components:
- `Config` class: Default configuration
- `Colors` class: Terminal color themes
- Tool-specific configurations
- File extension definitions
- Secret pattern definitions

## Development Workflow

### 1. Setting Up Development Environment

```bash
# Clone the repository
git clone <repository-url>
cd jsearch

# Run setup script
python3 setup.py

# Install tools
./install.sh

# Run tests
python3 test_jsearch.py
```

### 2. Running Tests

```bash
# Run all tests
python3 test_jsearch.py

# Test specific functionality
python3 -c "from test_jsearch import TestRunner; t = TestRunner(); t.test_imports()"
```

### 3. Adding New Tools

To add a new reconnaissance tool:

1. **Add tool check in `config.py`**:
```python
# Add to Config.validate_tools()
required_tools.append("newtool")
```

2. **Create discovery method in `jsearch.py`**:
```python
def discover_with_newtool(self):
    """Discover targets using newtool"""
    if self.skip_newtool:
        self.log("Skipping newtool", "INFO")
        return
    
    self.log("Running newtool...")
    # Implementation here
```

3. **Add skip flag**:
```python
# In __init__
self.skip_newtool = False
```

4. **Add CLI option in `cli.py`**:
```python
parser.add_argument(
    '--skip-newtool',
    action='store_true',
    help='Skip newtool discovery'
)
```

5. **Update run method**:
```python
def run(self):
    # Add to execution flow
    self.discover_with_newtool()
```

### 4. Customizing Output

#### Adding New Output Formats:

```python
def save_xml_output(self):
    """Save results in XML format"""
    # Implementation here
    pass

def save_csv_output(self):
    """Save results in CSV format"""
    # Implementation here
    pass
```

#### Modifying Existing Output:

Edit the `save_final_output()` method in `jsearch.py`.

### 5. Configuration Customization

Create a local configuration file:

```python
# config_local.py
from config import Config

class LocalConfig(Config):
    # Override default settings
    DEFAULT_TIMEOUT = 600
    HTTPX_THREADS = 100
```

Use in main application:
```python
from config_local import LocalConfig
config = LocalConfig()
```

## Code Style Guidelines

### 1. Python Style
- Follow PEP 8
- Use type hints where appropriate
- Document functions with docstrings
- Use meaningful variable names

### 2. Error Handling
- Always use try-except for external commands
- Log errors with appropriate levels
- Graceful degradation when tools are missing

### 3. Output Formatting
- Use the Colors class for consistent theming
- Provide clear progress indicators
- Include timestamps in logs

## Testing

### 1. Unit Tests

Add tests to `test_jsearch.py`:

```python
def test_new_functionality(self):
    """Test new functionality"""
    try:
        # Test implementation
        result = some_function()
        self.log_test("New functionality", result == expected)
    except Exception as e:
        self.log_test("New functionality", False, str(e))
```

### 2. Integration Tests

Test with real tools (when available):

```python
def test_tool_integration(self):
    """Test actual tool integration"""
    if tool_available:
        # Run real commands
        pass
    else:
        # Skip test
        pass
```

### 3. Manual Testing

```bash
# Test basic functionality
python3 jsearch.py -u example.com --check-tools

# Test with custom options
python3 jsearch.py -u example.com -p /tmp/test --skip-nuclei

# Test CLI
python3 cli.py --help
```

## Tool Integration

### 1. Adding Tool Configurations

In `config.py`:

```python
NEWTOOL_CONFIG = {
    "threads": 50,
    "timeout": 30,
    "output_format": "json"
}
```

### 2. Command Construction

```python
def build_command(self, tool_config):
    """Build command with configuration"""
    cmd_parts = [
        "newtool",
        f"-t {tool_config['threads']}",
        f"--timeout {tool_config['timeout']}"
    ]
    return " ".join(cmd_parts)
```

### 3. Output Parsing

```python
def parse_tool_output(self, output_file):
    """Parse tool output consistently"""
    results = set()
    
    if os.path.exists(output_file):
        with open(output_file, 'r') as f:
            # Parse based on format
            pass
    
    return results
```

## Debugging

### 1. Verbose Mode

Enable verbose output:
```bash
python3 jsearch.py -u example.com -v
```

### 2. Debug Logging

Add debug statements:
```python
if self.verbose_mode:
    self.log(f"Debug: {debug_info}", "INFO")
```

### 3. Temporary Files

Keep temporary files for debugging:
```python
# In config
KEEP_TEMP_FILES = True
```

## Performance Optimization

### 1. Threading

Adjust thread counts based on system:
```python
# In config
HTTPX_THREADS = min(100, os.cpu_count() * 10)
```

### 2. Timeouts

Configure appropriate timeouts:
```python
# Tool-specific timeouts
TOOL_TIMEOUTS = {
    "subfinder": 300,
    "ffuf": 600,
    "httpx": 30
}
```

### 3. Resource Management

Monitor resource usage:
```python
import psutil

def check_resources(self):
    """Check system resources"""
    if psutil.virtual_memory().percent > 90:
        self.log("High memory usage", "WARNING")
```

## Security Considerations

### 1. Input Validation

Always validate user input:
```python
def validate_url(self, url):
    """Validate target URL"""
    # Remove dangerous characters
    # Validate format
    return clean_url
```

### 2. Command Injection Prevention

Use subprocess safely:
```python
# Good
subprocess.run([tool, arg1, arg2])

# Avoid
subprocess.run(f"{tool} {user_input}", shell=True)
```

### 3. File Permissions

Set appropriate file permissions:
```python
os.chmod(output_file, 0o600)  # Owner read/write only
```

## Contributing Guidelines

### 1. Before Contributing

- Run the test suite
- Check code style with flake8/black
- Update documentation
- Add tests for new features

### 2. Pull Request Process

1. Fork the repository
2. Create a feature branch
3. Implement changes with tests
4. Update documentation
5. Submit pull request

### 3. Issue Reporting

Include in bug reports:
- OS and Python version
- Tool versions
- Full error messages
- Steps to reproduce

## Release Process

### 1. Version Bumping

Update version in:
- `cli.py` (version argument)
- `setup.py` (if using setuptools)
- `README.md` (installation instructions)

### 2. Testing

```bash
# Run full test suite
python3 test_jsearch.py

# Test installation
./install.sh

# Test on different systems
```

### 3. Documentation

Update:
- README.md
- CHANGELOG.md
- This file (DEVELOPMENT.md)

## Troubleshooting

### Common Issues

1. **Tools not found**: Check PATH and installation
2. **Permission denied**: Check file permissions
3. **Timeout errors**: Increase timeout values
4. **Memory issues**: Reduce thread counts

### Debug Commands

```bash
# Check tool availability
python3 -c "from config import Config; print(Config.validate_tools())"

# Test specific functionality
python3 -c "from jsearch import JSearch; j = JSearch('test.com'); j.check_tool_availability()"

# Verify wordlist
python3 -c "from config import Config; print(Config.get_wordlist_path())"
```

## Future Enhancements

### Planned Features

1. **Web Interface**: Flask/Django web UI
2. **Database Storage**: Store results in database
3. **Reporting**: HTML/PDF report generation
4. **Scheduling**: Cron-like scheduling
5. **Notifications**: Slack/Discord integration
6. **Clustering**: Distributed scanning

### Architecture Improvements

1. **Plugin System**: Modular tool plugins
2. **Configuration UI**: Web-based configuration
3. **API**: REST API for programmatic access
4. **Caching**: Result caching and deduplication

---

For questions or contributions, please refer to the main README.md or open an issue on GitHub.
