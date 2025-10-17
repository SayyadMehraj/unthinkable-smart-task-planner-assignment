"""
Tasks API router
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime

from app.database import get_db
from app.models import Task, TaskResponse, TaskCreate
from app.services.local_ai_service import LocalAIService

router = APIRouter()
llm_service = LocalAIService()

@router.get("/", response_model=List[TaskResponse])
async def get_tasks(
    skip: int = 0, 
    limit: int = 100, 
    status: Optional[str] = None,
    priority: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Get tasks with optional filtering"""
    try:
        query = db.query(Task)
        
        if status:
            query = query.filter(Task.status == status)
        if priority:
            query = query.filter(Task.priority == priority)
        
        tasks = query.offset(skip).limit(limit).all()
        return tasks
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching tasks: {str(e)}")

@router.get("/{task_id}", response_model=TaskResponse)
async def get_task(task_id: int, db: Session = Depends(get_db)):
    """Get a specific task"""
    try:
        task = db.query(Task).filter(Task.id == task_id).first()
        if not task:
            raise HTTPException(status_code=404, detail="Task not found")
        return task
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching task: {str(e)}")

@router.put("/{task_id}/status")
async def update_task_status(task_id: int, status: str, db: Session = Depends(get_db)):
    """Update task status"""
    try:
        valid_statuses = ["pending", "in_progress", "completed", "cancelled"]
        if status not in valid_statuses:
            raise HTTPException(status_code=400, detail=f"Invalid status. Must be one of: {valid_statuses}")
        
        task = db.query(Task).filter(Task.id == task_id).first()
        if not task:
            raise HTTPException(status_code=404, detail="Task not found")
        
        task.status = status
        if status == "completed":
            task.updated_at = datetime.now()
        
        db.commit()
        return {"message": f"Task status updated to {status}"}
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error updating task status: {str(e)}")

@router.put("/{task_id}/priority")
async def update_task_priority(task_id: int, priority: str, db: Session = Depends(get_db)):
    """Update task priority"""
    try:
        valid_priorities = ["low", "medium", "high", "urgent"]
        if priority not in valid_priorities:
            raise HTTPException(status_code=400, detail=f"Invalid priority. Must be one of: {valid_priorities}")
        
        task = db.query(Task).filter(Task.id == task_id).first()
        if not task:
            raise HTTPException(status_code=404, detail="Task not found")
        
        task.priority = priority
        db.commit()
        return {"message": f"Task priority updated to {priority}"}
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error updating task priority: {str(e)}")

@router.put("/{task_id}", response_model=TaskResponse)
async def update_task(task_id: int, task_update: TaskCreate, db: Session = Depends(get_db)):
    """Update a task"""
    try:
        task = db.query(Task).filter(Task.id == task_id).first()
        if not task:
            raise HTTPException(status_code=404, detail="Task not found")
        
        task.title = task_update.title
        task.description = task_update.description
        task.priority = task_update.priority
        task.estimated_duration_hours = task_update.estimated_duration_hours
        task.due_date = task_update.due_date
        task.dependencies = task_update.dependencies or []
        
        db.commit()
        db.refresh(task)
        return task
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error updating task: {str(e)}")

@router.delete("/{task_id}")
async def delete_task(task_id: int, db: Session = Depends(get_db)):
    """Delete a task"""
    try:
        task = db.query(Task).filter(Task.id == task_id).first()
        if not task:
            raise HTTPException(status_code=404, detail="Task not found")
        
        db.delete(task)
        db.commit()
        return {"message": "Task deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error deleting task: {str(e)}")

@router.get("/{task_id}/suggestions")
async def get_task_suggestions(task_id: int, db: Session = Depends(get_db)):
    """Get AI-powered suggestions for improving a task"""
    try:
        task = db.query(Task).filter(Task.id == task_id).first()
        if not task:
            raise HTTPException(status_code=404, detail="Task not found")
        
        context = f"Priority: {task.priority}, Estimated duration: {task.estimated_duration_hours} hours"
        suggestions = await llm_service.generate_task_suggestions(task.title, context)
        
        return {"suggestions": suggestions}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating suggestions: {str(e)}")

@router.get("/{task_id}/analysis")
async def analyze_task(task_id: int, db: Session = Depends(get_db)):
    """Get AI analysis of task complexity and requirements"""
    try:
        task = db.query(Task).filter(Task.id == task_id).first()
        if not task:
            raise HTTPException(status_code=404, detail="Task not found")
        
        analysis = await llm_service.analyze_task_complexity(task.title)
        return analysis
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error analyzing task: {str(e)}")

@router.get("/plan/{plan_id}", response_model=List[TaskResponse])
async def get_tasks_by_plan(plan_id: int, db: Session = Depends(get_db)):
    """Get all tasks for a specific plan"""
    try:
        tasks = db.query(Task).filter(Task.plan_id == plan_id).all()
        return tasks
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching tasks: {str(e)}")
