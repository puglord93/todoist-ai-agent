# Todoist AI Chat Assistant - Usage Guide

Your Todoist AI agent now has a **conversational interface**! Chat with your tasks using natural language.

## Quick Start

```bash
cd /Users/jj/Code/todoist-ai-agent
venv/bin/python3 chat.py
```

You'll see:
```
🎯 TODOIST AI ASSISTANT - Conversational Interface
======================================================================

I can help you manage your Todoist tasks using natural language!

💬 You: _
```

## How It Works

The chat agent uses **OpenAI GPT-4o-mini** to understand your natural language requests and route them to the appropriate functions. It maintains conversation history, so you can have natural back-and-forth conversations about your tasks.

## Example Conversations

### View Today's Tasks
```
💬 You: show me today's tasks

🤖 Assistant: Here are your tasks for 2025-11-02:

======================================================================

⚠️  OVERDUE (1)
----------------------------------------------------------------------
🔴 Send follow-up email to Prof Sum (commitment check)

📌 DUE TODAY (2)
----------------------------------------------------------------------
🔴 Respond to Leonard (CMG Tech) - micro-MIM project status
🔴 Follow up with DYT on WhatsApp regarding pending response

======================================================================
Total active tasks: 7
```

### Prioritize Tasks
```
💬 You: prioritize my tasks

🤖 Assistant: Analyzing and prioritizing your tasks...

📋 DAILY FOCUS PLAN - 2025-11-02
======================================================================

🎯 TODAY'S FOCUS TASKS (Top Priority):
----------------------------------------------------------------------

1. Send follow-up email to Prof Sum (commitment check)
   Priority Score: 95/100
   Quadrant: Q1: DO FIRST - Urgent & Important
   Due: ⚠️ OVERDUE
   💡 Address this immediately - it's overdue and urgent

2. Respond to Leonard (CMG Tech) - micro-MIM project status
   Priority Score: 92/100
   Quadrant: Q1: DO FIRST - Urgent & Important
   Due: 📅 TODAY
```

### Check Task Quality
```
💬 You: which tasks need polishing?

🤖 Assistant: Analyzing task quality...

Found 3 tasks below 50% quality:

1. call dentist
   Quality: 35%
   Issues: No clear action verb, task name too vague, missing description

2. meeting tomorrow
   Quality: 40%
   Issues: No due date set, missing description

💡 Tip: Use 'venv/bin/python3 interactive_polish.py' for interactive polishing
```

### Natural Language Variations
```
💬 You: what should I focus on today?
🤖 Assistant: [Shows prioritized focus plan]

💬 You: show me overdue stuff
🤖 Assistant: [Shows overdue tasks]

💬 You: help me add due dates
🤖 Assistant: [Shows tasks without due dates and suggests next steps]
```

## Available Commands

### 📋 Task Viewing
| Command | Description |
|---------|-------------|
| `show tasks` / `show` | Show today's tasks |
| `show all tasks` | Show all tasks |
| `show overdue` | Show overdue tasks only |
| `show upcoming` | Show upcoming tasks |
| `today` | Shortcut for today's tasks |

### 🎯 Task Management
| Command | Description |
|---------|-------------|
| `prioritize` / `p` | Prioritize tasks using Eisenhower matrix |
| `categorize` | Show task distribution by quadrants |
| `categorize Q1` | Show tasks in specific quadrant (Q1-Q4) |

### ✨ Task Improvement
| Command | Description |
|---------|-------------|
| `polish` | Check task quality and identify issues |
| `schedule` | Find tasks without due dates |

### 🔧 Utilities
| Command | Description |
|---------|-------------|
| `help` | Show available commands |
| `clear` / `reset` | Clear conversation history |
| `quit` / `exit` / `q` | Exit the chat |

## Conversation History

The agent maintains your last 10 interactions, so you can have natural conversations:

```
💬 You: show urgent tasks
🤖 Assistant: [Shows Q1 urgent tasks]

💬 You: polish those
🤖 Assistant: [Analyzes the urgent tasks for quality]

💬 You: now help me prioritize them
🤖 Assistant: [Shows prioritization of urgent tasks]
```

## Shortcuts

For quick access, use these single-word shortcuts:
- `show` → Show today's tasks
- `p` → Prioritize tasks
- `polish` → Check task quality
- `schedule` → Find tasks needing due dates
- `categorize` → Categorize by quadrants
- `help` → Show help

## Advanced Usage

### Quadrant Categories (Eisenhower Matrix)

The agent uses the Eisenhower Matrix to categorize tasks:

- **Q1 (Do First)** 🔥 - Urgent & Important
- **Q2 (Schedule)** 📆 - Important, Not Urgent
- **Q3 (Delegate)** 👥 - Urgent, Not Important
- **Q4 (Consider)** 🗑️ - Neither Urgent nor Important

Request specific quadrants:
```
💬 You: show me Q1 tasks
💬 You: categorize by quadrants
```

### Full Interactive Workflows

For more complex operations, the chat will guide you to dedicated scripts:

**Polish Tasks Interactively:**
```bash
venv/bin/python3 interactive_polish.py
```

**Schedule Tasks Interactively:**
```bash
venv/bin/python3 interactive_polish.py --mode schedule
```

**Full Prioritization Report:**
```bash
venv/bin/python3 main.py --full
```

## Natural Language Examples

The AI understands various phrasings:

**Viewing Tasks:**
- "show me today's tasks"
- "what's due today?"
- "what do I need to do?"
- "show overdue items"

**Prioritization:**
- "help me prioritize"
- "what should I focus on?"
- "which tasks are most important?"

**Task Quality:**
- "which tasks need work?"
- "check my task quality"
- "polish my tasks"

**Scheduling:**
- "what tasks don't have due dates?"
- "help me add due dates"
- "schedule my tasks"

## Tips

1. **Be natural** - The AI understands context, you don't need exact commands
2. **Use pronouns** - After showing tasks, you can say "polish those" or "prioritize them"
3. **Ask questions** - Try "what should I work on?" or "which tasks are urgent?"
4. **Use shortcuts** - For speed, just type `show`, `p`, or `polish`
5. **Clear history** - Type `clear` if you want to start fresh

## Troubleshooting

**"Error initializing"**
- Check your `.env` file has `OPENAI_API_KEY` and `TODOIST_API_TOKEN`
- Make sure you're in the virtual environment

**"I'm not sure what you'd like me to do"**
- Type `help` to see available commands
- Try using more explicit commands like "show tasks" or "prioritize"

**OpenAI API errors**
- Check your API key is valid
- Ensure you have API credits available
- The agent uses GPT-4o-mini (very low cost: ~$0.001 per request)

## Cost

Using GPT-4o-mini for intent detection:
- ~50 tokens per request
- **Cost: ~$0.0001 per chat message** (extremely affordable!)
- Typical session: ~$0.01 for 100 interactions

## Integration with Other Tools

The chat interface works alongside your existing scripts:

```bash
# Quick daily check
venv/bin/python3 today.py

# Interactive chat
venv/bin/python3 chat.py

# Full workflow
venv/bin/python3 interactive_polish.py

# Command-line mode
venv/bin/python3 main.py --full
```

Choose the tool that fits your workflow!

## Next Steps

Try these common workflows:

1. **Morning Routine:**
   ```
   venv/bin/python3 chat.py
   > show
   > prioritize
   ```

2. **Task Cleanup:**
   ```
   venv/bin/python3 chat.py
   > polish
   > schedule
   ```

3. **Focus Session:**
   ```
   venv/bin/python3 chat.py
   > what should I focus on today?
   > show me Q1 tasks
   ```

Enjoy your conversational Todoist assistant! 🎉
