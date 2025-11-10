# Quick Start: Task Polish Features

Get started with AI-powered task polishing in 5 minutes!

## 1. Install Dependencies

```bash
cd /Users/jj/todoist-ai-agent
source venv/bin/activate
pip install -r requirements.txt
```

## 2. Set Your Anthropic API Key

```bash
# Set for this session
export ANTHROPIC_API_KEY="your-api-key-here"

# OR make it permanent (recommended)
echo 'export ANTHROPIC_API_KEY="your-api-key"' >> ~/.zshrc
source ~/.zshrc
```

Get your API key from: https://console.anthropic.com/

## 3. Test with Mock Data

```bash
# Test the workflow with sample tasks
./interactive_polish.py --mock
```

This will:
- Load 8 mock tasks
- Analyze their quality
- Generate polish suggestions
- Let you review and approve
- Save updates to `pending_updates.json`

## 4. Try with Your Real Tasks

```bash
# Run the full workflow on your actual Todoist tasks
./interactive_polish.py
```

You'll see:
1. Tasks fetched from Todoist
2. Quality analysis
3. AI suggestions (before/after comparison)
4. Interactive approval (y/n for each)
5. Summary of approved updates

## 5. Apply Updates to Todoist

After approving updates, ask Claude Code:

```
"Apply the updates from pending_updates.json to Todoist using MCP"
```

Claude will apply each approved change to your Todoist account.

## Common Workflows

### Morning Task Cleanup
```bash
# Polish tasks you dumped yesterday
./interactive_polish.py --quality 40
# Review and approve
# Apply via Claude Code
```

### Just Add Due Dates
```bash
# Only suggest due dates, skip polishing
./interactive_polish.py --mode schedule
```

### Check Task Quality
```bash
# See which tasks need the most help
python -c "
from agent import TodoistAIAgent
agent = TodoistAIAgent()
report = agent.get_task_quality_report()
print(f'Average quality: {report[\"average_quality\"]}%')
print('Worst tasks:', [t['task_content'] for t in report['worst_tasks'][:3]])
"
```

## What Gets Improved?

### Task Names
- ❌ "call john" → ✅ "Call John about Q4 project review"
- ❌ "meeting" → ✅ "Team standup - discuss sprint planning"
- ❌ "fix bug" → ✅ "Fix login authentication bug in user dashboard"

### Due Dates
- "tomorrow" → Actual date calculated
- "by end of week" → Next Friday's date
- "urgent" → Tomorrow's date suggested
- "dentist appointment" → This week suggested

### Quality Issues Fixed
- Missing action verbs
- Too vague or too long
- Missing descriptions
- Missing due dates for important tasks
- Missing priority flags
- Missing categorization labels

## Tips

1. **Start conservative**: Use `--quality 60` for only the worst tasks
2. **Review carefully**: Don't auto-approve until you trust the AI
3. **Test first**: Always try `--mock` before running on real data
4. **Iterate**: Polish a few tasks, see results, adjust

## Troubleshooting

**"ANTHROPIC_API_KEY not set"**
```bash
export ANTHROPIC_API_KEY="sk-ant-..."
```

**"No tasks needing polish"**
Your tasks already look good! Try lowering the threshold:
```bash
./interactive_polish.py --quality 30
```

**Changes not applying**
Remember to use Claude Code MCP to apply changes:
- Run `./interactive_polish.py`
- Approve suggestions
- Ask Claude Code to apply via MCP

## Next Steps

- Read [POLISH_FEATURES.md](POLISH_FEATURES.md) for full documentation
- Customize quality thresholds for your needs
- Set up a daily/weekly task cleanup routine
- Explore the programmatic API in `agent.py`

Happy polishing! 🪄
