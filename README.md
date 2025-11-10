# Todoist AI Agent

<div align="center">

**Intelligent task management powered by AI**

An adaptive agent that understands your goals, learns your preferences, and helps you manage tasks intelligently through natural conversation.

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![OpenAI](https://img.shields.io/badge/OpenAI-GPT--4o--mini-green.svg)](https://openai.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

</div>

---

## ✨ What It Does

Transform your Todoist from a simple task list into an **intelligent assistant** that:

- 🗣️ **Converses naturally** - Just say what you want to achieve
- 🧠 **Understands context** - Adapts to your situation and preferences
- 📊 **Analyzes intelligently** - Prioritizes using Eisenhower Matrix + AI
- ✨ **Polishes tasks** - AI improves vague names and descriptions
- 📅 **Plans strategically** - Creates realistic, personalized plans
- 🤖 **Learns & adapts** - Gets better based on your behavior
- 📧 **Daily briefings** - Context-aware morning digests

**Example:** Say *"I'm overwhelmed"* → Agent creates a calming, realistic plan tailored to your situation.

---

## 🚀 Quick Start

### 1. Install Dependencies
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment:
# On macOS/Linux:
source venv/bin/activate

# On Windows:
# venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure API Keys
```bash
# Copy the example
cp .env.example .env

# Edit .env with your keys:
# - OPENAI_API_KEY: https://platform.openai.com/api-keys
# - TODOIST_API_TOKEN: https://todoist.com/app/settings/integrations
```

### 3. Start the Agent
```bash
# Activate virtual environment (if not already activated)
# On macOS/Linux:
source venv/bin/activate

# On Windows:
# venv\Scripts\activate

# Run the agent
python planner_agent.py
```

**That's it!** Just tell the agent what you need:
- *"What should I focus on today?"*
- *"Help me plan my day"*
- *"I'm overwhelmed, what should I do?"*
- *"Clean up my task list"*

---

## 🎯 One Intelligent System

### 🤖 AI Agent

**Natural, intelligent, adaptive**

```bash
python planner_agent.py
```

The agent has a built-in chat interface and understands natural language. It can:
- Show today's tasks when you say *"What should I focus on today?"*
- Plan your day when you say *"Help me plan my day"*
- Clean up tasks when you say *"Polish my task list"*
- Analyze and prioritize using AI
- Learn your preferences over time

**Everything you need in one program!**

---

## 📁 Project Structure

```
todoist-ai-agent/
│
├── 🤖 Main Program
│   └── planner_agent.py           # Single AI agent with chat interface
│
├── 🔧 Core System
│   ├── tools_registry.py          # Tools the agent can use
│   ├── user_profile_manager.py    # Learns from user behavior
│   ├── agent.py                   # Task analysis engine
│   ├── todoist_client.py          # Todoist API integration
│   └── intent_router.py           # Intent classification
│
├── 📋 Task Intelligence Modules
│   ├── task_analyzer.py          # Eisenhower Matrix analysis
│   ├── task_polisher.py          # AI task enhancement
│   ├── smart_scheduler.py        # Due date inference
│   ├── prioritizer.py            # Focus plan generation
│   └── task_updater.py           # Update tasks
│
├── 📧 Daily Automation
│   ├── daily_agent_briefing.py   # AI-driven daily briefing (for cron)
│   ├── daily_briefing.py         # Original briefing (legacy)
│   └── auto_polish.py            # Automated polishing (optional)
│
├── 🛠️ Utilities
│   └── list_tasks.py             # Quick task listing (optional)
│
├── 📚 Documentation
│   ├── docs/user-guide/          # User guides and tutorials
│   ├── docs/architecture/        # Technical documentation
│   └── docs/features/            # Feature deep-dives
│
└── 🎓 Examples
    ├── advanced_planning_examples.py  # Complex scenarios
    ├── pattern_comparison.py          # Patterns showcase
    └── ...                            # More examples
```

---

## 🎮 How to Use

### Start the AI Agent
```bash
# Activate virtual environment (macOS/Linux)
source venv/bin/activate

# Or on Windows:
# venv\Scripts\activate

# Run the agent
python planner_agent.py
```

Then just talk naturally! The agent understands:

**📅 Daily Planning:**
- "What should I focus on today?" (replaces today.py)
- "Help me plan my afternoon"
- "Show me my priorities for this week"

**🧹 Task Cleanup:**
- "Clean up my task list"
- "Polish my task names"
- "Add due dates to important tasks"

**📊 Analysis:**
- "Analyze my tasks using Eisenhower Matrix"
- "Which tasks need improvement?"
- "Show me overdue tasks"

**💡 Everything is conversational - no commands to remember!**

### Optional Utilities
```bash
# Quick task listing (standalone)
python list_tasks.py

# Automated daily briefing (via cron) - AI-powered
./setup_agent_cron.sh

# Legacy cron setup (non-agent based) - deprecated
# ./setup_cron.sh
```

---

## 📖 Documentation

**Comprehensive guides in the `docs/` directory:**

### For Users
- 📘 **[Quick Start Guide](docs/user-guide/quick-start.md)** - Get up and running
- 💬 **[Chat Usage](docs/user-guide/chat-usage.md)** - Conversational interface guide
- 📝 **[Quick Reference](docs/user-guide/quick-reference.md)** - Command reference
- 🔧 **[Standalone Usage](docs/user-guide/standalone-usage.md)** - Script usage

### For Developers
- 🏗️ **[Architecture Evolution](docs/architecture/evolution.md)** - Logic app → Agent transformation
- 📊 **[Project Structure](docs/architecture/structure.md)** - System design
- 📋 **[Implementation Summary](docs/architecture/summary.md)** - Complete overview

### Feature Deep Dives
- 📧 **[Briefing Evolution](docs/features/briefing-evolution.md)** - Static → AI briefings
- ✨ **[Polishing Features](docs/features/polish-features.md)** - Task improvement
- 🔌 **[MCP Integration](docs/features/mcp-integration.md)** - Model Context Protocol

---

## 🧪 Try Examples

### See Agent Capabilities
```bash
python examples/advanced_planning_examples.py --mock
```

### Compare Old vs New Patterns
```bash
python examples/pattern_comparison.py
```

### Test Polishing
```bash
python examples/test_polish_standalone.py
```

---

## 🏗️ Architecture Highlights

### The Evolution: Logic App → Agent

**Old System (Logic App):**
- Fixed pipelines (fetch → analyze → prioritize)
- Command-based ("polish tasks")
- Same behavior for everyone

**New System (Agent):**
- AI decides flow ("I'm overwhelmed")
- Goal-driven conversation
- Adapts to you personally

### Key Components

1. **PlannerAgent** - AI brain that decides what to do
2. **Tools Registry** - 13+ tools the agent can use
3. **User Profile** - Learns your preferences
4. **Original Modules** - All wrapped as tools

**Result:** A true AI agent that understands goals, not just commands!

---

## ⚙️ Configuration

### Environment Variables

```bash
# Required
OPENAI_API_KEY=sk-...
TODOIST_API_TOKEN=...

# Optional
OPENAI_MODEL=gpt-4o-mini
BRIEFING_EMAIL=your@email.com
BRIEFING_SMTP_HOST=smtp.gmail.com
BRIEFING_SMTP_PORT=587
BRIEFING_SMTP_USER=your@email.com
BRIEFING_SMTP_PASS=app_password
```

### User Profile

The agent learns from your behavior and stores preferences in:
- `~/.todoist_agent_profile.json` - Your preferences
- `~/.todoist_agent_interactions.json` - Interaction history
- `~/.todoist_agent_completions.json` - Task completion patterns

---

## 🔧 Troubleshooting

**Agent doesn't start?**
```bash
# Check your .env file
cat .env

# Verify API keys work
python -c "import openai; openai.OpenAI()"
```

**Using mock data for testing:**
```bash
python planner_agent.py --mock
python daily_agent_briefing.py --mock
```

**Reset conversation:**
```
💬 In chat: reset
```

**View session status:**
```
💬 In chat: status
```

---

## 📊 System Requirements

- **Python 3.8+**
- **OpenAI API key** (for AI features)
- **Todoist API token** (for task access)
- 4GB RAM recommended
- Internet connection (for API calls)

---

## 🎯 Common Use Cases

| Goal | How to Use |
|------|------------|
| **Daily planning** | `python planner_agent.py` → "What should I focus on today?" |
| **Task cleanup** | `python planner_agent.py` → "Clean up my list" |
| **Weekly review** | `python planner_agent.py` → "Plan my week strategically" |
| **Overwhelmed** | `python planner_agent.py` → "I'm overwhelmed" |
| **Quick task list** | `python planner_agent.py` → "Show me all my tasks" |
| **Morning briefing** | Cron: `python daily_agent_briefing.py` |
| **Task analysis** | `python planner_agent.py` → "Analyze my tasks" |

**Everything through one program - the AI agent!**

---

## 🤝 Contributing

This is a personal AI assistant project. Feel free to:
- Fork and adapt to your needs
- Submit issues for bugs
- Suggest improvements

---

## 📄 License

MIT License - see LICENSE file for details

---

## 🙏 Acknowledgments

- **OpenAI** - GPT-4o-mini for intelligence
- **Todoist** - Task management platform
- **Python** - Amazing programming language

---

## 🚀 Next Steps

1. **Try the agent:** `python planner_agent.py`
2. **Set up daily briefings:** `./setup_agent_cron.sh`
3. **Read the guides:** `docs/user-guide/`
4. **Explore examples:** `examples/`

**Happy task managing! 🎉**

---

<div align="center">

**[Website](https://github.com/puglord93/todoist-ai-agent)** •
**[Documentation](docs/)** •
**[Examples](examples/)**

</div>
