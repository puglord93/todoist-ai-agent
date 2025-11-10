# Standalone Usage Guide

Your Todoist AI Agent now works **standalone** without Claude Code! It uses OpenAI's GPT-4o-mini model for task polishing and prioritization.

## Setup Complete ✅

- OpenAI API integrated
- Environment variables configured in `.env`
- Using **gpt-4o-mini** model (cost-effective and fast)

## Running Scripts Standalone

All scripts can now be run directly from your terminal:

### 1. Fetch Today's Tasks
```bash
cd /Users/jj/Code/todoist-ai-agent
venv/bin/python3 list_tasks.py
```

### 2. Polish Tasks with AI
```bash
venv/bin/python3 demo_openai_polish.py
```

This will use OpenAI to:
- Improve task names with clear action verbs
- Add detailed descriptions
- Extract priority levels
- Suggest relevant labels

### 3. Test with Your Real Tasks
```bash
venv/bin/python3 test_polish_standalone.py
```

## Configuration

Your `.env` file contains:
- `TODOIST_API_TOKEN` - Your Todoist API key
- `OPENAI_API_KEY` - Your OpenAI API key
- `OPENAI_MODEL` - Set to `gpt-4o-mini` (you can change this)

### Available OpenAI Models
- **gpt-4o-mini** ✅ (Current - recommended for task polishing)
- gpt-4o (More powerful, higher cost)
- gpt-4-turbo (Good balance)

To change the model, edit `.env`:
```bash
OPENAI_MODEL=gpt-4o-mini
```

## Security

✅ API keys are stored in `.env` (not committed to git)
✅ `.gitignore` configured to protect sensitive files
✅ `.env.example` provided as a template

## Next Steps

You can now:

1. **Create custom scripts** that use `TaskPolisher` class
2. **Automate daily task reviews** via cron jobs
3. **Build your own task management workflows**

### Example: Polish All Tasks

```python
from task_polisher import TaskPolisher
import requests
import os
from dotenv import load_dotenv

load_dotenv()

# Fetch tasks
token = os.getenv("TODOIST_API_TOKEN")
response = requests.get(
    "https://api.todoist.com/rest/v2/tasks",
    headers={"Authorization": f"Bearer {token}"}
)
tasks = response.json()

# Polish them
polisher = TaskPolisher()
for task in tasks:
    result = polisher.polish_task(task)
    print(f"✨ {result['suggested_name']}")
```

## Cost Considerations

GPT-4o-mini pricing (as of Nov 2024):
- ~$0.15 per 1M input tokens
- ~$0.60 per 1M output tokens

For typical task polishing:
- ~100 tokens per task
- **Cost: ~$0.001 per task** (very affordable!)

## Support

For issues or questions, refer to:
- [OpenAI API Docs](https://platform.openai.com/docs)
- [Todoist API Docs](https://developer.todoist.com/rest/v2/)
