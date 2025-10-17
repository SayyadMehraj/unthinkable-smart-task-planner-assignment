#!/usr/bin/env python3
"""
Smart Task Planner Demo Script
Demonstrates the key features of the Smart Task Planner
"""

import asyncio
import json
from app.services.local_ai_service import LocalAIService
from app.database import init_db, get_db
from app.models import Goal, Plan, Task
from sqlalchemy.orm import Session

async def demo_llm_service():
    """Demonstrate LLM service functionality"""
    print("🤖 LLM Service Demo")
    print("=" * 40)
    
    llm_service = LocalAIService()
    
    # Test goal
    goal = "Launch a mobile app in 3 weeks"
    timeline_weeks = 3
    context = "Solo developer, first mobile app, using React Native"
    
    print(f"Goal: {goal}")
    print(f"Timeline: {timeline_weeks} weeks")
    print(f"Context: {context}")
    print("\n⏳ Generating task breakdown...")
    
    try:
        result = await llm_service.generate_task_breakdown(
            goal=goal,
            timeline_weeks=timeline_weeks,
            additional_context=context
        )
        
        print(f"\n✅ Task breakdown generated!")
        print(f"Estimated duration: {result['estimated_duration_days']} days")
        print(f"Number of tasks: {len(result['tasks'])}")
        print(f"\nReasoning: {result['reasoning']}")
        
        print(f"\n📋 Generated Tasks:")
        for i, task in enumerate(result['tasks'], 1):
            print(f"\n{i}. {task['title']}")
            print(f"   Description: {task.get('description', 'No description')}")
            print(f"   Priority: {task.get('priority', 'medium')}")
            print(f"   Duration: {task.get('estimated_duration_hours', 'TBD')} hours")
            print(f"   Dependencies: {task.get('dependencies', [])}")
            print(f"   Due in: {task.get('due_date_offset_days', 'TBD')} days")
        
        return result
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

async def demo_task_analysis():
    """Demonstrate task analysis functionality"""
    print("\n\n🔍 Task Analysis Demo")
    print("=" * 40)
    
    llm_service = LocalAIService()
    
    test_tasks = [
        "Set up development environment",
        "Design user interface mockups",
        "Implement user authentication",
        "Deploy to app stores"
    ]
    
    for task in test_tasks:
        print(f"\nAnalyzing: {task}")
        try:
            analysis = await llm_service.analyze_task_complexity(task)
            print(f"  Complexity: {analysis.get('complexity', 'unknown')}")
            print(f"  Estimated hours: {analysis.get('estimated_hours', 'TBD')}")
            print(f"  Required skills: {', '.join(analysis.get('required_skills', []))}")
            print(f"  Challenges: {', '.join(analysis.get('potential_challenges', []))}")
        except Exception as e:
            print(f"  ❌ Analysis error: {e}")

async def demo_task_suggestions():
    """Demonstrate task suggestions functionality"""
    print("\n\n💡 Task Suggestions Demo")
    print("=" * 40)
    
    llm_service = LocalAIService()
    
    test_cases = [
        ("Write API documentation", "For a REST API with 20 endpoints"),
        ("Set up CI/CD pipeline", "For a Python web application"),
        ("Conduct user testing", "For a mobile app with 5 core features")
    ]
    
    for task, context in test_cases:
        print(f"\nTask: {task}")
        print(f"Context: {context}")
        try:
            suggestions = await llm_service.generate_task_suggestions(task, context)
            print("Suggestions:")
            for i, suggestion in enumerate(suggestions, 1):
                print(f"  {i}. {suggestion}")
        except Exception as e:
            print(f"  ❌ Suggestions error: {e}")

async def demo_database_operations():
    """Demonstrate database operations"""
    print("\n\n🗄️ Database Operations Demo")
    print("=" * 40)
    
    try:
        # Initialize database
        await init_db()
        print("✅ Database initialized")
        
        # Get database session
        db_gen = get_db()
        db = next(db_gen)
        
        # Create a goal
        goal = Goal(
            title="Demo Goal",
            description="A demonstration goal",
            user_input="Launch a demo application"
        )
        db.add(goal)
        db.commit()
        db.refresh(goal)
        print(f"✅ Goal created with ID: {goal.id}")
        
        # Create a plan
        plan = Plan(
            goal_id=goal.id,
            title="Demo Plan",
            description="A demonstration plan",
            estimated_duration_days=7
        )
        db.add(plan)
        db.commit()
        db.refresh(plan)
        print(f"✅ Plan created with ID: {plan.id}")
        
        # Create tasks
        tasks_data = [
            {"title": "Setup project", "priority": "high", "estimated_duration_hours": 4},
            {"title": "Implement features", "priority": "medium", "estimated_duration_hours": 16},
            {"title": "Test application", "priority": "medium", "estimated_duration_hours": 8},
            {"title": "Deploy application", "priority": "high", "estimated_duration_hours": 4}
        ]
        
        for task_data in tasks_data:
            task = Task(
                plan_id=plan.id,
                title=task_data["title"],
                priority=task_data["priority"],
                estimated_duration_hours=task_data["estimated_duration_hours"]
            )
            db.add(task)
        
        db.commit()
        print(f"✅ {len(tasks_data)} tasks created")
        
        # Query data
        goals_count = db.query(Goal).count()
        plans_count = db.query(Plan).count()
        tasks_count = db.query(Task).count()
        
        print(f"\n📊 Database Statistics:")
        print(f"  Goals: {goals_count}")
        print(f"  Plans: {plans_count}")
        print(f"  Tasks: {tasks_count}")
        
        db.close()
        
    except Exception as e:
        print(f"❌ Database error: {e}")

async def main():
    """Run all demos"""
    print("🚀 Smart Task Planner Demo")
    print("=" * 50)
    
    # Check for OpenAI API key
    import os
    if not os.getenv("OPENAI_API_KEY"):
        print("⚠️  Warning: OPENAI_API_KEY not found.")
        print("   LLM demos will not work without an API key.")
        print("   Set your OpenAI API key in the .env file.")
        print()
    
    # Run demos
    await demo_llm_service()
    await demo_task_analysis()
    await demo_task_suggestions()
    await demo_database_operations()
    
    print("\n" + "=" * 50)
    print("🎉 Demo completed!")
    print("\n💡 Next steps:")
    print("   1. Set up your OpenAI API key in .env file")
    print("   2. Run: python run.py")
    print("   3. Visit: http://localhost:8000")
    print("   4. Test the API: python test_api.py")

if __name__ == "__main__":
    asyncio.run(main())
