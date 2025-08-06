#!/usr/bin/env python3
"""
JSearch Configuration File
Customize settings for your environment
"""

import os
from pathlib import Path

class Config:
    """Configuration settings for JSearch"""
    
    # Tool timeouts (in seconds)
    DEFAULT_TIMEOUT = 300
    HTTPX_TIMEOUT = 10
    FFUF_TIMEOUT = 10
    
    # Thread/concurrency settings
    HTTPX_THREADS = 50
    FFUF_THREADS = 50
    
    # Wordlist paths (customize for your system)
    WORDLIST_PATHS = [
        "/usr/share/wordlists/seclists/Discovery/DNS/bug-bounty-program-subdomains-trickest-inventory.txt",
        "/opt/SecLists/Discovery/DNS/bug-bounty-program-subdomains-trickest-inventory.txt",
        "./wordlists/subdomains.txt",  # Local fallback
    ]
    
    # Default output settings
    DEFAULT_OUTPUT_DIR = "jsearch_results"
    KEEP_TEMP_FILES = False
    
    # Tool-specific settings
    SUBFINDER_CONFIG = {
        "sources": ["all"],
        "timeout": 30,
        "silent": True
    }
    
    FFUF_CONFIG = {
        "threads": 50,
        "timeout": 10,
        "follow_redirects": True,
        "auto_calibration": True,
        "silent": True
    }
    
    HTTPX_CONFIG = {
        "threads": 50,
        "timeout": 10,
        "follow_redirects": True,
        "status_code": True,
        "silent": True
    }
    
    GAU_CONFIG = {
        "providers": ["wayback", "commoncrawl", "otx", "urlscan"],
        "threads": 5,
        "timeout": 30
    }
    
    KATANA_CONFIG = {
        "depth": 3,
        "js_crawl": True,
        "timeout": 30,
        "silent": True
    }
    
    MANTRA_CONFIG = {
        "patterns": ["all"],
        "timeout": 60
    }
    
    NUCLEI_CONFIG = {
        "severity": ["medium", "high", "critical"],
        "timeout": 30,
        "rate_limit": 150,
        "silent": True
    }
    
    @classmethod
    def get_wordlist_path(cls):
        """Get the first available wordlist path"""
        for path in cls.WORDLIST_PATHS:
            if os.path.exists(path):
                return path
        return None
    
    @classmethod
    def validate_tools(cls):
        """Check if required tools are available"""
        required_tools = [
            "subfinder",
            "ffuf", 
            "gau",
            "httpx",
            "mantra"
        ]
        
        optional_tools = [
            "katana",
            "nuclei"
        ]
        
        missing_required = []
        missing_optional = []
        
        import subprocess
        
        for tool in required_tools:
            try:
                subprocess.run([tool, "-h"], capture_output=True, timeout=5)
            except (subprocess.TimeoutExpired, FileNotFoundError):
                missing_required.append(tool)
        
        for tool in optional_tools:
            try:
                subprocess.run([tool, "-h"], capture_output=True, timeout=5)
            except (subprocess.TimeoutExpired, FileNotFoundError):
                missing_optional.append(tool)
        
        return {
            "missing_required": missing_required,
            "missing_optional": missing_optional,
            "all_required_available": len(missing_required) == 0
        }

# Color scheme for terminal output
class Colors:
    """Blue-themed color scheme"""
    # Blue theme colors
    BLUE = '\033[94m'
    LIGHT_BLUE = '\033[96m'
    DARK_BLUE = '\033[34m'
    NAVY = '\033[38;5;17m'
    
    # Standard colors
    BOLD = '\033[1m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    WHITE = '\033[97m'
    GRAY = '\033[90m'
    
    # Special formatting
    UNDERLINE = '\033[4m'
    ITALIC = '\033[3m'
    END = '\033[0m'
    
    @classmethod
    def format_text(cls, text, color, bold=False, underline=False):
        """Format text with colors and styles"""
        formatted = ""
        if bold:
            formatted += cls.BOLD
        if underline:
            formatted += cls.UNDERLINE
        formatted += color + text + cls.END
        return formatted

# Default file extensions to search for
FILE_EXTENSIONS = {
    "js": [".js", ".jsx", ".ts", ".tsx"],
    "config": [".json", ".yaml", ".yml", ".toml", ".ini"],
    "source": [".php", ".py", ".rb", ".go", ".java", ".cpp", ".c"],
    "web": [".html", ".htm", ".css", ".scss", ".sass"]
}

# Common secret patterns (used by mantra)
SECRET_PATTERNS = [
    "api[_-]?key",
    "secret[_-]?key", 
    "access[_-]?token",
    "auth[_-]?token",
    "jwt[_-]?token",
    "bearer[_-]?token",
    "client[_-]?secret",
    "client[_-]?id",
    "password",
    "passwd",
    "pwd",
    "private[_-]?key",
    "public[_-]?key",
    "ssh[_-]?key",
    "encryption[_-]?key",
    "database[_-]?url",
    "db[_-]?password",
    "mongodb[_-]?uri",
    "redis[_-]?url",
    "aws[_-]?access[_-]?key",
    "aws[_-]?secret[_-]?key",
    "s3[_-]?bucket",
    "google[_-]?api[_-]?key",
    "firebase[_-]?key",
    "stripe[_-]?key",
    "paypal[_-]?key",
    "github[_-]?token",
    "gitlab[_-]?token",
    "slack[_-]?token",
    "discord[_-]?token",
    "telegram[_-]?token",
    "twitter[_-]?api",
    "facebook[_-]?api",
    "linkedin[_-]?api"
]

# HTTP status codes to consider as "live"
LIVE_STATUS_CODES = [
    200, 201, 202, 204, 
    300, 301, 302, 303, 307, 308,
    400, 401, 403, 405, 406, 
    500, 501, 502, 503
]

# Common subdomain patterns for validation
COMMON_SUBDOMAINS = [
    "www", "mail", "ftp", "test", "dev", "staging", "api", "admin",
    "blog", "shop", "store", "news", "support", "help", "docs",
    "secure", "login", "auth", "sso", "vpn", "remote", "portal",
    "app", "mobile", "m", "beta", "alpha", "demo", "sandbox"
]
