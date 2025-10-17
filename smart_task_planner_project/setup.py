#!/usr/bin/env python3
"""
Smart Task Planner Setup Script
"""

import os
import sys
import subprocess
import shutil

def check_python_version():
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        return False
    print(f"✅ Python version: {sys.version.split()[0]}")
    return True

def install_dependencies():
    print("\n📦 Installing dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        return False

def setup_environment():
    """Set up environment file"""
    print("\n🔧 Setting up environment...")
    
    env_file = ".env"
    env_example = "env_example.txt"
    
    if os.path.exists(env_file):
        print("✅ .env file already exists")
        return True
    
    if os.path.exists(env_example):
        shutil.copy(env_example, env_file)
        print("✅ Created .env file from template")
        print("⚠️  Please edit .env file and add your OpenAI API key")
        return True
    else:
        print("❌ env_example.txt not found")
        return False

def create_directories():
    """Create necessary directories"""
    print("\n📁 Creating directories...")
    
    directories = [
        "static",
        "app/services",
        "app/routers"
    ]
    
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f"✅ Created directory: {directory}")
        else:
            print(f"✅ Directory exists: {directory}")

def check_openai_key():
    """Check if OpenAI API key is configured (optional)"""
    print("\n🔑 Checking OpenAI API key (optional)...")
    
    # Load environment variables
    try:
        from dotenv import load_dotenv
        load_dotenv()
        
        api_key = os.getenv("OPENAI_API_KEY")
        if api_key and api_key != "your_openai_api_key_here":
            print("✅ OpenAI API key is configured - enhanced AI features available")
            return True
        else:
            print("ℹ️  No OpenAI API key configured - using local AI service")
            print("   The system works perfectly without an API key!")
            print("   Optional: Add OpenAI API key for enhanced AI features")
            return True  # This is not an error anymore
    except ImportError:
        print("ℹ️  python-dotenv not installed, using local AI service")
        return True

def run_tests():
    """Run basic tests"""
    print("\n🧪 Running basic tests...")
    
    try:
        # Test imports
        from app.main import app
        from app.models import Goal, Plan, Task
        from app.services.local_ai_service import LocalAIService
        print("✅ All imports successful")
        
        # Test database models
        print("✅ Database models loaded")
        
        return True
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

def main():
    """Main setup function"""
    print("🚀 Smart Task Planner Setup")
    print("=" * 40)
    
    success = True
    
    # Check Python version
    if not check_python_version():
        success = False
    
    # Create directories
    create_directories()
    
    # Install dependencies
    if not install_dependencies():
        success = False
    
    # Setup environment
    if not setup_environment():
        success = False
    
    # Check OpenAI key
    check_openai_key()
    
    # Run tests
    if not run_tests():
        success = False
    
    print("\n" + "=" * 40)
    if success:
        print("🎉 Setup completed successfully!")
        print("\n📋 Next steps:")
        print("   1. Edit .env file and add your OpenAI API key")
        print("   2. Run: python run.py")
        print("   3. Visit: http://localhost:8000")
        print("   4. Test: python test_api.py")
        print("   5. Demo: python demo.py")
    else:
        print("❌ Setup completed with errors")
        print("   Please check the error messages above and fix them")
    
    print("\n📚 Documentation:")
    print("   - README.md: Complete project documentation")
    print("   - API Docs: http://localhost:8000/docs (after starting server)")

if __name__ == "__main__":
    main()
