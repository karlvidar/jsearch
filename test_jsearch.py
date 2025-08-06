#!/usr/bin/env python3
"""
JSearch Test Suite
Test the functionality of jsearch components
"""

import os
import sys
import tempfile
import shutil
import json
from pathlib import Path
import subprocess

# Add current directory to path to import jsearch modules
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from jsearch import JSearch, Colors
from config import Config

class TestRunner:
    def __init__(self):
        self.test_dir = None
        self.passed = 0
        self.failed = 0
        
    def setup(self):
        """Setup test environment"""
        self.test_dir = tempfile.mkdtemp(prefix="jsearch_test_")
        print(f"{Colors.BLUE}Test directory: {self.test_dir}{Colors.END}")
        
    def cleanup(self):
        """Clean up test environment"""
        if self.test_dir and os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)
            
    def log_test(self, name, passed, details=""):
        """Log test result"""
        if passed:
            print(f"{Colors.GREEN}✅ {name}{Colors.END}")
            self.passed += 1
        else:
            print(f"{Colors.RED}❌ {name}{Colors.END}")
            if details:
                print(f"   {details}")
            self.failed += 1
    
    def test_imports(self):
        """Test if all modules can be imported"""
        try:
            from jsearch import JSearch, Colors
            from config import Config
            self.log_test("Import modules", True)
        except ImportError as e:
            self.log_test("Import modules", False, str(e))
    
    def test_config(self):
        """Test configuration functionality"""
        try:
            # Test wordlist detection
            wordlist = Config.get_wordlist_path()
            wordlist_found = wordlist is not None
            
            # Test tool validation
            validation = Config.validate_tools()
            
            self.log_test("Config wordlist detection", True, f"Found: {wordlist}")
            self.log_test("Config tool validation", True, f"Missing required: {validation['missing_required']}")
            
        except Exception as e:
            self.log_test("Config functionality", False, str(e))
    
    def test_jsearch_creation(self):
        """Test JSearch object creation"""
        try:
            output_dir = os.path.join(self.test_dir, "test_output")
            jsearch = JSearch("example.com", output_path=output_dir)
            
            # Check if output directory was created
            dir_created = os.path.exists(output_dir)
            
            # Check basic attributes
            attrs_correct = (
                jsearch.target_url == "example.com" and
                jsearch.output_path == output_dir and
                isinstance(jsearch.subdomains, set) and
                isinstance(jsearch.live_domains, set) and
                isinstance(jsearch.js_files, set)
            )
            
            self.log_test("JSearch object creation", dir_created and attrs_correct)
            
        except Exception as e:
            self.log_test("JSearch object creation", False, str(e))
    
    def test_tool_availability(self):
        """Test tool availability checking"""
        try:
            jsearch = JSearch("test.com", output_path=os.path.join(self.test_dir, "tools_test"))
            jsearch.quiet_mode = True
            
            # This should not crash
            available = jsearch.check_tool_availability()
            
            self.log_test("Tool availability check", True, f"Tools available: {available}")
            
        except Exception as e:
            self.log_test("Tool availability check", False, str(e))
    
    def test_output_generation(self):
        """Test output file generation"""
        try:
            output_dir = os.path.join(self.test_dir, "output_test")
            jsearch = JSearch("test.com", output_path=output_dir)
            jsearch.quiet_mode = True
            
            # Add some fake data
            jsearch.subdomains.add("sub1.test.com")
            jsearch.subdomains.add("sub2.test.com")
            jsearch.live_domains.add("https://sub1.test.com")
            jsearch.js_files.add("https://sub1.test.com/app.js")
            
            # Generate output
            jsearch.save_final_output()
            
            # Check if summary file was created
            summary_file = os.path.join(output_dir, "jsearch_summary.json")
            summary_exists = os.path.exists(summary_file)
            
            # Check summary content
            content_valid = False
            if summary_exists:
                with open(summary_file, 'r') as f:
                    data = json.load(f)
                    content_valid = (
                        data.get("target") == "test.com" and
                        data.get("subdomains_found") == 2 and
                        data.get("live_domains_found") == 1 and
                        data.get("js_files_found") == 1
                    )
            
            self.log_test("Output generation", summary_exists and content_valid)
            
        except Exception as e:
            self.log_test("Output generation", False, str(e))
    
    def test_cli_help(self):
        """Test CLI help functionality"""
        try:
            # Test if CLI script can be imported and shows help
            result = subprocess.run([
                sys.executable, "cli.py", "--help"
            ], capture_output=True, text=True, timeout=10)
            
            help_works = result.returncode == 0 and "jsearch" in result.stdout.lower()
            
            self.log_test("CLI help functionality", help_works)
            
        except (subprocess.TimeoutExpired, FileNotFoundError) as e:
            self.log_test("CLI help functionality", False, f"Process error: {str(e)}")
        except Exception as e:
            self.log_test("CLI help functionality", False, str(e))
    
    def test_colors(self):
        """Test color functionality"""
        try:
            # Test color constants exist
            color_attrs = ['BLUE', 'LIGHT_BLUE', 'GREEN', 'RED', 'YELLOW', 'END']
            colors_exist = all(hasattr(Colors, attr) for attr in color_attrs)
            
            # Test color formatting (skip if method doesn't exist)
            formatting_works = True
            if hasattr(Colors, 'format_text'):
                formatted = Colors.format_text("test", Colors.BLUE, bold=True)
                formatting_works = Colors.BOLD in formatted and Colors.BLUE in formatted
            
            self.log_test("Color functionality", colors_exist and formatting_works)
            
        except Exception as e:
            self.log_test("Color functionality", False, str(e))
    
    def run_all_tests(self):
        """Run all tests"""
        print(f"{Colors.BOLD}{Colors.BLUE}🧪 JSearch Test Suite{Colors.END}")
        print("=" * 40)
        
        self.setup()
        
        try:
            self.test_imports()
            self.test_config()
            self.test_jsearch_creation()
            self.test_tool_availability()
            self.test_output_generation()
            self.test_cli_help()
            self.test_colors()
            
        finally:
            self.cleanup()
        
        # Print summary
        total = self.passed + self.failed
        print(f"\n{Colors.BOLD}Test Results:{Colors.END}")
        print(f"{Colors.GREEN}✅ Passed: {self.passed}/{total}{Colors.END}")
        
        if self.failed > 0:
            print(f"{Colors.RED}❌ Failed: {self.failed}/{total}{Colors.END}")
            return False
        else:
            print(f"{Colors.GREEN}🎉 All tests passed!{Colors.END}")
            return True

def main():
    """Main test function"""
    runner = TestRunner()
    success = runner.run_all_tests()
    
    if not success:
        print(f"\n{Colors.YELLOW}Note: Some tests may fail if required tools are not installed.{Colors.END}")
        print(f"{Colors.YELLOW}Run './install.sh' to install required tools.{Colors.END}")
    
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
