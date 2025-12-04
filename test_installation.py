#!/usr/bin/env python3
"""
Installation Test Script
Verifies that all dependencies and files are properly installed.
"""

import sys
import os
from pathlib import Path

def check_python_version():
    """Check if Python version is 3.8 or higher"""
    print("🐍 Checking Python version...")
    version = sys.version_info
    if version.major >= 3 and version.minor >= 8:
        print(f"   ✅ Python {version.major}.{version.minor}.{version.micro} detected")
        return True
    else:
        print(f"   ❌ Python {version.major}.{version.minor} detected, need 3.8+")
        return False

def check_dependencies():
    """Check if required Python packages are installed"""
    print("\n📦 Checking dependencies...")
    required = [
        'fastapi',
        'uvicorn',
        'websockets',
        'aiofiles',
    ]
    
    all_good = True
    for package in required:
        try:
            __import__(package)
            print(f"   ✅ {package} installed")
        except ImportError:
            print(f"   ❌ {package} NOT installed")
            all_good = False
    
    return all_good

def check_file_structure():
    """Check if all required files exist"""
    print("\n📁 Checking file structure...")
    
    base_dir = Path(__file__).parent
    required_files = [
        'backend/api.py',
        'backend/haas_machine.py',
        'frontend/index.html',
        'requirements.txt',
        'README.md',
        'LICENSE',
    ]
    
    all_good = True
    for file_path in required_files:
        full_path = base_dir / file_path
        if full_path.exists():
            print(f"   ✅ {file_path}")
        else:
            print(f"   ❌ {file_path} NOT FOUND")
            all_good = False
    
    return all_good

def check_static_directory():
    """Check if static directory is setup"""
    print("\n🌐 Checking static directory...")
    base_dir = Path(__file__).parent
    static_dir = base_dir / 'backend' / 'static'
    index_file = static_dir / 'index.html'
    
    if not static_dir.exists():
        print("   ⚠️  static directory doesn't exist")
        print("   💡 Run: mkdir -p backend/static && cp frontend/index.html backend/static/")
        return False
    
    if not index_file.exists():
        print("   ⚠️  index.html not in static directory")
        print("   💡 Run: cp frontend/index.html backend/static/")
        return False
    
    print("   ✅ Static directory properly configured")
    return True

def test_imports():
    """Test if backend modules can be imported"""
    print("\n🔧 Testing module imports...")
    
    try:
        sys.path.insert(0, str(Path(__file__).parent / 'backend'))
        from haas_machine import HaasMachine, create_default_machines
        print("   ✅ haas_machine module imports successfully")
        
        machines = create_default_machines()
        print(f"   ✅ Created {len(machines)} default machines")
        
        return True
    except Exception as e:
        print(f"   ❌ Import failed: {e}")
        return False

def main():
    print("=" * 60)
    print("CNC Machine Monitor - Installation Test")
    print("=" * 60)
    
    results = {
        'Python Version': check_python_version(),
        'Dependencies': check_dependencies(),
        'File Structure': check_file_structure(),
        'Static Directory': check_static_directory(),
        'Module Imports': test_imports(),
    }
    
    print("\n" + "=" * 60)
    print("RESULTS SUMMARY")
    print("=" * 60)
    
    all_passed = True
    for test, passed in results.items():
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{test:.<40} {status}")
        if not passed:
            all_passed = False
    
    print("=" * 60)
    
    if all_passed:
        print("\n🎉 All tests passed! You're ready to run the server.")
        print("\n📝 Next steps:")
        print("   1. cd backend")
        print("   2. python api.py")
        print("   3. Open http://localhost:5000 in your browser")
        return 0
    else:
        print("\n⚠️  Some tests failed. Please fix the issues above.")
        print("\n💡 Common fixes:")
        print("   - Install dependencies: pip install -r requirements.txt")
        print("   - Setup static dir: mkdir -p backend/static && cp frontend/index.html backend/static/")
        return 1

if __name__ == "__main__":
    sys.exit(main())
