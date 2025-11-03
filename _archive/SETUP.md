# Setup Guide

## Quick Start

1. **Activate the virtual environment:**
```bash
source venv/bin/activate
```

2. **Run the agent with mock data:**
```bash
python main.py --mock
```

## Connecting to Todoist MCP Server

When you're ready to connect to the real Todoist API via MCP:

### Step 1: Install Todoist MCP Server

Follow the instructions from the Todoist MCP server repository to install and configure it.

### Step 2: Update Claude Code Settings

Add the Todoist MCP server to your Claude Code MCP settings. This is typically done in your Claude configuration file.

### Step 3: Modify the Client Code

Once the MCP server is available, you'll need to update [todoist_client.py](todoist_client.py) to use the MCP tools instead of mock data.

In the `fetch_tasks()` method, replace:
```python
# When MCP is connected, this will call the MCP tool
# For now, return mock data
print("⚠️  Todoist MCP not connected. Using mock data.")
return self._get_mock_tasks()
```

With code that calls the actual MCP tool (the exact syntax will depend on how your MCP server exposes the Todoist API).

### Step 4: Test with Real Data

Once connected, remove the `--mock` flag:
```bash
python main.py
```

## Usage Examples

### Daily Focus Plan (default)
```bash
python main.py --mock
```

### Full Report with All Quadrants
```bash
python main.py --mock --full
```

### Top N Priorities
```bash
python main.py --mock --top 5
```

### Tasks by Quadrant
```bash
python main.py --mock --quadrant Q1  # Do First
python main.py --mock --quadrant Q2  # Schedule
python main.py --mock --quadrant Q3  # Delegate
python main.py --mock --quadrant Q4  # Consider
```

### Get Update Suggestions
```bash
python main.py --mock --suggest
```

## Customization

### Adjust Label Weights

Edit [task_analyzer.py](task_analyzer.py) to customize:

- `IMPORTANCE_LABELS`: Add or modify label-based importance scores
- `CATEGORY_WEIGHTS`: Adjust multipliers for different categories

### Change Focus Plan Size

Modify the `max_tasks` parameter in [agent.py](agent.py):

```python
focus_plan = self.prioritizer.create_daily_focus_plan(analyzed_tasks, max_tasks=10)
```

### Customize Scoring Algorithm

The priority score calculation is in [task_analyzer.py:85](task_analyzer.py#L85):

```python
def _calculate_priority_score(self, urgency: float, importance: float,
                              todoist_priority: int) -> float:
    # Adjust these weights to change prioritization
    score = (urgency * 0.6 + importance * 0.4) * 10
    return round(score, 2)
```

## Future Enhancements

### Google Calendar Integration

When ready to add Google Calendar:

1. Install Google Calendar MCP server
2. Create `calendar_client.py` similar to `todoist_client.py`
3. Update `agent.py` to cross-reference tasks with calendar events
4. Add time-blocking suggestions based on calendar availability

### Task Updates

To enable task updates:

1. Ensure your Todoist MCP server supports write operations
2. Implement the update logic in [todoist_client.py:40](todoist_client.py#L40)
3. Use the `apply_update()` method in [agent.py:130](agent.py#L130)

Example:
```python
agent = TodoistAIAgent()
agent.apply_update("task_id", {"due_date": "2025-11-05", "priority": 4})
```

## Troubleshooting

### ModuleNotFoundError

Make sure you've activated the virtual environment:
```bash
source venv/bin/activate
pip install -r requirements.txt
```

### No tasks showing

If using real Todoist data and seeing no tasks, check:
1. MCP server is running and connected
2. Todoist API token is configured correctly
3. You have active tasks in your Todoist account

### Incorrect prioritization

The AI agent uses heuristics that may not match your personal preferences. Customize:
- Label weights in [task_analyzer.py](task_analyzer.py)
- Priority calculation in `_calculate_priority_score()`
- Urgency/importance thresholds in `_classify_eisenhower()`
