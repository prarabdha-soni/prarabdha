#!/usr/bin/env python3
"""
Fix .pypirc file with correct token format
"""

import os
from pathlib import Path

def fix_pypirc():
    """Fix the .pypirc file with correct token format."""
    print("🔧 Fixing .pypirc file...")
    
    # Get the current token
    pypirc_path = Path.home() / ".pypirc"
    
    if not pypirc_path.exists():
        print("❌ .pypirc file not found")
        return False
    
    # Read current content
    with open(pypirc_path, 'r') as f:
        content = f.read()
    
    # Extract the token (it's the same for both)
    lines = content.split('\n')
    token = None
    for line in lines:
        if line.startswith('password = '):
            token = line.replace('password = ', '').strip()
            break
    
    if not token:
        print("❌ Could not find token in .pypirc")
        return False
    
    # Create corrected content
    corrected_content = f"""[distutils]
index-servers =
    pypi
    testpypi

[pypi]
repository = https://pypi.org/pypi
username = __token__
password = {token}

[testpypi]
repository = https://test.pypi.org/legacy/
username = __token__
password = {token}
"""
    
    # Write corrected content
    try:
        with open(pypirc_path, 'w') as f:
            f.write(corrected_content)
        
        # Set proper permissions
        os.chmod(pypirc_path, 0o600)
        
        print("✅ .pypirc file fixed with correct token format")
        print("🔒 Using __token__ as username for API tokens")
        
        return True
        
    except Exception as e:
        print(f"❌ Error fixing .pypirc: {e}")
        return False

def main():
    """Main fix process."""
    print("🔧 Fixing PyPI Credentials")
    print("=" * 30)
    
    if fix_pypirc():
        print("\n✅ Credentials fixed successfully!")
        print("\nYou can now try uploading again:")
        print("python3 build_and_publish.py --test")
    else:
        print("❌ Failed to fix credentials")

if __name__ == "__main__":
    main() 