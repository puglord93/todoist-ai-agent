"""
Task Updater Module

Handles task updates with preview, confirmation, and rollback capabilities.
"""

from typing import Dict, Any, List, Optional
from datetime import datetime


class TaskUpdater:
    """Manages task updates with safety features."""

    def __init__(self):
        """Initialize the task updater."""
        self.update_history: List[Dict[str, Any]] = []

    def create_update_preview(self, task: Dict[str, Any],
                             updates: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a before/after preview of task updates.

        Args:
            task: Original task data
            updates: Proposed updates

        Returns:
            Preview dictionary with before/after comparison
        """
        preview = {
            "task_id": task.get("id"),
            "task_name": task.get("content", ""),
            "changes": [],
            "before": {},
            "after": {}
        }

        # Content/name changes
        if "content" in updates and updates["content"] != task.get("content"):
            preview["changes"].append("name")
            preview["before"]["name"] = task.get("content", "")
            preview["after"]["name"] = updates["content"]

        # Description changes
        if "description" in updates and updates["description"] != task.get("description", ""):
            preview["changes"].append("description")
            preview["before"]["description"] = task.get("description", "(empty)")
            preview["after"]["description"] = updates["description"]

        # Priority changes
        if "priority" in updates and updates["priority"] != task.get("priority", 1):
            preview["changes"].append("priority")
            preview["before"]["priority"] = self._format_priority(task.get("priority", 1))
            preview["after"]["priority"] = self._format_priority(updates["priority"])

        # Due date changes
        if "due_date" in updates:
            current_due = task.get("due", {}).get("date") if task.get("due") else None
            if updates["due_date"] != current_due:
                preview["changes"].append("due_date")
                preview["before"]["due_date"] = current_due or "(no due date)"
                preview["after"]["due_date"] = updates["due_date"]

        # Label changes
        if "labels" in updates:
            current_labels = set(task.get("labels", []))
            new_labels = set(updates["labels"])
            if current_labels != new_labels:
                preview["changes"].append("labels")
                preview["before"]["labels"] = list(current_labels) or "(no labels)"
                preview["after"]["labels"] = list(new_labels)
                preview["labels_added"] = list(new_labels - current_labels)
                preview["labels_removed"] = list(current_labels - new_labels)

        return preview

    def format_preview(self, preview: Dict[str, Any]) -> str:
        """
        Format a preview for display to user.

        Args:
            preview: Preview dictionary

        Returns:
            Formatted string for display
        """
        lines = []
        lines.append(f"📝 Task: {preview['task_name']}")
        lines.append("")

        if not preview["changes"]:
            lines.append("✨ No changes needed - task is already optimal!")
            return "\n".join(lines)

        lines.append("Proposed changes:")
        lines.append("-" * 60)

        for change_type in preview["changes"]:
            before = preview["before"].get(change_type, "")
            after = preview["after"].get(change_type, "")

            if change_type == "name":
                lines.append(f"\n📌 Name:")
                lines.append(f"   Before: {before}")
                lines.append(f"   After:  {after}")

            elif change_type == "description":
                lines.append(f"\n📄 Description:")
                lines.append(f"   Before: {before}")
                lines.append(f"   After:  {after}")

            elif change_type == "priority":
                lines.append(f"\n⚡ Priority:")
                lines.append(f"   Before: {before}")
                lines.append(f"   After:  {after}")

            elif change_type == "due_date":
                lines.append(f"\n📅 Due Date:")
                lines.append(f"   Before: {before}")
                lines.append(f"   After:  {after}")

            elif change_type == "labels":
                lines.append(f"\n🏷️  Labels:")
                if preview.get("labels_added"):
                    lines.append(f"   + Added: {', '.join(preview['labels_added'])}")
                if preview.get("labels_removed"):
                    lines.append(f"   - Removed: {', '.join(preview['labels_removed'])}")

        return "\n".join(lines)

    def create_batch_preview(self, previews: List[Dict[str, Any]]) -> str:
        """
        Format multiple previews for batch operations.

        Args:
            previews: List of preview dictionaries

        Returns:
            Formatted string for display
        """
        lines = []
        lines.append(f"📋 Batch Update - {len(previews)} tasks")
        lines.append("=" * 70)

        for i, preview in enumerate(previews, 1):
            lines.append(f"\n{i}. {preview['task_name']}")
            if preview["changes"]:
                changes_str = ", ".join(preview["changes"])
                lines.append(f"   Changes: {changes_str}")
            else:
                lines.append("   No changes needed")

        lines.append("\n" + "=" * 70)
        return "\n".join(lines)

    def save_original_state(self, task: Dict[str, Any]):
        """
        Save original task state for potential rollback.

        Args:
            task: Task data to save
        """
        self.update_history.append({
            "timestamp": datetime.now().isoformat(),
            "task_id": task.get("id"),
            "original": task.copy()
        })

        # Keep only last 50 updates
        if len(self.update_history) > 50:
            self.update_history = self.update_history[-50:]

    def _format_priority(self, priority: int) -> str:
        """
        Format priority for display.

        Args:
            priority: Priority level (1-4)

        Returns:
            Formatted string
        """
        priority_map = {
            1: "1 (Low)",
            2: "2 (Medium)",
            3: "3 (High)",
            4: "4 (Urgent)"
        }
        return priority_map.get(priority, str(priority))

    def validate_updates(self, updates: Dict[str, Any]) -> tuple[bool, Optional[str]]:
        """
        Validate proposed updates.

        Args:
            updates: Update dictionary

        Returns:
            Tuple of (is_valid, error_message)
        """
        # Check if any updates provided
        if not updates:
            return False, "No updates provided"

        # Validate priority
        if "priority" in updates:
            if not isinstance(updates["priority"], int) or not 1 <= updates["priority"] <= 4:
                return False, "Priority must be between 1 and 4"

        # Validate content not empty
        if "content" in updates:
            if not updates["content"] or len(updates["content"].strip()) == 0:
                return False, "Task name cannot be empty"

        # Validate labels is a list
        if "labels" in updates:
            if not isinstance(updates["labels"], list):
                return False, "Labels must be a list"

        return True, None
