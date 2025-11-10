# Quick Start: Todoist AI Agent

## Getting Started

### Prerequisites

1. **Python 3.8+** installed
2. **API Keys** in `.env` file:
   ```bash
   TODOIST_API_TOKEN=your_todoist_token
   OPENAI_API_KEY=your_openai_key
   ```

### Installation

```bash
# Install dependencies
pip install -r requirements.txt

# The new agent system is ready to use!
```

---

## Usage Options

### Option 1: Interactive Chat (Recommended)

Start the new agent-based chat interface:

```bash
python planner_agent.py
```

**Example interactions:**
```
💬 You: help me plan my day
🤖 Assistant: I'll help you create a focused daily plan. Let me assess your current tasks...
[Agent fetches and analyzes tasks, creates personalized plan]

💬 You: I'm overwhelmed by my backlog
🤖 Assistant: I can see why - you have 47 tasks with 12 overdue. Let me help you create a realistic cleanup plan...
[Agent adapts approach for overwhelming situation]

💬 You: clean up my task list
🤖 Assistant: I'll help you clean up. Based on your current workload, I recommend a gentle approach...
[Agent considers context, suggests appropriate batch size]
```

---

### Option 2: Programmatic Usage

Use the planner agent directly:

```python
from planner_agent import PlannerAgent

# Create agent
agent = PlannerAgent(use_mock=False)  # or True for testing

# Handle a request
response = agent.handle_request(
    "What should I focus on today?",
    context={"energy_level": "high", "time_available": "2_hours"}
)

print(response)
```

---

### Option 3: Original CLI (Still Works!)

All original tools still work:

```bash
# Original scripts still available
python chat.py              # Original chat interface
python main.py              # Original CLI
python daily_briefing.py    # Automated briefing
python auto_polish.py       # Automated polishing
```

---

## What Changed

### Before (Old System)
- Command-based: `polish_tasks`, `prioritize_tasks`
- Fixed flows: always fetch → analyze → prioritize
- No context: same behavior for everyone
- Manual: you tell it exactly what to do

### After (New Agent System)
- Goal-based: "I'm overwhelmed", "help me plan"
- Adaptive flows: AI decides best sequence
- Context-aware: adapts to your situation
- Intelligent: figures out how to help

---

## Architecture Overview

```
┌─────────────────────────────────────────────────────────┐
│                     Your Request                         │
│              "I'm overwhelmed today"                     │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│              Planner Agent (AI Brain)                    │
│  • Understands goal                                      │
│  • Selects tools                                        │
│  • Creates plan                                         │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
        ┌────────────┴────────────┐
        │                         │
        ▼                         ▼
┌──────────────┐          ┌──────────────┐
│  Tool Calls  │          │ User Profile │
│              │          │              │
│ • fetch      │          │ • Preferences│
│ • analyze    │◄────────►│ • Patterns   │
│ • polish     │          │ • Feedback   │
│ • update     │          │              │
└──────────────┘          └──────────────┘
        │                         ▲
        │                         │
        └─────────┬───────────────┘
                  │
                  ▼
         ┌──────────────────┐
         │  Executed Tools  │
         │                  │
         │ All original     │
         │ modules wrapped  │
         └──────────────────┘
```

---

## Key Features

### 1. **Goal-Driven Planning**
```python
# Old way
User: "prioritize_tasks report_type=focus max_tasks=5"

# New way
User: "what should I focus on today?"
AI: Analyzes your situation, creates personalized plan
```

### 2. **Adaptive Behavior**
```python
# System learns from you:
# - If you accept polish suggestions → becomes more aggressive
# - If you don't finish tasks → reduces daily target
# - If overwhelmed → smaller batches
# - If energetic → larger challenges
```

### 3. **Context Awareness**
```python
# Same request, different responses based on context:

# Overwhelmed
"I have 50 tasks, 20 overdue, feeling stressed"
→ AI: Gentle approach, small batches, prioritize mental health

# Fresh start
"Monday morning, high energy, ready to tackle big projects"
→ AI: Ambitious plan, deep work focus, strategic thinking
```

### 4. **Natural Interaction**
```python
# You can say:
"I'm overwhelmed"          → AI helps prioritize and simplify
"Plan my week"            → AI creates strategic plan
"Clean up my list"        → AI organizes and clarifies
"Help me focus"           → AI reduces to essentials
"I'm procrastinating"     → AI breaks tasks down
"Prep for meeting"        → AI creates checklist
```

---

## File Structure

### New Files (Agent System)
```
tools_registry.py              # Wraps modules as OpenAI tools
planner_agent.py               # AI planner with tool-calling
user_profile_manager.py        # Learns from user behavior
advanced_planning_examples.py  # Complex scenario examples
pattern_comparison.py          # Old vs new comparison
ARCHITECTURE_EVOLUTION.md      # Full architecture guide
```

### Existing Files (Still Work)
```
agent.py              # Original orchestrator - still used by tools
task_analyzer.py      # Analysis logic - wrapped as tool
task_polisher.py      # Polishing logic - wrapped as tool
smart_scheduler.py    # Scheduling logic - wrapped as tool
chat.py               # Original chat - still available
main.py               # Original CLI - still available
... (all other files)
```

---

## Migration Guide

### If you're an **existing user**:

**Option 1: Use Both (Recommended)**
- Keep using original tools for automation
- Try new agent for complex planning
- Gradually transition as you prefer

**Option 2: Full Migration**
- Use `planner_agent.py` for all interactions
- Original tools still work as fallback
- More powerful, requires OpenAI API

### If you're a **new user**:

**Start with agent-based system:**
```bash
python planner_agent.py
```

**Learn the patterns:**
- State goals, not commands
- Be conversational
- Let AI adapt to you

---

## Examples

### Example 1: Morning Planning
```bash
$ python planner_agent.py

💬 You: good morning, help me plan my day
🤖 Assistant: Good morning! Let me check what you have today...
[Agent fetches tasks, analyzes, creates focus plan]

✅ Here are your top 3 priorities:
1. 📊 Review Q4 budget (due today) - 60 min
2. 📧 Send follow-up emails (due today) - 20 min
3. 📅 Schedule team meeting (due tomorrow) - 15 min

Your day looks manageable! The focus plan balances urgent and important tasks.
```

### Example 2: Overwhelmed
```bash
💬 You: I have 50 tasks and I'm overwhelmed
🤖 Assistant: I can help you through this. I see 50 tasks with 12 overdue.
[Agent adapts approach]

Let's take it step by step:
1. First, let's address the 12 overdue tasks (I'll prioritize 3 critical ones)
2. We'll tackle 5 due-today tasks
3. Defer 20 low-urgency tasks to next week
4. Polish 5 task names for clarity

This gives you 13 actionable items instead of 50. Does this approach help?
```

### Example 3: Strategic Planning
```bash
💬 You: help me plan next week strategically
🤖 Assistant: I'll create a strategic plan for next week.
[Agent analyzes all tasks, categorizes by impact]

📅 Strategic Week Plan:
- Monday: Deep work (focus on Q4 report)
- Tuesday: Meetings & communication
- Wednesday: Partnership outreach
- Thursday: Strategic planning
- Friday: Week review & next week prep

Themes: Week 1 of Q4 sprint, investor relations focus
Balanced: 60% strategic, 25% operational, 15% administrative
```

---

## Customization

### Adjust Profile
```python
from user_profile_manager import UserProfileManager

manager = UserProfileManager()
manager.update_preferences({
    "work_hours": "10:00-19:00",
    "max_deep_tasks_per_day": 2,
    "polish_aggressiveness": "conservative"
})
```

### Add Custom Tools
```python
# In tools_registry.py
def _custom_tool(self) -> Dict[str, Any]:
    return {
        "type": "function",
        "function": {
            "name": "my_custom_tool",
            "description": "Does something custom",
            "parameters": {...}
        }
    }

def _execute_my_custom_tool(self, **kwargs) -> Dict[str, Any]:
    # Your logic here
    return {"status": "success", "data": "..."}
```

---

## Best Practices

### 1. Be Conversational
❌ `polish_tasks scope=low_quality min_quality=50`
✅ `my tasks feel messy, can you clean them up?`

### 2. State Goals, Not Commands
❌ `run_analysis report_type=full`
✅ `I need to see the big picture of all my tasks`

### 3. Provide Context
❌ `help me`
✅ `I'm feeling overwhelmed, help me prioritize`

### 4. Let It Adapt
- The agent learns from your feedback
- Accept/reject suggestions
- It will adjust to your style

### 5. Use Natural Language
- Speak as you would to a human assistant
- The AI understands context and nuance

---

## Troubleshooting

### API Keys Not Working
```bash
# Check your .env file
cat .env

# Should have:
TODOIST_API_TOKEN=...
OPENAI_API_KEY=...
```

### Using Mock Data
```bash
# Test without real API access
python planner_agent.py --mock
python advanced_planning_examples.py --mock
```

### Reset Conversation
```
💬 You: reset
# Clears conversation history and context
```

### View Session Status
```
💬 You: status
# Shows session info and recent activity
```

---

## Learn More

- **Full Architecture**: See `ARCHITECTURE_EVOLUTION.md`
- **Pattern Comparison**: Run `python pattern_comparison.py`
- **Advanced Scenarios**: Run `python advanced_planning_examples.py --mock`
- **Original System**: See `README.md`

---

## Summary

The new agent system transforms your Todoist assistant from a **tool** into a **collaborative partner**. Instead of learning commands, you can simply state your goals and let the AI figure out how to help.

**Start with:**
```bash
python planner_agent.py
```

**Then just talk naturally:**
- "Help me plan my day"
- "I'm overwhelmed"
- "Clean up my backlog"
- "What should I focus on?"

The agent will adapt to you, learn from your preferences, and provide increasingly personalized assistance! 🎯
