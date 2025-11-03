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
  - Maintains conversation history and context
  - Shortcuts: `show`, `p`, `polish`, `schedule`, `categorize`, `help`
  - **NEW**: Fuzzy task matching - "Amazon unblock" matches "Amazon account unblock..."
  - **NEW**: Contextual references - "polish these tasks" after showing tasks
  - **NEW**: Label management - "analyze my labels", "show label usage"
  - **NEW**: Multi-word matching - handles partial task names better
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
- **intent_router.py** - AI intent detection for natural language commands (OpenAI function calling)
- **agent.py** - Main orchestrator for all task management functions
- **task_updater.py** - Safe task updates with preview/rollback (NEW)
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
- "polish the first task" or "polish Amazon and Kwang IBKR" (fuzzy matching works!)
- "polish these tasks" (after showing tasks - remembers context)
- "analyze my labels" or "show label usage" (NEW - identify insignificant labels)
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

## Recent Improvements (2024-11)

### Enhanced Chat Interface
The chat interface ([chat.py](chat.py)) now has significantly improved task handling:

**1. Fuzzy Task Matching with Stop Word Filtering**
- Multi-word matching: "Amazon unblock" correctly matches "Amazon account unblock - resubmit identity documents"
- Substring matching: Partial task names work much better
- **Stop word filtering**: Ignores common words like "the", "to", "from", "how" for more accurate matching
- Multi-word scoring: If 2+ significant words from your search appear in the task name, it's a match
- Implementation: Enhanced `_identify_task()` method in [chat.py:462-514](chat.py#L462-L514)

**2. Numbered List Support**
- Parse numbered lists: "polish 1) task one 2) task two" correctly identifies both tasks
- Regex-based splitting by `\d+\)` pattern
- Each numbered item treated as separate task identifier
- Works with natural language: "polish the tasks 1) research kwang 2) resubmit docs"
- Implementation: [chat.py:555-574](chat.py#L555-L574)

**3. Intent Routing Improvements**
- Clear separation between `polish_tasks` (quality report) and `polish_and_apply` (actual changes)
- Function descriptions guide OpenAI to choose correct intent
- `polish_tasks`: Only for "which tasks need polishing?" queries
- `polish_and_apply`: For actual polishing like "polish these tasks"
- Implementation: [intent_router.py:78-176](intent_router.py#L78-L176)

**4. Contextual References**
- After showing tasks, you can say "polish these tasks" or "polish the first 3"
- The system remembers `last_shown_tasks` and uses context for follow-up commands
- Pronouns work: "these", "those", "them" all reference previously shown tasks
- Implementation: Enhanced `_identify_tasks_for_polish()` in [chat.py:516-586](chat.py#L516-L586)

**5. Label Management**
- New `manage_labels` intent handles label analysis requests
- "analyze my labels" shows usage statistics
- Identifies insignificant labels (used on ≤2 tasks)
- Shows most-used labels and suggests cleanup
- **Disabled automatic label generation**: Polishing no longer adds labels automatically
- User maintains full control over manual labeling system
- Implementation: `_handle_manage_labels()` in [chat.py:408-460](chat.py#L408-L460)
- Function definition: [intent_router.py:177-195](intent_router.py#L177-L195)

**6. Improved Error Messages**
- When task not found, shows what was searched for (in quotes)
- Suggests recently shown tasks as alternatives
- Context-appropriate tips based on the situation
- Example: "Could not find task 'amazon'. Recently shown tasks: 1. Submit ATUM..."

### Files Modified
- **chat.py** - Main interface improvements, task matching, numbered lists, stop words
- **intent_router.py** - Clearer function descriptions, numbered list support
- **task_polisher.py** - Disabled automatic label generation
- **task_updater.py** - Safe update preview system
- **agent.py** - Supports all the new features through existing methods

### Testing
All improvements were based on real user CLI logs showing:
- Task identification failures after showing tasks → Fixed with specific task name matching
- Wrong tasks being polished due to poor matching → Fixed with stop word filtering
- "polish my tasks" showing no actionable output → Fixed with intent routing
- Label management requests not being handled → Added manage_labels intent
- Numbered list not working → Added regex parsing for "1) task 2) task" format
- Too many labels being added → Disabled automatic label generation
