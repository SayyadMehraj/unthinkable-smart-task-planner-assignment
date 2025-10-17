"""
Database models for Smart Task Planner
"""

from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, ForeignKey, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel

Base = declarative_base()

# Database Models
class Goal(Base):
    __tablename__ = "goals"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text)
    user_input = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    plans = relationship("Plan", back_populates="goal", cascade="all, delete-orphan")

class Plan(Base):
    __tablename__ = "plans"
    
    id = Column(Integer, primary_key=True, index=True)
    goal_id = Column(Integer, ForeignKey("goals.id"), nullable=False)
    title = Column(String(255), nullable=False)
    description = Column(Text)
    estimated_duration_days = Column(Integer)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    goal = relationship("Goal", back_populates="plans")
    tasks = relationship("Task", back_populates="plan", cascade="all, delete-orphan")

class Task(Base):
    __tablename__ = "tasks"
    
    id = Column(Integer, primary_key=True, index=True)
    plan_id = Column(Integer, ForeignKey("plans.id"), nullable=False)
    title = Column(String(255), nullable=False)
    description = Column(Text)
    priority = Column(String(20), default="medium")  # low, medium, high, urgent
    status = Column(String(20), default="pending")  # pending, in_progress, completed, cancelled
    estimated_duration_hours = Column(Integer)
    due_date = Column(DateTime(timezone=True))
    dependencies = Column(JSON)  # List of task IDs this task depends on
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    plan = relationship("Plan", back_populates="tasks")

# Pydantic Models for API
class GoalCreate(BaseModel):
    title: str
    description: Optional[str] = None
    user_input: str

class GoalResponse(BaseModel):
    id: int
    title: str
    description: Optional[str]
    user_input: str
    created_at: datetime
    
    class Config:
        from_attributes = True

class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None
    priority: str = "medium"
    estimated_duration_hours: Optional[int] = None
    due_date: Optional[datetime] = None
    dependencies: Optional[List[int]] = None

class TaskResponse(BaseModel):
    id: int
    title: str
    description: Optional[str]
    priority: str
    status: str
    estimated_duration_hours: Optional[int]
    due_date: Optional[datetime]
    dependencies: Optional[List[int]]
    created_at: datetime
    
    class Config:
        from_attributes = True

class PlanCreate(BaseModel):
    title: str
    description: Optional[str] = None
    estimated_duration_days: Optional[int] = None

class PlanResponse(BaseModel):
    id: int
    goal_id: int
    title: str
    description: Optional[str]
    estimated_duration_days: Optional[int]
    created_at: datetime
    tasks: List[TaskResponse] = []
    
    class Config:
        from_attributes = True

class GoalWithPlansResponse(BaseModel):
    id: int
    title: str
    description: Optional[str]
    user_input: str
    created_at: datetime
    plans: List[PlanResponse] = []
    
    class Config:
        from_attributes = True

class TaskBreakdownRequest(BaseModel):
    goal: str
    timeline_weeks: Optional[int] = None
    additional_context: Optional[str] = None

class TaskBreakdownResponse(BaseModel):
    goal_id: int
    plan_id: int
    tasks: List[TaskResponse]
    estimated_duration_days: int
    reasoning: str
