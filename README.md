# 🧠 Smart Task Planner

## Overview

Smart Task Planner is an AI-powered system that helps you break down complex goals into actionable tasks, with realistic timelines, priorities, and dependencies. It works completely offline—no API key is required—but can optionally use OpenAI for even more advanced AI features.

- **Modern FastAPI backend** with RESTful API
- **Local intelligent AI** task breakdown: works out of the box, offline, and free!
- **Web UI** at `/`, API docs at `/docs`
- **Support for product launches, learning, events, startups, mobile apps, and more**

---

## Features

- ✅ **AI-Powered Task Generation**: Any goal broken into logical, actionable steps
- ✅ **Intelligent Reasoning**: Understand how and why your plan is structured
- ✅ **No API Key Required**: Works out of the box via a local rule-based AI
- ✅ **Optional OpenAI Integration**: Just add your API key for enhanced features
- ✅ **Modern Web Interface**: Ready-to-use, responsive design (see `static/index.html`)
- ✅ **RESTful API**: Easy to integrate into other systems
- ✅ **Extensible Python codebase**: Built with FastAPI, SQLAlchemy, Pydantic

---

## Quick Start

```bash
cd smart_task_planner_project
python setup.py
python run.py
```

- **Web Interface**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

### Testing
```bash
python test_api.py
python demo.py
```

---

## Example Usage

### Web Interface
1. Go to http://localhost:8000
2. Enter a goal (e.g., "Launch a mobile app in 2 weeks")
3. Add context (optional)
4. Set a timeline (in weeks)
5. Click "Generate Task Plan" to get your breakdown!

### API Example
```bash
curl -X POST "http://localhost:8000/api/plans/generate" \
  -H "Content-Type: application/json" \
  -d '{
    "goal": "Learn Python in 1 month",
    "timeline_weeks": 4,
    "additional_context": "Complete beginner, 2 hours per day"
  }'
```

---

## How It Works

- **Automatic Goal Analysis:** The system analyzes your goal and picks the most relevant planning template
- **Local AI Service:** Uses internal logic/templates in `app/services/local_ai_service.py` to break down your goal (No API key, no cost, works offline!)
- **Realistic Schedules/Reasoning:** Produces an explanation for the plan and assigns proper timelines and dependencies
- **Optionally,** you can add an `OPENAI_API_KEY` in your `.env` file for even more advanced task reasoning.

---

## Project Structure

See [`PROJECT_STRUCTURE.md`](PROJECT_STRUCTURE.md) for complete details.

```
smart_task_planner_project/
├── app/
│   ├── main.py          # FastAPI application entry
│   ├── models.py        # SQLAlchemy models & Pydantic schemas
│   ├── database.py      # DB session & connection setup
│   ├── routers/         # API routers (goals, plans, tasks)
│   └── services/        # Core AI logic (local_ai_service.py)
├── static/
│   └── index.html       # Modern web interface
├── requirements.txt     # Dependencies
├── QUICK_START.md       # Step-by-step quick guide
├── PROJECT_STRUCTURE.md # Project structure & details
├── test_api.py          # API tests
├── demo.py              # Demo/feature showcase
├── setup.py             # Project/environment setup
├── env_example.txt      # Example environment config
└── run.py               # Main entry/start script
```

---

## Dependencies

- `fastapi==0.104.1`
- `uvicorn==0.24.0`
- `pydantic==2.5.0`
- `sqlalchemy==2.0.23`
- `openai==1.3.7` (optional)
- `python-dotenv==1.0.0`
- `python-multipart==0.0.6`
- `jinja2==3.1.2`
- `aiofiles==23.2.1`
- `httpx==0.25.2`

See `requirements.txt` for the full list.

---

## Environment Variables

See [`env_example.txt`](env_example.txt) for all available settings. Only `DATABASE_URL` is strictly required. `OPENAI_API_KEY` is optional for enhanced AI.

Example `.env`:
```env
DATABASE_URL=sqlite:///./smart_task_planner.db
OPENAI_API_KEY=your_api_key_here   # (optional)
APP_NAME=Smart Task Planner
DEBUG=True
```

---

## API Endpoints (Key Examples)

See automatic docs at `/docs` or [`PROJECT_STRUCTURE.md`](PROJECT_STRUCTURE.md) for full details.

- **Goals:**
  - `POST /api/goals/` — Create new goal
  - `GET /api/goals/` — List all goals
- **Plans:**
  - `POST /api/plans/generate` — Generate AI-powered task plan
  - `GET /api/plans/` — List all plans
- **Tasks:**
  - `POST /api/tasks/` — Create task
  - `GET /api/tasks/` — List tasks

---

## Troubleshooting

- **No API Key?** No problem! Local AI will generate plans.
- **Add enhanced AI?** Add `OPENAI_API_KEY` to `.env` (see docs).
- **Module not found?** Run `pip install -r requirements.txt` (Python 3.8+ recommended).
- **Database or port errors?** See `QUICK_START.md` for common fixes.
- **Questions?** See API docs at `/docs` or open an issue.

---

## Credits & License

MIT License. Created for Unthinkable assignment.

**Ready to turn big goals into reality?**

---
