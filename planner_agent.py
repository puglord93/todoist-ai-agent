"""
Planner Agent - Tool-using agent that orchestrates workflows based on user goals
"""
import os
import json
from typing import Dict, List, Any, Optional
from datetime import datetime
from pathlib import Path
from openai import OpenAI
from dotenv import load_dotenv
from tools_registry import ToolsRegistry

load_dotenv()


class PlannerAgent:
    """
    Agent that uses tool-calling to achieve user goals.

    The planner receives a user goal, determines the best sequence of tool calls,
    executes them, and provides a human-friendly summary.
    """

    def __init__(self, use_mock: bool = False):
        """
        Initialize the planner agent.

        Args:
            use_mock: If True, use mock data instead of real Todoist API
        """
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
        self.tools_registry = ToolsRegistry(use_mock=use_mock)
        self.tools = self.tools_registry.get_tools()
        self.conversation_history: List[Dict[str, str]] = []

        # Session memory for planning context
        self.session_memory = {
            "user_profile": None,
            "last_plan": None,
            "recent_results": [],
            "session_start": datetime.now().isoformat()
        }

    def handle_request(self, user_goal: str, context: Optional[Dict[str, Any]] = None) -> str:
        """
        Handle a user request by planning and executing a sequence of tool calls.

        Args:
            user_goal: User's natural language goal
            context: Optional context about the current situation

        Returns:
            Human-friendly response explaining what was done
        """
        print(f"\n🎯 Planning to achieve: {user_goal}")

        # Build system prompt with context
        system_prompt = self._build_system_prompt(context or {})

        # Add user goal to conversation
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_goal}
        ]

        # Add conversation history (last 10 messages)
        messages.extend(self.conversation_history[-10:])

        # Tool calling loop
        max_iterations = 10
        iteration = 0

        while iteration < max_iterations:
            iteration += 1

            try:
                # Call OpenAI with tool calling
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=messages,
                    tools=self.tools,
                    tool_choice="auto",
                    max_tokens=2000
                )

                message = response.choices[0].message

                # Check if model wants to call a tool
                if message.tool_calls:
                    print(f"  → Calling {len(message.tool_calls)} tool(s)...")

                    # Execute each tool call
                    tool_results = []
                    for tool_call in message.tool_calls:
                        tool_name = tool_call.function.name
                        tool_args = json.loads(tool_call.function.arguments)
                        tool_call_id = tool_call.id

                        print(f"    • {tool_name}({json.dumps(tool_args, indent=2)})")

                        # Execute tool
                        result = self.tools_registry.execute_tool(tool_name, tool_args)
                        tool_results.append({
                            "tool_name": tool_name,
                            "tool_call_id": tool_call_id,
                            "arguments": tool_args,
                            "result": result
                        })

                    # Store results in session memory
                    self.session_memory["recent_results"].extend(tool_results)

                    # Add tool results to conversation (one per tool call with tool_call_id)
                    messages.append(message)
                    for tool_result in tool_results:
                        messages.append({
                            "role": "tool",
                            "tool_call_id": tool_result["tool_call_id"],
                            "content": json.dumps(tool_result["result"], indent=2, default=str)
                        })

                    # Continue loop to let model process results
                    continue

                else:
                    # No more tool calls - model has final response
                    final_response = message.content
                    print(f"  ✓ Plan complete\n")

                    # Add to conversation history
                    self.conversation_history.append({"role": "user", "content": user_goal})
                    self.conversation_history.append({"role": "assistant", "content": final_response})

                    # Keep only last 20 messages
                    if len(self.conversation_history) > 20:
                        self.conversation_history = self.conversation_history[-20:]

                    return final_response

            except Exception as e:
                error_msg = f"Error during planning: {str(e)}"
                print(f"  ✗ {error_msg}")
                return error_msg

        # Max iterations reached
        return "Reached maximum planning iterations. Please simplify your request."

    def _build_system_prompt(self, context: Dict[str, Any]) -> str:
        """
        Build the system prompt with user context and guidelines.

        Args:
            context: Current context information

        Returns:
            System prompt string
        """
        # Get user profile
        if not self.session_memory["user_profile"]:
            profile_result = self.tools_registry.execute_tool("get_user_profile", {})
            self.session_memory["user_profile"] = profile_result.get("profile", {})

        profile = self.session_memory["user_profile"]

        return f"""You are JJ's Todoist AI Agent - a helpful, intelligent task management assistant.

Your role:
- Help JJ achieve their task-related goals through intelligent planning and execution
- Use tools to fetch, analyze, and manage tasks
- Provide clear, actionable advice in a friendly tone
- Never expose raw JSON or tool results unless asked

User Context:
- Name: JJ
- Role: Venture builder at ATOM Ventures in Singapore
- Work: Deep-tech startups and research institutes
- Timezone: {profile.get('timezone', 'Asia/Singapore')}
- Work hours: {profile.get('work_hours', '09:00-18:00')}
- Typical task completion rate: {profile.get('typical_task_completion_rate', 0.75) * 100:.0f}%
- Prefers: {profile.get('prefers_mornings_for_deep_work', True) and 'mornings for deep work' or 'flexible timing'}
- Batching preference: {profile.get('likes_batching', True) and 'likes' or 'dislikes'} batching similar tasks
- Polish aggressiveness: {profile.get('polish_aggressiveness', 'moderate')}

Available Tools:
You have access to these tools. Use them to achieve the user's goal:

1. fetch_tasks(filter) - Get tasks from Todoist
2. analyze_tasks() - Analyze all tasks for urgency/importance
3. prioritize_tasks(max_tasks) - Generate focus plan with top priorities
4. categorize_tasks(quadrant) - Group tasks by Eisenhower quadrants
5. polish_tasks(scope, min_quality) - Improve task names/descriptions
6. schedule_due_dates(scope) - Suggest due dates for tasks
7. update_tasks(updates, preview_only) - Update tasks (preview first!)
8. get_daily_briefing() - Get comprehensive daily overview
9. get_task_quality_report() - Identify tasks needing improvement
10. generate_focus_plan(timeframe, max_tasks) - Create realistic plans
11. suggest_updates() - Get AI-suggested improvements
12. get_user_profile() - Get user preferences
13. update_user_profile(preferences) - Update user preferences

Planning Guidelines:
- Always start by understanding the goal: "What does JJ want to achieve?"
- Fetch current tasks before making major changes
- When updating tasks, use preview_only=true first, then ask for permission
- Consider JJ's preferences and completion rate when making plans
- Break large goals into small, achievable steps
- Suggest batching similar tasks when appropriate
- For overwhelming situations, prioritize quality over quantity
- Use get_daily_briefing for morning check-ins
- Use prioritize_tasks for urgent decision-making

Important Rules:
- MAX 3 tool calls per turn (unless explicitly asked for more)
- ALWAYS show previews before bulk updates (preview_only=true)
- Ask user for confirmation before applying changes to >3 tasks
- Respect work hours and timezone
- Be encouraging and supportive
- Explain your reasoning briefly
- If unsure, ask clarifying questions

{json.dumps(context, indent=2) if context else ''}

Now, help JJ achieve their goal using the available tools. Think step by step, call tools strategically, and provide a friendly, helpful response."""

    def reset_session(self):
        """Reset the planning session."""
        self.conversation_history = []
        self.session_memory = {
            "user_profile": None,
            "last_plan": None,
            "recent_results": [],
            "session_start": datetime.now().isoformat()
        }
        print("🧹 Session reset")

    def get_session_summary(self) -> Dict[str, Any]:
        """Get a summary of the current session."""
        return {
            "session_start": self.session_memory["session_start"],
            "recent_results_count": len(self.session_memory["recent_results"]),
            "conversation_length": len(self.conversation_history),
            "user_profile_loaded": self.session_memory["user_profile"] is not None
        }


class ChatInterface:
    """Simple chat interface for the planner agent."""

    def __init__(self, use_mock: bool = False):
        """Initialize the chat interface."""
        print("🤖 Initializing Planner Agent...")
        try:
            self.agent = PlannerAgent(use_mock=use_mock)
            print("✅ Ready!\n")
        except Exception as e:
            print(f"❌ Error initializing: {e}")
            print("Make sure your .env file has OPENAI_API_KEY and TODOIST_API_TOKEN")
            raise

    def start(self):
        """Start the interactive chat loop."""
        self._print_welcome()

        while True:
            try:
                user_input = input("\n💬 You: ").strip()

                if not user_input:
                    continue

                if user_input.lower() in ['quit', 'exit', 'bye', 'q']:
                    print("\n👋 Goodbye! Your tasks are in good hands.")
                    break

                if user_input.lower() in ['reset', 'clear']:
                    self.agent.reset_session()
                    self._print_welcome()
                    continue

                if user_input.lower() == 'help':
                    self._print_help()
                    continue

                if user_input.lower() == 'status':
                    summary = self.agent.get_session_summary()
                    print(f"\n📊 Session Status: {json.dumps(summary, indent=2)}")
                    continue

                # Process the request
                response = self.agent.handle_request(user_input)
                print(f"\n🤖 Assistant: {response}")

            except KeyboardInterrupt:
                print("\n\n👋 Interrupted. Goodbye!")
                break
            except Exception as e:
                print(f"\n❌ Error: {e}")
                print("Type 'help' for available commands.")

    def _print_welcome(self):
        """Print welcome message."""
        print("=" * 60)
        print("🎯 TODOIST PLANNER AGENT")
        print("=" * 60)
        print("\nI'm your intelligent task management assistant!")
        print("I can help you:")
        print("  • Prioritize and plan your day")
        print("  • Clean up and organize tasks")
        print("  • Schedule due dates intelligently")
        print("  • Polish task descriptions")
        print("  • Generate focus plans")
        print("\nJust tell me what you want to achieve!")
        print("\nCommands:")
        print("  'status' - Show session info")
        print("  'reset' - Clear conversation")
        print("  'help' - Show this message")
        print("  'quit' - Exit")
        print("=" * 60)

    def _print_help(self):
        """Print help message."""
        print("\n" + "=" * 60)
        print("💡 HOW TO USE")
        print("=" * 60)
        print("\nJust speak naturally! Examples:")
        print("\n📅 Daily Planning:")
        print('  "What should I focus on today?"')
        print('  "Give me a realistic plan for this afternoon"')
        print('  "Show me my priorities for this week"')
        print("\n🧹 Task Cleanup:")
        print('  "Clean up my backlog"')
        print('  "Polish my task names"')
        print('  "Add due dates to important tasks"')
        print("\n📊 Analysis:")
        print('  "Analyze my tasks"')
        print('  "Show me tasks by Eisenhower quadrant"')
        print('  "Which tasks need improvement?"')
        print("\n🤝 I'm goal-driven and adapt to your preferences!")
        print("=" * 60 + "\n")


if __name__ == "__main__":
    import sys

    use_mock = "--mock" in sys.argv
    chat = ChatInterface(use_mock=use_mock)
    chat.start()
