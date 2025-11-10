# Task Polish Features Guide

## Overview

The Todoist AI Agent now includes powerful AI-powered features to automatically improve your tasks:

1. **Task Polishing** - Clean up vague task names and add detailed descriptions
2. **Smart Due Date Inference** - Automatically suggest due dates based on task content
3. **MCP Integration** - Apply updates directly to Todoist via Claude Code

## Features

### 1. AI-Powered Task Polishing

Automatically improve task quality by:
- Converting vague names into clear, actionable tasks
- Adding specific context and details
- Starting task names with action verbs
- Extracting implicit priority and labels from content

**Examples:**
```
"call john" → "Call John about Q4 project review"
"dentist" → "Dentist appointment for cleaning"
"fix bug" → "Fix login authentication bug in user dashboard"
"meeting" → "Team standup meeting - discuss sprint planning"
```

### 2. Smart Due Date Inference

Intelligently suggests due dates by:
- Parsing explicit dates ("tomorrow", "next Friday", "by end of month")
- Understanding urgency keywords ("urgent", "ASAP")
- Applying category heuristics (bills → end of month, appointments → soon)
- Using AI to infer implicit deadlines

**Supported Date Patterns:**
- Relative: "today", "tomorrow", "in 3 days", "in 2 weeks"
- Named days: "next Monday", "this Friday", "on Wednesday"
- Date formats: "2024-12-25", "by end of week", "by end of month"
- Natural language: Analyzed by AI for context

### 3. Task Quality Scoring

Each task gets a quality score (0-100) based on:
- Clear action verb at start (+25 points)
- Appropriate name length (+20 points)
- Has description (+20 points)
- Has due date (+15 points)
- Has priority set (+10 points)
- Has labels (+10 points)

Tasks below 50% are flagged for improvement.

## Setup

### 1. Install Dependencies

```bash
cd /Users/jj/todoist-ai-agent
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Set Anthropic API Key

```bash
export ANTHROPIC_API_KEY="your-api-key-here"
```

Or add to your `~/.bashrc` or `~/.zshrc`:
```bash
echo 'export ANTHROPIC_API_KEY="your-api-key"' >> ~/.zshrc
source ~/.zshrc
```

### 3. Verify Setup

```bash
python -c "from task_polisher import TaskPolisher; print('✅ Setup complete!')"
```

## Usage

### Interactive Workflow (Recommended)

The interactive workflow lets you review and approve suggestions before applying:

```bash
# Polish and schedule tasks (both)
./interactive_polish.py

# Only polish task names/descriptions
./interactive_polish.py --mode polish

# Only suggest due dates
./interactive_polish.py --mode schedule

# Test with mock data first
./interactive_polish.py --mock

# Higher quality threshold (stricter)
./interactive_polish.py --quality 60
```

**Workflow Steps:**
1. Fetches all your tasks from Todoist
2. Analyzes quality and identifies tasks needing attention
3. Generates AI-powered suggestions
4. Shows before/after comparison for each task
5. You approve/reject each suggestion interactively
6. Saves approved updates to `pending_updates.json`
7. You apply via Claude Code MCP

### Programmatic Usage

Use the agent API directly:

```python
from agent import TodoistAIAgent

# Initialize agent
agent = TodoistAIAgent()

# Get task quality report
quality_report = agent.get_task_quality_report()
print(f"Average quality: {quality_report['average_quality']}%")
print(f"Tasks needing attention: {quality_report['tasks_needing_attention']}")

# Polish tasks
polish_suggestions = agent.polish_tasks(min_quality=50)
for suggestion in polish_suggestions:
    if suggestion['needs_polishing']:
        print(f"Original: {suggestion['original_name']}")
        print(f"Improved: {suggestion['suggested_name']}")

# Suggest due dates
date_suggestions = agent.suggest_due_dates()
for suggestion in date_suggestions:
    print(f"{suggestion['task_content']} → {suggestion['suggested_date']}")
    print(f"  Confidence: {suggestion['confidence']}")
    print(f"  Reason: {suggestion['reasoning']}")
```

### Using with Claude Code MCP

After running the interactive workflow:

1. **Generate updates:**
   ```bash
   ./interactive_polish.py
   # Review and approve suggestions
   # Updates saved to pending_updates.json
   ```

2. **Apply via Claude Code:**
   Ask Claude:
   ```
   "Apply the updates from pending_updates.json to Todoist using MCP"
   ```

   Claude will:
   - Read the pending updates
   - Use the Todoist MCP `update-tasks` tool
   - Apply each approved change to Todoist
   - Confirm completion

3. **Verify changes:**
   ```bash
   ./run.sh  # See updated tasks in your focus plan
   ```

## Command Reference

### interactive_polish.py

```bash
# Full workflow with both polish and schedule
./interactive_polish.py

# Options:
--mode {polish,schedule,both}  # Workflow mode (default: both)
--quality N                     # Min quality score 0-100 (default: 50)
--mock                          # Test with mock data
--auto-approve                  # Skip interactive review (use with caution!)
```

### Task Quality Checks

The polisher checks for these quality issues:

| Issue | Impact | Fix |
|-------|--------|-----|
| No action verb | -25 points | Start with: Call, Write, Fix, etc. |
| Too short (<10 chars) | -20 points | Add context and specifics |
| Too long (>80 chars) | -20 points | Break into subtasks |
| No description | -20 points | Add why/how/context |
| No due date | -15 points | Add deadline or schedule |
| No priority | -10 points | Set priority 1-4 |
| No labels | -10 points | Tag with categories |

## Examples

### Example 1: Daily Morning Cleanup

```bash
# Morning routine to polish your dumped tasks from yesterday
./interactive_polish.py --quality 40

# Review suggestions
# Approve the good ones
# Apply via Claude Code
```

### Example 2: Weekly Task Audit

```bash
# Check overall task quality
python -c "
from agent import TodoistAIAgent
agent = TodoistAIAgent()
report = agent.get_task_quality_report()
print(f'Average quality: {report[\"average_quality\"]}%')
print('\\nWorst tasks:')
for task in report['worst_tasks']:
    print(f'  - {task[\"task_content\"]}: {task[\"percentage\"]}%')
"
```

### Example 3: Focus on Due Dates Only

```bash
# Just add due dates to tasks that need them
./interactive_polish.py --mode schedule
```

## Tips for Best Results

### Task Naming
- ✅ **Good:** "Call Dr. Smith to schedule annual checkup"
- ❌ **Bad:** "call dr"

### Descriptions
- ✅ **Good:** "Prepare slides for Q4 review meeting. Cover: sales data, team metrics, roadmap updates."
- ❌ **Bad:** "make slides" (no description)

### Due Dates
- Include hints in task name: "Pay electricity bill by end of month"
- Use standard phrases: "tomorrow", "next Friday", "in 3 days"

### Labels
- Use consistent labels: "work", "personal", "urgent", "health"
- The polisher will suggest relevant labels automatically

## Troubleshooting

### "ANTHROPIC_API_KEY not set"
```bash
export ANTHROPIC_API_KEY="your-key-here"
```

### "Task polisher not available"
The API key isn't set or is invalid. Set it and restart your script.

### Polish suggestions seem off
The AI learns from your task context. Try:
- Adding more detail to original tasks
- Using consistent labels
- Adjusting the quality threshold (--quality)

### Changes not applying to Todoist
Remember: You must use Claude Code MCP to apply changes:
1. Run `./interactive_polish.py`
2. Review and approve
3. Ask Claude Code to apply via MCP

## Advanced Usage

### Custom Quality Thresholds

```python
from task_polisher import TaskPolisher

polisher = TaskPolisher()

# Very strict - only perfect tasks pass
perfect_tasks = polisher.identify_tasks_needing_polish(tasks, min_quality=80)

# Lenient - catch only really bad tasks
bad_tasks = polisher.identify_tasks_needing_polish(tasks, min_quality=30)
```

### Custom Date Inference

```python
from smart_scheduler import SmartScheduler

scheduler = SmartScheduler()

# Infer date for a single task
task = {"content": "Submit report by Friday", "description": "", "labels": []}
suggestion = scheduler.infer_due_date(task)
print(suggestion)
# {'suggested_date': '2025-11-07', 'confidence': 'high', 'source': 'pattern_match'}
```

### Batch Processing

```python
from interactive_polish import InteractivePolishWorkflow

workflow = InteractivePolishWorkflow()

# Auto-approve all high-confidence suggestions
results = workflow.run(
    mode="both",
    min_quality=50,
    auto_approve=True  # Skip interactive review
)

print(f"Applied {len(results['approved_updates'])} updates")
```

## API Reference

### TaskPolisher

```python
polisher = TaskPolisher(api_key=None)  # Uses ANTHROPIC_API_KEY env var

# Polish a single task
result = polisher.polish_task(task)

# Batch polish
results = polisher.polish_tasks_batch(tasks)

# Get quality score
quality = polisher.get_quality_score(task)

# Find tasks needing polish
needs_work = polisher.identify_tasks_needing_polish(tasks, min_quality=50)
```

### SmartScheduler

```python
scheduler = SmartScheduler(api_key=None)

# Infer due date
suggestion = scheduler.infer_due_date(task)

# Batch suggest
suggestions = scheduler.suggest_due_dates_batch(tasks)

# Detect recurring patterns
pattern = scheduler.get_recurring_pattern(task)  # "daily", "weekly", etc.
```

### MCPUpdater

```python
updater = MCPUpdater()

# Format for MCP
update_request = updater.format_update_request(task_id, updates)

# Create summary
summary = updater.create_summary_report(updates, original_tasks)

# Save/load
updater.save_updates_to_file(updates, "updates.json")
loaded = updater.load_updates_from_file("updates.json")
```

## FAQ

**Q: Will this change my tasks immediately?**
A: No. The workflow generates suggestions and saves them to a file. You review and approve, then use Claude Code MCP to actually apply changes.

**Q: How much does it cost?**
A: Uses Claude API. Typical cost: ~$0.001-0.01 per task polished. A batch of 50 tasks ≈ $0.50.

**Q: Can I undo changes?**
A: Not automatically. Review carefully before applying via MCP. Keep backups.

**Q: Does it work with recurring tasks?**
A: Yes! It can detect recurring patterns and suggest appropriate due dates.

**Q: What if I disagree with a suggestion?**
A: Just press 'n' during interactive review to skip it. Only approved suggestions are applied.

## Next Steps

1. **Set up your API key** (see Setup section)
2. **Test with mock data:** `./interactive_polish.py --mock`
3. **Try on real tasks:** `./interactive_polish.py --quality 40`
4. **Review suggestions carefully**
5. **Apply via Claude Code MCP**
6. **Check your improved tasks:** `./run.sh`

Enjoy your cleaner, more organized Todoist! 🎯
