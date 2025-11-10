# Todoist AI Agent - Project Structure

Clean, organized structure as of 2025-11-02

## 📁 Directory Structure

```
todoist-ai-agent/
├── Core Engine (7 files)
│   ├── agent.py                    # Main orchestrator
│   ├── task_analyzer.py            # Urgency/importance analysis
│   ├── prioritizer.py              # Eisenhower Matrix & focus plans
│   ├── todoist_client.py           # Todoist API client
│   ├── task_polisher.py            # ✨ AI task name/description enhancement
│   ├── smart_scheduler.py          # ✨ Due date inference
│   └── mcp_updater.py              # ✨ MCP integration helpers
│
├── Entry Points (3 files)
│   ├── main.py                     # CLI for analysis/prioritization
│   ├── interactive_polish.py       # ✨ Interactive polish workflow
│   └── run.sh                      # Helper script
│
├── Utilities (2 files)
│   ├── list_tasks.py               # List all tasks utility
│   └── example_polish_usage.py     # Code examples
│
├── Documentation (5 files)
│   ├── README.md                   # Main project readme
│   ├── POLISH_FEATURES.md          # Polish features guide
│   ├── QUICKSTART_POLISH.md        # 5-minute quick start
│   ├── HOWTO_USE_WITH_MCP.md       # MCP usage instructions
│   ├── QUICK_REFERENCE.md          # Command reference
│   └── PROJECT_STRUCTURE.md        # This file
│
├── Dependencies
│   ├── requirements.txt            # Python dependencies
│   └── venv/                       # Virtual environment
│
├── Data
│   ├── logs/                       # Log files
│   └── pending_updates.json        # Generated update requests (gitignored)
│
└── Archive
    └── _archive/                   # Old/redundant files (18 files)
```

## 🎯 What Each File Does

### Core Engine

**agent.py** (9.7KB)
- Main TodoistAIAgent class
- Orchestrates all features: analysis, polish, scheduling
- Methods: `run_analysis()`, `polish_tasks()`, `suggest_due_dates()`, `get_task_quality_report()`

**task_analyzer.py** (8.6KB)
- Analyzes tasks for urgency and importance
- Implements Eisenhower Matrix classification
- Calculates priority scores (0-100)
- Generates actionable recommendations

**prioritizer.py** (8.7KB)
- Creates daily focus plans
- Generates reports by quadrant
- Sorts and ranks tasks

**todoist_client.py** (7.7KB)
- Interfaces with Todoist API
- Normalizes task data
- Includes mock data for testing

**task_polisher.py** ✨ (7.7KB)
- AI-powered task enhancement
- Cleans up vague task names
- Adds detailed descriptions
- Calculates task quality scores (0-100)
- Extracts priorities and labels from content

**smart_scheduler.py** ✨ (11KB)
- Due date inference from task content
- Pattern matching ("tomorrow", "next Friday", "by end of month")
- AI-powered implicit date inference
- Heuristic-based suggestions
- Recurring pattern detection

**mcp_updater.py** ✨ (9.0KB)
- Formats updates for Todoist MCP
- Batch update support
- Before/after summary reports
- Save/load update requests

### Entry Points

**main.py** (5.1KB)
- CLI for task analysis and prioritization
- Usage: `./run.sh` or `python3 main.py`
- Modes: `--full`, `--top N`, `--quadrant Q1`, `--suggest`, `--mock`

**interactive_polish.py** ✨ (12KB)
- Interactive workflow for polishing tasks
- Usage: `./interactive_polish.py [--mode polish|schedule|both]`
- Review and approve AI suggestions
- Saves approved updates to `pending_updates.json`

**run.sh** (318B)
- Helper script to run main.py
- Activates venv automatically

### Utilities

**list_tasks.py** (2.2KB)
- Simple utility to list all Todoist tasks
- Usage: `python3 list_tasks.py`

**example_polish_usage.py** ✨ (5.9KB)
- Code examples for using polish features
- 5 example scenarios with explanations
- Usage: `python3 example_polish_usage.py`

### Documentation

**README.md** (3.3KB)
- Project overview and quick start
- Feature list and architecture
- Basic setup instructions

**POLISH_FEATURES.md** ✨ (10KB)
- Complete guide to AI polish features
- Setup instructions with Anthropic API
- Usage examples and API reference
- Tips and troubleshooting

**QUICKSTART_POLISH.md** ✨ (3.4KB)
- 5-minute quick start guide
- Step-by-step setup
- Common workflows

**HOWTO_USE_WITH_MCP.md** (3.0KB)
- How to use agent with Todoist MCP
- Integration patterns
- Example workflows

**QUICK_REFERENCE.md** (5.6KB)
- Command reference
- CLI options
- Quick tips

## 🗂️ Archive (_archive/)

Contains 18 old/redundant files that were replaced by the new polish features:

**Old Scripts (replaced):**
- `add_due_dates.py` → replaced by `smart_scheduler.py`
- `add_priorities.py` → replaced by `task_polisher.py`
- `update_tasks*.py` → replaced by `mcp_updater.py`
- `fetch_real_tasks*.py` → replaced by `list_tasks.py`

**Old Documentation:**
- `STATUS.md`, `SETUP.md` → info in README now
- `DAILY_REMINDER_SETUP.md`, `setup_daily_reminder.sh` → user uses Omnara instead

**Old Utilities:**
- Various test and debug scripts

These are kept for reference but not needed for normal use.

## 🚀 Quick Usage Guide

### Daily Morning Routine (via Omnara)

Ask Claude Code:
```
"Review my Todoist tasks and suggest improvements"
```

### Run Analysis

```bash
./run.sh                    # Daily focus plan
./run.sh --full             # Full report by quadrant
./run.sh --mock             # Test with mock data
```

### Polish Tasks (if you want to run scripts)

```bash
./interactive_polish.py                  # Interactive polish & schedule
./interactive_polish.py --mode polish    # Only polish names
./interactive_polish.py --mode schedule  # Only suggest due dates
./interactive_polish.py --mock           # Test with mock data
```

### Programmatic Usage

```python
from agent import TodoistAIAgent

agent = TodoistAIAgent()

# Get quality report
report = agent.get_task_quality_report()

# Polish tasks
suggestions = agent.polish_tasks(min_quality=50)

# Suggest due dates
dates = agent.suggest_due_dates()
```

## 📝 Notes

- ✨ = New feature added 2025-11-02
- All core functionality works without Anthropic API key (analysis, prioritization)
- Polish features (task_polisher, smart_scheduler) require ANTHROPIC_API_KEY
- Or just use Claude Code directly via Omnara - no API key needed!
- Archive folder can be deleted if you're sure you don't need old scripts

## 🎯 Recommended Workflow

1. **Morning**: Ask Claude Code via Omnara: "Review my Todoist tasks"
2. **Review**: See suggestions for improvements
3. **Approve**: Tell me which ones to apply
4. **Apply**: I update via MCP automatically
5. **Done**: Clean, organized tasks in ~5 minutes!
