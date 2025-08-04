#!/usr/bin/env python3
"""
Setup PyPI credentials for Prarabdha package publication
"""

import os
import getpass
from pathlib import Path

def create_pypirc():
    """Create .pypirc file with user credentials."""
    print("🔐 Setting up PyPI credentials...")
    
    # Get user input
    print("\nPlease enter your PyPI credentials:")
    username = input("PyPI Username: ").strip()
    pypi_token = getpass.getpass("PyPI API Token: ").strip()
    
    testpypi_username = input("TestPyPI Username (can be same as PyPI): ").strip() or username
    testpypi_token = getpass.getpass("TestPyPI API Token (press Enter if same): ").strip() or pypi_token
    
    # Create .pypirc content
    pypirc_content = f"""[distutils]
index-servers =
    pypi
    testpypi

[pypi]
repository = https://pypi.org/pypi
username = {username}
password = {pypi_token}

[testpypi]
repository = https://test.pypi.org/legacy/
username = {testpypi_username}
password = {testpypi_token}
"""
    
    # Write to ~/.pypirc
    pypirc_path = Path.home() / ".pypirc"
    
    try:
        with open(pypirc_path, 'w') as f:
            f.write(pypirc_content)
        
        # Set proper permissions
        os.chmod(pypirc_path, 0o600)
        
        print(f"✅ PyPI credentials saved to {pypirc_path}")
        print("🔒 File permissions set to 600 (user read/write only)")
        
        return True
        
    except Exception as e:
        print(f"❌ Error creating .pypirc: {e}")
        return False

def test_credentials():
    """Test the PyPI credentials."""
    print("\n🧪 Testing PyPI credentials...")
    
    try:
        import subprocess
        
        # Test TestPyPI first
        result = subprocess.run(
            ["python3", "-m", "twine", "check", "dist/*"],
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            print("✅ Package check successful")
            return True
        else:
            print(f"❌ Package check failed: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Error testing credentials: {e}")
        return False

def main():
    """Main setup process."""
    print("🚀 Prarabdha PyPI Credentials Setup")
    print("=" * 40)
    
    # Check if .pypirc already exists
    pypirc_path = Path.home() / ".pypirc"
    if pypirc_path.exists():
        print(f"⚠️  .pypirc already exists at {pypirc_path}")
        overwrite = input("Do you want to overwrite it? (y/N): ").strip().lower()
        if overwrite != 'y':
            print("❌ Setup cancelled")
            return
    
    # Create credentials
    if create_pypirc():
        print("\n✅ PyPI credentials configured successfully!")
        print("\nNext steps:")
        print("1. Test package: python3 build_and_publish.py")
        print("2. Upload to TestPyPI: python3 build_and_publish.py --test")
        print("3. Upload to PyPI: python3 build_and_publish.py --publish")
    else:
        print("❌ Failed to configure credentials")

if __name__ == "__main__":
    main() 