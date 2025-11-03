# Todoist AI Agent

An intelligent assistant that helps manage your Todoist tasks by analyzing urgency, importance, and generating prioritized daily focus plans.

## Features

- **Conversational Chat Interface** (NEW!): Natural language task management - just chat with your tasks!
- **Task Analysis**: Evaluates tasks based on urgency, importance, and labels
- **Smart Prioritization**: Uses the Eisenhower Matrix and other heuristics
- **Daily Focus Plans**: Generates actionable daily task lists
- **AI-Powered Task Polishing**: Automatically improve vague task names and descriptions
- **Smart Due Date Inference**: Suggest due dates based on task content
- **Task Quality Scoring**: Identify tasks needing attention (0-100 score)
- **Label Management** (NEW!): Analyze label usage and identify insignificant labels
- **MCP Integration**: Apply updates directly to Todoist via Claude Code
- **Interactive Workflow**: Review and approve AI suggestions before applying

## Setup

1. **Install dependencies:**
```bash
cd todoist-ai-agent
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

2. **Set up Anthropic API key (for polish features):**
```bash
export ANTHROPIC_API_KEY="your-api-key-here"
# Or add to ~/.zshrc for persistence
```

3. **MCP Connection (CONFIGURED ✅):**
   - Todoist MCP server is configured in `~/.cursor/mcp.json`
   - API token is set
   - Restart Cursor/Claude Code to activate

## Usage

### Conversational Chat Interface (RECOMMENDED!)
The easiest way to interact with your tasks:
```bash
venv/bin/python3 chat.py
```

Natural language examples:
- "show today's tasks" or just `show`
- "prioritize my tasks" or just `p`
- "which tasks need polishing?" or `polish my tasks`
- "polish the first task" or "polish Amazon and Kwang IBKR"
- "analyze my labels" or "show label usage"
- "help me add due dates" or just `schedule`
- "categorize tasks" or just `categorize`

Features:
- **Context-aware**: Remember recently shown tasks ("polish these tasks")
- **Fuzzy matching**: "Amazon unblock" matches "Amazon account unblock - resubmit..."
- **Helpful feedback**: Clear error messages with suggestions
- **Label analytics**: Find and consolidate insignificant labels

### Quick CLI Tools
```bash
# View today's tasks (overdue, due today, upcoming)
venv/bin/python3 today.py

# List all tasks
venv/bin/python3 list_tasks.py
```

### With Mock Data (for testing)
```bash
./run.sh --mock
./run.sh --mock --full    # Full report
./run.sh --mock --top 3   # Top 3 priorities
```

### With Real Todoist Data (via Claude)
Ask Claude Code:
```
"Fetch my Todoist tasks and analyze them with the AI agent"
```

**See [HOWTO_USE_WITH_MCP.md](HOWTO_USE_WITH_MCP.md) for detailed MCP usage instructions.**

### Polish Your Tasks
```bash
# Interactive workflow - polish names, add descriptions, suggest due dates
./interactive_polish.py

# Test with mock data first
./interactive_polish.py --mock

# Only polish task names/descriptions
./interactive_polish.py --mode polish

# Only suggest due dates
./interactive_polish.py --mode schedule
```

**See [POLISH_FEATURES.md](POLISH_FEATURES.md) for detailed polish features guide.**

## Architecture

### Core Engine
- `todoist_client.py`: Interface for Todoist operations (MCP-ready)
- `task_analyzer.py`: Task analysis and scoring logic
- `prioritizer.py`: Prioritization algorithms and focus plan generation
- `agent.py`: Main agent orchestrator

### Conversational Interface
- `chat.py`: Natural language chat interface (RECOMMENDED!)
- `intent_router.py`: OpenAI-powered intent detection and routing
- `task_updater.py`: Safe task updates with preview and rollback

### Polish Features
- `task_polisher.py`: AI-powered task name/description enhancement
- `smart_scheduler.py`: Due date inference from task content
- `mcp_updater.py`: Update formatting and MCP integration helpers
- `interactive_polish.py`: Interactive workflow for reviewing suggestions

### Entry Points
- `chat.py`: Conversational CLI interface
- `today.py`: Quick today's tasks view
- `main.py`: CLI for analysis and prioritization
- `interactive_polish.py`: CLI for task polishing workflow

## Recent Updates

### 2024-11 - Enhanced Chat Interface
- ✅ **Fuzzy Task Matching** - Multi-word matching, partial names work better
- ✅ **Contextual References** - "polish these tasks" after showing tasks
- ✅ **Label Management** - Analyze and identify insignificant labels
- ✅ **Improved Feedback** - Clearer error messages with suggestions

### 2024-10 - Initial Release
- ✅ **AI-Powered Task Polishing** - Clean up task names and descriptions
- ✅ **Smart Due Date Inference** - Auto-suggest due dates from content
- ✅ **Task Quality Scoring** - Identify tasks needing improvement
- ✅ **Interactive Update Workflow** - Review before applying changes
- ✅ **MCP Update Integration** - Apply changes via Claude Code

## Future Enhancements

- [ ] Google Calendar integration
- [ ] Natural language task creation via voice/chat
- [ ] Weekly planning and goal tracking
- [ ] Automatic task breakdown for large projects
- [ ] Integration with email/Slack for task capture
