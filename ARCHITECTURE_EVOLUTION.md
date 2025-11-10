# Architecture Evolution: From Logic App to Agent

## Overview

This document describes the transformation of the Todoist AI Agent from a **logic app** pattern to a **tool-using agent** pattern.

---

## Before: Logic App Pattern

### Characteristics

**Fixed Pipeline:**
```python
# agent.py - Hardcoded orchestration
def run_analysis(self):
    # Step 1: Fetch
    tasks = self.client.fetch_tasks()

    # Step 2: Normalize
    normalized = [normalize(task) for task in tasks]

    # Step 3: Analyze
    analyzed = [self.analyzer.analyze(t) for t in normalized]

    # Step 4: Prioritize
    focus = self.prioritizer.create_plan(analyzed)

    return {"tasks": tasks, "analyzed": analyzed, "focus": focus}
```

**Deterministic Scoring:**
```python
# task_analyzer.py - Fixed weights
CATEGORY_WEIGHTS = {
    "work": 1.2,
    "health": 1.3,
    "family": 1.3,
}

# Always applies same weights, never adapts
```

**User Tells System What To Do:**
```
User: "prioritize my tasks"
System: (hardcoded flow) → "Here are your priorities"

User: "polish low quality tasks"
System: (fixed rules) → "Polishing tasks with quality < 50"
```

### Problems

- ✗ Flow decided by code, not by AI based on goal
- ✗ Fixed weights don't adapt to user behavior
- ✗ "What to do" logic is in code, not AI
- ✗ Hard to handle complex, multi-step scenarios
- ✗ No learning from user feedback

---

## After: Tool-Using Agent Pattern

### Characteristics

**AI Decides Flow:**
```python
# planner_agent.py - AI plans the sequence
def handle_request(user_goal):
    messages = [
        {"role": "system", "prompt": system_prompt},
        {"role": "user", "content": user_goal}
    ]

    # AI decides which tools to call and in what order
    response = openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        tools=available_tools,  # Tools the AI can use
        tool_choice="auto"      # AI chooses which to use
    )

    # Execute tool calls
    for tool_call in response.tool_calls:
        result = execute_tool(tool_call.name, tool_call.arguments)

    # AI continues until it has a plan
    return final_response
```

**AI Judges with Hints:**
```python
# Old: Deterministic scoring
priority_score = (urgency * 0.6 + importance * 0.4) * 10

# New: AI makes final decision with numeric hints
System: "You are prioritizing JJ's tasks. Heuristic scores provided below.
         You may override them based on context and judgment."

Tasks with scores:
- "Quarterly report" (urgency: 8, importance: 9) → AI judges: "Due tomorrow, this is Q1 priority"
- "Learn new framework" (urgency: 2, importance: 7) → AI judges: "Important for long-term, but not this week"

AI returns: final_priority (1-100), reason, recommended_action
```

**Goal-Driven, Not Command-Driven:**
```
User: "I'm overwhelmed by my backlog"
AI:   1. Let me assess your current situation
     2. Fetching your tasks...

     2. Analyzing urgency and importance...

     3. I see 47 tasks, 12 overdue, 15 due this week.
        This is indeed overwhelming.

     4. Creating a realistic plan:
        - Focus on overdue and due-today (12 tasks)
        - Defer 8 low-urgency, low-importance tasks
        - Schedule 5 important tasks across next 2 weeks
        - Polish task names for clarity

     5. Do you want me to apply these changes?
```

### Benefits

- ✓ AI decides flow based on goal
- ✓ Adapts to user context and preferences
- ✓ Handles complex, multi-step scenarios naturally
- ✓ Learns from user feedback
- ✓ More natural, conversational interaction
- ✓ Extensible (add tools without changing core logic)

---

## Migration Path

### Phase 1: Wrap Tools ✅
**Status:** Complete

Converted all modules to OpenAI-compatible tools:

```python
class ToolsRegistry:
    def get_tools(self):
        return [
            {
                "type": "function",
                "function": {
                    "name": "fetch_tasks",
                    "description": "Fetch tasks from Todoist",
                    "parameters": {...}
                }
            },
            # ... 12 more tools
        ]
```

**What changed:** Modules are now callable via AI

**What stayed the same:** All original logic preserved

---

### Phase 2: Planner Agent ✅
**Status:** Complete

Created planner that uses tool-calling:

```python
class PlannerAgent:
    def handle_request(self, user_goal):
        # Build system prompt with context
        system_prompt = self._build_system_prompt()

        # Send to OpenAI with tools
        response = self.client.chat.completions.create(
            tools=self.tools,
            tool_choice="auto"
        )

        # Execute tool calls
        # Continue until AI returns natural language response
```

**What changed:** New agent orchestrates workflows

**What stayed the same:** Original modules still work independently

---

### Phase 3: Replace Hardcoded Flows ✅
**Status:** Complete

**Before (hardcoded):**
```python
# auto_polish.py - Fixed rules
if quality < AUTO_POLISH_QUALITY_THRESHOLD:
    if tasks_processed < AUTO_POLISH_MAX_TASKS:
        polish(task)
```

**After (AI-driven):**
```python
# AI decides based on context
AI: "Looking at today: 5 high-energy tasks scheduled, backlog of 20.
     Recommend polishing 3 tasks max to avoid overload.
     Focus on high-impact tasks without due dates."

# Code still enforces safety
if ai_suggested_count > 5:  # Safety limit
    suggested_count = 5
```

**What changed:** AI determines scope and approach

**What stayed the same:** Safety limits and validation

---

### Phase 4: User Preference Memory ✅
**Status:** Complete

Profile learns from behavior:

```python
class UserProfileManager:
    def record_interaction(self, action, task_count, success):
        # Track what works for this user

    def _adapt_from_interactions(self):
        # Adjust preferences based on patterns
        if polish_acceptance_rate > 0.8:
            self.preferences.polish_aggressiveness = "aggressive"
```

**What changed:** System adapts to user patterns

**What stayed the same:** All original features available

---

## Key Differences: Old vs New

| Aspect | Old (Logic App) | New (Agent) |
|--------|----------------|-------------|
| **Flow Control** | Hardcoded in Python | AI decides sequence |
| **Task Analysis** | Deterministic formula | AI judgment + numeric hints |
| **Scheduling** | Regex → AI → Heuristics | AI-first with validation |
| **User Interaction** | Command-based | Goal-based, conversational |
| **Adaptation** | Fixed weights | Learns from behavior |
| **Complexity** | Simple commands | Handles multi-step scenarios |
| **Extensibility** | Modify code to add flows | Add new tools |
| **Context Awareness** | None | Maintains session memory |
| **Personalization** | None | Builds user profile |

---

## Example Transformations

### Example 1: Daily Planning

**Old Pattern:**
```python
# User must specify exact command
User: "prioritize my tasks"
System: (runs fixed pipeline)
Output: Focus plan with top 5
```

**New Pattern:**
```python
# User states goal
User: "I'm overwhelmed, help me plan today"
System: AI thinks: "User is overwhelmed. Need to:
  1. Fetch current tasks
  2. Analyze situation
  3. Create realistic, calming plan
  4. Suggest batch processing for low-priority tasks"
Output: Personalized plan with context and options
```

### Example 2: Task Cleanup

**Old Pattern:**
```python
# User must know the tool
User: "polish tasks with quality < 50"
System: Polishes exactly those tasks
```

**New Pattern:**
```python
# User states outcome wanted
User: "My task list feels messy, help me clean it up"
System: AI thinks: "User wants cleanup. Should:
  1. Show quality report
  2. Polish vague task names
  3. Add due dates to important tasks
  4. Consolidate similar tasks
  5. Present changes for approval"
Output: Comprehensive cleanup with preview
```

### Example 3: Weekly Planning

**Old Pattern:**
```python
# No clear way to do this - would need new script
# User needs to run multiple commands manually
```

**New Pattern:**
```python
# User states goal
User: "Plan next week strategically"
System: AI thinks: "Strategic weekly planning requires:
  1. Fetch all tasks
  2. Analyze by impact and effort
  3. Identify themes/projects
  4. Create time blocks
  5. Balance work/personal
  6. Consider energy patterns"
Output: Complete weekly plan with rationale
```

---

## Using the New Architecture

### Quick Start

```python
from planner_agent import ChatInterface

# Start the agent
chat = ChatInterface(use_mock=False)
chat.start()

# Or use programmatically
from planner_agent import PlannerAgent

agent = PlannerAgent()
response = agent.handle_request("What should I focus on today?")
print(response)
```

### Advanced Usage

```python
# Add custom context
agent = PlannerAgent()
response = agent.handle_request(
    user_goal="Plan my afternoon",
    context={
        "energy_level": "low",
        "time_available": "2 hours",
        "interruption_risk": "high"
    }
)
```

### Accessing User Profile

```python
from user_profile_manager import UserProfileManager

manager = UserProfileManager()
prefs = manager.get_preferences()

# See what the system learned
insights = manager.get_insights()
print(insights)
```

---

## When to Use Each Pattern

### Use the **Old Pattern** (Direct Module Calls) When:
- You need deterministic, repeatable results
- Writing scripts or automation
- Testing or debugging specific features
- Performance is critical (no AI overhead)

**Examples:**
```python
# Automated cron jobs
agent = TodoistAIAgent()
agent.polish_tasks(min_quality=30)

# Testing
analyzer = TaskAnalyzer()
score = analyzer.analyze_task(task)
```

### Use the **New Pattern** (Planner Agent) When:
- User has a goal, not a specific command
- Need adaptive, context-aware responses
- Handling complex, multi-step scenarios
- Want personalized experience
- Exploring options, not just executing

**Examples:**
```python
# Goal-driven planning
agent = PlannerAgent()
response = agent.handle_request("I'm overwhelmed, help me")

# Conversational interaction
chat = ChatInterface()
chat.start()
```

---

## Benefits Summary

### For Users
- **More natural interaction**: Say what you want, not how to do it
- **Adaptive**: Learns your preferences and patterns
- **Intelligent**: Handles complex scenarios without explicit instructions
- **Flexible**: Same goal can be achieved in different ways based on context

### For Developers
- **Extensible**: Add tools without changing core logic
- **Maintainable**: Separation between tools (what) and orchestration (how)
- **Testable**: Tools can be tested independently
- **Flexible**: Easy to add new planning strategies

### For the System
- **Robust**: Multiple fallback strategies
- **Safe**: Validation at every step
- **Efficient**: Only uses AI when needed
- **Adaptive**: Improves with use

---

## Future Enhancements

### Phase 5: Advanced Capabilities
- **Reflection**: Agent reviews its own decisions
- **Self-correction**: Adjusts approach when results aren't satisfactory
- **Multi-agent**: Specialized agents for different domains
- **Memory**: Long-term memory of user projects and goals

### Phase 6: Integration
- **Calendar integration**: Access calendar data for scheduling
- **Email integration**: Pull context from recent emails
- **Project management**: Integration with actual projects
- **Team collaboration**: Multi-user task management

---

## Conclusion

The transformation from logic app to agent creates a more powerful, flexible, and user-friendly system. Users interact naturally with their AI assistant, which adapts to their needs and learns from their behavior, all while maintaining the robust, well-tested core functionality.

The key insight: **Tools + AI = Agent**, but the magic is in how they're orchestrated. By moving orchestration to the AI level, we unlock capabilities that would be nearly impossible to code manually.
