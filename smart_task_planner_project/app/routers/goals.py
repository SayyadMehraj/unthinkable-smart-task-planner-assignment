"""
Goals API router
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime

from app.database import get_db
from app.models import Goal, GoalCreate, GoalResponse, GoalWithPlansResponse
from app.services.local_ai_service import LocalAIService

router = APIRouter()
llm_service = LocalAIService()

@router.post("/", response_model=GoalResponse)
async def create_goal(goal: GoalCreate, db: Session = Depends(get_db)):
    """Create a new goal"""
    try:
        db_goal = Goal(
            title=goal.title,
            description=goal.description,
            user_input=goal.user_input
        )
        db.add(db_goal)
        db.commit()
        db.refresh(db_goal)
        return db_goal
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error creating goal: {str(e)}")

@router.get("/", response_model=List[GoalResponse])
async def get_goals(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get all goals"""
    try:
        goals = db.query(Goal).offset(skip).limit(limit).all()
        return goals
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching goals: {str(e)}")

@router.get("/{goal_id}", response_model=GoalWithPlansResponse)
async def get_goal(goal_id: int, db: Session = Depends(get_db)):
    """Get a specific goal with its plans"""
    try:
        goal = db.query(Goal).filter(Goal.id == goal_id).first()
        if not goal:
            raise HTTPException(status_code=404, detail="Goal not found")
        return goal
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching goal: {str(e)}")

@router.delete("/{goal_id}")
async def delete_goal(goal_id: int, db: Session = Depends(get_db)):
    """Delete a goal and all its associated plans and tasks"""
    try:
        goal = db.query(Goal).filter(Goal.id == goal_id).first()
        if not goal:
            raise HTTPException(status_code=404, detail="Goal not found")
        
        db.delete(goal)
        db.commit()
        return {"message": "Goal deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error deleting goal: {str(e)}")

@router.put("/{goal_id}", response_model=GoalResponse)
async def update_goal(goal_id: int, goal_update: GoalCreate, db: Session = Depends(get_db)):
    """Update a goal"""
    try:
        goal = db.query(Goal).filter(Goal.id == goal_id).first()
        if not goal:
            raise HTTPException(status_code=404, detail="Goal not found")
        
        goal.title = goal_update.title
        goal.description = goal_update.description
        goal.user_input = goal_update.user_input
        
        db.commit()
        db.refresh(goal)
        return goal
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error updating goal: {str(e)}")
