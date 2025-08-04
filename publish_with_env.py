#!/usr/bin/env python3
"""
Publish to PyPI using environment variables for credentials
"""

import os
import subprocess
import sys
from pathlib import Path

def load_env_file():
    """Load environment variables from .env file."""
    env_file = Path(".env")
    if env_file.exists():
        with open(env_file, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    os.environ[key] = value
        print("✅ Loaded credentials from .env file")
    else:
        print("⚠️  No .env file found, using system environment variables")

def build_package():
    """Build the package."""
    print("🔄 Building package...")
    try:
        subprocess.run(["python3", "-m", "build"], check=True, capture_output=True)
        print("✅ Package built successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Build failed: {e.stderr.decode()}")
        return False

def check_package():
    """Check the package for issues."""
    print("🔄 Checking package...")
    try:
        subprocess.run(["python3", "-m", "twine", "check", "dist/*"], check=True, capture_output=True)
        print("✅ Package check passed")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Package check failed: {e.stderr.decode()}")
        return False

def upload_to_pypi():
    """Upload to PyPI using environment variables."""
    print("🔄 Uploading to PyPI...")
    
    username = os.getenv('PYPI_USERNAME', '__token__')
    password = os.getenv('PYPI_PASSWORD')
    
    if not password:
        print("❌ PYPI_PASSWORD not found in environment variables")
        return False
    
    try:
        cmd = [
            "python3", "-m", "twine", "upload", "dist/*",
            "--username", username,
            "--password", password,
            "--repository-url", "https://upload.pypi.org/legacy/"
        ]
        
        result = subprocess.run(cmd, check=True)
        print("✅ Upload to PyPI successful!")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Upload failed: {e.stderr}")
        print(f"Return code: {e.returncode}")
        return False

def upload_to_testpypi():
    """Upload to TestPyPI using environment variables."""
    print("🔄 Uploading to TestPyPI...")
    
    username = os.getenv('TESTPYPI_USERNAME', '__token__')
    password = os.getenv('TESTPYPI_PASSWORD') or os.getenv('PYPI_PASSWORD')
    
    if not password:
        print("❌ TESTPYPI_PASSWORD not found in environment variables")
        return False
    
    try:
        cmd = [
            "python3", "-m", "twine", "upload", "--repository", "testpypi", "dist/*",
            "--username", username,
            "--password", password,
            "--repository-url", "https://test.pypi.org/legacy/"
        ]
        
        result = subprocess.run(cmd, check=True)
        print("✅ Upload to TestPyPI successful!")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Upload failed: {e.stderr}")
        print(f"Return code: {e.returncode}")
        return False

def create_env_template():
    """Create a template .env file."""
    env_template = """# PyPI Credentials
# Replace with your actual tokens
PYPI_USERNAME=__token__
PYPI_PASSWORD=your-pypi-token-here

# TestPyPI Credentials (if different)
TESTPYPI_USERNAME=__token__
TESTPYPI_PASSWORD=your-testpypi-token-here
"""
    
    with open(".env.template", "w") as f:
        f.write(env_template)
    
    print("✅ Created .env.template file")
    print("📝 Copy .env.template to .env and add your tokens")

def main():
    """Main publish process."""
    print("🚀 Prarabdha PyPI Publisher (Environment Variables)")
    print("=" * 50)
    
    # Load environment variables
    load_env_file()
    
    # Check if we have credentials
    if not os.getenv('PYPI_PASSWORD'):
        print("❌ No PyPI credentials found!")
        print("\nTo set up credentials:")
        print("1. Copy .env.template to .env")
        print("2. Add your PyPI tokens to .env")
        print("3. Run this script again")
        
        create_env_template()
        return
    
    # Build package
    if not build_package():
        return
    
    # Check package
    if not check_package():
        return
    
    # Handle command line arguments
    if len(sys.argv) > 1:
        if sys.argv[1] == "--test":
            if upload_to_testpypi():
                print("\n🎉 Package uploaded to TestPyPI!")
                print("🔗 https://test.pypi.org/project/prarabdha/")
            else:
                print("❌ TestPyPI upload failed")
        
        elif sys.argv[1] == "--publish":
            if upload_to_pypi():
                print("\n🎉 Package uploaded to PyPI!")
                print("🔗 https://pypi.org/project/prarabdha/")
                print("📦 Users can now install with: pip install prarabdha")
            else:
                print("❌ PyPI upload failed")
        
        else:
            print(f"❌ Unknown argument: {sys.argv[1]}")
            print("Usage: python3 publish_with_env.py [--test|--publish]")
    else:
        print("\n📦 Package ready for upload!")
        print("Commands:")
        print("  python3 publish_with_env.py --test    # Upload to TestPyPI")
        print("  python3 publish_with_env.py --publish # Upload to PyPI")

if __name__ == "__main__":
    main() 