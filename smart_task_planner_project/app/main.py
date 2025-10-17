"""
Smart Task Planner - Main FastAPI Application
"""

from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from contextlib import asynccontextmanager
import uvicorn
import os
from dotenv import load_dotenv

from app.database import init_db
from app.routers import goals, tasks, plans
from app.models import database

load_dotenv()

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager"""
    await init_db()
    yield
    await database.disconnect()

app = FastAPI(
    title="Smart Task Planner",
    description="Break user goals into actionable tasks with timelines using AI reasoning",
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(goals.router, prefix="/api/goals", tags=["goals"])
app.include_router(tasks.router, prefix="/api/tasks", tags=["tasks"])
app.include_router(plans.router, prefix="/api/plans", tags=["plans"])

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
async def read_root():
    try:
        with open("static/index.html", "r") as f:
            return HTMLResponse(content=f.read())
    except FileNotFoundError:
        return HTMLResponse(content="""
        <html>
            <head><title>Smart Task Planner</title></head>
            <body>
                <h1>Smart Task Planner API</h1>
                <p>API is running! Visit <a href="/docs">/docs</a> for API documentation.</p>
            </body>
        </html>
        """)

@app.get("/health")
async def health_check():
    return {"status": "healthy", "message": "Smart Task Planner API is running"}

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
