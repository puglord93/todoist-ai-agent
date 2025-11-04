#!/usr/bin/env python3
"""
Conversational Todoist AI Agent

Interactive chat interface for managing Todoist tasks using natural language.
"""

import sys
import os
import json
from pathlib import Path
from typing import Dict, Any, List, Optional
from agent import TodoistAIAgent
from intent_router import IntentRouter
from datetime import datetime
from openai import OpenAI


class TodoistChatAgent:
    """Conversational interface for Todoist AI Agent."""

    def __init__(self):
        """Initialize the chat agent."""
        print("🤖 Initializing Todoist AI Assistant...")
        try:
            self.agent = TodoistAIAgent(use_mock=False)
            self.router = IntentRouter()
            self.last_shown_tasks = []  # Track tasks shown to user for context

            # Initialize OpenAI client for conversational fallback
            self.openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
            self.openai_model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

            # Conversation history persistence
            self.history_file = Path.home() / ".todoist_chat_history.json"
            self._load_history()

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
                    # Also delete the history file
                    if self.history_file.exists():
                        self.history_file.unlink()
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

        try:
            if intent == "show_tasks":
                self._handle_show_tasks(params)
            elif intent == "prioritize_tasks":
                self._handle_prioritize(params)
            elif intent == "polish_tasks":
                self._handle_polish(params)
            elif intent == "schedule_tasks":
                self._handle_schedule(params)
            elif intent == "schedule_due_dates":
                self._handle_schedule_due_dates(params)
            elif intent == "categorize_tasks":
                self._handle_categorize(params)
            elif intent == "update_task":
                self._handle_update_task(params)
            elif intent == "polish_and_apply":
                self._handle_polish_and_apply(params)
            elif intent == "manage_labels":
                self._handle_manage_labels(params)
            elif intent == "get_help":
                self._print_help()
            elif intent == "general_response":
                # Use conversational fallback for better responses
                response = self._conversational_fallback(user_input)
                print(response)
            elif intent == "error":
                # Handle errors with conversational fallback
                response = self._conversational_fallback(user_input)
                print(response)
            else:
                # Unknown intent - use conversational fallback
                response = self._conversational_fallback(user_input)
                print(response)

            # Save history after successful interaction
            if intent not in ["error"]:
                self._save_history()

        except Exception as e:
            print(f"\n\n⚠️  Oops! Something went wrong: {e}")
            print("\n💡 Let me try to help anyway...")
            # Use conversational fallback to recover gracefully
            response = self._conversational_fallback(f"I tried to {intent} but got an error: {e}. How can I help you?")
            print(f"\n{response}")
            self._save_history()

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
                # Filter tasks below threshold
                tasks_below_threshold = [t for t in worst_tasks if t["percentage"] < min_quality]
                print(f"Found {len(tasks_below_threshold)} tasks below {min_quality}% quality:\n")
                for i, task in enumerate(tasks_below_threshold, 1):
                    print(f"{i}. {task['task_content']}")
                    print(f"   Quality: {task['percentage']}%")
                    print(f"   Issues: {', '.join(task['issues'])}")
                    print()

                # Store these tasks for potential follow-up commands
                all_tasks = self.agent.client.fetch_tasks()
                task_ids_to_polish = [t["task_id"] for t in tasks_below_threshold]
                self.last_shown_tasks = [t for t in all_tasks if str(t.get("id")) in task_ids_to_polish]

                print(f"\n💡 You can say 'polish these tasks' or 'polish the first 3' to improve them")

    def _handle_schedule_due_dates(self, params: Dict[str, Any]):
        """Handle schedule_due_dates intent with AI suggestions and confirmation."""
        scope = params.get("scope", "no_date")
        task_identifier = params.get("task_identifier")

        # Get tasks to schedule
        if scope == "specific" and task_identifier:
            tasks_to_schedule = self._identify_tasks_for_polish(task_identifier, count=10)
        elif scope == "no_date":
            tasks_to_schedule = self.agent.get_tasks_filtered("no_date")
        else:
            # Get all tasks without dates first
            tasks_to_schedule = self.agent.get_tasks_filtered("no_date")

        if not tasks_to_schedule:
            print("✅ All tasks already have due dates!")
            return

        print(f"📅 Scheduling {len(tasks_to_schedule)} task(s)...\n")

        # Generate AI suggestions
        suggestions = self.agent.scheduler.suggest_due_dates_batch(tasks_to_schedule)

        if not suggestions:
            print("✨ Unable to generate due date suggestions for these tasks.")
            return

        # Show suggestions with interactive approval
        approved_updates = []
        for i, suggestion in enumerate(suggestions, 1):
            print(f"\n{'='*70}")
            print(f"Task {i}/{len(suggestions)}")
            print('='*70)
            print(f"📝 Task: {suggestion['task_content']}")
            print(f"\n📅 Suggested date: {suggestion['suggested_date']}")
            print(f"💡 Reasoning: {suggestion.get('reasoning', suggestion.get('source', 'N/A'))}")
            print(f"Confidence: {suggestion.get('confidence', 'medium')}")

            # Ask for confirmation
            while True:
                choice = input("\nApply this due date? (y/n/q): ").lower().strip()
                if choice in ['y', 'yes']:
                    approved_updates.append(suggestion)
                    print("✅ Approved")
                    break
                elif choice in ['n', 'no']:
                    print("⏭️  Skipped")
                    break
                elif choice in ['q', 'quit']:
                    print("\n🛑 Exiting scheduling...")
                    if approved_updates:
                        print(f"Will apply {len(approved_updates)} approved dates")
                    break
                else:
                    print("Please answer 'y', 'n', or 'q'")

            if choice in ['q', 'quit']:
                break

        # Apply approved updates
        if approved_updates:
            print(f"\n{'='*70}")
            print(f"Applying {len(approved_updates)} due date(s)...")
            print('='*70)

            success_count = 0
            for update in approved_updates:
                task_id = update["task_id"]
                due_date = update["suggested_date"]

                # Apply update
                success = self.agent.client.update_task(task_id, {"due_date": due_date})
                if success:
                    success_count += 1
                    print(f"✅ {update['task_content'][:50]}... → {due_date}")
                else:
                    print(f"❌ Failed: {update['task_content'][:50]}...")

            print(f"\n✅ Successfully added {success_count}/{len(approved_updates)} due dates!")
        else:
            print("\n❌ No due dates were applied.")

    def _handle_schedule(self, params: Dict[str, Any]):
        """Handle old schedule_tasks intent - redirect to new handler."""
        # Redirect to new handler for backward compatibility
        return self._handle_schedule_due_dates(params)

    def _handle_categorize(self, params: Dict[str, Any]):
        """Handle categorize_tasks intent."""
        quadrant = params.get("quadrant")

        # Handle "all" as None
        if quadrant and quadrant.lower() == "all":
            quadrant = None

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
            # Show all quadrants with tasks
            all_quadrants = result.get("all_quadrants", {})
            stats = result.get("statistics", {})

            quadrant_info = [
                ("Q1_do_first", "🔥 DO FIRST (Urgent & Important)", stats.get('q1_count', 0)),
                ("Q2_schedule", "📆 SCHEDULE (Important, Not Urgent)", stats.get('q2_count', 0)),
                ("Q3_delegate", "👥 DELEGATE (Urgent, Not Important)", stats.get('q3_count', 0)),
                ("Q4_consider", "🗑️ ELIMINATE/MINIMIZE (Neither Urgent nor Important)", stats.get('q4_count', 0))
            ]

            for key, name, count in quadrant_info:
                tasks = all_quadrants.get(key, [])
                print(f"\n{name}")
                print("=" * 70)
                if tasks:
                    for i, task in enumerate(tasks[:5], 1):  # Show first 5
                        print(f"{i}. {task['task_content']}")
                        print(f"   Priority Score: {task['priority_score']}/100")
                    if len(tasks) > 5:
                        print(f"   ... and {len(tasks) - 5} more")
                else:
                    print("   No tasks")
                print()

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
            print(f"❌ Could not find task: '{task_identifier}'")
            if self.last_shown_tasks:
                task_names = [t.get("content", "")[:40] for t in self.last_shown_tasks[:3]]
                print(f"💡 Recently shown tasks: {', '.join(task_names)}")
                print("   Try using 'first task', 'second task', etc.")
            else:
                print("💡 Tip: First show tasks, then reference them by position or name")
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
            print(f"❌ Could not find tasks matching: '{task_identifier}'\n")

            # Show helpful suggestions
            if self.last_shown_tasks:
                print(f"Recently shown tasks:")
                for i, task in enumerate(self.last_shown_tasks[:5], 1):
                    print(f"  {i}. {task.get('content', '')}")
                print(f"\n💡 Try: 'polish the first task' or 'polish these tasks'")
            else:
                # Show all tasks
                all_tasks = self.agent.client.fetch_tasks()
                print(f"Available tasks:")
                for i, task in enumerate(all_tasks[:10], 1):
                    content = task.get('content', '')
                    # Truncate long task names
                    if len(content) > 60:
                        content = content[:57] + "..."
                    print(f"  {i}. {content}")
                if len(all_tasks) > 10:
                    print(f"  ... and {len(all_tasks) - 10} more")
                print("\n💡 Tip: First show tasks (e.g., 'show all tasks'), then polish them")
                print("   Or be more specific: 'polish [task name]'")
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

    def _handle_manage_labels(self, params: Dict[str, Any]):
        """Handle label management requests."""
        action = params.get("action", "analyze")
        task_identifier = params.get("task_identifier")

        all_tasks = self.agent.client.fetch_tasks()

        if action == "analyze":
            # Analyze label usage across all tasks
            label_stats = {}
            for task in all_tasks:
                for label in task.get("labels", []):
                    if label not in label_stats:
                        label_stats[label] = {"count": 0, "tasks": []}
                    label_stats[label]["count"] += 1
                    label_stats[label]["tasks"].append(task.get("content", "")[:50])

            # Sort by count
            sorted_labels = sorted(label_stats.items(), key=lambda x: x[1]["count"], reverse=True)

            print("📊 Label Usage Analysis\n")
            print("=" * 70)
            print(f"Total labels: {len(sorted_labels)}\n")

            # Find potentially insignificant labels (used only once or twice)
            insignificant = [(label, info) for label, info in sorted_labels if info["count"] <= 2]

            if insignificant:
                print(f"⚠️  {len(insignificant)} labels used on 2 or fewer tasks:\n")
                for label, info in insignificant[:10]:
                    print(f"  • {label} ({info['count']} task{'s' if info['count'] > 1 else ''})")
                    for task_name in info["tasks"]:
                        print(f"     - {task_name}")
                print()

            print(f"✅ Most used labels:\n")
            for label, info in sorted_labels[:10]:
                print(f"  • {label}: {info['count']} tasks")

            print("\n" + "=" * 70)
            print("💡 You can say 'remove label Joseph from all tasks' to clean up")

        elif action == "view":
            # Show all labels
            all_labels = set()
            for task in all_tasks:
                all_labels.update(task.get("labels", []))

            print(f"🏷️  All Labels ({len(all_labels)})\n")
            print("=" * 70)
            for label in sorted(all_labels):
                print(f"  • {label}")
            print("=" * 70)

        elif action == "suggest":
            # Suggest labels for tasks without labels
            tasks_without_labels = [t for t in all_tasks if not t.get("labels")]

            if not tasks_without_labels:
                print("✅ All tasks already have labels!")
                return

            print(f"🏷️  Found {len(tasks_without_labels)} tasks without labels\n")

            # Get existing labels for suggestions
            existing_labels = set()
            for task in all_tasks:
                existing_labels.update(task.get("labels", []))

            print(f"Existing labels: {', '.join(sorted(existing_labels))}\n")
            print("=" * 70)

            # Generate suggestions for each task
            from openai import OpenAI
            import os
            client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

            approved_updates = []
            for i, task in enumerate(tasks_without_labels, 1):
                content = task.get("content", "")
                description = task.get("description", "")

                print(f"\nTask {i}/{len(tasks_without_labels)}")
                print(f"📝 {content}")
                if description:
                    print(f"   {description[:100]}")

                # Ask AI to suggest labels
                prompt = f"""Suggest 1-2 relevant labels for this task. Prefer existing labels if appropriate.

Task: "{content}"
Description: "{description or '(none)'}"

Existing labels: {', '.join(sorted(existing_labels)) if existing_labels else '(none)'}

Return ONLY a JSON object:
{{
  "labels": ["label1", "label2"],
  "reasoning": "Brief explanation"
}}

Prefer existing labels. Only create new labels if necessary. Keep labels short and lowercase."""

                try:
                    response = client.chat.completions.create(
                        model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
                        max_tokens=256,
                        messages=[{"role": "user", "content": prompt}],
                        response_format={"type": "json_object"}
                    )

                    import json
                    result = json.loads(response.choices[0].message.content)
                    suggested_labels = result.get("labels", [])
                    reasoning = result.get("reasoning", "")

                    print(f"💡 Suggested: {', '.join(suggested_labels)}")
                    print(f"   Reasoning: {reasoning}")

                    choice = input("\nApply these labels? (y/n/q): ").lower().strip()
                    if choice in ['y', 'yes']:
                        approved_updates.append({
                            "task_id": task.get("id"),
                            "task_content": content,
                            "labels": suggested_labels
                        })
                        print("✅ Approved")
                    elif choice in ['q', 'quit']:
                        print("\n⏸️  Stopped label suggestions")
                        break
                    else:
                        print("⏭️  Skipped")

                except Exception as e:
                    print(f"❌ Error generating suggestion: {e}")
                    continue

            # Apply approved updates
            if approved_updates:
                print(f"\n{'='*70}")
                print(f"Applying {len(approved_updates)} label updates...")
                print('='*70)

                success_count = 0
                for update in approved_updates:
                    task_id = update["task_id"]
                    labels = update["labels"]

                    success = self.agent.client.update_task(task_id, {"labels": labels})
                    if success:
                        success_count += 1
                        print(f"✅ Updated: {update['task_content'][:50]} -> {', '.join(labels)}")
                    else:
                        print(f"❌ Failed: {update['task_content'][:50]}")

                print(f"\n✨ Successfully updated {success_count}/{len(approved_updates)} tasks")
            else:
                print("\nNo labels were added.")

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

        # Common stop words to ignore in matching
        stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
                     'of', 'with', 'by', 'from', 'as', 'is', 'was', 'are', 'be', 'been',
                     'how', 'its', 'it', 'this', 'that', 'these', 'those', 'help', 'me', 'my'}

        # Try exact substring match first (highest confidence)
        # Try recently shown tasks first (for better context)
        for task in self.last_shown_tasks:
            task_content_lower = task.get("content", "").lower()
            if identifier_lower in task_content_lower:
                return task

        # Try all tasks for exact substring match
        all_tasks = self.agent.client.fetch_tasks()
        for task in all_tasks:
            task_content_lower = task.get("content", "").lower()
            if identifier_lower in task_content_lower:
                return task

        # Try multi-word matching (lower confidence)
        # Only do this if identifier has at least 2 significant words
        identifier_words = [w for w in identifier_lower.split() if w not in stop_words and len(w) > 2]
        if len(identifier_words) >= 2:
            # Try recently shown tasks
            best_match = None
            best_score = 0
            for task in self.last_shown_tasks:
                task_content_lower = task.get("content", "").lower()
                matches = sum(1 for word in identifier_words if word in task_content_lower)
                # Require ALL identifier words to match (not just 2)
                if matches == len(identifier_words) and matches > best_score:
                    best_match = task
                    best_score = matches

            if best_match:
                return best_match

            # Try all tasks
            for task in all_tasks:
                task_content_lower = task.get("content", "").lower()
                matches = sum(1 for word in identifier_words if word in task_content_lower)
                # Require ALL identifier words to match (not just 2)
                if matches == len(identifier_words) and matches > best_score:
                    best_match = task
                    best_score = matches

            if best_match:
                return best_match

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

        # Handle "these", "those", "them" - refers to recently shown tasks
        if any(word in identifier_lower for word in ["these", "those", "them", "they"]):
            if self.last_shown_tasks:
                # If a number is mentioned, use that, otherwise use all shown tasks
                return self.last_shown_tasks[:count] if count > 1 else self.last_shown_tasks
            return []

        # Handle "top N" or "first N"
        if ("top" in identifier_lower or "first" in identifier_lower) and self.last_shown_tasks:
            return self.last_shown_tasks[:count]

        # Handle "all" or general task references
        if "all" in identifier_lower or "my tasks" in identifier_lower:
            if "overdue" in identifier_lower:
                return self.agent.get_tasks_filtered("overdue")
            elif "no date" in identifier_lower or "without date" in identifier_lower:
                return self.agent.get_tasks_filtered("no_date")
            elif "all tasks" in identifier_lower:
                return self.agent.get_tasks_filtered("all")
            elif self.last_shown_tasks:
                return self.last_shown_tasks

        # Handle "tasks without dates" or similar
        if "without" in identifier_lower and ("date" in identifier_lower or "dates" in identifier_lower):
            return self.agent.get_tasks_filtered("no_date")

        # Try to match task names (e.g., "Amazon and Kwang IBKR")
        # Also handle numbered lists like "1) task one 2) task two"
        if " and " in identifier_lower or "," in identifier_lower or any(f"{i})" in identifier_lower for i in range(1, 10)):
            # Handle numbered lists: "1) task 2) task" format
            if any(f"{i})" in identifier_lower for i in range(1, 10)):
                import re
                # Split by numbered patterns like "1)", "2)", etc.
                parts = re.split(r'\d+\)', identifier_lower)
                task_names = [name.strip() for name in parts if name.strip()]
            else:
                # Split by "and" or comma
                task_names = [name.strip() for name in identifier_lower.replace(" and ", ",").split(",")]

            matched_tasks = []
            for name in task_names:
                task = self._identify_task(name)
                if task and task not in matched_tasks:
                    matched_tasks.append(task)
            if matched_tasks:
                return matched_tasks

        # Try to match a single specific task by name
        # This handles cases like "send email to iras" or "amazon account"
        task = self._identify_task(identifier)
        if task:
            return [task]

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

    def _load_history(self):
        """Load conversation history from file."""
        try:
            if self.history_file.exists():
                with open(self.history_file, 'r') as f:
                    data = json.load(f)
                    # Restore router's conversation history
                    self.router.conversation_history = data.get("conversation_history", [])
                    print(f"📚 Loaded {len(self.router.conversation_history)//2} previous conversations")
        except Exception as e:
            print(f"⚠️  Could not load history: {e}")

    def _save_history(self):
        """Save conversation history to file."""
        try:
            data = {
                "conversation_history": self.router.conversation_history,
                "last_updated": datetime.now().isoformat()
            }
            with open(self.history_file, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            print(f"⚠️  Could not save history: {e}")

    def _conversational_fallback(self, user_input: str) -> str:
        """
        When no function matches, have an intelligent conversation.

        Args:
            user_input: User's input

        Returns:
            AI-generated response
        """
        # Build context about available capabilities
        system_context = """You are a helpful Todoist task management assistant.

You have these capabilities:
- Show tasks (today, all, overdue, upcoming, tasks without due dates)
- Prioritize tasks using Eisenhower matrix
- Polish/improve task names and descriptions
- Suggest due dates for tasks
- Categorize tasks by urgency/importance
- Analyze and manage task labels
- Update individual task properties

When the user asks something you can't directly do:
1. Try to understand what they want
2. Ask clarifying questions
3. Suggest how you CAN help them achieve their goal
4. Be friendly and conversational

Important: Don't make up capabilities you don't have. If unsure, ask the user to clarify or suggest alternatives."""

        # Get last few messages for context
        recent_history = self.router.conversation_history[-6:] if self.router.conversation_history else []

        messages = [{"role": "system", "content": system_context}]
        messages.extend(recent_history)
        messages.append({"role": "user", "content": user_input})

        try:
            response = self.openai_client.chat.completions.create(
                model=self.openai_model,
                messages=messages,
                max_tokens=300,
                temperature=0.7
            )

            ai_response = response.choices[0].message.content

            # Save to history
            self.router.add_to_history(user_input, ai_response)
            self._save_history()

            return ai_response

        except Exception as e:
            return f"I'm having trouble understanding that. Could you try rephrasing? (Error: {e})\n\nType 'help' to see what I can do!"

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
