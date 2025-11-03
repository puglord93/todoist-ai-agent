
# How to Use the Agent with Todoist MCP

Since you've configured the Todoist MCP server, here's how to use it with Claude Code:

## Method 1: Ask Claude to Fetch and Analyze (Easiest!)

Simply ask Claude Code:

```
"Fetch my Todoist tasks and run the AI agent analysis on them"
```

Claude will:
1. Use the MCP `find-tasks` tool to get your real Todoist tasks
2. Save them to a JSON file
3. Run the Python agent on your real data
4. Show you the prioritized focus plan

## Method 2: Manual Python Execution

If you want to run it yourself:

### Step 1: Ask Claude to fetch your tasks

```
"Use the Todoist MCP to fetch all my tasks and save them to tasks.json"
```

### Step 2: Run the agent

```bash
cd /Users/jj/todoist-ai-agent
source venv/bin/activate

# Pass the tasks to the analysis script
python run_with_claude.py "$(cat tasks.json)"

# Or for full report:
python run_with_claude.py "$(cat tasks.json)" --full
```

## Method 3: Hybrid Approach (Best of Both Worlds)

Use the mock flag to test, then ask Claude for real data:

```bash
# Test with mock data
./run.sh --mock

# When ready, ask Claude:
# "Fetch my real Todoist tasks and analyze them with the agent"
```

## Available Commands When Claude Fetches Your Data

Once Claude has your tasks, you can ask:

- "Show me my top 3 priorities"
- "What tasks are in Q1 (urgent and important)?"
- "Generate a full report by quadrant"
- "What tasks are due today?"
- "Give me suggestions for task updates"

## What MCP Tools Are Available

The Todoist MCP server provides these tools to Claude:

- `find-tasks` - Search/fetch tasks
- `find-tasks-by-date` - Get tasks for specific dates
- `add-tasks` - Create new tasks
- `update-tasks` - Modify existing tasks
- `complete-tasks` - Mark tasks as done
- `find-projects` - Get project info
- And many more...

## Example Workflow

1. **Morning routine:**
   ```
   Ask Claude: "Fetch my Todoist tasks and show me today's focus plan"
   ```

2. **Check specific quadrant:**
   ```
   Ask Claude: "Show me all my Q2 (important but not urgent) tasks"
   ```

3. **Get suggestions:**
   ```
   Ask Claude: "Analyze my tasks and suggest which ones need due dates or priority updates"
   ```

4. **Make updates:**
   ```
   Ask Claude: "Update task [task_id] to be due tomorrow with priority 4"
   ```

## Why This Approach?

The MCP tools are available to **Claude** (the AI assistant), not directly to your Python scripts. This is by design - MCP provides a secure way for AI assistants to interact with your services.

Your Python agent does the smart analysis and prioritization, while Claude handles the secure API communication through MCP.

It's the best of both worlds:
- ✅ Your Python code stays simple and focused on analysis
- ✅ Claude handles secure API communication
- ✅ You get real-time analysis of your actual Todoist data
- ✅ You can ask for updates in natural language

## Next Steps

Try it out! Just ask:

**"Fetch my Todoist tasks using MCP and run the AI agent analysis"**

I'll handle the rest!
