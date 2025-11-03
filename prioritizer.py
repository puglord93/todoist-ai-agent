"""
Task Prioritizer Module

Generates prioritized task lists and daily focus plans.
"""

from typing import List, Dict, Any
from datetime import datetime
import pytz


class TaskPrioritizer:
    """Creates prioritized lists and focus plans from analyzed tasks."""

    def __init__(self):
        """Initialize the prioritizer."""
        self.today = datetime.now(pytz.UTC)

    def create_prioritized_list(self, analyzed_tasks: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Create a prioritized list of all tasks.

        Args:
            analyzed_tasks: List of task analysis dictionaries

        Returns:
            Sorted list of tasks by priority score (highest first)
        """
        return sorted(
            analyzed_tasks,
            key=lambda x: (
                -x["priority_score"],  # Higher priority first
                x["is_overdue"],  # Overdue tasks first
                x["days_until_due"] if x["days_until_due"] is not None else 9999  # Sooner due dates first
            )
        )

    def create_daily_focus_plan(self, analyzed_tasks: List[Dict[str, Any]],
                               max_tasks: int = 5) -> Dict[str, Any]:
        """
        Create a daily focus plan with the most important tasks.

        Args:
            analyzed_tasks: List of task analysis dictionaries
            max_tasks: Maximum number of tasks to include in focus plan

        Returns:
            Dictionary containing daily focus plan
        """
        # Get prioritized list
        prioritized = self.create_prioritized_list(analyzed_tasks)

        # Split into categories
        do_first = []  # Q1: Urgent & Important
        schedule = []  # Q2: Important, Not Urgent
        delegate = []  # Q3: Urgent, Not Important
        consider = []  # Q4: Neither Urgent nor Important

        for task in prioritized:
            quadrant = task["eisenhower_quadrant"]
            if quadrant.startswith("Q1"):
                do_first.append(task)
            elif quadrant.startswith("Q2"):
                schedule.append(task)
            elif quadrant.startswith("Q3"):
                delegate.append(task)
            else:
                consider.append(task)

        # Build focus plan
        focus_tasks = []

        # 1. Add all Q1 tasks (urgent & important)
        focus_tasks.extend(do_first)

        # 2. Add Q2 tasks (important, not urgent) until we hit max_tasks
        remaining_slots = max_tasks - len(focus_tasks)
        if remaining_slots > 0:
            focus_tasks.extend(schedule[:remaining_slots])

        # 3. If still room, add Q3 tasks
        remaining_slots = max_tasks - len(focus_tasks)
        if remaining_slots > 0:
            focus_tasks.extend(delegate[:remaining_slots])

        # Calculate stats
        total_tasks = len(analyzed_tasks)
        overdue_count = sum(1 for t in analyzed_tasks if t["is_overdue"])
        due_today_count = sum(1 for t in analyzed_tasks if t["days_until_due"] == 0)
        due_this_week_count = sum(1 for t in analyzed_tasks
                                  if t["days_until_due"] is not None and 0 <= t["days_until_due"] <= 7)

        return {
            "date": self.today.strftime("%Y-%m-%d"),
            "focus_tasks": focus_tasks[:max_tasks],
            "statistics": {
                "total_tasks": total_tasks,
                "overdue": overdue_count,
                "due_today": due_today_count,
                "due_this_week": due_this_week_count,
                "q1_count": len(do_first),
                "q2_count": len(schedule),
                "q3_count": len(delegate),
                "q4_count": len(consider)
            },
            "by_quadrant": {
                "Q1_do_first": do_first,
                "Q2_schedule": schedule,
                "Q3_delegate": delegate,
                "Q4_consider": consider
            }
        }

    def generate_focus_summary(self, focus_plan: Dict[str, Any]) -> str:
        """
        Generate a human-readable summary of the daily focus plan.

        Args:
            focus_plan: Daily focus plan dictionary

        Returns:
            Formatted string summary
        """
        lines = []
        stats = focus_plan["statistics"]

        # Header
        lines.append("=" * 60)
        lines.append(f"📋 DAILY FOCUS PLAN - {focus_plan['date']}")
        lines.append("=" * 60)
        lines.append("")

        # Statistics
        lines.append("📊 Task Overview:")
        lines.append(f"   • Total tasks: {stats['total_tasks']}")
        if stats['overdue'] > 0:
            lines.append(f"   • ⚠️  Overdue: {stats['overdue']}")
        if stats['due_today'] > 0:
            lines.append(f"   • 📅 Due today: {stats['due_today']}")
        lines.append(f"   • Due this week: {stats['due_this_week']}")
        lines.append("")

        # Eisenhower breakdown
        lines.append("📈 Task Distribution (Eisenhower Matrix):")
        lines.append(f"   • Q1 (Do First): {stats['q1_count']}")
        lines.append(f"   • Q2 (Schedule): {stats['q2_count']}")
        lines.append(f"   • Q3 (Delegate): {stats['q3_count']}")
        lines.append(f"   • Q4 (Consider): {stats['q4_count']}")
        lines.append("")

        # Focus tasks
        lines.append("🎯 TODAY'S FOCUS TASKS (Top Priority):")
        lines.append("-" * 60)

        if not focus_plan["focus_tasks"]:
            lines.append("   No tasks to focus on today!")
        else:
            for i, task in enumerate(focus_plan["focus_tasks"], 1):
                lines.append(f"\n{i}. {task['task_content']}")
                lines.append(f"   Priority Score: {task['priority_score']}/100")
                lines.append(f"   Quadrant: {task['eisenhower_quadrant']}")

                if task["days_until_due"] is not None:
                    if task["is_overdue"]:
                        lines.append(f"   Due: ⚠️ OVERDUE")
                    elif task["days_until_due"] == 0:
                        lines.append(f"   Due: 📅 TODAY")
                    elif task["days_until_due"] == 1:
                        lines.append(f"   Due: 📅 TOMORROW")
                    else:
                        lines.append(f"   Due: In {task['days_until_due']} days")

                if task["labels"]:
                    lines.append(f"   Labels: {', '.join(task['labels'])}")

                if task["recommendations"]:
                    lines.append(f"   💡 {task['recommendations'][0]}")

        lines.append("")
        lines.append("=" * 60)

        return "\n".join(lines)

    def generate_full_report(self, focus_plan: Dict[str, Any]) -> str:
        """
        Generate a comprehensive report of all tasks by quadrant.

        Args:
            focus_plan: Daily focus plan dictionary

        Returns:
            Formatted string report
        """
        lines = []

        # Add focus summary first
        lines.append(self.generate_focus_summary(focus_plan))
        lines.append("\n")

        # Add detailed breakdown by quadrant
        lines.append("=" * 60)
        lines.append("📑 DETAILED TASK BREAKDOWN BY QUADRANT")
        lines.append("=" * 60)

        quadrants = [
            ("Q1_do_first", "Q1: DO FIRST (Urgent & Important)", "🔥"),
            ("Q2_schedule", "Q2: SCHEDULE (Important, Not Urgent)", "📆"),
            ("Q3_delegate", "Q3: DELEGATE (Urgent, Not Important)", "👥"),
            ("Q4_consider", "Q4: CONSIDER (Neither Urgent nor Important)", "🗑️")
        ]

        for key, title, emoji in quadrants:
            tasks = focus_plan["by_quadrant"][key]
            lines.append(f"\n{emoji} {title}")
            lines.append("-" * 60)

            if not tasks:
                lines.append("   No tasks in this quadrant")
            else:
                for i, task in enumerate(tasks, 1):
                    lines.append(f"\n{i}. {task['task_content']}")
                    lines.append(f"   Score: {task['priority_score']}/100 "
                               f"(Urgency: {task['urgency_score']:.1f}, "
                               f"Importance: {task['importance_score']:.1f})")

                    if task["days_until_due"] is not None:
                        if task["is_overdue"]:
                            lines.append(f"   Due: ⚠️ OVERDUE")
                        elif task["days_until_due"] == 0:
                            lines.append(f"   Due: TODAY")
                        else:
                            lines.append(f"   Due: {task['days_until_due']} days")

                    if task["labels"]:
                        lines.append(f"   Labels: {', '.join(task['labels'])}")

                    if task["recommendations"]:
                        for rec in task["recommendations"]:
                            lines.append(f"   💡 {rec}")

        lines.append("\n" + "=" * 60)
        return "\n".join(lines)
