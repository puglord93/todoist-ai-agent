"""
MCP Updater Module

Provides utilities for applying task updates via Todoist MCP.
This module is designed to work with Claude Code's MCP integration.
"""

from typing import Dict, Any, List, Optional
import json


class MCPUpdater:
    """
    Helper for structuring Todoist task updates for MCP.

    Note: MCP tools are only available to Claude Code (the AI assistant).
    This module provides utilities to format update requests that Claude
    can then execute via the Todoist MCP server.
    """

    def __init__(self):
        """Initialize the MCP updater."""
        pass

    def format_update_request(self, task_id: str, updates: Dict[str, Any]) -> Dict[str, Any]:
        """
        Format a task update request for MCP.

        Args:
            task_id: Todoist task ID
            updates: Dictionary of fields to update

        Returns:
            Formatted update request
        """
        request = {
            "task_id": task_id,
            "updates": {}
        }

        # Map our field names to Todoist API field names
        field_mapping = {
            "content": "content",
            "description": "description",
            "due_date": "due_string",  # MCP uses due_string for natural language
            "priority": "priority",
            "labels": "labels"
        }

        for key, value in updates.items():
            if key in field_mapping:
                request["updates"][field_mapping[key]] = value

        return request

    def format_batch_updates(self, updates: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Format multiple task updates for batch processing.

        Args:
            updates: List of update dictionaries, each with 'task_id' and 'updates'

        Returns:
            List of formatted update requests
        """
        formatted = []
        for update in updates:
            task_id = update.get("task_id")
            changes = update.get("updates", {})
            formatted.append(self.format_update_request(task_id, changes))

        return formatted

    def create_polish_updates(self, polish_results: List[Dict[str, Any]],
                             auto_approve: bool = False) -> List[Dict[str, Any]]:
        """
        Convert task polish results into update requests.

        Args:
            polish_results: Results from TaskPolisher.polish_tasks_batch()
            auto_approve: If True, include all suggestions; if False, only approved ones

        Returns:
            List of update requests
        """
        updates = []

        for result in polish_results:
            if not auto_approve and not result.get("approved", False):
                continue

            if not result.get("needs_polishing", False):
                continue

            task_updates = {}

            # Update task name if changed
            if result["suggested_name"] != result["original_name"]:
                task_updates["content"] = result["suggested_name"]

            # Update description if changed
            if result["suggested_description"] != result["original_description"]:
                task_updates["description"] = result["suggested_description"]

            # Update priority if extracted
            if result.get("extracted_priority"):
                task_updates["priority"] = result["extracted_priority"]

            # Add extracted labels
            if result.get("extracted_labels"):
                task_updates["labels"] = result["extracted_labels"]

            if task_updates:
                updates.append({
                    "task_id": result["task_id"],
                    "updates": task_updates
                })

        return updates

    def create_scheduling_updates(self, schedule_results: List[Dict[str, Any]],
                                  min_confidence: str = "medium") -> List[Dict[str, Any]]:
        """
        Convert due date suggestions into update requests.

        Args:
            schedule_results: Results from SmartScheduler.suggest_due_dates_batch()
            min_confidence: Minimum confidence level ("low", "medium", "high")

        Returns:
            List of update requests
        """
        confidence_levels = ["low", "medium", "high"]
        min_level = confidence_levels.index(min_confidence)

        updates = []

        for result in schedule_results:
            confidence = result.get("confidence", "low")
            if confidence_levels.index(confidence) < min_level:
                continue

            updates.append({
                "task_id": result["task_id"],
                "updates": {
                    "due_date": result["suggested_date"]
                }
            })

        return updates

    def generate_mcp_instructions(self, updates: List[Dict[str, Any]]) -> str:
        """
        Generate human-readable instructions for Claude to execute via MCP.

        Args:
            updates: List of update requests

        Returns:
            Formatted instruction string
        """
        if not updates:
            return "No updates to apply."

        instructions = ["To apply these updates via MCP, execute the following:\n"]

        for i, update in enumerate(updates, 1):
            task_id = update["task_id"]
            changes = update["updates"]

            instructions.append(f"\n{i}. Update task {task_id}:")
            for field, value in changes.items():
                instructions.append(f"   - Set {field} to: {value}")

        instructions.append("\n\nUse the Todoist MCP 'update-tasks' tool with these parameters.")

        return "\n".join(instructions)

    def create_summary_report(self, updates: List[Dict[str, Any]],
                            original_tasks: List[Dict[str, Any]]) -> str:
        """
        Create a before/after summary report of proposed updates.

        Args:
            updates: List of update requests
            original_tasks: Original task data

        Returns:
            Formatted summary report
        """
        if not updates:
            return "No updates proposed."

        # Create task lookup
        task_lookup = {task.get("id"): task for task in original_tasks}

        report_lines = ["=" * 80]
        report_lines.append("TASK UPDATE SUMMARY")
        report_lines.append("=" * 80)
        report_lines.append(f"\nTotal updates: {len(updates)}\n")

        for i, update in enumerate(updates, 1):
            task_id = update["task_id"]
            changes = update["updates"]
            original = task_lookup.get(task_id, {})

            report_lines.append(f"\n{i}. Task: {original.get('content', 'Unknown')}")
            report_lines.append(f"   ID: {task_id}")
            report_lines.append("   Changes:")

            for field, new_value in changes.items():
                old_value = original.get(field, "(not set)")
                report_lines.append(f"     {field}:")
                report_lines.append(f"       Before: {old_value}")
                report_lines.append(f"       After:  {new_value}")

        report_lines.append("\n" + "=" * 80)

        return "\n".join(report_lines)

    def save_updates_to_file(self, updates: List[Dict[str, Any]], filepath: str) -> None:
        """
        Save update requests to a JSON file.

        Args:
            updates: List of update requests
            filepath: Path to save file
        """
        with open(filepath, 'w') as f:
            json.dump({
                "updates": updates,
                "count": len(updates)
            }, f, indent=2)

    def load_updates_from_file(self, filepath: str) -> List[Dict[str, Any]]:
        """
        Load update requests from a JSON file.

        Args:
            filepath: Path to load from

        Returns:
            List of update requests
        """
        with open(filepath, 'r') as f:
            data = json.load(f)
            return data.get("updates", [])


def apply_updates_via_mcp_instructions() -> str:
    """
    Return instructions for how Claude Code should apply updates via MCP.

    Returns:
        Instruction text
    """
    return """
=== HOW TO APPLY UPDATES VIA TODOIST MCP ===

Since MCP tools are only available to Claude Code (the AI assistant),
here's how to apply the generated updates:

1. USING CLAUDE CODE DIRECTLY:
   Ask Claude: "Apply these updates to Todoist using MCP"
   Claude will use the 'update-tasks' tool from the Todoist MCP server.

2. BATCH UPDATE FORMAT:
   For each task update, Claude should call:

   Tool: update-tasks
   Parameters:
   {
     "taskId": "task_id_here",
     "content": "new task name",
     "description": "new description",
     "dueString": "tomorrow",  // or "2024-12-25", etc.
     "priority": 4
   }

3. EXAMPLE WORKFLOW:

   # Generate updates
   python interactive_polish.py

   # Review the suggestions
   # Approve the ones you want

   # Then ask Claude Code:
   "Please apply the approved updates from pending_updates.json to Todoist using MCP"

4. SAFETY:
   - Always review updates before applying
   - Start with a small batch to test
   - Keep backups of important task data

=== END INSTRUCTIONS ===
"""
