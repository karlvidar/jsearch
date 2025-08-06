#!/usr/bin/env python3
"""
JSearch Setup Script
Simple setup for development and installation
"""

import os
import sys
import subprocess
from pathlib import Path

def run_command(command, description):
    """Run a command and return success status"""
    print(f"🔵 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e}")
        return False

def main():
    print("🔵 JSearch Setup Script")
    print("=" * 30)
    
    # Make scripts executable
    scripts = ["jsearch.py", "cli.py", "install.sh"]
    for script in scripts:
        if os.path.exists(script):
            os.chmod(script, 0o755)
            print(f"✅ Made {script} executable")
    
    # Install Python requirements
    if os.path.exists("requirements.txt"):
        success = run_command(
            f"{sys.executable} -m pip install -r requirements.txt",
            "Installing Python requirements"
        )
        if not success:
            print("⚠️  Failed to install Python requirements")
    
    # Create symbolic link for easy access (Linux/macOS)
    if os.name != 'nt':  # Not Windows
        try:
            current_dir = os.path.abspath('.')
            jsearch_path = os.path.join(current_dir, 'jsearch.py')
            link_path = '/usr/local/bin/jsearch'
            
            if not os.path.exists(link_path):
                subprocess.run(['sudo', 'ln', '-s', jsearch_path, link_path], check=True)
                print(f"✅ Created symbolic link: {link_path}")
            else:
                print(f"⚠️  Symbolic link already exists: {link_path}")
        except subprocess.CalledProcessError:
            print("⚠️  Could not create symbolic link (requires sudo)")
            print(f"   You can manually add {os.path.abspath('.')} to your PATH")
    
    print("\n🎉 Setup completed!")
    print("\nNext steps:")
    print("1. Run ./install.sh to install required tools")
    print("2. Test with: python3 jsearch.py --check-tools")
    print("3. Start scanning: python3 jsearch.py -u example.com")
    
    if os.name != 'nt' and os.path.exists('/usr/local/bin/jsearch'):
        print("4. Or simply use: jsearch -u example.com")

if __name__ == "__main__":
    main()
