# Todoist AI Agent

An intelligent assistant powered by OpenAI that helps manage your Todoist tasks through natural language conversation, smart prioritization, and AI-powered task improvements.

## Features

- **Conversational Chat Interface** (NEW!): Talk to your tasks in natural language - powered by OpenAI GPT-4o-mini
- **Task Analysis**: Evaluates tasks based on urgency, importance, and labels
- **Smart Prioritization**: Uses the Eisenhower Matrix and other heuristics
- **Daily Focus Plans**: Generates actionable daily task lists
- **AI-Powered Task Polishing**: OpenAI improves vague task names and descriptions
- **Smart Due Date Inference**: AI suggests due dates based on task content
- **Task Quality Scoring**: Identify tasks needing attention (0-100 score)
- **Label Management** (NEW!): Analyze label usage and identify insignificant labels
- **Interactive Workflow**: Review and approve AI suggestions before applying

## Setup

1. **Install dependencies:**
```bash
cd todoist-ai-agent
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

2. **Configure API keys:**

Create a `.env` file in the project root:
```bash
# Required: OpenAI API for natural language processing
OPENAI_API_KEY="your-openai-api-key-here"

# Required: Todoist API for task management
TODOIST_API_TOKEN="your-todoist-api-token-here"

# Optional: OpenAI model (defaults to gpt-4o-mini)
OPENAI_MODEL="gpt-4o-mini"
```

**Get your API keys:**
- **OpenAI API**: Get from [platform.openai.com/api-keys](https://platform.openai.com/api-keys)
- **Todoist API**: Get from [todoist.com/app/settings/integrations/developer](https://todoist.com/app/settings/integrations/developer)

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
- "polish the tasks 1) research kwang 2) resubmit docs" (numbered lists!)
- "polish these tasks" (after showing tasks)
- "analyze my labels" or "show label usage"
- "help me add due dates" or just `schedule`
- "categorize tasks" or just `categorize`

Features:
- **Context-aware**: Remember recently shown tasks ("polish these tasks")
- **Fuzzy matching**: "Amazon unblock" matches "Amazon account unblock - resubmit..."
- **Stop word filtering**: Ignores common words like "the", "to", "from" for accurate matching
- **Numbered list support**: "polish 1) task one 2) task two" works perfectly
- **Helpful feedback**: Clear error messages with suggestions
- **Label analytics**: Find and consolidate insignificant labels
- **Manual label control**: Polisher won't add labels automatically

### Quick CLI Tools
```bash
# View today's tasks (overdue, due today, upcoming)
venv/bin/python3 today.py

# List all tasks
venv/bin/python3 list_tasks.py
```

### Advanced Usage

**With Mock Data (for testing):**
```bash
./run.sh --mock
./run.sh --mock --full    # Full report
./run.sh --mock --top 3   # Top 3 priorities
```

**Direct CLI (legacy):**
```bash
venv/bin/python3 main.py              # Generate focus plan
venv/bin/python3 main.py --full       # Full report
venv/bin/python3 main.py --top 3      # Top 3 priorities
```

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
- `todoist_client.py`: Interface for Todoist API operations
- `task_analyzer.py`: Task analysis and scoring logic
- `prioritizer.py`: Prioritization algorithms and focus plan generation
- `agent.py`: Main agent orchestrator

### Conversational Interface (OpenAI-powered)
- `chat.py`: Natural language chat interface (RECOMMENDED!)
- `intent_router.py`: OpenAI GPT-4o-mini for intent detection and routing
- `task_updater.py`: Safe task updates with preview and rollback

### AI Features (OpenAI-powered)
- `task_polisher.py`: OpenAI-powered task name/description enhancement
- `smart_scheduler.py`: Due date inference from task content
- `interactive_polish.py`: Interactive workflow for reviewing AI suggestions
- `mcp_updater.py`: Update formatting helpers (legacy MCP support)

### Entry Points
- `chat.py`: Conversational CLI interface
- `today.py`: Quick today's tasks view
- `main.py`: CLI for analysis and prioritization
- `interactive_polish.py`: CLI for task polishing workflow

## Recent Updates

### 2024-11 - OpenAI Migration & Enhanced Chat Interface

#### Latest Improvements (Nov 2024)
- ✅ **Stop Word Filtering** - Ignores common words ("to", "from", "the", "how") for more accurate task matching
- ✅ **Numbered List Support** - Parse "polish 1) task one 2) task two" format correctly
- ✅ **Intent Routing Fixed** - Clear separation between quality reports and actual polishing actions
- ✅ **Label Control** - Disabled automatic label generation; users maintain full control over manual labeling
- ✅ **Multi-Word Matching** - Only significant words count for fuzzy matching (2+ chars, no stop words)
- ✅ **Better Error Messages** - Shows what was searched for, suggests recently shown tasks

#### Core Features (Nov 2024)
- ✅ **OpenAI Integration** - Migrated from Anthropic to OpenAI GPT-4o-mini
- ✅ **Direct Todoist API** - Standalone operation without MCP dependency
- ✅ **Fuzzy Task Matching** - Multi-word matching, partial names work better
- ✅ **Contextual References** - "polish these tasks" after showing tasks
- ✅ **Label Management** - Analyze label usage and identify insignificant labels
- ✅ **Improved Feedback** - Clearer error messages with suggestions

### 2024-10 - Initial Release
- ✅ **AI-Powered Task Polishing** - Clean up task names and descriptions
- ✅ **Smart Due Date Inference** - Auto-suggest due dates from content
- ✅ **Task Quality Scoring** - Identify tasks needing improvement
- ✅ **Interactive Update Workflow** - Review before applying changes
- ✅ **Conversational Interface** - Natural language chat with tasks

## Future Enhancements

- [ ] Google Calendar integration
- [ ] Natural language task creation via voice/chat
- [ ] Weekly planning and goal tracking
- [ ] Automatic task breakdown for large projects
- [ ] Integration with email/Slack for task capture
