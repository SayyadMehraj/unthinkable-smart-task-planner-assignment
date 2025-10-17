# 📁 Smart Task Planner - Project Structure

## Overview
This document outlines the complete project structure of the Smart Task Planner system.

## Root Directory
```
smart_task_planner_project/
├── README.md                    # Main project documentation
├── requirements.txt             # Python dependencies
├── run.py                      # Main application entry point
├── setup.py                    # Project setup script
├── demo.py                     # Demo script for testing features
├── test_api.py                 # API testing script
├── env_example.txt             # Environment variables template
├── DEMO_VIDEO_SCRIPT.md        # Demo video creation guide
├── PROJECT_STRUCTURE.md        # This file
└── smart_task_planner.db       # SQLite database (created at runtime)
```

## Application Structure
```
app/                            # Main application package
├── __init__.py                 # Package initialization
├── main.py                     # FastAPI application entry point
├── models.py                   # Database models and Pydantic schemas
├── database.py                 # Database configuration and connection
├── routers/                    # API route handlers
│   ├── __init__.py
│   ├── goals.py               # Goals API endpoints
│   ├── plans.py               # Plans and task generation API
│   └── tasks.py               # Tasks management API
└── services/                   # Business logic services
    ├── __init__.py
    └── llm_service.py         # OpenAI LLM integration
```

## Static Files
```
static/                         # Frontend static files
└── index.html                 # Main web interface
```

## Key Files Description

### Core Application Files

#### `app/main.py`
- FastAPI application setup
- CORS middleware configuration
- Router registration
- Static file serving
- Health check endpoint

#### `app/models.py`
- SQLAlchemy database models (Goal, Plan, Task)
- Pydantic schemas for API requests/responses
- Data validation and serialization

#### `app/database.py`
- Database connection management
- Session factory configuration
- Database initialization
- Connection lifecycle management

### API Routers

#### `app/routers/goals.py`
- Goal CRUD operations
- Goal listing and filtering
- Goal deletion with cascade

#### `app/routers/plans.py`
- AI-powered task plan generation
- Plan management
- Task addition to plans
- Plan deletion with cascade

#### `app/routers/tasks.py`
- Task CRUD operations
- Task status and priority updates
- AI-powered task suggestions
- Task complexity analysis

### Services

#### `app/services/llm_service.py`
- OpenAI GPT integration
- Task breakdown generation
- Task analysis and suggestions
- Prompt engineering and response parsing

### Frontend

#### `static/index.html`
- Responsive web interface
- Goal input form
- Real-time task plan display
- Modern CSS styling
- JavaScript API integration

### Utility Scripts

#### `run.py`
- Application startup script
- Environment validation
- Server configuration

#### `setup.py`
- Project setup automation
- Dependency installation
- Environment configuration
- Basic testing

#### `demo.py`
- Feature demonstration script
- LLM service testing
- Database operations demo
- Task analysis examples

#### `test_api.py`
- API endpoint testing
- Integration testing
- Error handling validation
- Performance testing

## Database Schema

### Goals Table
```sql
CREATE TABLE goals (
    id INTEGER PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    user_input TEXT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME
);
```

### Plans Table
```sql
CREATE TABLE plans (
    id INTEGER PRIMARY KEY,
    goal_id INTEGER NOT NULL,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    estimated_duration_days INTEGER,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME,
    FOREIGN KEY (goal_id) REFERENCES goals (id)
);
```

### Tasks Table
```sql
CREATE TABLE tasks (
    id INTEGER PRIMARY KEY,
    plan_id INTEGER NOT NULL,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    priority VARCHAR(20) DEFAULT 'medium',
    status VARCHAR(20) DEFAULT 'pending',
    estimated_duration_hours INTEGER,
    due_date DATETIME,
    dependencies JSON,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME,
    FOREIGN KEY (plan_id) REFERENCES plans (id)
);
```

## API Endpoints

### Goals API (`/api/goals/`)
- `POST /` - Create goal
- `GET /` - List goals
- `GET /{goal_id}` - Get goal with plans
- `PUT /{goal_id}` - Update goal
- `DELETE /{goal_id}` - Delete goal

### Plans API (`/api/plans/`)
- `POST /generate` - Generate AI task plan
- `GET /` - List plans
- `GET /{plan_id}` - Get plan with tasks
- `GET /goal/{goal_id}` - Get plans for goal
- `POST /{plan_id}/tasks` - Add task to plan
- `DELETE /{plan_id}` - Delete plan

### Tasks API (`/api/tasks/`)
- `GET /` - List tasks (with filtering)
- `GET /{task_id}` - Get task
- `PUT /{task_id}/status` - Update status
- `PUT /{task_id}/priority` - Update priority
- `PUT /{task_id}` - Update task
- `DELETE /{task_id}` - Delete task
- `GET /{task_id}/suggestions` - Get AI suggestions
- `GET /{task_id}/analysis` - Get complexity analysis
- `GET /plan/{plan_id}` - Get tasks for plan

## Environment Configuration

### Required Environment Variables
```bash
OPENAI_API_KEY=your_openai_api_key_here
DATABASE_URL=sqlite:///./smart_task_planner.db
APP_NAME=Smart Task Planner
APP_VERSION=1.0.0
DEBUG=True
```

## Dependencies

### Core Dependencies
- `fastapi==0.104.1` - Web framework
- `uvicorn==0.24.0` - ASGI server
- `pydantic==2.5.0` - Data validation
- `sqlalchemy==2.0.23` - Database ORM
- `openai==1.3.7` - OpenAI API client
- `python-dotenv==1.0.0` - Environment management

### Additional Dependencies
- `python-multipart==0.0.6` - Form data handling
- `jinja2==3.1.2` - Template engine
- `aiofiles==23.2.1` - Async file operations
- `httpx==0.25.2` - HTTP client

## Development Workflow

### Setup
1. Run `python setup.py` to initialize the project
2. Configure environment variables in `.env`
3. Install dependencies with `pip install -r requirements.txt`

### Development
1. Start server with `python run.py`
2. Access frontend at `http://localhost:8000`
3. View API docs at `http://localhost:8000/docs`

### Testing
1. Run `python test_api.py` for API testing
2. Run `python demo.py` for feature demonstration
3. Manual testing through web interface

### Deployment
1. Configure production database
2. Set production environment variables
3. Use production ASGI server (Gunicorn)
4. Set up reverse proxy (Nginx)
5. Configure SSL certificates

## File Naming Conventions

- **Python files**: snake_case (e.g., `llm_service.py`)
- **HTML files**: kebab-case (e.g., `index.html`)
- **Configuration files**: lowercase (e.g., `requirements.txt`)
- **Documentation**: UPPERCASE (e.g., `README.md`)

## Code Organization Principles

1. **Separation of Concerns**: Clear separation between API, business logic, and data layers
2. **Modularity**: Each component has a single responsibility
3. **Reusability**: Services and utilities are designed for reuse
4. **Testability**: Code is structured for easy testing
5. **Scalability**: Architecture supports future enhancements

## Security Considerations

- Environment variables for sensitive data
- Input validation with Pydantic
- SQL injection prevention with SQLAlchemy
- CORS configuration for API access
- Error handling without information leakage

---

This structure provides a solid foundation for the Smart Task Planner system while maintaining clean code organization and scalability for future enhancements.
