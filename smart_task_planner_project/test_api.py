#!/usr/bin/env python3
"""
Test script for Smart Task Planner API
Run this to test the API functionality
"""

import requests
import json
import time

BASE_URL = "http://localhost:8000"

def test_health():
    """Test health endpoint"""
    print("🔍 Testing health endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code == 200:
            print("✅ Health check passed")
            return True
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Health check error: {e}")
        return False

def test_goal_creation():
    """Test goal creation"""
    print("\n🔍 Testing goal creation...")
    try:
        goal_data = {
            "title": "Test Goal",
            "description": "A test goal for API testing",
            "user_input": "Test goal input"
        }
        
        response = requests.post(f"{BASE_URL}/api/goals/", json=goal_data)
        if response.status_code == 200:
            goal = response.json()
            print(f"✅ Goal created with ID: {goal['id']}")
            return goal['id']
        else:
            print(f"❌ Goal creation failed: {response.status_code}")
            print(f"Response: {response.text}")
            return None
    except Exception as e:
        print(f"❌ Goal creation error: {e}")
        return None

def test_task_plan_generation():
    """Test task plan generation"""
    print("\n🔍 Testing task plan generation...")
    try:
        plan_data = {
            "goal": "Launch a simple web application in 1 week",
            "timeline_weeks": 1,
            "additional_context": "Solo developer, basic CRUD application"
        }
        
        print("⏳ Generating task plan (this may take a moment)...")
        response = requests.post(f"{BASE_URL}/api/plans/generate", json=plan_data)
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Task plan generated successfully!")
            print(f"   Goal ID: {result['goal_id']}")
            print(f"   Plan ID: {result['plan_id']}")
            print(f"   Tasks: {len(result['tasks'])}")
            print(f"   Duration: {result['estimated_duration_days']} days")
            print(f"   Reasoning: {result['reasoning'][:100]}...")
            return result
        else:
            print(f"❌ Task plan generation failed: {response.status_code}")
            print(f"Response: {response.text}")
            return None
    except Exception as e:
        print(f"❌ Task plan generation error: {e}")
        return None

def test_task_operations(plan_result):
    """Test task operations"""
    if not plan_result or not plan_result.get('tasks'):
        print("\n❌ No tasks to test")
        return
    
    print("\n🔍 Testing task operations...")
    task_id = plan_result['tasks'][0]['id']
    
    try:
        # Test getting task
        response = requests.get(f"{BASE_URL}/api/tasks/{task_id}")
        if response.status_code == 200:
            print("✅ Task retrieval successful")
        else:
            print(f"❌ Task retrieval failed: {response.status_code}")
        
        # Test updating task status
        response = requests.put(f"{BASE_URL}/api/tasks/{task_id}/status", params={"status": "in_progress"})
        if response.status_code == 200:
            print("✅ Task status update successful")
        else:
            print(f"❌ Task status update failed: {response.status_code}")
        
        # Test getting task suggestions
        response = requests.get(f"{BASE_URL}/api/tasks/{task_id}/suggestions")
        if response.status_code == 200:
            suggestions = response.json()
            print(f"✅ Task suggestions retrieved: {len(suggestions.get('suggestions', []))} suggestions")
        else:
            print(f"❌ Task suggestions failed: {response.status_code}")
        
        # Test task analysis
        response = requests.get(f"{BASE_URL}/api/tasks/{task_id}/analysis")
        if response.status_code == 200:
            analysis = response.json()
            print(f"✅ Task analysis retrieved: complexity = {analysis.get('complexity', 'unknown')}")
        else:
            print(f"❌ Task analysis failed: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Task operations error: {e}")

def test_goals_list():
    """Test goals listing"""
    print("\n🔍 Testing goals listing...")
    try:
        response = requests.get(f"{BASE_URL}/api/goals/")
        if response.status_code == 200:
            goals = response.json()
            print(f"✅ Goals listing successful: {len(goals)} goals found")
        else:
            print(f"❌ Goals listing failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Goals listing error: {e}")

def main():
    """Run all tests"""
    print("🧪 Smart Task Planner API Test Suite")
    print("=" * 50)
    
    # Test health
    if not test_health():
        print("\n❌ Server is not running. Please start the server first:")
        print("   python run.py")
        return
    
    # Test goal creation
    goal_id = test_goal_creation()
    
    # Test task plan generation
    plan_result = test_task_plan_generation()
    
    # Test task operations
    test_task_operations(plan_result)
    
    # Test goals listing
    test_goals_list()
    
    print("\n" + "=" * 50)
    print("🎉 Test suite completed!")
    print("\n💡 Tips:")
    print("   - Visit http://localhost:8000 for the web interface")
    print("   - Visit http://localhost:8000/docs for API documentation")
    print("   - Check the database file: smart_task_planner.db")

if __name__ == "__main__":
    main()
