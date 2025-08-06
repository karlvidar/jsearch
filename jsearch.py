#!/usr/bin/env python3
"""
jsearch - Bug Bounty Reconnaissance Tool
A comprehensive subdomain discovery                  if output:
                    line = output.strip()
                    # Add [SUBDOMAIN] prefix for subfinder output
                    if "subfinder subdomain discovery" in description.lower():
                        if line and line.strip():
                            print(f"{Colors.DARK_BLUE}[SUBDOMAIN]{Colors.END} {line}")
                    else:
                        print(line)  # Show live output     # Filter mantra banner if requested
                    if filter_mantra_banner and "mantra secret analysis" in description.lower():
                        # Only show lines that start with [+] (secrets found), skip [-] errors and banner
                        if line and line.startswith('[+]'):
                            print(line)JavaScript analysis tool
"""

import argparse
import os
import sys
import subprocess
import json
import time
from pathlib import Path
from datetime import datetime
from typing import Set, List
import threading

class Colors:
    """Blue-themed color scheme for terminal output"""
    BLUE = '\033[94m'
    LIGHT_BLUE = '\033[96m'
    DARK_BLUE = '\033[34m'
    BOLD = '\033[1m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    GRAY = '\033[90m'
    END = '\033[0m'

class JSearch:
    def __init__(self, target_url: str, output_path: str = None, output_file: str = None):
        self.target_url = target_url.replace('https://', '').replace('http://', '').strip('/')
        self.output_path = output_path or f"jsearch_{self.target_url.replace('.', '_')}"
        self.output_file = output_file
        self.subdomains: Set[str] = set()
        self.live_domains: Set[str] = set()
        self.live_domains_ordered: List[str] = []  # Maintain order for processing
        self.js_files: Set[str] = set()
        
        # Configuration options
        self.custom_wordlist = None
        self.timeout = 300
        self.threads = 50
        self.quiet_mode = False
        self.verbose_mode = False
        
        # Tool skip flags
        self.skip_katana = False
        self.skip_nuclei = False
        self.skip_ffuf = False
        self.skip_gau = False
        self.skip_mantra = False
        
        # Create output directory
        Path(self.output_path).mkdir(parents=True, exist_ok=True)
        
        if not self.quiet_mode:
            self.print_banner()
    
    def print_banner(self):
        """Print the tool banner"""
        banner = f"""
{Colors.BOLD}{Colors.BLUE}
                 __                                         .__
                |__|  ______  ____  _____   _______   ____  |  |__
                |  | /  ___/_/ __ \\ \\__  \\  \\_  __ \\_/ ___\\ |  |  \\ 
                |  | \\___ \\ \\  ___/  / __ \\_ |  | \\/\\  \\___ |   Y  \\ 
            /\\__|  |/____  > \\___  >(____  / |__|    \\___  >|___|  /
            \\______|     \\/      \\/      \\/              \\/      \\/
{Colors.END}
{Colors.LIGHT_BLUE}                          JavaScript Search Tool{Colors.END}
{Colors.DARK_BLUE}                          Target: {self.target_url}{Colors.END}
{Colors.DARK_BLUE}                          Output: {self.output_path}{Colors.END}
        """
        print(banner)
    
    def log(self, message: str, level: str = "INFO"):
        """Log messages with blue theme"""
        if self.quiet_mode and level == "INFO":
            return
            
        timestamp = datetime.now().strftime("%H:%M:%S")
        color_map = {
            "INFO": Colors.LIGHT_BLUE,
            "SUCCESS": Colors.GREEN,
            "WARNING": Colors.YELLOW,
            "ERROR": Colors.RED
        }
        color = color_map.get(level, Colors.LIGHT_BLUE)
        print(f"{color}[{timestamp}] [{level}] {message}{Colors.END}")
    
    def run_command_live(self, command: str, description: str, filter_mantra_banner: bool = False) -> str:
        """Run a shell command and show live output"""
        self.log(f"Running: {description}")
        try:
            process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, bufsize=1, universal_newlines=True)
            
            output_lines = []
            
            # Read output line by line as it comes
            while True:
                output = process.stdout.readline()
                if output == '' and process.poll() is not None:
                    break
                if output:
                    line = output.strip()
                    # Filter mantra banner if requested
                    if filter_mantra_banner and "mantra secret analysis" in description.lower():
                        # Only show lines that start with [+] or [-], skip banner lines
                        if line and (line.startswith('[+]') or line.startswith('[-]')):
                            print(line)
                    # Add [SUBDOMAIN] prefix for subfinder output
                    elif "subfinder subdomain discovery" in description.lower():
                        if line and line.strip():
                            print(f"{Colors.DARK_BLUE}[SUBDOMAIN]{Colors.END} {line}")
                    else:
                        print(line)  # Show live output
                    output_lines.append(output)
            
            # Wait for process to complete and get any remaining output
            stdout, stderr = process.communicate()
            if stdout:
                output_lines.append(stdout)
            
            if process.returncode != 0 and stderr:
                # Only treat as error if it's actually an error, not just warnings
                if not ("warning" in stderr.lower() and "config" in stderr.lower()):
                    self.log(f"Error running {description}: {stderr}", "ERROR")
                    return ""
                elif "warning" in stderr.lower():
                    self.log(f"Warning from {description}: {stderr.strip()}", "WARNING")
            
            return ''.join(output_lines)
            
        except Exception as e:
            self.log(f"Exception running {description}: {str(e)}", "ERROR")
            return ""
    
    def run_command(self, command: str, description: str) -> str:
        """Run a shell command and return output (silent)"""
        self.log(f"Running: {description}")
        try:
            result = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=None)
            if result.returncode != 0:
                # Only treat as error if it's actually an error, not just warnings
                if result.stderr and not ("warning" in result.stderr.lower() and "config" in result.stderr.lower()):
                    self.log(f"Error running {description}: {result.stderr}", "ERROR")
                    return ""
                elif result.stderr and "warning" in result.stderr.lower():
                    self.log(f"Warning from {description}: {result.stderr.strip()}", "WARNING")
            return result.stdout
        except subprocess.TimeoutExpired:
            self.log(f"Timeout running {description}", "WARNING")
            return ""
        except Exception as e:
            self.log(f"Exception running {description}: {str(e)}", "ERROR")
            return ""
    
    def check_tool_availability(self) -> bool:
        """Check if required tools are installed"""
        tools = ["subfinder", "ffuf", "gau", "httpx", "mantra"]
        missing_tools = []
        
        self.log("Checking tool availability...")
        
        for tool in tools:
            try:
                subprocess.run([tool, "-h"], capture_output=True, timeout=5)
            except (subprocess.TimeoutExpired, FileNotFoundError, PermissionError):
                missing_tools.append(tool)
        
        if missing_tools:
            self.log(f"Missing tools: {', '.join(missing_tools)}", "ERROR")
            self.log("Please install missing tools before running jsearch", "ERROR")
            if "mantra" in missing_tools:
                self.log("For mantra, install from: https://github.com/brosck/mantra", "INFO")
            return False
        
        self.log("All required tools are available", "SUCCESS")
        print()
        return True
    
    def discover_subdomains_subfinder(self):
        """Discover subdomains using subfinder"""
        self.log("Starting subdomain discovery with subfinder...")
        
        # Add the target URL itself as the first subdomain
        self.subdomains.add(self.target_url)
        
        output_file = os.path.join(self.output_path, "subfinder_results.txt")
        command = f"subfinder -d {self.target_url} -o {output_file}"
        
        self.run_command_live(command, "subfinder subdomain discovery")
        
        if os.path.exists(output_file):
            with open(output_file, 'r') as f:
                for line in f:
                    subdomain = line.strip()
                    if subdomain and subdomain not in self.subdomains:
                        self.subdomains.add(subdomain)
                        # Don't print here since we already saw it in live output
            
            self.log(f"Found {len(self.subdomains)} subdomains with subfinder", "SUCCESS")
        else:
            self.log("No subfinder results file found", "WARNING")
    
    def discover_subdomains_ffuf(self):
        """Discover subdomains using ffuf with wordlist"""
        if self.skip_ffuf:
            self.log("Skipping ffuf subdomain discovery", "INFO")
            return
            
        self.log("Starting subdomain fuzzing with ffuf...")
        
        # Use custom wordlist if provided, otherwise use default paths
        wordlist_path = self.custom_wordlist or "/usr/share/wordlists/seclists/Discovery/DNS/deepmagic.com-prefixes-top500.txt"
        
        # Check if wordlist exists
        if not os.path.exists(wordlist_path):
            self.log(f"Wordlist not found at {wordlist_path}", "WARNING")
            self.log("Skipping ffuf subdomain discovery", "WARNING")
            return
        
        output_file = os.path.join(self.output_path, "ffuf_results.json")
        command = f"ffuf -w {wordlist_path} -u https://FUZZ.{self.target_url} -o {output_file} -of json -t {self.threads} -timeout {self.timeout}"
        
        self.run_command_live(command, "ffuf subdomain fuzzing")
        
        if os.path.exists(output_file):
            try:
                with open(output_file, 'r') as f:
                    data = json.load(f)
                    initial_count = len(self.subdomains)
                    
                    for result in data.get('results', []):
                        subdomain = result.get('url', '').replace('https://', '').replace('http://', '').strip('/')
                        if subdomain and subdomain not in self.subdomains:
                            self.subdomains.add(subdomain)
                            print(f"{Colors.DARK_BLUE}[SUBDOMAIN]{Colors.END} {subdomain}")
                    
                    new_count = len(self.subdomains) - initial_count
                    self.log(f"Found {new_count} new subdomains with ffuf", "SUCCESS")
            except json.JSONDecodeError:
                self.log("Failed to parse ffuf JSON output", "ERROR")
        else:
            self.log("No ffuf results file found", "WARNING")
    
    def check_live_domains(self):
        """Check which domains are live using httpx"""
        self.log("Checking live domains with httpx...")
        
        if not self.subdomains:
            self.log("No subdomains to check", "WARNING")
            return
        
        # Write subdomains to temp file
        temp_file = os.path.join(self.output_path, "temp_subdomains.txt")
        with open(temp_file, 'w') as f:
            for subdomain in self.subdomains:
                f.write(f"{subdomain}\n")
        
        output_file = os.path.join(self.output_path, "live_domains.txt")
        command = f"httpx -l {temp_file} -o {output_file}"
        
        self.run_command(command, "httpx live domain check")
        
        if os.path.exists(output_file):
            # Use a list to preserve order instead of a set
            live_domains_list = []
            with open(output_file, 'r') as f:
                for line in f:
                    domain = line.strip()
                    if domain:
                        live_domains_list.append(domain)
                        print(f"{Colors.GREEN}[LIVE]{Colors.END} {domain}")
            
            # Convert to set for deduplication but keep the list for order
            self.live_domains = set(live_domains_list)
            # Store ordered list for gau processing
            self.live_domains_ordered = live_domains_list
            
            self.log(f"Found {len(self.live_domains)} live domains", "SUCCESS")
        else:
            self.log("No live domains found", "WARNING")
            self.live_domains_ordered = []
        
        # Clean up temp file
        if os.path.exists(temp_file):
            os.remove(temp_file)
    
    def discover_js_files_gau(self):
        """Discover JS files using gau"""
        if self.skip_gau:
            self.log("Skipping gau JS file discovery", "INFO")
            return
            
        self.log("Discovering JS files with gau...")
        
        if not self.live_domains_ordered:
            self.log("No live domains to scan", "WARNING")
            return
        
        total_js_files_found = 0
        
        for domain in self.live_domains_ordered:
            clean_domain = domain.replace('https://', '').replace('http://', '').strip('/')
            self.log(f"Running: gau JS discovery for {clean_domain}")
            
            # Run gau with live output and filter for JS files
            command = f"gau {clean_domain}"
            
            try:
                process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, bufsize=1, universal_newlines=True)
                
                js_files_for_domain = 0
                
                # Read output line by line as it comes
                while True:
                    output = process.stdout.readline()
                    if output == '' and process.poll() is not None:
                        break
                    if output:
                        url = output.strip()
                        # Check if it's a JS file
                        if url.endswith('.js') and url not in self.js_files:
                            self.js_files.add(url)
                            js_files_for_domain += 1
                            total_js_files_found += 1
                            print(f"{Colors.YELLOW}[JS FILE]{Colors.END} {url}")
                
                # Check for any stderr (warnings) - ignore gau config warnings
                stderr = process.stderr.read()
                if stderr and "warning" in stderr.lower() and "config" not in stderr.lower():
                    self.log(f"Warning from gau JS discovery for {clean_domain}: {stderr.strip()}", "WARNING")
                
                if js_files_for_domain > 0:
                    print(f"{Colors.GREEN}Found {js_files_for_domain} JS files for {clean_domain}{Colors.END}")
                else:
                    print(f"{Colors.RED}No JS files found for {clean_domain}{Colors.END}")
                    
            except Exception as e:
                self.log(f"Error running gau for {clean_domain}: {str(e)}", "ERROR")
        
        if total_js_files_found > 0:
            self.log(f"Found {total_js_files_found} total JS files with gau", "SUCCESS")
        else:
            self.log("No JS files found with gau", "WARNING")
    
    def discover_js_files_katana(self):
        """Discover JS files using katana (optional)"""
        if self.skip_katana:
            self.log("Skipping katana JS file discovery", "INFO")
            return
            
        try:
            subprocess.run(["katana", "-h"], capture_output=True, timeout=5)
        except (subprocess.TimeoutExpired, FileNotFoundError):
            self.log("Katana not found, skipping katana JS discovery", "WARNING")
            return
        
        self.log("Discovering JS files with katana...")
        
        if not self.live_domains_ordered:
            self.log("No live domains to scan", "WARNING")
            return
        
        output_file = os.path.join(self.output_path, "katana_js_files.txt")
        
        # Create temp file with live domains
        temp_file = os.path.join(self.output_path, "temp_live_domains.txt")
        with open(temp_file, 'w') as f:
            for domain in self.live_domains_ordered:
                f.write(f"{domain}\n")
        
        command = f"katana -list {temp_file} -jc -o {output_file}"
        self.run_command_live(command, "katana JS discovery")
        
        if os.path.exists(output_file):
            initial_count = len(self.js_files)
            with open(output_file, 'r') as f:
                for line in f:
                    js_file = line.strip()
                    if js_file and js_file.endswith('.js') and js_file not in self.js_files:
                        self.js_files.add(js_file)
                        # Don't print here since we already saw it in live output
            
            new_count = len(self.js_files) - initial_count
            self.log(f"Found {new_count} new JS files with katana", "SUCCESS")
        else:
            self.log("No JS files found with katana", "WARNING")
        
        # Clean up temp file
        if os.path.exists(temp_file):
            os.remove(temp_file)
    
    def analyze_secrets_mantra(self):
        """Analyze JS files for secrets using mantra"""
        if self.skip_mantra:
            self.log("Skipping mantra secret analysis", "INFO")
            return
            
        self.log("Analyzing JS files for secrets with mantra...")
        
        if not self.js_files:
            self.log("No JS files to analyze", "WARNING")
            return
        
        output_file = os.path.join(self.output_path, "mantra_secrets.txt")
        
        # Create temp file with JS URLs
        temp_file = os.path.join(self.output_path, "temp_js_files.txt")
        with open(temp_file, 'w') as f:
            for js_file in self.js_files:
                f.write(f"{js_file}\n")
        
        # Try different command formats for mantra (correct syntax: cat INPUT | mantra | tee OUTPUT)
        commands_to_try = [
            f"cat {temp_file} | mantra | tee {output_file}",
            f"type {temp_file} | mantra | tee {output_file}"  # Windows alternative to cat
        ]
        
        success = False
        for command in commands_to_try:
            try:
                self.log(f"Trying command: {command}")
                
                # Use run_command_live to show real-time output
                output = self.run_command_live(command, "mantra secret analysis")
                
                if os.path.exists(output_file):
                    success = True
                    break
                    
            except Exception as e:
                self.log(f"Error running mantra: {str(e)}", "ERROR")
                continue
        
        if not success:
            self.log("Could not execute mantra with any known command format", "ERROR")
            # Clean up temp file
            if os.path.exists(temp_file):
                os.remove(temp_file)
            return
        
        if os.path.exists(output_file):
            with open(output_file, 'r') as f:
                content = f.read()
                if content.strip():
                    self.log("Mantra analysis complete! Check mantra_secrets.txt for results", "SUCCESS")
                else:
                    self.log("No secrets found", "INFO")
        else:
            self.log("No mantra output file generated", "WARNING")
        
        # Clean up temp file
        if os.path.exists(temp_file):
            os.remove(temp_file)
    
    def analyze_with_nuclei(self):
        """Run nuclei scans (optional)"""
        if self.skip_nuclei:
            self.log("Skipping nuclei vulnerability scanning", "INFO")
            return
            
        try:
            subprocess.run(["nuclei", "-h"], capture_output=True, timeout=5)
        except (subprocess.TimeoutExpired, FileNotFoundError):
            self.log("Nuclei not found, skipping nuclei analysis", "WARNING")
            return
        
        self.log("Running nuclei scans...")
        
        if not self.live_domains_ordered:
            self.log("No live domains to scan", "WARNING")
            return
        
        # Create temp file with live domains
        temp_file = os.path.join(self.output_path, "temp_live_domains_nuclei.txt")
        with open(temp_file, 'w') as f:
            for domain in self.live_domains_ordered:
                f.write(f"{domain}\n")
        
        output_file = os.path.join(self.output_path, "nuclei_results.txt")
        command = f"nuclei -list {temp_file} -o {output_file} -severity medium,high,critical"
        
        self.run_command(command, "nuclei vulnerability scanning")
        
        if os.path.exists(output_file):
            with open(output_file, 'r') as f:
                content = f.read()
                if content.strip():
                    # Show vulnerabilities found
                    lines = content.strip().split('\n')
                    for line in lines[:3]:  # Show first 3 vulnerabilities
                        if line.strip():
                            print(f"{Colors.RED}[VULN]{Colors.END} {line.strip()[:100]}...")
                    if len(lines) > 3:
                        print(f"{Colors.RED}[VULN]{Colors.END} ... and {len(lines) - 3} more vulnerabilities found")
                    self.log(f"Found {len(lines)} potential vulnerabilities with nuclei", "SUCCESS")
                else:
                    self.log("No vulnerabilities found with nuclei", "INFO")
        else:
            self.log("No nuclei output file generated", "WARNING")
        
        # Clean up temp file
        if os.path.exists(temp_file):
            os.remove(temp_file)
    
    def save_final_output(self):
        """Save final consolidated output"""
        summary = {
            "target": self.target_url,
            "timestamp": datetime.now().isoformat(),
            "subdomains_found": len(self.subdomains),
            "live_domains_found": len(self.live_domains),
            "js_files_found": len(self.js_files),
            "subdomains": list(self.subdomains),
            "live_domains": list(self.live_domains),
            "js_files": list(self.js_files)
        }
        
        # Save summary as JSON
        summary_file = os.path.join(self.output_path, "jsearch_summary.json")
        with open(summary_file, 'w') as f:
            json.dump(summary, f, indent=2)
        
        # Save to custom output file if specified
        if self.output_file:
            with open(self.output_file, 'w') as f:
                json.dump(summary, f, indent=2)
            self.log(f"Results saved to {self.output_file}", "SUCCESS")
        
        self.log(f"Summary saved to {summary_file}", "SUCCESS")
    
    def print_summary(self):
        """Print final summary"""
        print(f"\n{Colors.BOLD}{Colors.BLUE}=== JSEARCH SUMMARY ==={Colors.END}")
        print(f"{Colors.LIGHT_BLUE}Target: {self.target_url}{Colors.END}")
        print(f"{Colors.LIGHT_BLUE}Subdomains found: {len(self.subdomains)}{Colors.END}")
        print(f"{Colors.LIGHT_BLUE}Live domains: {len(self.live_domains)}{Colors.END}")
        print(f"{Colors.LIGHT_BLUE}JS files found: {len(self.js_files)}{Colors.END}")
        print(f"{Colors.LIGHT_BLUE}Output directory: {self.output_path}{Colors.END}")
        print(f"{Colors.BOLD}{Colors.BLUE}========================{Colors.END}\n")
    
    def run(self):
        """Main execution flow"""
        if not self.check_tool_availability():
            return False
        
        try:
            
            # Step 1: Discover subdomains
            print(f"{Colors.BOLD}{Colors.BLUE}[1/5] Gathering Subdomains{Colors.END}")
            self.discover_subdomains_subfinder()
            self.discover_subdomains_ffuf()
            
            # Step 2: Check live domains
            print(f"\n{Colors.BOLD}{Colors.BLUE}[2/5] Checking Live Domains{Colors.END}")
            self.check_live_domains()
            
            # Step 3: Discover JS files
            print(f"\n{Colors.BOLD}{Colors.BLUE}[3/5] Discovering JS Files{Colors.END}")
            self.discover_js_files_gau()
            self.discover_js_files_katana()
            
            # Step 4: Analyze for secrets
            print(f"\n{Colors.BOLD}{Colors.BLUE}[4/5] Analyzing for Secrets{Colors.END}")
            self.analyze_secrets_mantra()
            
            # Step 5: Optional nuclei scan
            print(f"\n{Colors.BOLD}{Colors.BLUE}[5/5] Scanning for Vulnerabilities{Colors.END}")
            self.analyze_with_nuclei()
            
            # Step 6: Save results
            print(f"\n{Colors.BOLD}{Colors.BLUE}Finalizing Results{Colors.END}")
            self.save_final_output()
            self.print_summary()
            
            return True
            
        except KeyboardInterrupt:
            self.log("Scan interrupted by user", "WARNING")
            return False
        except Exception as e:
            self.log(f"Unexpected error: {str(e)}", "ERROR")
            return False

def main():
    parser = argparse.ArgumentParser(
        description="jsearch - JavaScript Search Tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  jsearch -u example.com
  jsearch -u example.com -p /tmp/results
  jsearch -u example.com -o results.json
        """
    )
    
    parser.add_argument('-u', '--url', required=True, help='Target URL/domain')
    parser.add_argument('-p', '--path', help='Output directory path')
    parser.add_argument('-o', '--output', help='Output file for results')
    
    args = parser.parse_args()
    
    if not args.url:
        parser.print_help()
        return
    
    jsearch = JSearch(args.url, args.path, args.output)
    
    start_time = time.time()
    success = jsearch.run()
    end_time = time.time()
    
    if success:
        duration = int(end_time - start_time)
        jsearch.log(f"Scan completed in {duration} seconds", "SUCCESS")
    else:
        jsearch.log("Scan failed or was interrupted", "ERROR")

if __name__ == "__main__":
    main()
