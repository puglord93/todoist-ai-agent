"""
Pattern Comparison: Old vs New Architecture

This script demonstrates the difference between the old "logic app" pattern
and the new "agent" pattern.
"""
from agent import TodoistAIAgent
from planner_agent import PlannerAgent
from user_profile_manager import UserProfileManager


def compare_patterns():
    """Compare old vs new patterns with examples."""

    print("=" * 80)
    print("PATTERN COMPARISON: Logic App vs Tool-Using Agent")
    print("=" * 80)

    # Example 1: Task Prioritization
    print("\n" + "=" * 80)
    print("EXAMPLE 1: Task Prioritization")
    print("=" * 80)

    print("\n📋 OLD PATTERN (Logic App - Deterministic):")
    print("-" * 80)
    print("""
def run_analysis():
    # Fixed pipeline - always the same steps
    tasks = fetch_tasks()
    normalized = [normalize(t) for t in tasks]
    analyzed = [analyzer.analyze(t) for t in normalized]
    focus = prioritizer.create_plan(analyzed)
    return focus

# User interaction:
User: "prioritize my tasks"
System: (runs fixed pipeline)
Output: "Here are your top 5 priorities"

# Characteristics:
- Flow is hardcoded in Python
- Same weights applied to all users
- No context about user's situation
- User must know the exact command
- No adaptation based on feedback
""")

    print("\n🤖 NEW PATTERN (Agent - Adaptive):")
    print("-" * 80)
    print("""
def handle_request(user_goal):
    # AI decides flow based on goal and context
    system_prompt = build_prompt(user_context, preferences)

    while True:
        response = ai.chat.completions.create(
            messages=messages,
            tools=available_tools,
            tool_choice="auto"
        )

        if response.tool_calls:
            results = execute_tools(response.tool_calls)
            messages.append(results)
        else:
            return response.content

# User interaction:
User: "I'm overwhelmed and don't know what to focus on"
AI: "Let me assess your situation first... I see 47 tasks with 12 overdue.
     This is indeed overwhelming. Let me create a calming, realistic plan:
     1. Address 12 overdue items (focus on 3 most critical)
     2. Complete 5 due-today tasks
     3. Defer 15 low-urgency tasks to next week
     4. Polish task names for clarity
     Does this approach work for you?"

# Characteristics:
- AI decides flow based on goal
- Adapts to user's emotional state
- Considers context (overwhelmed → smaller batches)
- Natural language goal, not command
- Learns from user feedback
""")

    # Example 2: Task Polishing
    print("\n" + "=" * 80)
    print("EXAMPLE 2: Task Polishing")
    print("=" * 80)

    print("\n📋 OLD PATTERN (Logic App - Rules-Based):")
    print("-" * 80)
    print("""
# Hardcoded rules
if quality < AUTO_POLISH_QUALITY_THRESHOLD:  # Fixed at 40
    if tasks_processed < AUTO_POLISH_MAX_TASKS:  # Fixed at 5
        polish(task)

# User interaction:
User: "polish tasks"
System: (applies fixed rules)
Output: "Polished 5 tasks (all with quality < 40)"

# Problems:
- Same threshold for everyone
- Same batch size for everyone
- No consideration of user's current workload
- If overwhelmed, still polishes 5 tasks
""")

    print("\n🤖 NEW PATTERN (Agent - Context-Aware):")
    print("-" * 80)
    print("""
# AI decides based on context
if overwhelmed:
    recommended_count = 2  # Small batch
    threshold = 60  # Higher threshold (only worst tasks)
else:
    recommended_count = 8
    threshold = 40

# User interaction:
User: "my task list feels messy"
AI: "Looking at your current state:
     - 3 high-priority tasks due today
     - Energy level: moderate
     - Backlog: 20 tasks

     I recommend polishing 3 tasks max to avoid overload.
     Focus on the 3 most vague high-importance tasks?
     This will give immediate clarity without overwhelming you."

# Benefits:
- Adapts to current situation
- Smaller batch when overwhelmed
- Explains reasoning
- Asks for confirmation
""")

    # Example 3: Daily Planning
    print("\n" + "=" * 80)
    print("EXAMPLE 3: Daily Planning")
    print("=" * 80)

    print("\n📋 OLD PATTERN (Logic App - No Support):")
    print("-" * 80)
    print("""
# No clear way to do this - would need new script
# User needs to run multiple commands manually:
# 1. Get today's tasks
# 2. Prioritize them
# 3. Check for conflicts
# 4. Suggest schedule

# Very cumbersome for user
""")

    print("\n🤖 NEW PATTERN (Agent - Natural):")
    print("-" * 80)
    print("""
# User states goal
User: "Plan my afternoon - I have 2 hours free"

# AI handles the complexity
AI: "Based on your 2-hour window and energy patterns:
     Recommended approach:
     1. Quick win: 'Send follow-up email' (5 min)
     2. Deep work: 'Review Q4 report' (60 min)
     3. Buffer: 'Prep tomorrow's meeting' (30 min)
     4. Buffer: 'Email response' (15 min)

     This gives you focused time without overcommitting.
     Would you like me to schedule these with due dates?"

# Much more natural and helpful
""")

    # Comparison Table
    print("\n" + "=" * 80)
    print("SIDE-BY-SIDE COMPARISON")
    print("=" * 80)

    comparison = """
╔════════════════════════╤═════════════════════════╤═════════════════════════╗
║ Aspect                 │ Old (Logic App)          │ New (Agent)             ║
╠════════════════════════╪═════════════════════════╪═════════════════════════╣
║ Flow Control           │ Hardcoded in Python      │ AI decides sequence     ║
╠════════════════════════╪═════════════════════════╪═════════════════════════╣
║ User Input             │ Specific commands        │ Natural language goals  ║
║                        │ "prioritize my tasks"    │ "I'm overwhelmed"       ║
╠════════════════════════╪═════════════════════════╪═════════════════════════╣
║ Adaptation             │ Fixed weights            │ Learns from feedback    ║
║                        │ work: 1.2, health: 1.3  │ Polish aggressiveness:  ║
║                        │                          │ adaptive based on use   ║
╠════════════════════════╪═════════════════════════╪═════════════════════════╣
║ Context Awareness      │ None                     │ Session memory          ║
║                        │                          │ User profile            ║
║                        │                          │ Current situation       ║
╠════════════════════════╪═════════════════════════╪═════════════════════════╣
║ Error Handling         │ Try/except blocks        │ Conversational recovery ║
║                        │ Fails silently           │ "Let me try a different ║
║                        │                          │  approach..."           ║
╠════════════════════════╪═════════════════════════╪═════════════════════════╣
║ Extensibility          │ Modify code to add flow  │ Add new tools           ║
║                        │                          │ No core changes needed  ║
╠════════════════════════╪═════════════════════════╪═════════════════════════╣
║ User Experience        │ Learn specific commands  │ Just state your goal    ║
║                        │                          │ AI figures out how      ║
╠════════════════════════╪═════════════════════════╪═════════════════════════╣
║ Complexity Handling    │ Can't handle complex     │ Multi-step planning     ║
║                        │ multi-step scenarios     │ Natural for AI          ║
╠════════════════════════╪═════════════════════════╪═════════════════════════╣
║ Personalization        │ None                     │ Adapts to user          ║
║                        │                          │ • Completion rate       ║
║                        │                          │ • Batch preferences     ║
║                        │                          │ • Energy patterns       ║
╚════════════════════════╧═════════════════════════╧═════════════════════════╝
"""
    print(comparison)

    # Code Comparison
    print("\n" + "=" * 80)
    print("CODE COMPARISON")
    print("=" * 80)

    print("\n📋 OLD: Hardcoded Flow")
    print("-" * 80)
    print("""
# agent.py
def run_analysis(self):
    # Always the same steps
    tasks = self.client.fetch_tasks()
    normalized = [self.client.normalize_task(t) for t in tasks]
    analyzed = [self.analyzer.analyze_task(t) for t in normalized]
    focus = self.prioritizer.create_daily_focus_plan(analyzed)
    return {"analyzed_tasks": analyzed, "focus_plan": focus}

# Limited to this exact flow
""")

    print("\n🤖 NEW: AI-Directed Flow")
    print("-" * 80)
    print("""
# planner_agent.py
def handle_request(self, user_goal):
    system_prompt = self._build_system_prompt(context)

    while iteration < max_iterations:
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            tools=self.tools,  # AI can use any tool
            tool_choice="auto"
        )

        if message.tool_calls:
            for tool_call in message.tool_calls:
                result = self.tools_registry.execute_tool(
                    tool_call.name,
                    json.loads(tool_call.function.arguments)
                )
                messages.append({
                    "role": "tool",
                    "content": json.dumps(result)
                })
        else:
            return message.content

# AI decides which tools to use and in what order
""")

    print("\n" + "=" * 80)
    print("KEY INSIGHT")
    print("=" * 80)
    print("""
The fundamental shift:

OLD:  User tells system WHAT TO DO
      → "polish my tasks"
      → System does it the same way every time

NEW:  User tells system WHAT THEY WANT TO ACHIEVE
      → "I'm overwhelmed"
      → System decides HOW to help based on context

Result: Much more natural, adaptive, and intelligent interaction.
""")

    print("=" * 80)
    print()


def demonstrate_adaptation():
    """Show how the agent adapts based on user profile."""
    print("\n" + "=" * 80)
    print("ADAPTATION DEMONSTRATION")
    print("=" * 80)

    manager = UserProfileManager()

    print("\n📊 User Profile Insights:")
    print("-" * 80)
    insights = manager.get_insights()
    print(f"Total interactions tracked: {insights.get('total_interactions', 0)}")
    print(f"Total task completions: {insights.get('total_completions', 0)}")

    if '30_day_completion_rate' in insights:
        print(f"30-day completion rate: {insights['30_day_completion_rate']}%")

    if 'polish_acceptance_rate' in insights:
        print(f"Polish suggestion acceptance: {insights['polish_acceptance_rate']}%")

    print("\n💡 Adaptive Behaviors:")
    print("-" * 80)
    print("Based on your profile, the agent will:")
    print(f"  • Polish aggressiveness: {manager.preferences.polish_aggressiveness}")
    print(f"  • Max deep tasks per day: {manager.preferences.max_deep_tasks_per_day}")
    print(f"  • Prefers batching: {manager.preferences.likes_batching}")
    print(f"  • Morning deep work: {manager.preferences.prefers_mornings_for_deep_work}")

    print("\n📈 Learning Examples:")
    print("-" * 80)
    print("If you consistently:")
    print("  ✓ Accept polish suggestions → increases aggressiveness")
    print("  ✓ Complete large batches → learns you like batching")
    print("  ✗ Don't finish planned tasks → reduces daily target")
    print("  ✗ Reject suggestions → becomes more conservative")

    print("\n" + "=" * 80)


if __name__ == "__main__":
    compare_patterns()
    demonstrate_adaptation()

    print("\n✅ Comparison complete!")
    print("\nTo see the agent in action, run:")
    print("  python planner_agent.py")
    print("\nOr try the scenarios:")
    print("  python advanced_planning_examples.py --mock")
