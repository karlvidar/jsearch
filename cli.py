#!/usr/bin/env python3
"""
JSearch CLI Interface
Enhanced command-line interface with additional options
"""

import argparse
import sys
from pathlib import Path
from jsearch import JSearch, Colors
from config import Config

def create_parser():
    """Create and configure argument parser"""
    parser = argparse.ArgumentParser(
        prog='jsearch',
        description=f"""{Colors.BLUE}
     ╦╔═╗╔═╗╔═╗╦═╗╔═╗╦ ╦
     ║╚═╗║╣ ╠═╣╠╦╝║  ╠═╣
    ╚╝╚═╝╚═╝╩ ╩╩╚═╚═╝╩ ╩
{Colors.END}
{Colors.LIGHT_BLUE}Bug Bounty Reconnaissance Tool{Colors.END}

A comprehensive subdomain discovery and JavaScript analysis tool
that combines multiple reconnaissance tools in a streamlined workflow.
        """,
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=f"""{Colors.DARK_BLUE}Examples:{Colors.END}
  {Colors.LIGHT_BLUE}Basic scan:{Colors.END}
    jsearch -u example.com
    
  {Colors.LIGHT_BLUE}Custom output directory:{Colors.END}
    jsearch -u example.com -p /tmp/bug_bounty_results
    
  {Colors.LIGHT_BLUE}Save to specific file:{Colors.END}
    jsearch -u example.com -o results.json
    
  {Colors.LIGHT_BLUE}Quiet mode with custom wordlist:{Colors.END}
    jsearch -u example.com -q --wordlist /path/to/wordlist.txt
    
  {Colors.LIGHT_BLUE}Skip certain tools:{Colors.END}
    jsearch -u example.com --skip-katana --skip-nuclei
    
  {Colors.LIGHT_BLUE}Check tool availability:{Colors.END}
    jsearch --check-tools

{Colors.DARK_BLUE}Tool Integration:{Colors.END}
  • subfinder    - Passive subdomain discovery
  • ffuf         - Active subdomain fuzzing  
  • httpx        - Live domain verification
  • gau          - JavaScript file discovery
  • katana       - Additional JS crawling (optional)
  • mantra       - Secret analysis
  • nuclei       - Vulnerability scanning (optional)
        """
    )
    
    # Main arguments
    parser.add_argument(
        '-u', '--url', 
        required=False,
        help='Target URL/domain (required for scans)'
    )
    
    parser.add_argument(
        '-p', '--path', 
        help='Custom output directory path'
    )
    
    parser.add_argument(
        '-o', '--output', 
        help='Output file for JSON results'
    )
    
    # Tool control options
    parser.add_argument(
        '--skip-katana',
        action='store_true',
        help='Skip katana JS file discovery'
    )
    
    parser.add_argument(
        '--skip-nuclei',
        action='store_true', 
        help='Skip nuclei vulnerability scanning'
    )
    
    parser.add_argument(
        '--skip-ffuf',
        action='store_true',
        help='Skip ffuf subdomain fuzzing'
    )
    
    parser.add_argument(
        '--skip-gau',
        action='store_true',
        help='Skip gau JS file discovery'
    )
    
    parser.add_argument(
        '--skip-mantra',
        action='store_true',
        help='Skip mantra secret analysis'
    )
    
    # Configuration options
    parser.add_argument(
        '--wordlist',
        help='Custom wordlist path for ffuf'
    )
    
    parser.add_argument(
        '--timeout',
        type=int,
        default=Config.DEFAULT_TIMEOUT,
        help=f'Command timeout in seconds (default: {Config.DEFAULT_TIMEOUT})'
    )
    
    parser.add_argument(
        '--threads',
        type=int,
        default=Config.HTTPX_THREADS,
        help=f'Number of threads for tools (default: {Config.HTTPX_THREADS})'
    )
    
    # Output control
    parser.add_argument(
        '-q', '--quiet',
        action='store_true',
        help='Reduce output verbosity'
    )
    
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Increase output verbosity'
    )
    
    parser.add_argument(
        '--no-color',
        action='store_true',
        help='Disable colored output'
    )
    
    # Utility options
    parser.add_argument(
        '--check-tools',
        action='store_true',
        help='Check if required tools are installed'
    )
    
    parser.add_argument(
        '--version',
        action='version',
        version='%(prog)s 1.0.0'
    )
    
    return parser

def check_tools():
    """Check tool availability and print status"""
    print(f"{Colors.BOLD}{Colors.BLUE}=== Tool Availability Check ==={Colors.END}\n")
    
    validation = Config.validate_tools()
    
    # Check required tools
    if validation["missing_required"]:
        print(f"{Colors.RED}❌ Missing required tools:{Colors.END}")
        for tool in validation["missing_required"]:
            print(f"   • {tool}")
        print()
    else:
        print(f"{Colors.GREEN}✅ All required tools are available{Colors.END}\n")
    
    # Check optional tools
    if validation["missing_optional"]:
        print(f"{Colors.YELLOW}⚠️  Missing optional tools:{Colors.END}")
        for tool in validation["missing_optional"]:
            print(f"   • {tool}")
        print()
    else:
        print(f"{Colors.GREEN}✅ All optional tools are available{Colors.END}\n")
    
    # Check wordlist
    wordlist_path = Config.get_wordlist_path()
    if wordlist_path:
        print(f"{Colors.GREEN}✅ Wordlist found: {wordlist_path}{Colors.END}")
    else:
        print(f"{Colors.YELLOW}⚠️  No wordlist found in default locations{Colors.END}")
        print(f"   Expected locations:")
        for path in Config.WORDLIST_PATHS:
            print(f"   • {path}")
    
    print(f"\n{Colors.BLUE}Installation help:{Colors.END}")
    print(f"   Run: ./install.sh")
    print(f"   Or check README.md for manual installation\n")
    
    return validation["all_required_available"]

def validate_arguments(args):
    """Validate command line arguments"""
    if not args.check_tools and not args.url:
        print(f"{Colors.RED}Error: URL is required for scans{Colors.END}")
        print(f"Use {Colors.LIGHT_BLUE}jsearch -u example.com{Colors.END} or {Colors.LIGHT_BLUE}jsearch --check-tools{Colors.END}")
        return False
    
    if args.url:
        # Basic URL validation
        url = args.url.lower()
        if url.startswith(('http://', 'https://')):
            args.url = args.url.replace('https://', '').replace('http://', '')
        
        if '/' in args.url:
            args.url = args.url.split('/')[0]
    
    # Check output path permissions
    if args.path:
        try:
            Path(args.path).mkdir(parents=True, exist_ok=True)
        except PermissionError:
            print(f"{Colors.RED}Error: Permission denied for path: {args.path}{Colors.END}")
            return False
    
    return True

def main():
    """Main CLI entry point"""
    parser = create_parser()
    args = parser.parse_args()
    
    # Handle color output
    if args.no_color:
        # Disable colors
        for attr in dir(Colors):
            if not attr.startswith('_') and attr != 'format_text':
                setattr(Colors, attr, '')
    
    # Handle tool check
    if args.check_tools:
        success = check_tools()
        sys.exit(0 if success else 1)
    
    # Validate arguments
    if not validate_arguments(args):
        sys.exit(1)
    
    # Create JSearch instance with custom configuration
    jsearch = JSearch(
        target_url=args.url,
        output_path=args.path,
        output_file=args.output
    )
    
    # Apply configuration overrides
    if args.wordlist:
        jsearch.custom_wordlist = args.wordlist
    
    if args.timeout:
        jsearch.timeout = args.timeout
    
    if args.threads:
        jsearch.threads = args.threads
    
    if args.quiet:
        jsearch.quiet_mode = True
    
    if args.verbose:
        jsearch.verbose_mode = True
    
    # Set tool skip flags
    jsearch.skip_katana = args.skip_katana
    jsearch.skip_nuclei = args.skip_nuclei
    jsearch.skip_ffuf = args.skip_ffuf
    jsearch.skip_gau = args.skip_gau
    jsearch.skip_mantra = args.skip_mantra
    
    # Run the scan
    try:
        import time
        start_time = time.time()
        
        success = jsearch.run()
        
        end_time = time.time()
        duration = int(end_time - start_time)
        
        if success:
            jsearch.log(f"Scan completed successfully in {duration} seconds", "SUCCESS")
            sys.exit(0)
        else:
            jsearch.log("Scan failed or was interrupted", "ERROR")
            sys.exit(1)
            
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}Scan interrupted by user{Colors.END}")
        sys.exit(130)
    except Exception as e:
        print(f"\n{Colors.RED}Unexpected error: {str(e)}{Colors.END}")
        sys.exit(1)

if __name__ == "__main__":
    main()
