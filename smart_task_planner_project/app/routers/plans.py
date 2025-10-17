"""
Plans API router - handles task breakdown generation
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime, timedelta

from app.database import get_db
from app.models import (
    Plan, Task, Goal, PlanCreate, PlanResponse, 
    TaskBreakdownRequest, TaskBreakdownResponse, TaskCreate
)
from app.services.local_ai_service import LocalAIService

router = APIRouter()
llm_service = LocalAIService()

@router.post("/generate", response_model=TaskBreakdownResponse)
async def generate_task_plan(request: TaskBreakdownRequest, db: Session = Depends(get_db)):
    """
    Generate a task breakdown plan for a goal using LLM reasoning
    """
    try:
        # Create the goal first
        goal = Goal(
            title=f"Goal: {request.goal[:50]}...",
            description=request.additional_context,
            user_input=request.goal
        )
        db.add(goal)
        db.commit()
        db.refresh(goal)
        
        # Generate task breakdown using LLM
        llm_response = await llm_service.generate_task_breakdown(
            goal=request.goal,
            timeline_weeks=request.timeline_weeks,
            additional_context=request.additional_context
        )
        
        # Create the plan
        plan = Plan(
            goal_id=goal.id,
            title=f"Plan for: {request.goal[:50]}...",
            description=f"AI-generated plan with {len(llm_response['tasks'])} tasks",
            estimated_duration_days=llm_response.get('estimated_duration_days', 30)
        )
        db.add(plan)
        db.commit()
        db.refresh(plan)
        
        # Create tasks
        created_tasks = []
        start_date = datetime.now()
        
        for i, task_data in enumerate(llm_response['tasks']):
            # Calculate due date based on offset
            due_date_offset = task_data.get('due_date_offset_days', i * 2)
            due_date = start_date + timedelta(days=due_date_offset)
            
            task = Task(
                plan_id=plan.id,
                title=task_data['title'],
                description=task_data.get('description', ''),
                priority=task_data.get('priority', 'medium'),
                estimated_duration_hours=task_data.get('estimated_duration_hours', 8),
                due_date=due_date,
                dependencies=task_data.get('dependencies', [])
            )
            db.add(task)
            created_tasks.append(task)
        
        db.commit()
        
        # Refresh all tasks to get their IDs
        for task in created_tasks:
            db.refresh(task)
        
        return TaskBreakdownResponse(
            goal_id=goal.id,
            plan_id=plan.id,
            tasks=created_tasks,
            estimated_duration_days=plan.estimated_duration_days,
            reasoning=llm_response.get('reasoning', 'No reasoning provided')
        )
        
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error generating task plan: {str(e)}")

@router.get("/", response_model=List[PlanResponse])
async def get_plans(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get all plans"""
    try:
        plans = db.query(Plan).offset(skip).limit(limit).all()
        return plans
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching plans: {str(e)}")

@router.get("/{plan_id}", response_model=PlanResponse)
async def get_plan(plan_id: int, db: Session = Depends(get_db)):
    """Get a specific plan with its tasks"""
    try:
        plan = db.query(Plan).filter(Plan.id == plan_id).first()
        if not plan:
            raise HTTPException(status_code=404, detail="Plan not found")
        return plan
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching plan: {str(e)}")

@router.get("/goal/{goal_id}", response_model=List[PlanResponse])
async def get_plans_by_goal(goal_id: int, db: Session = Depends(get_db)):
    """Get all plans for a specific goal"""
    try:
        plans = db.query(Plan).filter(Plan.goal_id == goal_id).all()
        return plans
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching plans: {str(e)}")

@router.post("/{plan_id}/tasks", response_model=PlanResponse)
async def add_task_to_plan(plan_id: int, task: TaskCreate, db: Session = Depends(get_db)):
    """Add a new task to an existing plan"""
    try:
        plan = db.query(Plan).filter(Plan.id == plan_id).first()
        if not plan:
            raise HTTPException(status_code=404, detail="Plan not found")
        
        new_task = Task(
            plan_id=plan_id,
            title=task.title,
            description=task.description,
            priority=task.priority,
            estimated_duration_hours=task.estimated_duration_hours,
            due_date=task.due_date,
            dependencies=task.dependencies or []
        )
        
        db.add(new_task)
        db.commit()
        db.refresh(plan)
        return plan
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error adding task: {str(e)}")

@router.delete("/{plan_id}")
async def delete_plan(plan_id: int, db: Session = Depends(get_db)):
    """Delete a plan and all its tasks"""
    try:
        plan = db.query(Plan).filter(Plan.id == plan_id).first()
        if not plan:
            raise HTTPException(status_code=404, detail="Plan not found")
        
        db.delete(plan)
        db.commit()
        return {"message": "Plan deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error deleting plan: {str(e)}")
