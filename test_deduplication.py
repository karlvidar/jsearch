#!/usr/bin/env python3

# Simple test to verify deduplication logic
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
    # Remove ANSI escape codes if present
    h = re.sub(r'\x1b\[[0-9;]*m', '', h)
    # Remove path, query, fragment
    for sep in ['/', '?', '#']:
        if sep in h:
            h = h.split(sep, 1)[0]
    # Trim leading/trailing dots and whitespace
    h = h.strip().strip('.')
    return h

# Simulate subfinder results (what the user saw in output)
subfinder_results = set([
    "landspitali.is",
    "f5-vs-common-misc.landspitali.is",
    "lsh005.landspitali.is",
    "vpn.landspitali.is",
    "docs.landspitali.is",
    "www.landspitali.is",
    "ftp.landspitali.is",
    "iris.landspitali.is",
    "join.landspitali.is",
    "gh.landspitali.is"
])

# Simulate ffuf results (what the user saw in output)
ffuf_raw = [
    "ftp                     [Status: 403, Size: 38, Words: 6, Lines: 1, Duration: 2ms]",
    "vpn                     [Status: 200, Size: 345, Words: 113, Lines: 11, Duration: 4ms]",
    "www                     [Status: 200, Size: 45831, Words: 3342, Lines: 205, Duration: 19ms]",
    "helpdesk                [Status: 200, Size: 13901, Words: 2202, Lines: 323, Duration: 25ms]",
    "docs                    [Status: 200, Size: 3637, Words: 447, Lines: 117, Duration: 37ms]",
    "iris                    [Status: 403, Size: 6686, Words: 108, Lines: 1, Duration: 16ms]",
    "join                    [Status: 200, Size: 991, Words: 59, Lines: 1, Duration: 225ms]",
    "gh                      [Status: 403, Size: 2000, Words: 328, Lines: 60, Duration: 2ms]",
    "oc                      [Status: 302, Size: 0, Words: 1, Lines: 1, Duration: 49ms]"
]

target_url = "landspitali.is"

# Parse ffuf results using same logic as in jsearch
found_by_ffuf = set()

for raw in ffuf_raw:
    line = raw.strip()
    if not line or '[Status:' not in line:
        continue
    # Strip ANSI codes and extract left side before status
    clean_line = re.sub(r'\x1b\[[0-9;]*m', '', line)
    left = clean_line.split('[Status:', 1)[0].strip().strip('.')
    if not left:
        continue
    # If ffuf printed a full FQDN, use it as-is; otherwise append the target
    if '.' in left:
        candidate = left
    else:
        candidate = f"{left}.{target_url}"
    full_sub = normalize_host(candidate)
    if full_sub:
        found_by_ffuf.add(full_sub)

print("Subfinder results:")
for domain in sorted(subfinder_results):
    print(f"  {domain}")

print(f"\nFFuf found:")
for domain in sorted(found_by_ffuf):
    print(f"  {domain}")

print(f"\nNew from ffuf (should only be helpdesk and oc):")
new_from_ffuf = []
for h in found_by_ffuf:
    if h not in subfinder_results:
        new_from_ffuf.append(h)
        print(f"  {h} (NEW)")
    else:
        print(f"  {h} (duplicate from subfinder)")

print(f"\nSummary: {len(new_from_ffuf)} new domains found by ffuf")
print("Expected: 2 new domains (helpdesk.landspitali.is, oc.landspitali.is)")
