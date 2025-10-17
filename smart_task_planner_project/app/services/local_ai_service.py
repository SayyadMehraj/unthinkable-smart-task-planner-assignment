"""
Local AI Service - No API key required
Uses rule-based logic and templates to generate task breakdowns
"""

import json
import re
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
import random

class LocalAIService:
    def __init__(self):
        """Initialize the local AI service with templates and patterns"""
        self.task_templates = self._load_task_templates()
        self.priority_keywords = self._load_priority_keywords()
        self.duration_estimates = self._load_duration_estimates()
    
    def _load_task_templates(self) -> Dict[str, List[Dict]]:
        """Load task templates for different types of goals"""
        return {
            "product_launch": [
                {"title": "Market Research and Analysis", "duration": 16, "priority": "high"},
                {"title": "Define Product Requirements", "duration": 12, "priority": "high"},
                {"title": "Create Project Timeline", "duration": 4, "priority": "high"},
                {"title": "Set up Development Environment", "duration": 8, "priority": "high"},
                {"title": "Design User Interface", "duration": 20, "priority": "medium"},
                {"title": "Implement Core Features", "duration": 40, "priority": "high"},
                {"title": "Write Unit Tests", "duration": 16, "priority": "medium"},
                {"title": "Integration Testing", "duration": 12, "priority": "medium"},
                {"title": "User Acceptance Testing", "duration": 8, "priority": "medium"},
                {"title": "Deploy to Production", "duration": 8, "priority": "high"},
                {"title": "Create Documentation", "duration": 12, "priority": "low"},
                {"title": "Marketing and Promotion", "duration": 16, "priority": "medium"}
            ],
            "learning": [
                {"title": "Research Learning Resources", "duration": 4, "priority": "high"},
                {"title": "Set Learning Goals", "duration": 2, "priority": "high"},
                {"title": "Create Study Schedule", "duration": 2, "priority": "high"},
                {"title": "Complete Basic Tutorials", "duration": 16, "priority": "high"},
                {"title": "Practice with Small Projects", "duration": 24, "priority": "medium"},
                {"title": "Join Learning Community", "duration": 4, "priority": "low"},
                {"title": "Build Portfolio Project", "duration": 32, "priority": "medium"},
                {"title": "Seek Feedback and Mentorship", "duration": 8, "priority": "medium"},
                {"title": "Advanced Practice", "duration": 20, "priority": "medium"},
                {"title": "Document Learning Journey", "duration": 4, "priority": "low"}
            ],
            "event_planning": [
                {"title": "Define Event Objectives", "duration": 4, "priority": "high"},
                {"title": "Set Budget and Timeline", "duration": 4, "priority": "high"},
                {"title": "Choose Venue and Date", "duration": 8, "priority": "high"},
                {"title": "Create Guest List", "duration": 4, "priority": "medium"},
                {"title": "Send Invitations", "duration": 4, "priority": "medium"},
                {"title": "Plan Activities and Agenda", "duration": 12, "priority": "medium"},
                {"title": "Arrange Catering", "duration": 6, "priority": "medium"},
                {"title": "Set up Equipment and Decorations", "duration": 8, "priority": "low"},
                {"title": "Coordinate with Vendors", "duration": 6, "priority": "medium"},
                {"title": "Final Preparations", "duration": 4, "priority": "high"},
                {"title": "Execute Event", "duration": 8, "priority": "high"},
                {"title": "Follow-up and Feedback", "duration": 4, "priority": "low"}
            ],
            "business_startup": [
                {"title": "Market Research and Validation", "duration": 20, "priority": "high"},
                {"title": "Create Business Plan", "duration": 16, "priority": "high"},
                {"title": "Register Business Entity", "duration": 4, "priority": "high"},
                {"title": "Set up Financial Systems", "duration": 8, "priority": "high"},
                {"title": "Develop MVP (Minimum Viable Product)", "duration": 60, "priority": "high"},
                {"title": "Build Brand Identity", "duration": 12, "priority": "medium"},
                {"title": "Create Marketing Strategy", "duration": 16, "priority": "medium"},
                {"title": "Launch Website", "duration": 20, "priority": "medium"},
                {"title": "Find First Customers", "duration": 24, "priority": "high"},
                {"title": "Gather Customer Feedback", "duration": 8, "priority": "medium"},
                {"title": "Iterate and Improve", "duration": 20, "priority": "medium"},
                {"title": "Scale Operations", "duration": 32, "priority": "low"}
            ],
            "mobile_app": [
                {"title": "Define App Requirements", "duration": 8, "priority": "high"},
                {"title": "Create Wireframes and Mockups", "duration": 16, "priority": "high"},
                {"title": "Set up Development Environment", "duration": 6, "priority": "high"},
                {"title": "Implement User Authentication", "duration": 12, "priority": "high"},
                {"title": "Develop Core Features", "duration": 40, "priority": "high"},
                {"title": "Integrate APIs and Backend", "duration": 20, "priority": "medium"},
                {"title": "Implement UI/UX Design", "duration": 24, "priority": "medium"},
                {"title": "Testing and Bug Fixes", "duration": 16, "priority": "medium"},
                {"title": "Performance Optimization", "duration": 12, "priority": "medium"},
                {"title": "Prepare for App Store", "duration": 8, "priority": "high"},
                {"title": "Submit for Review", "duration": 2, "priority": "high"},
                {"title": "Launch and Marketing", "duration": 16, "priority": "medium"}
            ]
        }
    
    def _load_priority_keywords(self) -> Dict[str, List[str]]:
        """Load keywords for priority assignment"""
        return {
            "high": ["urgent", "critical", "essential", "immediate", "launch", "deadline", "core", "main", "primary"],
            "medium": ["important", "secondary", "support", "enhancement", "feature", "improvement"],
            "low": ["optional", "nice-to-have", "future", "documentation", "cleanup", "optimization"]
        }
    
    def _load_duration_estimates(self) -> Dict[str, int]:
        """Load duration estimates for different task types"""
        return {
            "research": 8,
            "planning": 4,
            "development": 16,
            "testing": 8,
            "deployment": 6,
            "documentation": 4,
            "marketing": 12,
            "design": 12,
            "setup": 4,
            "default": 8
        }
    
    async def generate_task_breakdown(self, goal: str, timeline_weeks: Optional[int] = None, 
                                    additional_context: Optional[str] = None) -> Dict[str, Any]:
        """
        Generate task breakdown using local AI logic
        """
        try:
            # Analyze the goal to determine the type
            goal_type = self._analyze_goal_type(goal, additional_context)
            
            # Get base templates
            base_tasks = self.task_templates.get(goal_type, self.task_templates["product_launch"])
            
            # Customize tasks based on goal specifics
            customized_tasks = self._customize_tasks(base_tasks, goal, additional_context, timeline_weeks)
            
            # Calculate dependencies
            tasks_with_dependencies = self._add_dependencies(customized_tasks)
            
            # Generate reasoning
            reasoning = self._generate_reasoning(goal, goal_type, len(customized_tasks), timeline_weeks)
            
            # Calculate total duration
            total_hours = sum(task["estimated_duration_hours"] for task in customized_tasks)
            estimated_days = max(1, total_hours // 8)
            
            return {
                "reasoning": reasoning,
                "estimated_duration_days": estimated_days,
                "tasks": tasks_with_dependencies
            }
            
        except Exception as e:
            return {
                "reasoning": f"Generated using local AI logic. Error: {str(e)}",
                "estimated_duration_days": 14,
                "tasks": self._get_fallback_tasks(goal)
            }
    
    def _analyze_goal_type(self, goal: str, context: Optional[str] = None) -> str:
        """Analyze goal to determine the most appropriate template"""
        text = (goal + " " + (context or "")).lower()
        
        # Check for specific keywords
        if any(word in text for word in ["app", "mobile", "ios", "android", "react native"]):
            return "mobile_app"
        elif any(word in text for word in ["learn", "study", "course", "tutorial", "skill"]):
            return "learning"
        elif any(word in text for word in ["event", "party", "conference", "meeting", "gathering"]):
            return "event_planning"
        elif any(word in text for word in ["business", "startup", "company", "entrepreneur"]):
            return "business_startup"
        elif any(word in text for word in ["launch", "product", "release", "deploy"]):
            return "product_launch"
        else:
            return "product_launch"  # Default fallback
    
    def _customize_tasks(self, base_tasks: List[Dict], goal: str, context: Optional[str], 
                        timeline_weeks: Optional[int]) -> List[Dict]:
        """Customize tasks based on specific goal requirements"""
        customized = []
        
        for i, task in enumerate(base_tasks):
            # Customize title based on goal
            title = self._customize_task_title(task["title"], goal, context)
            
            # Adjust duration based on timeline constraints
            duration = task["duration"]
            if timeline_weeks:
                # Scale duration based on timeline
                max_hours = timeline_weeks * 40  # 40 hours per week
                if duration > max_hours / len(base_tasks):
                    duration = max(4, max_hours // len(base_tasks))
            
            # Determine priority
            priority = self._determine_priority(task["title"], goal, context)
            
            customized_task = {
                "title": title,
                "description": self._generate_task_description(title, goal),
                "priority": priority,
                "estimated_duration_hours": duration,
                "dependencies": [],
                "due_date_offset_days": i * 2  # Spread tasks over time
            }
            
            customized.append(customized_task)
        
        return customized
    
    def _customize_task_title(self, base_title: str, goal: str, context: Optional[str]) -> str:
        """Customize task title based on goal specifics"""
        # Extract key terms from goal
        goal_lower = goal.lower()
        
        # Replace generic terms with specific ones
        if "app" in goal_lower or "mobile" in goal_lower:
            base_title = base_title.replace("Product", "App")
        elif "website" in goal_lower or "web" in goal_lower:
            base_title = base_title.replace("Product", "Website")
        elif "business" in goal_lower:
            base_title = base_title.replace("Product", "Business")
        
        return base_title
    
    def _generate_task_description(self, title: str, goal: str) -> str:
        """Generate a description for the task"""
        descriptions = {
            "Market Research": f"Research the target market for {goal.lower()} to understand user needs and competition.",
            "Define Requirements": f"Define clear requirements and specifications for {goal.lower()}.",
            "Set up Environment": f"Set up the development environment and necessary tools for {goal.lower()}.",
            "Design": f"Create designs and mockups for {goal.lower()} focusing on user experience.",
            "Implement": f"Implement the core functionality for {goal.lower()}.",
            "Testing": f"Test {goal.lower()} thoroughly to ensure quality and functionality.",
            "Deploy": f"Deploy {goal.lower()} to production environment.",
            "Documentation": f"Create comprehensive documentation for {goal.lower()}.",
            "Marketing": f"Develop marketing strategy and materials for {goal.lower()}."
        }
        
        # Find matching description
        for key, desc in descriptions.items():
            if key.lower() in title.lower():
                return desc
        
        return f"Complete the {title.lower()} phase for {goal.lower()}."
    
    def _determine_priority(self, title: str, goal: str, context: Optional[str]) -> str:
        """Determine task priority based on keywords and context"""
        text = (title + " " + goal + " " + (context or "")).lower()
        
        for priority, keywords in self.priority_keywords.items():
            if any(keyword in text for keyword in keywords):
                return priority
        
        return "medium"  # Default priority
    
    def _add_dependencies(self, tasks: List[Dict]) -> List[Dict]:
        """Add logical dependencies between tasks"""
        for i, task in enumerate(tasks):
            dependencies = []
            
            # Add dependencies based on task type and position
            if i > 0:
                # Each task depends on the previous one (simple linear dependency)
                dependencies.append(i - 1)
            
            # Special dependency rules
            task_title = task["title"].lower()
            if "testing" in task_title:
                # Testing depends on implementation
                for j, prev_task in enumerate(tasks[:i]):
                    if "implement" in prev_task["title"].lower() or "develop" in prev_task["title"].lower():
                        dependencies.append(j)
            elif "deploy" in task_title:
                # Deployment depends on testing
                for j, prev_task in enumerate(tasks[:i]):
                    if "test" in prev_task["title"].lower():
                        dependencies.append(j)
            
            task["dependencies"] = list(set(dependencies))  # Remove duplicates
        
        return tasks
    
    def _generate_reasoning(self, goal: str, goal_type: str, task_count: int, 
                          timeline_weeks: Optional[int]) -> str:
        """Generate reasoning for the task breakdown"""
        reasoning_parts = [
            f"Analyzed the goal '{goal}' and identified it as a {goal_type.replace('_', ' ')} project.",
            f"Generated {task_count} actionable tasks based on best practices for this type of project.",
        ]
        
        if timeline_weeks:
            reasoning_parts.append(f"Adjusted task durations to fit within the {timeline_weeks}-week timeline.")
        
        reasoning_parts.extend([
            "Tasks are ordered logically with dependencies to ensure smooth progression.",
            "Priority levels are assigned based on importance and dependencies.",
            "Time estimates are realistic and account for potential challenges."
        ])
        
        return " ".join(reasoning_parts)
    
    def _get_fallback_tasks(self, goal: str) -> List[Dict]:
        """Get fallback tasks if main logic fails"""
        return [
            {
                "title": f"Plan and Research {goal}",
                "description": f"Research and plan the approach for {goal}",
                "priority": "high",
                "estimated_duration_hours": 8,
                "dependencies": [],
                "due_date_offset_days": 0
            },
            {
                "title": f"Implement Core Features for {goal}",
                "description": f"Implement the main functionality for {goal}",
                "priority": "high",
                "estimated_duration_hours": 16,
                "dependencies": [0],
                "due_date_offset_days": 2
            },
            {
                "title": f"Test and Validate {goal}",
                "description": f"Test the implementation of {goal}",
                "priority": "medium",
                "estimated_duration_hours": 8,
                "dependencies": [1],
                "due_date_offset_days": 4
            },
            {
                "title": f"Deploy and Launch {goal}",
                "description": f"Deploy and launch {goal}",
                "priority": "high",
                "estimated_duration_hours": 4,
                "dependencies": [2],
                "due_date_offset_days": 6
            }
        ]
    
    async def generate_task_suggestions(self, current_task: str, context: str = "") -> List[str]:
        """Generate suggestions for improving a task"""
        suggestions = [
            "Break down into smaller, more specific subtasks",
            "Add measurable success criteria",
            "Consider potential blockers and mitigation strategies",
            "Set up regular check-ins or milestones",
            "Document lessons learned for future reference"
        ]
        
        # Customize suggestions based on task type
        task_lower = current_task.lower()
        if "research" in task_lower:
            suggestions.extend([
                "Create a research plan with specific questions",
                "Identify key sources and experts to consult"
            ])
        elif "implement" in task_lower or "develop" in task_lower:
            suggestions.extend([
                "Write unit tests alongside implementation",
                "Consider code review and pair programming"
            ])
        elif "test" in task_lower:
            suggestions.extend([
                "Create test cases before testing begins",
                "Document bugs and their resolutions"
            ])
        
        return suggestions[:5]  # Return top 5 suggestions
    
    async def analyze_task_complexity(self, task: str) -> Dict[str, Any]:
        """Analyze task complexity"""
        task_lower = task.lower()
        
        # Determine complexity based on keywords
        if any(word in task_lower for word in ["research", "plan", "setup", "configure"]):
            complexity = "low"
            hours = 4
            skills = ["Research", "Planning", "Basic technical skills"]
        elif any(word in task_lower for word in ["implement", "develop", "build", "create"]):
            complexity = "high"
            hours = 16
            skills = ["Programming", "System design", "Problem solving"]
        elif any(word in task_lower for word in ["test", "validate", "review"]):
            complexity = "medium"
            hours = 8
            skills = ["Testing", "Quality assurance", "Attention to detail"]
        else:
            complexity = "medium"
            hours = 8
            skills = ["General project management", "Communication"]
        
        challenges = [
            "Time estimation accuracy",
            "Resource availability",
            "Technical complexity",
            "External dependencies"
        ]
        
        return {
            "complexity": complexity,
            "estimated_hours": hours,
            "required_skills": skills,
            "potential_challenges": challenges,
            "suggested_approach": f"Break down the {complexity} complexity task into smaller steps and allocate appropriate time for each phase."
        }
