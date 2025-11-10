"""
Todoist AI Agent

Main orchestrator that coordinates task fetching, analysis, and prioritization.
"""

from typing import List, Dict, Any, Optional
from datetime import datetime
from todoist_client import TodoistClient
from task_analyzer import TaskAnalyzer
from prioritizer import TaskPrioritizer
from task_polisher import TaskPolisher
from smart_scheduler import SmartScheduler
from task_updater import TaskUpdater

# Import MCPUpdater from examples (for Claude Code integration)
try:
    from examples.mcp_updater import MCPUpdater
except ImportError:
    # Fallback if examples not accessible
    MCPUpdater = None


class TodoistAIAgent:
    """AI agent for managing Todoist tasks intelligently."""

    def __init__(self, use_mock: bool = False):
        """
        Initialize the AI agent.

        Args:
            use_mock: If True, use mock data instead of real Todoist API
        """
        self.client = TodoistClient(use_mock=use_mock)
        self.analyzer = TaskAnalyzer()
        self.prioritizer = TaskPrioritizer()
        self.task_updater = TaskUpdater()

        # Initialize new features (may be None if API key not set)
        try:
            self.polisher = TaskPolisher()
            self.scheduler = SmartScheduler()
        except ValueError:
            # API key not set - polishing features disabled
            self.polisher = None
            self.scheduler = None

        # Initialize MCPUpdater (may be None if not available)
        self.updater = MCPUpdater() if MCPUpdater else None

    def run_analysis(self) -> Dict[str, Any]:
        """
        Run full task analysis and generate focus plan.

        Returns:
            Dictionary containing analyzed tasks and focus plan
        """
        print("🤖 Todoist AI Agent starting...")
        print()

        # Step 1: Fetch tasks
        print("📥 Fetching tasks from Todoist...")
        raw_tasks = self.client.fetch_tasks()
        print(f"   Found {len(raw_tasks)} tasks")
        print()

        # Step 2: Normalize tasks
        normalized_tasks = [self.client.normalize_task(task) for task in raw_tasks]

        # Step 3: Analyze each task
        print("🔍 Analyzing tasks...")
        analyzed_tasks = []
        for task in normalized_tasks:
            analysis = self.analyzer.analyze_task(task)
            analyzed_tasks.append(analysis)
        print(f"   Analyzed {len(analyzed_tasks)} tasks")
        print()

        # Step 4: Create focus plan
        print("🎯 Generating daily focus plan...")
        focus_plan = self.prioritizer.create_daily_focus_plan(analyzed_tasks, max_tasks=5)
        print()

        return {
            "raw_tasks": raw_tasks,
            "analyzed_tasks": analyzed_tasks,
            "focus_plan": focus_plan
        }

    def generate_report(self, report_type: str = "focus") -> str:
        """
        Generate a formatted report.

        Args:
            report_type: Type of report ("focus" or "full")

        Returns:
            Formatted report string
        """
        results = self.run_analysis()
        focus_plan = results["focus_plan"]

        if report_type == "focus":
            return self.prioritizer.generate_focus_summary(focus_plan)
        elif report_type == "full":
            return self.prioritizer.generate_full_report(focus_plan)
        else:
            return "Invalid report type. Choose 'focus' or 'full'."

    def get_top_priorities(self, n: int = 3) -> List[Dict[str, Any]]:
        """
        Get the top N priority tasks.

        Args:
            n: Number of top tasks to return

        Returns:
            List of top priority task analyses
        """
        results = self.run_analysis()
        focus_plan = results["focus_plan"]
        return focus_plan["focus_tasks"][:n]

    def get_tasks_by_quadrant(self, quadrant: str) -> List[Dict[str, Any]]:
        """
        Get tasks in a specific Eisenhower quadrant.

        Args:
            quadrant: Quadrant name (Q1, Q2, Q3, or Q4)

        Returns:
            List of tasks in that quadrant
        """
        results = self.run_analysis()
        focus_plan = results["focus_plan"]

        quadrant_map = {
            "Q1": "Q1_do_first",
            "Q2": "Q2_schedule",
            "Q3": "Q3_delegate",
            "Q4": "Q4_consider"
        }

        key = quadrant_map.get(quadrant.upper())
        if key:
            return focus_plan["by_quadrant"][key]
        else:
            return []

    def suggest_updates(self) -> List[Dict[str, Any]]:
        """
        Suggest task updates (due dates, priorities) based on analysis.

        Returns:
            List of suggested updates
        """
        results = self.run_analysis()
        analyzed_tasks = results["analyzed_tasks"]
        suggestions = []

        for task in analyzed_tasks:
            # Suggest adding due dates to important tasks without them
            if not task["has_due_date"] and task["importance_score"] > 6:
                suggestions.append({
                    "task_id": task["task_id"],
                    "task_content": task["task_content"],
                    "suggestion": "Add a due date",
                    "reason": "This task is important but has no deadline",
                    "action": {
                        "type": "add_due_date",
                        "suggested_date": None  # Could be calculated
                    }
                })

            # Suggest increasing priority for urgent tasks
            if task["urgency_score"] >= 8 and task["todoist_priority"] < 3:
                suggestions.append({
                    "task_id": task["task_id"],
                    "task_content": task["task_content"],
                    "suggestion": "Increase priority",
                    "reason": "This task is urgent but has low Todoist priority",
                    "action": {
                        "type": "update_priority",
                        "current_priority": task["todoist_priority"],
                        "suggested_priority": 4
                    }
                })

        return suggestions

    def apply_update(self, task_id: str, updates: Dict[str, Any]) -> bool:
        """
        Apply an update to a task in Todoist.

        Args:
            task_id: Task ID to update
            updates: Dictionary of updates to apply

        Returns:
            True if successful, False otherwise
        """
        return self.client.update_task(task_id, updates)

    def polish_tasks(self, tasks: Optional[List[Dict[str, Any]]] = None,
                    min_quality: int = 50) -> List[Dict[str, Any]]:
        """
        Polish task names and descriptions using AI.

        Args:
            tasks: List of tasks to polish (fetches if None)
            min_quality: Minimum quality score threshold

        Returns:
            List of polish suggestions
        """
        if self.polisher is None:
            raise ValueError("Task polisher not available. Set ANTHROPIC_API_KEY.")

        if tasks is None:
            raw_tasks = self.client.fetch_tasks()
            tasks = [self.client.normalize_task(task) for task in raw_tasks]

        # Identify tasks needing polish
        needs_polish = self.polisher.identify_tasks_needing_polish(tasks, min_quality)

        # Generate polish suggestions
        if needs_polish:
            return self.polisher.polish_tasks_batch(needs_polish)

        return []

    def suggest_due_dates(self, tasks: Optional[List[Dict[str, Any]]] = None) -> List[Dict[str, Any]]:
        """
        Suggest due dates for tasks that don't have them.

        Args:
            tasks: List of tasks (fetches if None)

        Returns:
            List of due date suggestions
        """
        if self.scheduler is None:
            raise ValueError("Smart scheduler not available. Set ANTHROPIC_API_KEY.")

        if tasks is None:
            raw_tasks = self.client.fetch_tasks()
            tasks = [self.client.normalize_task(task) for task in raw_tasks]

        return self.scheduler.suggest_due_dates_batch(tasks)

    def get_task_quality_report(self, tasks: Optional[List[Dict[str, Any]]] = None) -> Dict[str, Any]:
        """
        Generate a quality report for all tasks.

        Args:
            tasks: List of tasks (fetches if None)

        Returns:
            Quality report dictionary
        """
        if self.polisher is None:
            raise ValueError("Task polisher not available. Set ANTHROPIC_API_KEY.")

        if tasks is None:
            raw_tasks = self.client.fetch_tasks()
            tasks = [self.client.normalize_task(task) for task in raw_tasks]

        quality_scores = []
        for task in tasks:
            quality = self.polisher.get_quality_score(task)
            quality_scores.append(quality)

        # Sort by quality score (worst first)
        quality_scores.sort(key=lambda x: x["percentage"])

        # Calculate stats
        total_tasks = len(quality_scores)
        avg_quality = sum(q["percentage"] for q in quality_scores) / total_tasks if total_tasks > 0 else 0
        needs_attention = sum(1 for q in quality_scores if q["needs_attention"])

        return {
            "total_tasks": total_tasks,
            "average_quality": round(avg_quality, 1),
            "tasks_needing_attention": needs_attention,
            "quality_scores": quality_scores,
            "worst_tasks": quality_scores[:5]  # Top 5 worst
        }

    def prepare_updates(self, polish_results: List[Dict[str, Any]],
                       schedule_results: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Prepare update requests from polish and schedule results.

        Args:
            polish_results: Results from polish_tasks()
            schedule_results: Results from suggest_due_dates()

        Returns:
            List of formatted update requests
        """
        updates = []

        # Add polish updates
        polish_updates = self.updater.create_polish_updates(polish_results)
        updates.extend(polish_updates)

        # Add schedule updates
        schedule_updates = self.updater.create_scheduling_updates(schedule_results)
        updates.extend(schedule_updates)

        return updates

    def get_today_tasks(self) -> Dict[str, Any]:
        """
        Get tasks organized by today's status (overdue, due today, upcoming).

        Returns:
            Dictionary with categorized tasks
        """
        today = datetime.now().strftime("%Y-%m-%d")

        # Fetch all tasks
        raw_tasks = self.client.fetch_tasks()

        # Categorize
        overdue = []
        due_today = []
        upcoming = []
        no_date = []

        for task in raw_tasks:
            due_date = task.get('due', {}).get('date') if task.get('due') else None

            if not due_date:
                no_date.append(task)
            elif due_date < today:
                overdue.append(task)
            elif due_date == today:
                due_today.append(task)
            else:
                upcoming.append(task)

        return {
            "today": today,
            "overdue": overdue,
            "due_today": due_today,
            "upcoming": upcoming[:7],  # Next 7 upcoming
            "no_date": no_date,
            "total": len(raw_tasks)
        }

    def categorize_by_quadrant(self, quadrant: Optional[str] = None) -> Dict[str, Any]:
        """
        Categorize all tasks by Eisenhower matrix quadrants.

        Args:
            quadrant: Specific quadrant to return (Q1, Q2, Q3, Q4) or None for all

        Returns:
            Dictionary with categorized tasks
        """
        results = self.run_analysis()
        focus_plan = results["focus_plan"]

        if quadrant:
            quadrant_map = {
                "Q1": "Q1_do_first",
                "Q2": "Q2_schedule",
                "Q3": "Q3_delegate",
                "Q4": "Q4_consider"
            }
            key = quadrant_map.get(quadrant.upper())
            if key:
                return {
                    "quadrant": quadrant,
                    "tasks": focus_plan["by_quadrant"][key]
                }
            else:
                return {"error": f"Invalid quadrant: {quadrant}"}

        return {
            "all_quadrants": focus_plan["by_quadrant"],
            "statistics": focus_plan["statistics"]
        }

    def get_tasks_filtered(self, filter_type: str) -> List[Dict[str, Any]]:
        """
        Get tasks filtered by specific criteria.

        Args:
            filter_type: Filter type (today, all, overdue, upcoming, no_date)

        Returns:
            List of filtered tasks
        """
        if filter_type == "today":
            today_data = self.get_today_tasks()
            return today_data["due_today"]
        elif filter_type == "overdue":
            today_data = self.get_today_tasks()
            return today_data["overdue"]
        elif filter_type == "upcoming":
            today_data = self.get_today_tasks()
            return today_data["upcoming"]
        elif filter_type == "no_date":
            today_data = self.get_today_tasks()
            return today_data["no_date"]
        elif filter_type == "all":
            return self.client.fetch_tasks()
        else:
            return []

    def update_single_task(self, task_id: str, updates: Dict[str, Any],
                          preview_only: bool = False) -> Dict[str, Any]:
        """
        Update a single task with preview.

        Args:
            task_id: Task ID to update
            updates: Dictionary of updates
            preview_only: If True, only return preview without applying

        Returns:
            Dictionary with preview and success status
        """
        # Find the task
        all_tasks = self.client.fetch_tasks()
        task = next((t for t in all_tasks if str(t.get("id")) == str(task_id)), None)

        if not task:
            return {"error": f"Task not found: {task_id}"}

        # Validate updates
        is_valid, error_msg = self.task_updater.validate_updates(updates)
        if not is_valid:
            return {"error": error_msg}

        # Create preview
        preview = self.task_updater.create_update_preview(task, updates)

        if preview_only or not preview["changes"]:
            return {"preview": preview, "applied": False}

        # Save original state
        self.task_updater.save_original_state(task)

        # Apply updates
        success = self.client.update_task(task_id, updates)

        return {
            "preview": preview,
            "applied": success,
            "success": success
        }

    def polish_and_update(self, task_ids: List[str],
                         preview_only: bool = False) -> List[Dict[str, Any]]:
        """
        Polish tasks and optionally apply updates.

        Args:
            task_ids: List of task IDs to polish
            preview_only: If True, only generate previews

        Returns:
            List of results for each task
        """
        if not self.polisher:
            return [{"error": "Task polisher not available (OpenAI API key not set)"}]

        all_tasks = self.client.fetch_tasks()
        results = []

        for task_id in task_ids:
            task = next((t for t in all_tasks if str(t.get("id")) == str(task_id)), None)

            if not task:
                results.append({"error": f"Task not found: {task_id}"})
                continue

            # Polish the task
            polish_result = self.polisher.polish_task(task)

            if not polish_result.get("needs_polishing", False):
                results.append({
                    "task_id": task_id,
                    "task_name": task.get("content", ""),
                    "needs_polishing": False,
                    "message": "Task is already well-formatted"
                })
                continue

            # Prepare updates
            updates = {}
            if polish_result["suggested_name"] != task.get("content"):
                updates["content"] = polish_result["suggested_name"]
            if polish_result["suggested_description"] != task.get("description", ""):
                updates["description"] = polish_result["suggested_description"]
            if polish_result.get("extracted_priority"):
                updates["priority"] = polish_result["extracted_priority"]
            if polish_result.get("extracted_labels"):
                # Merge with existing labels
                current_labels = set(task.get("labels", []))
                new_labels = set(polish_result["extracted_labels"])
                updates["labels"] = list(current_labels | new_labels)

            # Create preview
            preview = self.task_updater.create_update_preview(task, updates)

            if preview_only or not updates:
                results.append({
                    "task_id": task_id,
                    "task_name": task.get("content", ""),
                    "preview": preview,
                    "polish_reason": polish_result.get("polishing_reason", ""),
                    "applied": False
                })
            else:
                # Apply updates
                self.task_updater.save_original_state(task)
                success = self.client.update_task(task_id, updates)

                results.append({
                    "task_id": task_id,
                    "task_name": task.get("content", ""),
                    "preview": preview,
                    "polish_reason": polish_result.get("polishing_reason", ""),
                    "applied": success,
                    "success": success
                })

        return results

    def batch_update_tasks(self, task_updates: List[Dict[str, Any]],
                          preview_only: bool = False) -> Dict[str, Any]:
        """
        Update multiple tasks at once.

        Args:
            task_updates: List of {task_id, updates} dictionaries
            preview_only: If True, only generate previews

        Returns:
            Dictionary with batch results
        """
        all_tasks = self.client.fetch_tasks()
        previews = []
        results = []

        for item in task_updates:
            task_id = item.get("task_id")
            updates = item.get("updates", {})

            task = next((t for t in all_tasks if str(t.get("id")) == str(task_id)), None)

            if not task:
                results.append({"task_id": task_id, "error": "Task not found"})
                continue

            preview = self.task_updater.create_update_preview(task, updates)
            previews.append(preview)

            if not preview_only and preview["changes"]:
                self.task_updater.save_original_state(task)
                success = self.client.update_task(task_id, updates)
                results.append({
                    "task_id": task_id,
                    "success": success,
                    "changes": preview["changes"]
                })

        return {
            "total": len(task_updates),
            "previews": previews,
            "results": results,
            "applied": not preview_only
        }
