#!/usr/bin/env python3
"""
============================================
EchoMind AI - Quick Start Script
Sprint 1: Run the development server
============================================

This script helps you quickly start the EchoMind AI backend server.
It checks for dependencies and provides helpful error messages.
"""

import sys
import subprocess
import os
from pathlib import Path

def check_python_version():
    """Check if Python version is 3.11+"""
    if sys.version_info < (3, 11):
        print("❌ Error: Python 3.11+ is required")
        print(f"   Current version: {sys.version}")
        print("   Please upgrade Python and try again")
        return False
    print(f"✅ Python version: {sys.version_info.major}.{sys.version_info.minor}")
    return True

def check_virtual_env():
    """Check if running in virtual environment"""
    in_venv = hasattr(sys, 'real_prefix') or (
        hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix
    )
    if not in_venv:
        print("⚠️  Warning: Not running in a virtual environment")
        print("   Recommendation: Create and activate a virtual environment")
        print("   Windows: python -m venv venv && venv\\Scripts\\activate")
        print("   Mac/Linux: python -m venv venv && source venv/bin/activate")
        response = input("\n   Continue anyway? (y/N): ")
        if response.lower() != 'y':
            return False
    else:
        print("✅ Virtual environment: Active")
    return True

def check_dependencies():
    """Check if required packages are installed"""
    try:
        import fastapi
        import uvicorn
        import pydantic
        import sqlalchemy
        print("✅ Core dependencies: Installed")
        return True
    except ImportError as e:
        print(f"❌ Missing dependencies: {e.name}")
        print("   Run: pip install -r requirements.txt")
        return False

def check_env_file():
    """Check if .env file exists"""
    env_path = Path(__file__).parent / ".env"
    if not env_path.exists():
        print("⚠️  Warning: .env file not found")
        print("   Creating from .env.example...")
        
        example_path = Path(__file__).parent / ".env.example"
        if example_path.exists():
            import shutil
            shutil.copy(example_path, env_path)
            print("✅ .env file created")
            print("   ⚠️  IMPORTANT: Edit .env and set your SECRET_KEY and other values")
            print("   Generate secrets with:")
            print("   python -c \"import secrets; print(secrets.token_urlsafe(32))\"")
            return False
        else:
            print("❌ .env.example not found")
            return False
    else:
        print("✅ .env file: Found")
        return True

def check_spacy_model():
    """Check if spaCy model is downloaded"""
    try:
        import spacy
        try:
            spacy.load("en_core_web_sm")
            print("✅ spaCy model: Installed")
            return True
        except OSError:
            print("⚠️  spaCy model not found")
            print("   Downloading en_core_web_sm...")
            subprocess.run([sys.executable, "-m", "spacy", "download", "en_core_web_sm"])
            print("✅ spaCy model: Installed")
            return True
    except ImportError:
        print("⚠️  spaCy not installed (will be installed with requirements.txt)")
        return True

def run_server():
    """Run the FastAPI server"""
    print("\n" + "=" * 60)
    print("🚀 Starting EchoMind AI Backend Server")
    print("=" * 60)
    print("\nServer will be available at:")
    print("   - API: http://localhost:8000")
    print("   - Docs: http://localhost:8000/api/docs")
    print("   - Health: http://localhost:8000/health")
    print("\nPress Ctrl+C to stop the server")
    print("=" * 60 + "\n")
    
    try:
        # Run uvicorn
        subprocess.run([
            sys.executable, "-m", "uvicorn",
            "main:app",
            "--reload",
            "--host", "0.0.0.0",
            "--port", "8000",
            "--log-level", "info"
        ])
    except KeyboardInterrupt:
        print("\n\n🛑 Server stopped")
    except Exception as e:
        print(f"\n❌ Error starting server: {e}")
        return False
    
    return True

def main():
    """Main entry point"""
    print("=" * 60)
    print("🌱 EchoMind AI - Quick Start")
    print("=" * 60)
    print("\nChecking prerequisites...\n")
    
    # Run all checks
    checks = [
        ("Python version", check_python_version),
        ("Virtual environment", check_virtual_env),
        ("Dependencies", check_dependencies),
        ("Environment file", check_env_file),
        ("spaCy model", check_spacy_model),
    ]
    
    all_passed = True
    for name, check_func in checks:
        if not check_func():
            all_passed = False
    
    if not all_passed:
        print("\n❌ Some checks failed. Please fix the issues above and try again.")
        return 1
    
    print("\n✅ All checks passed!")
    
    # Ask to start server
    print("\n" + "=" * 60)
    response = input("Start the development server? (Y/n): ")
    if response.lower() != 'n':
        run_server()
    else:
        print("👋 Goodbye!")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
