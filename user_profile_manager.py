"""
User Profile Manager - Learns from user behavior and adapts

This module tracks user interactions and gradually builds a profile
to make the agent more personalized and effective.
"""
import json
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
from pathlib import Path
from dataclasses import dataclass, asdict
from tools_registry import ToolsRegistry


@dataclass
class InteractionEvent:
    """Record of a single user interaction."""
    timestamp: str
    action: str  # e.g., "polish_tasks", "update_tasks", "accept_preview"
    task_count: int
    success: bool
    user_feedback: Optional[str] = None
    time_taken_seconds: Optional[float] = None


@dataclass
class TaskCompletion:
    """Record of task completion or abandonment."""
    timestamp: str
    task_id: str
    task_content: str
    planned_duration_minutes: Optional[int]
    actual_duration_minutes: Optional[int]
    completed: bool
    abandoned: bool
    quality_score: Optional[float] = None


@dataclass
class UserPreferences:
    """User preferences that adapt over time."""
    work_hours: str = "09:00-18:00"
    timezone: str = "Asia/Singapore"
    max_deep_tasks_per_day: int = 3
    likes_batching: bool = True
    prefers_mornings_for_deep_work: bool = True
    avoid_evenings_for_admin: bool = True
    polish_aggressiveness: str = "moderate"  # conservative, moderate, aggressive
    typical_task_completion_rate: float = 0.75
    preferred_focus_blocks: List[str] = None

    def __post_init__(self):
        if self.preferred_focus_blocks is None:
            self.preferred_focus_blocks = ["09:00-11:00", "14:00-16:00"]


class UserProfileManager:
    """
    Manages user profile and learns from behavior.

    This class tracks:
    - User interactions (what they do, what succeeds)
    - Task completion patterns
    - Time estimation accuracy
    - Preferences and adapts them
    """

    def __init__(self, profile_file: Optional[Path] = None):
        """
        Initialize the profile manager.

        Args:
            profile_file: Path to profile JSON file
        """
        self.profile_file = profile_file or Path.home() / ".todoist_agent_profile.json"
        self.interactions_file = Path.home() / ".todoist_agent_interactions.json"
        self.completions_file = Path.home() / ".todoist_agent_completions.json"

        # Load existing data
        self.preferences = self._load_preferences()
        self.interactions: List[InteractionEvent] = self._load_interactions()
        self.completions: List[TaskCompletion] = self._load_completions()

    def _load_preferences(self) -> UserPreferences:
        """Load user preferences from file."""
        if self.profile_file.exists():
            try:
                data = json.loads(self.profile_file.read_text())
                return UserPreferences(**data)
            except Exception as e:
                print(f"Warning: Could not load profile: {e}")

        return UserPreferences()

    def _load_interactions(self) -> List[InteractionEvent]:
        """Load interaction history."""
        if self.interactions_file.exists():
            try:
                data = json.loads(self.interactions_file.read_text())
                return [InteractionEvent(**event) for event in data]
            except Exception as e:
                print(f"Warning: Could not load interactions: {e}")

        return []

    def _load_completions(self) -> List[TaskCompletion]:
        """Load completion history."""
        if self.completions_file.exists():
            try:
                data = json.loads(self.completions_file.read_text())
                return [TaskCompletion(**completion) for completion in data]
            except Exception as e:
                print(f"Warning: Could not load completions: {e}")

        return []

    def _save_all(self):
        """Save all data to files."""
        try:
            self.profile_file.write_text(json.dumps(asdict(self.preferences), indent=2))
            self.interactions_file.write_text(json.dumps([asdict(i) for i in self.interactions], indent=2))
            self.completions_file.write_text(json.dumps([asdict(c) for c in self.completions], indent=2))
        except Exception as e:
            print(f"Warning: Could not save profile data: {e}")

    def record_interaction(self, action: str, task_count: int, success: bool,
                          user_feedback: Optional[str] = None,
                          time_taken_seconds: Optional[float] = None):
        """
        Record a user interaction.

        Args:
            action: What action was taken
            task_count: How many tasks were affected
            success: Whether it was successful
            user_feedback: Optional user feedback
            time_taken_seconds: How long it took
        """
        event = InteractionEvent(
            timestamp=datetime.now().isoformat(),
            action=action,
            task_count=task_count,
            success=success,
            user_feedback=user_feedback,
            time_taken_seconds=time_taken_seconds
        )

        self.interactions.append(event)

        # Keep only last 1000 interactions
        if len(self.interactions) > 1000:
            self.interactions = self.interactions[-1000:]

        self._adapt_from_interactions()
        self._save_all()

    def record_task_completion(self, task_id: str, task_content: str,
                               planned_duration_minutes: Optional[int] = None,
                               actual_duration_minutes: Optional[int] = None,
                               completed: bool = True,
                               abandoned: bool = False,
                               quality_score: Optional[float] = None):
        """
        Record task completion or abandonment.

        Args:
            task_id: Task ID
            task_content: Task name
            planned_duration_minutes: How long user planned
            actual_duration_minutes: How long it actually took
            completed: Whether task was completed
            abandoned: Whether task was abandoned
            quality_score: Quality score at completion
        """
        completion = TaskCompletion(
            timestamp=datetime.now().isoformat(),
            task_id=task_id,
            task_content=task_content,
            planned_duration_minutes=planned_duration_minutes,
            actual_duration_minutes=actual_duration_minutes,
            completed=completed,
            abandoned=abandoned,
            quality_score=quality_score
        )

        self.completions.append(completion)

        # Keep only last 500 completions
        if len(self.completions) > 500:
            self.completions = self.completions[-500:]

        self._adapt_from_completions()
        self._save_all()

    def _adapt_from_interactions(self):
        """Adapt preferences based on interaction patterns."""
        if len(self.interactions) < 10:
            return

        recent_interactions = [i for i in self.interactions
                              if datetime.fromisoformat(i.timestamp) > datetime.now() - timedelta(days=30)]

        if not recent_interactions:
            return

        # Analyze polish acceptance rate
        polish_actions = [i for i in recent_interactions if i.action == "polish_tasks"]
        if polish_actions:
            acceptance_rate = sum(1 for i in polish_actions if i.success) / len(polish_actions)

            if acceptance_rate > 0.8:
                self.preferences.polish_aggressiveness = "aggressive"
            elif acceptance_rate < 0.4:
                self.preferences.polish_aggressiveness = "conservative"
            else:
                self.preferences.polish_aggressiveness = "moderate"

        # Analyze batch size preferences
        avg_batch_size = sum(i.task_count for i in recent_interactions if i.action == "update_tasks") / max(1, len([i for i in recent_interactions if i.action == "update_tasks"]))

        if avg_batch_size > 10:
            self.preferences.likes_batching = True
        elif avg_batch_size < 3:
            self.preferences.likes_batching = False

    def _adapt_from_completions(self):
        """Adapt preferences based on completion patterns."""
        if len(self.completions) < 5:
            return

        recent_completions = [c for c in self.completions
                             if datetime.fromisoformat(c.timestamp) > datetime.now() - timedelta(days=30)]

        if not recent_completions:
            return

        # Calculate actual completion rate
        completed_tasks = [c for c in recent_completions if c.completed]
        completion_rate = len(completed_tasks) / len(recent_completions)

        # Update completion rate (weighted average)
        self.preferences.typical_task_completion_rate = (self.preferences.typical_task_completion_rate * 0.7) + (completion_rate * 0.3)

        # Analyze time estimation accuracy
        tasks_with_duration = [c for c in recent_completions
                              if c.planned_duration_minutes and c.actual_duration_minutes]

        if tasks_with_duration:
            errors = [abs(c.actual_duration_minutes - c.planned_duration_minutes) / c.planned_duration_minutes
                     for c in tasks_with_duration]
            avg_error = sum(errors) / len(errors)

            # If consistently underestimating, reduce max_deep_tasks
            if avg_error > 0.5:  # 50% error
                self.preferences.max_deep_tasks_per_day = max(2, self.preferences.max_deep_tasks_per_day - 1)
            elif avg_error < 0.2:  # Less than 20% error
                self.preferences.max_deep_tasks_per_day = min(5, self.preferences.max_deep_tasks_per_day + 1)

    def get_adaptive_suggestion(self, action: str, current_value: Any) -> Any:
        """
        Get an adaptive suggestion based on user patterns.

        Args:
            action: The action being considered
            current_value: Current value for comparison

        Returns:
            Suggested value (may be same as current)
        """
        if len(self.completions) < 5:
            return current_value

        recent_completions = [c for c in self.completions
                             if datetime.fromisoformat(c.timestamp) > datetime.now() - timedelta(days=7)]

        if not recent_completions:
            return current_value

        # Example: Suggest number of tasks to process based on completion rate
        if action == "polish_task_count":
            completion_rate = sum(1 for c in recent_completions if c.completed) / len(recent_completions)
            if completion_rate < 0.5:
                return min(3, current_value)  # Conservative
            elif completion_rate > 0.8:
                return max(10, current_value)  # Aggressive
            return current_value

        # Example: Suggest quality threshold based on acceptance patterns
        if action == "polish_quality_threshold":
            polish_events = [i for i in self.interactions if i.action == "polish_tasks"]
            if polish_events:
                acceptance_rate = sum(1 for e in polish_events if e.success) / len(polish_events)
                if acceptance_rate < 0.3:
                    return max(70, current_value)  # Higher threshold (only polish really bad tasks)
                elif acceptance_rate > 0.9:
                    return min(30, current_value)  # Lower threshold (user wants aggressive polishing)

        return current_value

    def get_preferences(self) -> Dict[str, Any]:
        """Get current user preferences."""
        return asdict(self.preferences)

    def update_preferences(self, updates: Dict[str, Any]):
        """Update user preferences manually."""
        current = asdict(self.preferences)
        current.update(updates)
        self.preferences = UserPreferences(**current)
        self._save_all()

    def get_insights(self) -> Dict[str, Any]:
        """
        Generate insights about user patterns.

        Returns:
            Dictionary of insights
        """
        if not self.interactions and not self.completions:
            return {"message": "Not enough data for insights yet"}

        insights = {
            "total_interactions": len(self.interactions),
            "total_completions": len(self.completions),
            "preferences": asdict(self.preferences)
        }

        # Recent completion rate
        recent_completions = [c for c in self.completions
                             if datetime.fromisoformat(c.timestamp) > datetime.now() - timedelta(days=30)]

        if recent_completions:
            completion_rate = sum(1 for c in recent_completions if c.completed) / len(recent_completions)
            insights["30_day_completion_rate"] = round(completion_rate * 100, 1)

        # Polish acceptance rate
        polish_events = [i for i in self.interactions if i.action == "polish_tasks"]
        if polish_events:
            acceptance_rate = sum(1 for e in polish_events if e.success) / len(polish_events)
            insights["polish_acceptance_rate"] = round(acceptance_rate * 100, 1)

        # Most common actions
        if self.interactions:
            action_counts = {}
            for i in self.interactions:
                action_counts[i.action] = action_counts.get(i.action, 0) + 1
            insights["top_actions"] = sorted(action_counts.items(), key=lambda x: x[1], reverse=True)[:5]

        return insights

    def export_data(self, file_path: Path):
        """Export all profile data to a file."""
        export_data = {
            "preferences": asdict(self.preferences),
            "interactions": [asdict(i) for i in self.interactions],
            "completions": [asdict(c) for c in self.completions],
            "insights": self.get_insights(),
            "exported_at": datetime.now().isoformat()
        }

        file_path.write_text(json.dumps(export_data, indent=2, default=str))


def create_sample_profile():
    """Create a sample profile for testing."""
    manager = UserProfileManager()

    # Simulate user behavior
    manager.record_interaction("polish_tasks", 5, True, "These suggestions look great!")
    manager.record_interaction("update_tasks", 3, True)
    manager.record_interaction("polish_tasks", 8, False, "Too aggressive")

    manager.record_task_completion("1", "Review quarterly report", 60, 45, True, quality_score=85)
    manager.record_task_completion("2", "Call client", 30, 60, True, quality_score=70)
    manager.record_task_completion("3", "Write proposal", 120, 180, True, quality_score=90)

    print("Sample profile created!")
    print(json.dumps(manager.get_insights(), indent=2))


if __name__ == "__main__":
    create_sample_profile()
