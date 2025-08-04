#!/usr/bin/env python3
"""
Build and publish script for Prarabdha Cache System
"""

import subprocess
import sys
import os
from pathlib import Path

def run_command(command, description):
    """Run a command and handle errors."""
    print(f"\n🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed:")
        print(f"Error: {e.stderr}")
        return False

def clean_build():
    """Clean previous build artifacts."""
    print("\n🧹 Cleaning previous build artifacts...")
    commands = [
        "rm -rf build/",
        "rm -rf dist/",
        "rm -rf *.egg-info/",
        "find . -name '*.pyc' -delete",
        "find . -name '__pycache__' -type d -exec rm -rf {} +"
    ]
    
    for cmd in commands:
        try:
            subprocess.run(cmd, shell=True, check=True)
        except subprocess.CalledProcessError:
            pass  # Ignore errors for cleaning
    
    print("✅ Build artifacts cleaned")

def build_package():
    """Build the package."""
    return run_command(
        "python3 -m build",
        "Building package"
    )

def check_package():
    """Check the package for issues."""
    return run_command(
        "python3 -m twine check dist/*",
        "Checking package"
    )

def upload_to_testpypi():
    """Upload to TestPyPI."""
    return run_command(
        "python3 -m twine upload --repository testpypi dist/*",
        "Uploading to TestPyPI"
    )

def upload_to_pypi():
    """Upload to PyPI."""
    return run_command(
        "python3 -m twine upload dist/*",
        "Uploading to PyPI"
    )

def install_test():
    """Test installation from PyPI."""
    return run_command(
        "pip install prarabdha --index-url https://test.pypi.org/simple/",
        "Testing installation from TestPyPI"
    )

def main():
    """Main build and publish process."""
    print("🚀 Prarabdha Cache System - Build and Publish")
    print("=" * 50)
    
    # Check if we're in the right directory
    if not Path("pyproject.toml").exists():
        print("❌ Error: pyproject.toml not found. Please run this script from the project root.")
        sys.exit(1)
    
    # Clean previous builds
    clean_build()
    
    # Build package
    if not build_package():
        print("❌ Build failed. Exiting.")
        sys.exit(1)
    
    # Check package
    if not check_package():
        print("❌ Package check failed. Exiting.")
        sys.exit(1)
    
    print("\n📦 Package built successfully!")
    print("\nNext steps:")
    print("1. Test on TestPyPI: python3 build_and_publish.py --test")
    print("2. Publish to PyPI: python3 build_and_publish.py --publish")
    print("3. Test installation: python3 build_and_publish.py --install-test")
    
    # Handle command line arguments
    if len(sys.argv) > 1:
        if sys.argv[1] == "--test":
            if upload_to_testpypi():
                print("\n✅ Package uploaded to TestPyPI successfully!")
                print("🔗 TestPyPI URL: https://test.pypi.org/project/prarabdha/")
            else:
                print("❌ TestPyPI upload failed.")
                sys.exit(1)
        
        elif sys.argv[1] == "--publish":
            if upload_to_pypi():
                print("\n✅ Package uploaded to PyPI successfully!")
                print("🔗 PyPI URL: https://pypi.org/project/prarabdha/")
            else:
                print("❌ PyPI upload failed.")
                sys.exit(1)
        
        elif sys.argv[1] == "--install-test":
            if install_test():
                print("\n✅ Installation test successful!")
                print("🎉 Users can now install with: pip install prarabdha")
            else:
                print("❌ Installation test failed.")
                sys.exit(1)
        
        else:
            print(f"❌ Unknown argument: {sys.argv[1]}")
            print("Usage: python3 build_and_publish.py [--test|--publish|--install-test]")

if __name__ == "__main__":
    main() 