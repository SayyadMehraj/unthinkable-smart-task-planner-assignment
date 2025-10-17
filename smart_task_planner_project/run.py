#!/usr/bin/env python3
"""
Smart Task Planner - Main entry point
"""

import uvicorn
import os
from dotenv import load_dotenv

load_dotenv()

if __name__ == "__main__":
    if not os.getenv("OPENAI_API_KEY"):
        print("ℹ️  Using local AI service (no API key required)")
        print()
    
    print("🚀 Starting Smart Task Planner...")
    print("📱 Frontend: http://localhost:8000")
    print("📚 API Docs: http://localhost:8000/docs")
    print()
    
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
