# Daily Briefing Evolution: Static → Agent-Driven

## Overview

Your daily briefing has evolved from a static, rule-based report to an **intelligent, context-aware assistant** that adapts to your workload, day of week, and current situation.

---

## Comparison: Old vs New

### Old System (Static)

**File:** `daily_briefing.py` + `setup_cron.sh`

**Characteristics:**
- Fixed template with if-else rules
- Same structure every day
- Static tone and content
- Limited context awareness
- Lists tasks without intelligent analysis

**Example Output:**
```
DAILY BRIEFING - Monday, November 10, 2025

OVERDUE TASKS (6):
- Task 1
- Task 2
...

DUE TODAY (3):
- Task A
- Task B
...

PRIORITIES:
1. Review report
2. Call client
...

QUALITY SUMMARY:
Average quality: 72%
Tasks needing attention: 3
```

**Cron Command:**
```bash
0 8 * * * python daily_briefing.py
```

---

### New System (Agent-Driven)

**File:** `daily_agent_briefing.py` + `setup_agent_cron.sh`

**Characteristics:**
- AI decides what to include
- Context-aware based on workload
- Adaptive tone (Monday energy, Friday wrap-up, etc.)
- Intelligent insights and patterns
- Motivational and personalized

**Example Output:**
```
🗓️ Good morning, JJ! It's Monday - time to kick off an awesome week.

I've analyzed your workload and here's what I see:

🎯 Your Day at a Glance
You have 3 core priorities today, which is perfect for a focused Monday.
The good news: only 1 overdue item (last week's report review).

📊 Workload Status
• Overdue: 1 item (easy to clear)
• Due today: 3 items (all manageable)
• This week: 8 items (healthy pipeline)

💡 Strategic Insight
Since it's Monday and your energy is high, I recommend tackling the
quarterly report first (deep work in the morning), then moving to
communication tasks in the afternoon.

🔥 Your Top 3 for Today
1. Complete Q4 budget review (60 min) - Strategic, high-impact
2. Send follow-up to TechCorp (15 min) - Quick win
3. Schedule team sync (10 min) - Sets up the week

✨ Weekend Prep
With 5 tasks deferred from last week, consider batching them
on Wednesday afternoon for a productive mid-week push.

You've got this! 🚀
```

**Cron Command:**
```bash
0 8 * * * cd todoist-ai-agent && python daily_agent_briefing.py
```

---

## Key Differences

| Aspect | Old (Static) | New (Agent-Driven) |
|--------|-------------|-------------------|
| **Content** | Lists tasks | Analyzes and provides insights |
| **Tone** | Neutral, robotic | Motivational, conversational |
| **Context** | None | Adapts to day of week, workload |
| **Intelligence** | Rules-based | AI-powered reasoning |
| **Personalization** | None | Adapts to your patterns |
| **Insights** | Task counts | Patterns, trends, recommendations |
| **Actionability** | Lists | Prioritized with reasoning |
| **Failover** | None | Falls back to original system |

---

## How It Works

### Old Flow (Cron → Script → Output)

```
Cron Trigger (8 AM)
        ↓
daily_briefing.py
        ↓
Fetch tasks from Todoist
        ↓
Categorize (overdue, today, upcoming)
        ↓
Apply fixed formatting rules
        ↓
Send email / save to file
```

### New Flow (Cron → Agent → Intelligence)

```
Cron Trigger (8 AM)
        ↓
daily_agent_briefing.py
        ↓
PlannerAgent receives goal:
"Generate JJ's morning briefing with context-aware insights"
        ↓
Agent decides steps:
• Fetch tasks
• Analyze workload
• Get user profile
• Check day of week context
        ↓
AI reasons about content:
• "It's Monday - motivational tone"
• "Only 3 tasks - encourage to add more"
• "1 overdue - recommend clearing it first"
        ↓
Generate intelligent briefing
        ↓
Send email / save to file
```

---

## Setup and Usage

### Option 1: Keep Old System
```bash
./setup_cron.sh
```
- Select "Daily Briefing"
- Cron runs: `python daily_briefing.py`
- Static, predictable output

### Option 2: Use New Agent System
```bash
./setup_agent_cron.sh
```
- Interactive setup for email
- Cron runs: `python daily_agent_briefing.py`
- Intelligent, adaptive output

### Option 3: Both (Recommended)
```bash
# Set up agent-driven as primary
./setup_agent_cron.sh

# Keep original as backup
./setup_cron.sh
```
- Morning: Agent-driven intelligent briefing
- If agent fails: Fallback to original
- Best of both worlds

---

## Testing

### Test Agent-Driven Briefing
```bash
# With mock data
python daily_agent_briefing.py --mock

# With real data
python daily_agent_briefing.py

# With email
python daily_agent_briefing.py --email
```

### Test Old Briefing
```bash
python daily_briefing.py
```

---

## Configuration

### Email Settings (`.env`)

```bash
# Agent-driven briefing
BRIEFING_EMAIL=your@email.com
BRIEFING_SMTP_HOST=smtp.gmail.com
BRIEFING_SMTP_PORT=587
BRIEFING_SMTP_USER=your@email.com
BRIEFING_SMTP_PASS=your_app_password
```

### Output Location

```bash
# File path (default)
BRIEFING_OUTPUT_PATH=~/todoist_briefing.txt
```

---

## Features

### Intelligent Context Awareness

**Monday Morning:**
- Motivational, energetic tone
- Strategic planning focus
- "Week kickoff" language

**Friday Afternoon:**
- Wrap-up focused
- Review progress
- Prep for next week

**Heavy Workload:**
- Encouraging tone
- Breaking down tasks
- Prioritization help

**Light Workload:**
- Suggest adding goals
- Time for deep work
- Strategic thinking

### Fallback System

If the agent fails:
1. Log the error
2. Switch to original `daily_briefing.py`
3. Send via email/file as configured
4. Still get your briefing!

### Logging

Check `~/todoist_briefing_cron.log` for:
- Execution status
- Errors
- Performance metrics

---

## Example Use Cases

### Scenario 1: Monday Fresh Start
**User Input:** (automatic at 8 AM)

**Agent Response:**
```
🗓️ Good morning, JJ! It's Monday - fresh start, new possibilities!

I've reviewed your tasks and here's what I see:
• 12 total tasks (manageable workload)
• 0 overdue (great job staying on top!)
• 2 high-priority strategic items

💡 Since it's Monday and your energy is high, I recommend:
1. Tackle the partnership proposal (deep work, morning energy)
2. Clear quick wins (emails, follow-ups) in afternoon

This sets you up for a focused, productive week! 🚀
```

### Scenario 2: Overwhelming Wednesday
**User Input:** (automatic at 8 AM)

**Agent Response:**
```
🗓️ Good morning, JJ. I see you're carrying a heavier load today.

Your situation:
• 23 tasks (above your typical 15-18)
• 6 overdue items
• 4 due today

🧘 Let's take this one step at a time:

TOP PRIORITIES (do these first):
1. Address 6 overdue items (I'll flag the 2 most critical)
2. Tackle 4 due-today tasks
3. Push 8 lower-priority items to tomorrow

💪 You've handled heavy weeks before. Focus on the essentials,
and I'll help you create a realistic plan. You got this!
```

### Scenario 3: Friday Wind-Down
**User Input:** (automatic at 8 AM)

**Agent Response:**
```
🗓️ Happy Friday, JJ! 🎉

Week wrap-up:
• You've completed 18 tasks this week (85% of planned)
• Only 3 items carried over
• Great productivity!

📋 Today's focus:
1. Wrap up the 3 carried-over items
2. Plan next week's priorities
3. Celebrate your wins!

Have a great weekend! 🌟
```

---

## Benefits

### For You
- ✅ More engaging to read
- ✅ Actually helps you plan your day
- ✅ Adapts to your situation
- ✅ Motivational when you need it
- ✅ Smart insights, not just lists

### For Productivity
- ✅ Better task prioritization
- ✅ Context-aware planning
- ✅ Reduced decision fatigue
- ✅ Improved work-life balance
- ✅ Strategic thinking prompts

---

## Migration Path

### Step 1: Test the New System
```bash
python daily_agent_briefing.py --mock
```

### Step 2: Configure Email
```bash
./setup_agent_cron.sh
```

### Step 3: Monitor for a Week
```bash
tail -f ~/todoist_briefing_cron.log
```

### Step 4: Keep or Switch
- Like the new system? Remove old cron: `crontab -r` + re-run setup
- Prefer the old system? Just ignore the new one
- Use both? Keep both cron jobs (new primary, old fallback)

---

## Files Reference

| File | Purpose | Lines |
|------|---------|-------|
| `daily_briefing.py` | Original static briefing | 253 |
| `daily_agent_briefing.py` | New agent-driven briefing | 230 |
| `setup_cron.sh` | Setup old system | 253 |
| `setup_agent_cron.sh` | Setup new system | 200 |
| `planner_agent.py` | Core agent engine | 420 |

---

## Summary

The evolution from static to agent-driven briefings transforms your morning digest from a **task list** into a **thinking assistant** that:

1. Understands your context
2. Provides intelligent insights
3. Adapts to your situation
4. Motivates and guides you
5. Falls back gracefully if needed

**Try it:** `./setup_agent_cron.sh` 🚀
