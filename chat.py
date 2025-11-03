#!/usr/bin/env python3
"""
Conversational Todoist AI Agent

Interactive chat interface for managing Todoist tasks using natural language.
"""

import sys
import os
from typing import Dict, Any, List
from agent import TodoistAIAgent
from intent_router import IntentRouter
from datetime import datetime


class TodoistChatAgent:
    """Conversational interface for Todoist AI Agent."""

    def __init__(self):
        """Initialize the chat agent."""
        print("🤖 Initializing Todoist AI Assistant...")
        try:
            self.agent = TodoistAIAgent(use_mock=False)
            self.router = IntentRouter()
            self.last_shown_tasks = []  # Track tasks shown to user for context
            print("✅ Ready!\n")
        except Exception as e:
            print(f"❌ Error initializing: {e}")
            print("Make sure your .env file has OPENAI_API_KEY and TODOIST_API_TOKEN")
            sys.exit(1)

    def start(self):
        """Start the interactive chat loop."""
        self._print_welcome()

        while True:
            try:
                # Get user input
                user_input = input("\n💬 You: ").strip()

                if not user_input:
                    continue

                # Check for exit commands
                if user_input.lower() in ['quit', 'exit', 'bye', 'q']:
                    print("\n👋 Goodbye! Your tasks are in good hands.")
                    break

                # Check for clear command
                if user_input.lower() in ['clear', 'reset']:
                    self.router.clear_history()
                    print("🧹 Conversation history cleared!")
                    continue

                # Process the request
                self._process_request(user_input)

            except KeyboardInterrupt:
                print("\n\n👋 Interrupted. Goodbye!")
                break
            except Exception as e:
                print(f"\n❌ Error: {e}")
                print("Type 'help' for available commands.")

    def _process_request(self, user_input: str):
        """
        Process a user request.

        Args:
            user_input: User's natural language input
        """
        # Handle shortcuts
        shortcuts = {
            'help': 'get_help',
            'show': 'show_tasks',
            'p': 'prioritize_tasks',
            'polish': 'polish_tasks',
            'schedule': 'schedule_tasks',
            'categorize': 'categorize_tasks'
        }

        # Check if input is a shortcut
        intent_result = None
        if user_input.lower() in shortcuts:
            intent_result = {
                "intent": shortcuts[user_input.lower()],
                "parameters": self._default_params(shortcuts[user_input.lower()]),
                "confidence": "high"
            }
        else:
            # Detect intent using AI
            intent_result = self.router.detect_intent(user_input)

        # Route to appropriate handler
        intent = intent_result.get("intent")
        params = intent_result.get("parameters", {})

        print(f"\n🤖 Assistant: ", end="")

        if intent == "show_tasks":
            self._handle_show_tasks(params)
        elif intent == "prioritize_tasks":
            self._handle_prioritize(params)
        elif intent == "polish_tasks":
            self._handle_polish(params)
        elif intent == "schedule_tasks":
            self._handle_schedule(params)
        elif intent == "categorize_tasks":
            self._handle_categorize(params)
        elif intent == "update_task":
            self._handle_update_task(params)
        elif intent == "polish_and_apply":
            self._handle_polish_and_apply(params)
        elif intent == "get_help":
            self._print_help()
        elif intent == "general_response":
            print(intent_result.get("response", "I'm not sure how to help with that."))
        else:
            print("I'm not sure what you'd like me to do. Type 'help' for available commands.")

    def _handle_show_tasks(self, params: Dict[str, Any]):
        """Handle show_tasks intent."""
        filter_type = params.get("filter", "today")

        if filter_type == "today":
            today_data = self.agent.get_today_tasks()
            self._display_today_tasks(today_data)
        elif filter_type == "all":
            tasks = self.agent.get_tasks_filtered("all")
            print(f"Found {len(tasks)} total tasks\n")
            self._display_task_list(tasks[:10], "ALL TASKS (showing first 10)")
        elif filter_type == "overdue":
            tasks = self.agent.get_tasks_filtered("overdue")
            self._display_task_list(tasks, "OVERDUE TASKS")
        elif filter_type == "upcoming":
            tasks = self.agent.get_tasks_filtered("upcoming")
            self._display_task_list(tasks, "UPCOMING TASKS")
        elif filter_type == "no_date":
            tasks = self.agent.get_tasks_filtered("no_date")
            self._display_task_list(tasks, "TASKS WITHOUT DUE DATES")

    def _handle_prioritize(self, params: Dict[str, Any]):
        """Handle prioritize_tasks intent."""
        report_type = params.get("report_type", "focus")

        print("Analyzing and prioritizing your tasks...\n")
        report = self.agent.generate_report(report_type)
        print(report)

    def _handle_polish(self, params: Dict[str, Any]):
        """Handle polish_tasks intent."""
        scope = params.get("scope", "low_quality")
        min_quality = params.get("min_quality", 50)

        print("Analyzing task quality...\n")

        if scope == "low_quality":
            quality_report = self.agent.get_task_quality_report()
            worst_tasks = quality_report["worst_tasks"]

            if not worst_tasks or worst_tasks[0]["percentage"] >= min_quality:
                print(f"✨ All tasks meet the quality threshold ({min_quality}%)!")
                print(f"Average quality score: {quality_report['average_quality']}%")
            else:
                print(f"Found {len(worst_tasks)} tasks below {min_quality}% quality:\n")
                for i, task in enumerate(worst_tasks, 1):
                    if task["percentage"] < min_quality:
                        print(f"{i}. {task['task_content']}")
                        print(f"   Quality: {task['percentage']}%")
                        print(f"   Issues: {', '.join(task['issues'])}")
                        print()

                print("\n💡 Tip: Use 'venv/bin/python3 interactive_polish.py' for interactive polishing")

    def _handle_schedule(self, params: Dict[str, Any]):
        """Handle schedule_tasks intent."""
        scope = params.get("scope", "no_date")

        print("Checking tasks without due dates...\n")

        tasks_no_date = self.agent.get_tasks_filtered("no_date")

        if not tasks_no_date:
            print("✅ All tasks have due dates!")
        else:
            print(f"Found {len(tasks_no_date)} tasks without due dates:\n")
            for i, task in enumerate(tasks_no_date[:10], 1):
                print(f"{i}. {task.get('content', '')}")
                if task.get('labels'):
                    print(f"   Labels: {', '.join(task['labels'])}")

            print("\n💡 Tip: Use 'venv/bin/python3 interactive_polish.py --mode schedule' to add due dates")

    def _handle_categorize(self, params: Dict[str, Any]):
        """Handle categorize_tasks intent."""
        quadrant = params.get("quadrant")

        print("Categorizing tasks by Eisenhower matrix...\n")

        result = self.agent.categorize_by_quadrant(quadrant)

        if "error" in result:
            print(result["error"])
            return

        if quadrant:
            tasks = result.get("tasks", [])
            quadrant_names = {
                "Q1": "🔥 DO FIRST (Urgent & Important)",
                "Q2": "📆 SCHEDULE (Important, Not Urgent)",
                "Q3": "👥 DELEGATE (Urgent, Not Important)",
                "Q4": "🗑️ CONSIDER (Neither Urgent nor Important)"
            }
            print(f"{quadrant_names.get(quadrant, quadrant)}\n")
            print("=" * 70)
            if tasks:
                for i, task in enumerate(tasks, 1):
                    print(f"\n{i}. {task['task_content']}")
                    print(f"   Priority Score: {task['priority_score']}/100")
            else:
                print("\nNo tasks in this quadrant")
        else:
            stats = result.get("statistics", {})
            print("Task Distribution:")
            print(f"  🔥 Q1 (Do First): {stats.get('q1_count', 0)}")
            print(f"  📆 Q2 (Schedule): {stats.get('q2_count', 0)}")
            print(f"  👥 Q3 (Delegate): {stats.get('q3_count', 0)}")
            print(f"  🗑️ Q4 (Consider): {stats.get('q4_count', 0)}")

    def _display_today_tasks(self, data: Dict[str, Any]):
        """Display today's tasks in a formatted way."""
        print(f"Here are your tasks for {data['today']}:\n")
        print("=" * 70)

        # Track tasks for context
        self.last_shown_tasks = []

        if data["overdue"]:
            print(f"\n⚠️  OVERDUE ({len(data['overdue'])})")
            print("-" * 70)
            for task in data["overdue"]:
                priority_emoji = "🔴" if task.get('priority', 1) >= 3 else "🟡"
                print(f"{priority_emoji} {task.get('content', '')}")
                self.last_shown_tasks.append(task)
            print()

        if data["due_today"]:
            print(f"📌 DUE TODAY ({len(data['due_today'])})")
            print("-" * 70)
            for task in data["due_today"]:
                priority_emoji = "🔴" if task.get('priority', 1) >= 3 else "🟢"
                print(f"{priority_emoji} {task.get('content', '')}")
                self.last_shown_tasks.append(task)
            print()
        else:
            print("\n✨ No tasks due today!\n")

        if data["upcoming"]:
            print(f"📆 UPCOMING (Next 7 days)")
            print("-" * 70)
            for task in data["upcoming"]:
                due_date = task.get('due', {}).get('date', '')
                print(f"   {task.get('content', '')} (Due: {due_date})")
                self.last_shown_tasks.append(task)
            print()

        print("=" * 70)
        print(f"Total active tasks: {data['total']}")

    def _display_task_list(self, tasks: List[Dict[str, Any]], title: str):
        """Display a list of tasks."""
        print(f"{title}\n")
        print("=" * 70)

        # Track tasks for context
        self.last_shown_tasks = tasks

        if not tasks:
            print("\nNo tasks found")
        else:
            for i, task in enumerate(tasks, 1):
                priority_emoji = "🔴" if task.get('priority', 1) >= 3 else "🟢"
                print(f"\n{i}. {priority_emoji} {task.get('content', '')}")

                due_date = task.get('due', {}).get('date') if task.get('due') else None
                if due_date:
                    print(f"   Due: {due_date}")

                if task.get('labels'):
                    print(f"   Labels: {', '.join(task['labels'])}")

        print("\n" + "=" * 70)

    def _handle_update_task(self, params: Dict[str, Any]):
        """Handle update_task intent with confirmation."""
        task_identifier = params.get("task_identifier", "")
        update_type = params.get("update_type", "")
        new_value = params.get("new_value", "")

        # Find the task
        task = self._identify_task(task_identifier)
        if not task:
            print(f"Could not find task: {task_identifier}")
            print("Tip: First show tasks, then use 'first task', 'second task', etc.")
            return

        # Build update dict
        updates = {}
        if update_type == "name":
            updates["content"] = new_value
        elif update_type == "description":
            updates["description"] = new_value
        elif update_type == "priority":
            try:
                updates["priority"] = int(new_value)
            except:
                print("Priority must be a number between 1-4")
                return
        elif update_type == "due_date":
            updates["due_date"] = new_value

        # Get preview
        result = self.agent.update_single_task(str(task.get("id")), updates, preview_only=True)

        if "error" in result:
            print(f"Error: {result['error']}")
            return

        preview = result["preview"]
        if not preview.get("changes"):
            print("No changes needed - the task is already set to that value.")
            return

        # Show preview
        print(self.agent.task_updater.format_preview(preview))
        print()

        # Ask for confirmation
        if self._confirm_changes():
            # Apply the update
            result = self.agent.update_single_task(str(task.get("id")), updates)
            if result.get("success"):
                print("\n✅ Task updated successfully!")
            else:
                print("\n❌ Failed to update task.")
        else:
            print("\n❌ Update cancelled.")

    def _handle_polish_and_apply(self, params: Dict[str, Any]):
        """Handle polish_and_apply intent with confirmation."""
        task_identifier = params.get("task_identifier", "")
        count = params.get("count", 1)

        # Identify tasks to polish
        tasks_to_polish = self._identify_tasks_for_polish(task_identifier, count)

        if not tasks_to_polish:
            print(f"Could not find tasks matching: {task_identifier}")
            print("Tip: First show tasks, then use 'first task', 'top 3', etc.")
            return

        print(f"🎨 Polishing {len(tasks_to_polish)} task(s)...\n")

        # Get task IDs
        task_ids = [str(task.get("id")) for task in tasks_to_polish]

        # Polish with preview
        results = self.agent.polish_and_update(task_ids, preview_only=True)

        # Filter out tasks that don't need polishing
        tasks_needing_polish = [r for r in results if r.get("preview", {}).get("changes")]

        if not tasks_needing_polish:
            print("✨ All selected tasks are already well-formatted!")
            return

        # Show previews
        for i, result in enumerate(tasks_needing_polish, 1):
            print(f"\n{'='*70}")
            print(f"Task {i}/{len(tasks_needing_polish)}")
            print('='*70)
            preview_str = self.agent.task_updater.format_preview(result["preview"])
            print(preview_str)
            if result.get("polish_reason"):
                print(f"\n💡 Reason: {result['polish_reason']}")

        print(f"\n{'='*70}")

        # Ask for confirmation
        if len(tasks_needing_polish) > 1:
            print(f"\nApply changes to all {len(tasks_needing_polish)} tasks?")
        else:
            print("\nApply these changes?")

        if self._confirm_changes():
            # Apply updates
            task_ids_to_update = [r["task_id"] for r in tasks_needing_polish]
            final_results = self.agent.polish_and_update(task_ids_to_update, preview_only=False)

            success_count = sum(1 for r in final_results if r.get("success"))
            print(f"\n✅ Successfully updated {success_count}/{len(tasks_needing_polish)} tasks!")
        else:
            print("\n❌ Updates cancelled.")

    def _identify_task(self, identifier: str) -> Optional[Dict[str, Any]]:
        """
        Identify a task from user input.

        Args:
            identifier: Task identifier like "first task", task name, etc.

        Returns:
            Task dictionary or None
        """
        identifier_lower = identifier.lower()

        # Handle positional references
        if "first" in identifier_lower and self.last_shown_tasks:
            return self.last_shown_tasks[0] if len(self.last_shown_tasks) > 0 else None
        elif "second" in identifier_lower and self.last_shown_tasks:
            return self.last_shown_tasks[1] if len(self.last_shown_tasks) > 1 else None
        elif "third" in identifier_lower and self.last_shown_tasks:
            return self.last_shown_tasks[2] if len(self.last_shown_tasks) > 2 else None

        # Try to match by name
        all_tasks = self.agent.client.fetch_tasks()
        for task in all_tasks:
            if identifier_lower in task.get("content", "").lower():
                return task

        return None

    def _identify_tasks_for_polish(self, identifier: str, count: int) -> List[Dict[str, Any]]:
        """
        Identify multiple tasks for polishing.

        Args:
            identifier: Task identifier like "top 3", "all overdue", etc.
            count: Number of tasks

        Returns:
            List of task dictionaries
        """
        identifier_lower = identifier.lower()

        # Handle "top N" or "first N"
        if ("top" in identifier_lower or "first" in identifier_lower) and self.last_shown_tasks:
            return self.last_shown_tasks[:count]

        # Handle "all"
        if "all" in identifier_lower:
            if "overdue" in identifier_lower:
                return self.agent.get_tasks_filtered("overdue")
            elif self.last_shown_tasks:
                return self.last_shown_tasks

        # Default to first N of last shown
        if self.last_shown_tasks:
            return self.last_shown_tasks[:count]

        return []

    def _confirm_changes(self) -> bool:
        """
        Ask user to confirm changes.

        Returns:
            True if confirmed, False otherwise
        """
        while True:
            response = input("Proceed? (y/n): ").lower().strip()
            if response in ['y', 'yes']:
                return True
            elif response in ['n', 'no']:
                return False
            else:
                print("Please answer 'y' or 'n'")

    def _default_params(self, intent: str) -> Dict[str, Any]:
        """Get default parameters for shortcuts."""
        defaults = {
            "show_tasks": {"filter": "today"},
            "prioritize_tasks": {"report_type": "focus"},
            "polish_tasks": {"scope": "low_quality", "min_quality": 50},
            "schedule_tasks": {"scope": "no_date"},
            "categorize_tasks": {"quadrant": None},
            "get_help": {}
        }
        return defaults.get(intent, {})

    def _print_welcome(self):
        """Print welcome message."""
        print("=" * 70)
        print("🎯 TODOIST AI ASSISTANT - Conversational Interface")
        print("=" * 70)
        print("\nI can help you manage your Todoist tasks using natural language!")
        print("\nExamples:")
        print("  • 'show me today's tasks'")
        print("  • 'prioritize my tasks'")
        print("  • 'which tasks need polishing?'")
        print("  • 'help me add due dates'")
        print("  • 'categorize by urgency'")
        print("\nShortcuts: show, p, polish, schedule, categorize, help")
        print("Type 'quit' to exit")
        print("=" * 70)

    def _print_help(self):
        """Print help information."""
        print("\n" + "=" * 70)
        print("AVAILABLE COMMANDS")
        print("=" * 70)
        print("\n📋 Task Viewing:")
        print("  • 'show tasks' / 'today' - Show today's tasks")
        print("  • 'show all tasks' - Show all tasks")
        print("  • 'show overdue' - Show overdue tasks")
        print("  • 'show upcoming' - Show upcoming tasks")
        print("\n🎯 Task Management:")
        print("  • 'prioritize' / 'p' - Prioritize tasks (Eisenhower matrix)")
        print("  • 'categorize' - Categorize by quadrants")
        print("  • 'categorize Q1' - Show specific quadrant tasks")
        print("\n✨ Task Improvement:")
        print("  • 'polish' - Check task quality")
        print("  • 'schedule' - Find tasks without due dates")
        print("\n🔧 Utilities:")
        print("  • 'help' - Show this help")
        print("  • 'clear' - Clear conversation history")
        print("  • 'quit' - Exit")
        print("\n💡 Tip: You can also use natural language!")
        print("   Try: 'show me my urgent tasks' or 'what should I focus on today?'")
        print("=" * 70)


def main():
    """Main entry point."""
    chat = TodoistChatAgent()
    chat.start()


if __name__ == "__main__":
    main()
