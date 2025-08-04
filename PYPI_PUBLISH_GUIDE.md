# PyPI Publication Guide for Prarabdha

This guide will help you publish the Prarabdha cache system to PyPI so users can install it with `pip install prarabdha`.

## 📦 Package Structure

Your package is now ready for PyPI with the following structure:

```
prarabdha_cache_package/
├── README.md                    # ✅ Complete documentation
├── LICENSE                      # ✅ MIT License
├── requirements.txt             # ✅ Dependencies
├── pyproject.toml              # ✅ Modern build configuration
├── setup.py                    # ✅ Legacy build support
├── MANIFEST.in                 # ✅ Package file inclusion
├── build_and_publish.py        # ✅ Automated build script
├── prarabdha/                  # ✅ Complete caching system
├── simple_example.py           # ✅ Usage examples
├── example_usage.py            # ✅ Comprehensive examples
├── advanced_features_demo.py   # ✅ Advanced features demo
├── quick_advanced_test.py      # ✅ Quick test script
└── test_api.py                 # ✅ API test script
```

## 🚀 Quick Start

### 1. Build the Package
```bash
python3 build_and_publish.py
```

### 2. Test on TestPyPI (Recommended First)
```bash
python3 build_and_publish.py --test
```

### 3. Publish to PyPI
```bash
python3 build_and_publish.py --publish
```

### 4. Test Installation
```bash
python3 build_and_publish.py --install-test
```

## 📋 Manual Steps

### Step 1: Create PyPI Account
1. Go to https://pypi.org/account/register/
2. Create an account
3. Enable two-factor authentication (recommended)

### Step 2: Create TestPyPI Account
1. Go to https://test.pypi.org/account/register/
2. Create an account (can use same email as PyPI)

### Step 3: Configure Credentials
Create `~/.pypirc` file:
```ini
[distutils]
index-servers =
    pypi
    testpypi

[pypi]
repository = https://pypi.org/pypi
username = __token__
password = pypi-your-token-here

[testpypi]
repository = https://test.pypi.org/legacy/
username = __token__
password = pypi-your-test-token-here
```

### Step 4: Get API Tokens
1. **PyPI Token**: Go to https://pypi.org/manage/account/token/
2. **TestPyPI Token**: Go to https://test.pypi.org/manage/account/token/

## 🔧 Build Commands

### Clean Build
```bash
rm -rf build/ dist/ *.egg-info/
python3 -m build
```

### Check Package
```bash
python3 -m twine check dist/*
```

### Upload to TestPyPI
```bash
python3 -m twine upload --repository testpypi dist/*
```

### Upload to PyPI
```bash
python3 -m twine upload dist/*
```

## 📊 Package Information

### Metadata
- **Name**: prarabdha
- **Version**: 0.1.0
- **Description**: Modular AI Cache System for chats, audio, and video data ingestion
- **Author**: Prarabdha Soni
- **License**: MIT
- **Python**: >=3.8

### Dependencies
- redis>=4.0
- faiss-cpu
- fastapi
- uvicorn
- numpy
- aiohttp
- pydantic
- typer[all]
- cryptography
- pandas
- pyarrow
- psutil

### Entry Points
- **CLI**: `prarabdha` command
- **Module**: `from prarabdha.chats import ChatCache`

## 🎯 Installation for Users

After publication, users can install with:

```bash
# Install from PyPI
pip install prarabdha

# Install with development dependencies
pip install prarabdha[dev]

# Install from TestPyPI (for testing)
pip install prarabdha --index-url https://test.pypi.org/simple/
```

## 📖 Usage Examples

### Basic Usage
```python
from prarabdha.chats import ChatCache
from prarabdha.audio import audioCache
from prarabdha.video import videoCache
from prarabdha.rag import RAGCache

# Create cache instances
chat_cache = ChatCache()
audio_cache = audioCache()
video_cache = videoCache()
rag_cache = RAGCache()
```

### CLI Usage
```bash
# Show help
prarabdha --help

# View statistics
prarabdha stats

# Search similar segments
prarabdha search "Python programming help"
```

### API Usage
```python
import requests

# Health check
response = requests.get("http://localhost:8000/health")

# Ingest data
response = requests.post("http://localhost:8000/ingest", json={
    "segments": [{"content": "Hello world"}]
})
```

## 🔍 Verification

### Check Package on PyPI
- **PyPI**: https://pypi.org/project/prarabdha/
- **TestPyPI**: https://test.pypi.org/project/prarabdha/

### Test Installation
```bash
# Create virtual environment
python3 -m venv test_env
source test_env/bin/activate

# Install package
pip install prarabdha

# Test import
python3 -c "from prarabdha.chats import ChatCache; print('✅ Installation successful!')"
```

## 🚨 Troubleshooting

### Common Issues

1. **Build Errors**
   - Ensure all dependencies are installed
   - Check Python version compatibility
   - Verify file permissions

2. **Upload Errors**
   - Check API token validity
   - Verify ~/.pypirc configuration
   - Ensure package name is unique

3. **Installation Errors**
   - Check Python version (>=3.8)
   - Verify internet connection
   - Try installing dependencies manually

### Version Management
```bash
# Update version in pyproject.toml
# Update version in setup.py
# Update version in __init__.py files
```

## 📈 Post-Publication

### Monitor Downloads
- Check PyPI statistics
- Monitor GitHub stars/issues
- Track user feedback

### Update Package
1. Update version numbers
2. Rebuild package
3. Upload new version

### Documentation
- Keep README.md updated
- Add more examples
- Create tutorials

## 🎉 Success!

Once published, users worldwide can install your package with:
```bash
pip install prarabdha
```

And use it with:
```python
from prarabdha.chats import ChatCache
chat_cache = ChatCache()
```

Your Prarabdha cache system is now available to the Python community! 🚀 