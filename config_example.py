# JSearch Example Configuration
# Copy this file to config_local.py and customize for your environment

import os
from config import Config

class LocalConfig(Config):
    """Local configuration overrides"""
    
    # Custom wordlist paths for your environment
    WORDLIST_PATHS = [
        "/usr/share/wordlists/seclists/Discovery/DNS/bug-bounty-program-subdomains-trickest-inventory.txt",
        "/opt/SecLists/Discovery/DNS/bug-bounty-program-subdomains-trickest-inventory.txt",
        "/home/user/wordlists/subdomains.txt",
        "C:\\Tools\\wordlists\\subdomains.txt",  # Windows path example
        "./wordlists/subdomains.txt",
    ]
    
    # Adjust timeouts for your network
    DEFAULT_TIMEOUT = 600  # 10 minutes for slow networks
    HTTPX_TIMEOUT = 15
    FFUF_TIMEOUT = 15
    
    # Adjust thread counts for your system
    HTTPX_THREADS = 100  # Increase for faster systems
    FFUF_THREADS = 100
    
    # Custom tool configurations
    SUBFINDER_CONFIG = {
        "sources": ["all"],
        "timeout": 60,
        "silent": True,
        "max_time": 300  # 5 minutes max
    }
    
    NUCLEI_CONFIG = {
        "severity": ["medium", "high", "critical"],
        "timeout": 60,
        "rate_limit": 200,  # Increase for faster scanning
        "silent": True,
        "templates": [
            "cves/",
            "exposures/",
            "vulnerabilities/"
        ]
    }
    
    # Output preferences
    DEFAULT_OUTPUT_DIR = "jsearch_results"
    KEEP_TEMP_FILES = True  # Keep temp files for debugging
    
    # Custom patterns for secret detection
    CUSTOM_SECRET_PATTERNS = [
        "my_api_key",
        "company_secret",
        "internal_token"
    ]

# Example usage:
# from config_local import LocalConfig
# config = LocalConfig()
# wordlist = config.get_wordlist_path()
