# Todoist AI Agent - Project Instructions

## Project Overview
This is a Todoist task management system with AI-powered features, OpenAI integration, and MCP support.

**Project Location**: `/Users/jj/Code/todoist-ai-agent`

## Environment Setup
- **Python Virtual Environment**: `venv/bin/python3`
- **Working Directory**: Always run scripts from `/Users/jj/Code/todoist-ai-agent`
- **API Configuration**: Uses `.env` file with `OPENAI_API_KEY` and `TODOIST_API_TOKEN`
- **AI Model**: Uses OpenAI GPT-4o-mini for cost-effective task management

## Available Scripts

### 🎯 Main Interface (RECOMMENDED)
- **chat.py** - **CONVERSATIONAL AI INTERFACE** - Chat with your tasks using natural language!
  - Natural language commands: "show today's tasks", "prioritize", "which need polishing?"
  - Maintains conversation history
  - Shortcuts: `show`, `p`, `polish`, `schedule`, `categorize`, `help`
  - See [CHAT_USAGE.md](CHAT_USAGE.md) for full guide

### Quick CLI Tools
- **today.py** - Quick view of today's tasks (overdue, due today, upcoming)
- **list_tasks.py** - List all Todoist tasks

### Core Scripts
- **todoist_client.py** - Unified interface for Todoist operations (API, MCP, or mock)
- **task_analyzer.py** - Analyzes and categorizes tasks
- **prioritizer.py** - AI-powered task prioritization
- **smart_scheduler.py** - Intelligent task scheduling with due dates
- **task_polisher.py** - Improves task descriptions using OpenAI
- **interactive_polish.py** - Interactive task improvement workflow
- **intent_router.py** - AI intent detection for natural language commands
- **agent.py** - Main orchestrator for all task management functions
- **main.py** - Command-line interface with flags
- **mcp_updater.py** - Updates tasks via MCP server

## How to Run Scripts
Always use the virtual environment:
```bash
venv/bin/python3 <script_name.py>
```

## Common User Requests & Actions

### 🌟 RECOMMENDED: Use the Chat Interface
For most tasks, use the conversational interface:
```bash
venv/bin/python3 chat.py
```

Then use natural language:
- "show today's tasks" or just `show`
- "prioritize my tasks" or just `p`
- "which tasks need polishing?" or just `polish`
- "help me add due dates" or just `schedule`
- "categorize tasks" or just `categorize`

### Alternative: Direct Script Execution

**Fetch today's tasks:**
```bash
venv/bin/python3 today.py
```

**List all tasks:**
```bash
venv/bin/python3 list_tasks.py
```

**Prioritize tasks:**
```bash
venv/bin/python3 main.py
```

**Polish tasks interactively:**
```bash
venv/bin/python3 interactive_polish.py
```

**Add due dates interactively:**
```bash
venv/bin/python3 interactive_polish.py --mode schedule
```

## MCP Integration
- The project supports Todoist MCP server when available
- `todoist_client.py` automatically detects and uses MCP tools if present
- Falls back to direct API calls or mock data for testing

## Task Context
- User manages both **work tasks** (venture building, deep-tech scouting) and **personal tasks**
- Work tasks often relate to: partnerships, POCs, market validation, academic collaborations
- Labels help categorize: work, personal, urgent, email, follow-up, etc.

## Notes
- Scripts filter out Todoist tutorial/onboarding tasks automatically
- Priority system: 1 (low) to 4 (urgent) in Todoist API format
- Always check if tasks are overdue, due today, or upcoming when presenting results
