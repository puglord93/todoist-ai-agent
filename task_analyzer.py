"""
Task Analysis Module

Analyzes tasks based on urgency, importance, labels, and other factors.
Implements the Eisenhower Matrix and other prioritization heuristics.
"""

from typing import Dict, Any, List
from datetime import datetime, timedelta
from dateutil import parser
import pytz


class TaskAnalyzer:
    """Analyzes and scores tasks for prioritization."""

    # Label-based importance weights
    IMPORTANCE_LABELS = {
        "urgent": 10,
        "important": 8,
        "critical": 10,
        "high-priority": 7,
        "bug": 9,
        "deadline": 8
    }

    # Label-based category weights
    CATEGORY_WEIGHTS = {
        "work": 1.2,
        "health": 1.3,
        "family": 1.3,
        "learning": 0.8,
        "personal": 0.9
    }

    def __init__(self):
        """Initialize the task analyzer."""
        self.today = datetime.now(pytz.UTC)

    def analyze_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze a single task and compute various scores.

        Args:
            task: Task dictionary with normalized format

        Returns:
            Analysis dictionary with scores and classifications
        """
        analysis = {
            "task_id": task.get("id"),
            "task_content": task.get("content"),
            "urgency_score": self._calculate_urgency(task),
            "importance_score": self._calculate_importance(task),
            "priority_score": 0,  # Will be calculated below
            "eisenhower_quadrant": "",
            "days_until_due": self._days_until_due(task),
            "is_overdue": self._is_overdue(task),
            "has_due_date": task.get("due_date") is not None,
            "todoist_priority": task.get("priority", 1),
            "labels": task.get("labels", []),
            "recommendations": []
        }

        # Calculate overall priority score (0-100)
        analysis["priority_score"] = self._calculate_priority_score(
            analysis["urgency_score"],
            analysis["importance_score"],
            analysis["todoist_priority"]
        )

        # Classify into Eisenhower Matrix
        analysis["eisenhower_quadrant"] = self._classify_eisenhower(
            analysis["urgency_score"],
            analysis["importance_score"]
        )

        # Generate recommendations
        analysis["recommendations"] = self._generate_recommendations(task, analysis)

        return analysis

    def _calculate_urgency(self, task: Dict[str, Any]) -> float:
        """
        Calculate urgency score (0-10) based on due date and labels.

        Args:
            task: Task dictionary

        Returns:
            Urgency score between 0 and 10
        """
        score = 0.0

        # Check for urgency labels
        labels = [label.lower() for label in task.get("labels", [])]
        if "urgent" in labels or "critical" in labels:
            score += 5.0

        # Calculate based on due date
        days_until_due = self._days_until_due(task)
        if days_until_due is not None:
            if days_until_due < 0:
                # Overdue
                score += 10.0
            elif days_until_due == 0:
                # Due today
                score += 9.0
            elif days_until_due == 1:
                # Due tomorrow
                score += 8.0
            elif days_until_due <= 3:
                # Due within 3 days
                score += 6.0
            elif days_until_due <= 7:
                # Due within a week
                score += 4.0
            elif days_until_due <= 14:
                # Due within 2 weeks
                score += 2.0
            else:
                # Due later
                score += 1.0

        # Cap at 10
        return min(score, 10.0)

    def _calculate_importance(self, task: Dict[str, Any]) -> float:
        """
        Calculate importance score (0-10) based on labels, priority, and context.

        Args:
            task: Task dictionary

        Returns:
            Importance score between 0 and 10
        """
        score = 0.0

        # Base score from Todoist priority (1-4, where 4 is highest)
        todoist_priority = task.get("priority", 1)
        score += (todoist_priority / 4.0) * 4.0

        # Check importance labels
        labels = [label.lower() for label in task.get("labels", [])]
        for label in labels:
            if label in self.IMPORTANCE_LABELS:
                score += self.IMPORTANCE_LABELS[label] / 10.0

        # Apply category weight multiplier
        for label in labels:
            if label in self.CATEGORY_WEIGHTS:
                score *= self.CATEGORY_WEIGHTS[label]
                break  # Only apply one category weight

        # Cap at 10
        return min(score, 10.0)

    def _calculate_priority_score(self, urgency: float, importance: float,
                                  todoist_priority: int) -> float:
        """
        Calculate overall priority score (0-100).

        Args:
            urgency: Urgency score (0-10)
            importance: Importance score (0-10)
            todoist_priority: Todoist priority (1-4)

        Returns:
            Priority score between 0 and 100
        """
        # Weighted combination: urgency is slightly more important for immediate action
        score = (urgency * 0.6 + importance * 0.4) * 10
        return round(score, 2)

    def _classify_eisenhower(self, urgency: float, importance: float) -> str:
        """
        Classify task into Eisenhower Matrix quadrant.

        Args:
            urgency: Urgency score (0-10)
            importance: Importance score (0-10)

        Returns:
            Quadrant name
        """
        urgent = urgency >= 5.0
        important = importance >= 5.0

        if urgent and important:
            return "Q1: Do First (Urgent & Important)"
        elif not urgent and important:
            return "Q2: Schedule (Important, Not Urgent)"
        elif urgent and not important:
            return "Q3: Delegate (Urgent, Not Important)"
        else:
            return "Q4: Eliminate (Neither Urgent nor Important)"

    def _days_until_due(self, task: Dict[str, Any]) -> int | None:
        """
        Calculate days until task is due.

        Args:
            task: Task dictionary

        Returns:
            Number of days until due, or None if no due date
        """
        due_date_str = task.get("due_date")
        if not due_date_str:
            return None

        try:
            due_date = parser.parse(due_date_str)
            if due_date.tzinfo is None:
                due_date = pytz.UTC.localize(due_date)

            today_start = self.today.replace(hour=0, minute=0, second=0, microsecond=0)
            delta = due_date - today_start
            return delta.days
        except Exception:
            return None

    def _is_overdue(self, task: Dict[str, Any]) -> bool:
        """
        Check if task is overdue.

        Args:
            task: Task dictionary

        Returns:
            True if overdue, False otherwise
        """
        days_until_due = self._days_until_due(task)
        return days_until_due is not None and days_until_due < 0

    def _generate_recommendations(self, task: Dict[str, Any],
                                 analysis: Dict[str, Any]) -> List[str]:
        """
        Generate actionable recommendations for the task.

        Args:
            task: Task dictionary
            analysis: Analysis results

        Returns:
            List of recommendation strings
        """
        recommendations = []

        if analysis["is_overdue"]:
            recommendations.append("⚠️ This task is overdue. Consider completing it immediately or rescheduling.")

        if analysis["days_until_due"] == 0:
            recommendations.append("📅 Due today! Prioritize this task.")

        if analysis["days_until_due"] == 1:
            recommendations.append("📅 Due tomorrow. Plan to complete soon.")

        if analysis["eisenhower_quadrant"].startswith("Q1"):
            recommendations.append("🔥 High priority: Do this first!")

        if analysis["eisenhower_quadrant"].startswith("Q2"):
            recommendations.append("📆 Important but not urgent: Schedule a specific time to work on this.")

        if analysis["eisenhower_quadrant"].startswith("Q3"):
            recommendations.append("👥 Consider delegating this task if possible.")

        if analysis["eisenhower_quadrant"].startswith("Q4"):
            recommendations.append("🗑️ Low priority: Consider if this task is still necessary.")

        if not analysis["has_due_date"] and analysis["importance_score"] > 5:
            recommendations.append("📅 Consider adding a due date to this important task.")

        return recommendations
