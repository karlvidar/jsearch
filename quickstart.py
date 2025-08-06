#!/usr/bin/env python3
"""
JSearch Quick Start Guide
Interactive demo and usage examples
"""

import os
import sys
import time

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config import Colors, Config

def print_banner():
    """Print the JSearch banner"""
    banner = f"""
{Colors.BOLD}{Colors.BLUE}
     ╦╔═╗╔═╗╔═╗╦═╗╔═╗╦ ╦
     ║╚═╗║╣ ╠═╣╠╦╝║  ╠═╣
    ╚╝╚═╝╚═╝╩ ╩╩╚═╚═╝╩ ╩
{Colors.END}
{Colors.LIGHT_BLUE}    Bug Bounty Reconnaissance Tool{Colors.END}
{Colors.DARK_BLUE}    Quick Start Guide{Colors.END}
    """
    print(banner)

def show_installation():
    """Show installation steps"""
    print(f"{Colors.BOLD}{Colors.BLUE}🔧 Installation{Colors.END}")
    print("=" * 40)
    
    steps = [
        "1. Clone the repository:",
        "   git clone <repository-url>",
        "   cd jsearch",
        "",
        "2. Run setup script:",
        "   python3 setup.py",
        "",
        "3. Install required tools:",
        "   ./install.sh",
        "",
        "4. Verify installation:",
        "   python3 cli.py --check-tools"
    ]
    
    for step in steps:
        if step.startswith(("   git", "   python", "   ./", "   python3")):
            print(f"{Colors.LIGHT_BLUE}{step}{Colors.END}")
        else:
            print(step)
    print()

def show_basic_usage():
    """Show basic usage examples"""
    print(f"{Colors.BOLD}{Colors.BLUE}🚀 Basic Usage{Colors.END}")
    print("=" * 40)
    
    examples = [
        ("Simple scan:", "python3 jsearch.py -u example.com"),
        ("Custom output directory:", "python3 jsearch.py -u example.com -p /tmp/results"),
        ("Save to specific file:", "python3 jsearch.py -u example.com -o results.json"),
        ("Quiet mode:", "python3 jsearch.py -u example.com -q"),
        ("Skip optional tools:", "python3 jsearch.py -u example.com --skip-katana --skip-nuclei"),
        ("Custom wordlist:", "python3 jsearch.py -u example.com --wordlist /path/to/wordlist.txt"),
        ("Enhanced CLI:", "python3 cli.py -u example.com -v")
    ]
    
    for description, command in examples:
        print(f"{Colors.GREEN}{description}{Colors.END}")
        print(f"  {Colors.LIGHT_BLUE}{command}{Colors.END}")
        print()

def show_workflow():
    """Show the tool workflow"""
    print(f"{Colors.BOLD}{Colors.BLUE}⚙️  Workflow{Colors.END}")
    print("=" * 40)
    
    steps = [
        ("1. Subdomain Discovery", "subfinder + ffuf", "Passive & active subdomain enumeration"),
        ("2. Live Domain Check", "httpx", "Verify which subdomains are live"),
        ("3. JavaScript Discovery", "gau + katana", "Find JS files from live domains"),
        ("4. Secret Analysis", "mantra", "Analyze JS files for secrets"),
        ("5. Vulnerability Scan", "nuclei", "Optional vulnerability scanning"),
        ("6. Report Generation", "JSON output", "Consolidated results")
    ]
    
    for step, tools, description in steps:
        print(f"{Colors.GREEN}{step}{Colors.END}")
        print(f"  Tools: {Colors.LIGHT_BLUE}{tools}{Colors.END}")
        print(f"  {Colors.GRAY}{description}{Colors.END}")
        print()

def show_output_structure():
    """Show output directory structure"""
    print(f"{Colors.BOLD}{Colors.BLUE}📁 Output Structure{Colors.END}")
    print("=" * 40)
    
    structure = """
jsearch_example_com/
├── subfinder_results.txt      # Subfinder discoveries
├── ffuf_results.json         # Ffuf fuzzing results  
├── live_domains.txt          # Live domain verification
├── gau_js_files.txt          # JS files from gau
├── katana_js_files.txt       # JS files from katana
├── mantra_secrets.txt        # Secret analysis results
├── nuclei_results.txt        # Vulnerability scan results
└── jsearch_summary.json      # Consolidated summary
    """
    
    print(f"{Colors.LIGHT_BLUE}{structure}{Colors.END}")

def check_system_status():
    """Check system readiness"""
    print(f"{Colors.BOLD}{Colors.BLUE}🔍 System Status{Colors.END}")
    print("=" * 40)
    
    # Check Python
    python_version = sys.version.split()[0]
    print(f"Python Version: {Colors.GREEN}{python_version}{Colors.END}")
    
    # Check tools
    validation = Config.validate_tools()
    
    if validation["all_required_available"]:
        print(f"Required Tools: {Colors.GREEN}✅ All available{Colors.END}")
    else:
        print(f"Required Tools: {Colors.RED}❌ Missing: {', '.join(validation['missing_required'])}{Colors.END}")
    
    if not validation["missing_optional"]:
        print(f"Optional Tools: {Colors.GREEN}✅ All available{Colors.END}")
    else:
        print(f"Optional Tools: {Colors.YELLOW}⚠️  Missing: {', '.join(validation['missing_optional'])}{Colors.END}")
    
    # Check wordlist
    wordlist = Config.get_wordlist_path()
    if wordlist:
        print(f"Wordlist: {Colors.GREEN}✅ Found at {wordlist}{Colors.END}")
    else:
        print(f"Wordlist: {Colors.YELLOW}⚠️  Not found in default locations{Colors.END}")
    
    print()

def show_troubleshooting():
    """Show common troubleshooting tips"""
    print(f"{Colors.BOLD}{Colors.BLUE}🛠️  Troubleshooting{Colors.END}")
    print("=" * 40)
    
    tips = [
        ("Tools not found", "Add Go bin to PATH: export PATH=\"$PATH:$HOME/go/bin\""),
        ("Permission denied", "Make scripts executable: chmod +x *.py *.sh"),
        ("Wordlist missing", "Install SecLists: sudo apt install seclists"),
        ("Timeout errors", "Increase timeout: --timeout 600"),
        ("Memory issues", "Reduce threads: --threads 25"),
        ("Network issues", "Check firewall and proxy settings")
    ]
    
    for problem, solution in tips:
        print(f"{Colors.YELLOW}Problem: {problem}{Colors.END}")
        print(f"  Solution: {Colors.LIGHT_BLUE}{solution}{Colors.END}")
        print()

def interactive_demo():
    """Run interactive demo"""
    print(f"{Colors.BOLD}{Colors.BLUE}🎯 Interactive Demo{Colors.END}")
    print("=" * 40)
    
    try:
        target = input(f"{Colors.LIGHT_BLUE}Enter a target domain (or press Enter for demo): {Colors.END}").strip()
        if not target:
            target = "example.com"
        
        print(f"\n{Colors.GREEN}Demo command for {target}:{Colors.END}")
        print(f"{Colors.LIGHT_BLUE}python3 cli.py -u {target} --check-tools{Colors.END}")
        
        run_demo = input(f"\n{Colors.YELLOW}Run the demo? (y/N): {Colors.END}").strip().lower()
        
        if run_demo == 'y':
            print(f"\n{Colors.BLUE}Running demo...{Colors.END}")
            os.system(f'python3 cli.py -u {target} --check-tools')
        else:
            print(f"{Colors.GRAY}Demo skipped{Colors.END}")
            
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}Demo cancelled{Colors.END}")

def main():
    """Main quick start function"""
    print_banner()
    
    sections = [
        ("Installation", show_installation),
        ("Basic Usage", show_basic_usage),  
        ("Workflow", show_workflow),
        ("Output Structure", show_output_structure),
        ("System Status", check_system_status),
        ("Troubleshooting", show_troubleshooting)
    ]
    
    for title, func in sections:
        func()
        time.sleep(1)  # Brief pause between sections
    
    # Interactive demo
    try:
        interactive_demo()
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}Quick start guide interrupted{Colors.END}")
    
    print(f"\n{Colors.BOLD}{Colors.GREEN}🎉 Ready to start bug hunting!{Colors.END}")
    print(f"{Colors.BLUE}For more information, check README.md or DEVELOPMENT.md{Colors.END}")

if __name__ == "__main__":
    main()
