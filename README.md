# Todoist AI Agent

An intelligent assistant that helps manage your Todoist tasks by analyzing urgency, importance, and generating prioritized daily focus plans.

## Features

- **Task Analysis**: Evaluates tasks based on urgency, importance, and labels
- **Smart Prioritization**: Uses the Eisenhower Matrix and other heuristics
- **Daily Focus Plans**: Generates actionable daily task lists
- **AI-Powered Task Polishing**: Automatically improve vague task names and descriptions
- **Smart Due Date Inference**: Suggest due dates based on task content
- **Task Quality Scoring**: Identify tasks needing attention (0-100 score)
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

### Polish Your Tasks (NEW!)
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

### Polish Features (NEW!)
- `task_polisher.py`: AI-powered task name/description enhancement
- `smart_scheduler.py`: Due date inference from task content
- `mcp_updater.py`: Update formatting and MCP integration helpers
- `interactive_polish.py`: Interactive workflow for reviewing suggestions

### Entry Points
- `main.py`: CLI for analysis and prioritization
- `interactive_polish.py`: CLI for task polishing workflow

## Recent Updates

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
