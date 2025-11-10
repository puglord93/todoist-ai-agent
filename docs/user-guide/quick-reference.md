# Quick Reference Guide

## Project Structure

```
todoist-ai-agent/
├── agent.py                      # Main agent orchestrator
├── task_analyzer.py              # Task analysis & scoring logic
├── prioritizer.py                # Prioritization & focus plans
├── todoist_client.py             # Todoist API interface (MCP-ready)
├── main.py                       # CLI entry point
├── run.sh                        # Helper script to run agent
├── requirements.txt              # Python dependencies
├── README.md                     # Project overview
├── SETUP.md                      # Detailed setup guide
├── QUICK_REFERENCE.md           # This file
├── mcp_integration_example.py   # MCP integration examples
└── venv/                        # Virtual environment
```

## Quick Start

```bash
# Run with mock data
./run.sh --mock

# Or manually:
source venv/bin/activate
python main.py --mock
```

## Common Commands

```bash
# Daily focus plan (default)
./run.sh --mock

# Full report with all quadrants
./run.sh --mock --full

# Top 3 priorities
./run.sh --mock --top 3

# Show Q1 tasks (Do First)
./run.sh --mock --quadrant Q1

# Get update suggestions
./run.sh --mock --suggest

# Help
./run.sh --help
```

## Eisenhower Matrix Quadrants

- **Q1**: Urgent & Important → **Do First**
- **Q2**: Important, Not Urgent → **Schedule**
- **Q3**: Urgent, Not Important → **Delegate**
- **Q4**: Neither → **Consider Eliminating**

## Scoring System

### Priority Score (0-100)
- Combines urgency and importance
- Higher = more priority
- Formula: `(urgency × 0.6 + importance × 0.4) × 10`

### Urgency Score (0-10)
Based on:
- Due date proximity
- "urgent" or "critical" labels
- Overdue status

### Importance Score (0-10)
Based on:
- Todoist priority (1-4)
- Importance labels (urgent, important, bug, etc.)
- Category weights (work, health, family)

## Key Features

### 1. Task Analysis
- Evaluates urgency based on due dates and labels
- Calculates importance from priority and context
- Classifies tasks into Eisenhower quadrants
- Generates actionable recommendations

### 2. Daily Focus Plans
- Selects top priority tasks for the day
- Provides overview statistics
- Highlights overdue and due-today tasks

### 3. Smart Prioritization
- Sorts by priority score
- Considers overdue status
- Accounts for due dates

### 4. Update Suggestions
- Identifies tasks needing due dates
- Suggests priority adjustments
- Finds inconsistencies

## Customization Points

### Label Weights
Edit [task_analyzer.py:18-25](task_analyzer.py#L18-L25):
```python
IMPORTANCE_LABELS = {
    "urgent": 10,
    "important": 8,
    # Add your labels here
}
```

### Category Multipliers
Edit [task_analyzer.py:27-33](task_analyzer.py#L27-L33):
```python
CATEGORY_WEIGHTS = {
    "work": 1.2,
    "health": 1.3,
    # Add your categories here
}
```

### Priority Formula
Edit [task_analyzer.py:103-108](task_analyzer.py#L103-L108):
```python
def _calculate_priority_score(self, urgency: float, importance: float,
                              todoist_priority: int) -> float:
    # Adjust these weights
    score = (urgency * 0.6 + importance * 0.4) * 10
    return round(score, 2)
```

### Focus Plan Size
Edit [agent.py:48](agent.py#L48):
```python
focus_plan = self.prioritizer.create_daily_focus_plan(
    analyzed_tasks,
    max_tasks=5  # Change this number
)
```

## Next Steps

1. **Test with mock data** → Understand how it works
2. **Customize weights** → Match your preferences
3. **Connect MCP server** → Use real Todoist data
4. **Add Calendar integration** → Time blocking
5. **Enable task updates** → Automatic rescheduling

## Troubleshooting

| Problem | Solution |
|---------|----------|
| Command not found | Run `chmod +x run.sh` |
| Module not found | Activate venv: `source venv/bin/activate` |
| No tasks showing | Use `--mock` flag for testing |
| Wrong priorities | Adjust weights in `task_analyzer.py` |

## Architecture Flow

```
1. TodoistClient → Fetches tasks (mock or real)
                ↓
2. TaskAnalyzer → Scores each task
                ↓
3. TaskPrioritizer → Creates focus plan
                ↓
4. Agent → Orchestrates & formats
                ↓
5. CLI → Displays to user
```

## API Methods

### TodoistClient
- `fetch_tasks()` → Get all tasks
- `update_task(id, updates)` → Update a task
- `normalize_task(task)` → Standardize format

### TaskAnalyzer
- `analyze_task(task)` → Full analysis with scores

### TaskPrioritizer
- `create_prioritized_list(tasks)` → Sorted by priority
- `create_daily_focus_plan(tasks, n)` → Top N tasks
- `generate_focus_summary(plan)` → Formatted output
- `generate_full_report(plan)` → Complete breakdown

### TodoistAIAgent
- `run_analysis()` → Full pipeline
- `generate_report(type)` → Format output
- `get_top_priorities(n)` → Top N tasks
- `get_tasks_by_quadrant(q)` → Filter by quadrant
- `suggest_updates()` → Smart suggestions
- `apply_update(id, updates)` → Update task

## Example Python Usage

```python
from agent import TodoistAIAgent

# Initialize
agent = TodoistAIAgent(use_mock=True)

# Get top 3 priorities
top_tasks = agent.get_top_priorities(3)
for task in top_tasks:
    print(f"{task['task_content']}: {task['priority_score']}")

# Get Q1 tasks
urgent_important = agent.get_tasks_by_quadrant("Q1")

# Get suggestions
suggestions = agent.suggest_updates()

# Apply an update (when MCP connected)
agent.apply_update("task_123", {"due_date": "2025-11-05"})
```

## Resources

- [README.md](README.md) - Project overview
- [SETUP.md](SETUP.md) - Detailed setup instructions
- [mcp_integration_example.py](mcp_integration_example.py) - MCP integration guide
