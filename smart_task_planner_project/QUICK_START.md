# 🚀 Smart Task Planner - Quick Start

### 1. Setup
```bash
cd smart_task_planner_project
python setup.py
```

### 2. Start Application
```bash
python run.py
```

### 3. Access
- **Web Interface**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

### 4. Test
```bash
python test_api.py
python demo.py
```

## Example Usage

### Web Interface
1. Go to http://localhost:8000
2. Enter a goal: "Launch a mobile app in 2 weeks"
3. Add context: "Solo developer, React Native, first app"
4. Set timeline: 2 weeks
5. Click "Generate Task Plan"
6. View the AI-generated task breakdown!

### API Usage
```bash
# Generate a task plan
curl -X POST "http://localhost:8000/api/plans/generate" \
     -H "Content-Type: application/json" \
     -d '{
       "goal": "Learn Python in 1 month",
       "timeline_weeks": 4,
       "additional_context": "Complete beginner, 2 hours per day"
     }'
```

## What You Get

✅ **AI-Powered Task Generation** - Break any goal into actionable tasks  
✅ **Intelligent Reasoning** - Understand why tasks are structured this way  
✅ **Realistic Timelines** - Get accurate time estimates and due dates  
✅ **Dependency Management** - Tasks are ordered logically  
✅ **Priority Assignment** - AI assigns appropriate priority levels  
✅ **Modern Web Interface** - Clean, responsive design  
✅ **RESTful API** - Integrate with your own applications  
✅ **Comprehensive Documentation** - Everything you need to get started  

## Troubleshooting

### Common Issues

**"OPENAI_API_KEY not found"**
- This is not an error! The system works without an API key
- Optional: Add OpenAI API key for enhanced AI features
- Get an API key from https://platform.openai.com/api-keys if desired

**"Module not found" errors**
- Run `pip install -r requirements.txt`
- Make sure you're using Python 3.8+

**"Port 8000 already in use"**
- Change the port in `run.py` or stop the other service
- Use `--port 8001` flag with uvicorn

**Database errors**
- Delete `smart_task_planner.db` and restart
- Check file permissions in the project directory

### Getting Help

1. **Check the logs** - Look at the terminal output for error messages
2. **Read the documentation** - See `README.md` for detailed information
3. **Test the API** - Use `python test_api.py` to verify functionality
4. **Check the demo** - Run `python demo.py` to see features in action

## Next Steps

1. **Explore the API** - Visit http://localhost:8000/docs
2. **Try different goals** - Test with various types of projects
3. **Customize the system** - Modify prompts, add features
4. **Deploy to production** - Follow the deployment guide in README.md
5. **Contribute** - Fork the repository and submit improvements

## Example Goals to Try

- "Launch a product in 2 weeks"
- "Learn a new programming language in 3 months"
- "Organize a team building event"
- "Write a technical blog post"
- "Plan a vacation trip"
- "Start a side business"
- "Learn to cook Italian cuisine"
- "Organize a conference"

---

**Ready to transform your goals into actionable plans? Start now!** 🎯
