#!/usr/bin/env python3

import re

def normalize_host(host: str) -> str:
    """Normalize a hostname for consistent comparisons and storage."""
    if not host:
        return ""
    h = host.strip().lower()
    # Strip scheme if present
    if h.startswith('http://'):
        h = h[7:]
    elif h.startswith('https://'):
        h = h[8:]
    # Remove ANSI escape codes if present (including cursor control sequences)
    # Updated regex to handle both uppercase and lowercase command letters
    h = re.sub(r'\x1b\[[0-9;]*[a-zA-Z]', '', h)
    # Remove path, query, fragment
    for sep in ['/', '?', '#']:
        if sep in h:
            h = h.split(sep, 1)[0]
    # Trim leading/trailing dots and whitespace
    h = h.strip().strip('.')
    return h

# Test the normalize_host function with the problematic domains from the debug output
test_domains = [
    '\x1b[2kdocs.landspitali.is',
    '\x1b[2kftp.landspitali.is', 
    '\x1b[2kgh.landspitali.is',
    'docs.landspitali.is',
    'ftp.landspitali.is'
]

print("Testing normalize_host function:")
for domain in test_domains:
    normalized = normalize_host(domain)
    print(f"'{domain}' -> '{normalized}' (length: {len(normalized)})")

# Test if they would match
subfinder_set = {'docs.landspitali.is', 'ftp.landspitali.is', 'gh.landspitali.is'}
ffuf_set = {normalize_host('\x1b[2kdocs.landspitali.is'), normalize_host('\x1b[2kftp.landspitali.is')}

print(f"\nSubfinder set: {subfinder_set}")
print(f"FFuf normalized set: {ffuf_set}")
print(f"Intersection: {subfinder_set & ffuf_set}")
