"""
Todoist Client Interface

This module provides a unified interface for Todoist operations.
When an MCP server is available, it will use MCP tools.
Otherwise, it can use direct API calls or mock data for testing.
"""

from typing import List, Dict, Optional, Any
from datetime import datetime
import json
import os
import requests
from dotenv import load_dotenv

load_dotenv()


class TodoistClient:
    """Client for interacting with Todoist tasks."""

    def __init__(self, use_mock: bool = False):
        """
        Initialize the Todoist client.

        Args:
            use_mock: If True, use mock data instead of real API
        """
        self.use_mock = use_mock
        self.api_token = os.getenv("TODOIST_API_TOKEN")
        self.api_url = "https://api.todoist.com/rest/v2/tasks"

    def fetch_tasks(self) -> List[Dict[str, Any]]:
        """
        Fetch all active tasks from Todoist.

        Returns:
            List of task dictionaries with standardized format
        """
        if self.use_mock:
            return self._get_mock_tasks()

        # Try direct API call first
        if self.api_token:
            try:
                headers = {"Authorization": f"Bearer {self.api_token}"}
                response = requests.get(self.api_url, headers=headers)

                if response.status_code == 200:
                    tasks = response.json()
                    # Filter out tutorial tasks
                    tutorial_keywords = ['Download Todoist', 'Capture:', 'Review', 'Complete:', 'Try our']
                    real_tasks = [t for t in tasks if not any(kw in t.get('content', '') for kw in tutorial_keywords)]
                    return real_tasks
                else:
                    print(f"⚠️  Todoist API error {response.status_code}. Using mock data.")
                    return self._get_mock_tasks()
            except Exception as e:
                print(f"⚠️  Error calling Todoist API: {e}. Using mock data.")
                return self._get_mock_tasks()

        # Try to use MCP tools if available
        try:
            # Check if MCP find-tasks tool is available
            if 'mcp__todoist__find_tasks' in dir():
                print("✅ Using Todoist MCP server to fetch tasks...")
                # Call the MCP tool to find all active tasks
                mcp_result = mcp__todoist__find_tasks(filter="all")

                # The MCP tool returns tasks in Todoist API format
                if isinstance(mcp_result, list):
                    return mcp_result
                elif isinstance(mcp_result, dict) and 'tasks' in mcp_result:
                    return mcp_result['tasks']
                else:
                    print(f"⚠️  Unexpected MCP response format. Using mock data.")
                    return self._get_mock_tasks()
            else:
                print("⚠️  No Todoist API token or MCP tools detected. Using mock data.")
                return self._get_mock_tasks()
        except Exception as e:
            print(f"⚠️  Error: {e}. Using mock data.")
            return self._get_mock_tasks()

    def update_task(self, task_id: str, updates: Dict[str, Any]) -> bool:
        """
        Update a task in Todoist.

        Args:
            task_id: The task ID to update
            updates: Dictionary of fields to update (due_date, priority, etc.)

        Returns:
            True if successful, False otherwise
        """
        if self.use_mock:
            print(f"[MOCK] Would update task {task_id} with: {updates}")
            return True

        # Try direct API first
        if self.api_token:
            try:
                url = f"https://api.todoist.com/rest/v2/tasks/{task_id}"
                headers = {
                    "Authorization": f"Bearer {self.api_token}",
                    "Content-Type": "application/json"
                }

                # Prepare update payload
                payload = {}
                if "content" in updates:
                    payload["content"] = updates["content"]
                if "description" in updates:
                    payload["description"] = updates["description"]
                if "priority" in updates:
                    payload["priority"] = updates["priority"]
                if "due_date" in updates:
                    payload["due_string"] = updates["due_date"]
                if "labels" in updates:
                    payload["labels"] = updates["labels"]

                response = requests.post(url, headers=headers, json=payload)

                if response.status_code == 200:
                    return True
                else:
                    print(f"⚠️  Todoist API error {response.status_code}: {response.text}")
                    return False
            except Exception as e:
                print(f"❌ Error updating task via API: {e}")
                return False

        # Try to use MCP update tool if available
        try:
            if 'mcp__todoist__update_tasks' in dir():
                print(f"✅ Updating task {task_id} via Todoist MCP...")

                # Prepare update parameters
                update_params = {"id": task_id}

                # Map our update keys to Todoist API format
                if "due_date" in updates:
                    update_params["due_string"] = updates["due_date"]
                if "priority" in updates:
                    update_params["priority"] = updates["priority"]
                if "content" in updates:
                    update_params["content"] = updates["content"]
                if "description" in updates:
                    update_params["description"] = updates["description"]
                if "labels" in updates:
                    update_params["labels"] = updates["labels"]

                # Call the MCP update tool
                result = mcp__todoist__update_tasks(tasks=[update_params])
                print(f"✅ Task {task_id} updated successfully")
                return True
            else:
                print(f"⚠️  No API token or MCP connection. Cannot update task {task_id}")
                return False
        except Exception as e:
            print(f"❌ Error updating task {task_id}: {e}")
            return False

    def _get_mock_tasks(self) -> List[Dict[str, Any]]:
        """Generate mock tasks for testing."""
        return [
            {
                "id": "1",
                "content": "Finish quarterly report",
                "description": "Complete Q4 financial analysis",
                "due": {"date": "2025-10-31", "is_recurring": False},
                "priority": 4,  # Todoist uses 1-4, where 4 is highest
                "labels": ["work", "urgent"],
                "project_id": "project1",
                "created_at": "2025-10-25T10:00:00Z"
            },
            {
                "id": "2",
                "content": "Call dentist for checkup",
                "description": "",
                "due": {"date": "2025-11-05", "is_recurring": False},
                "priority": 2,
                "labels": ["health", "personal"],
                "project_id": "project2",
                "created_at": "2025-10-28T14:30:00Z"
            },
            {
                "id": "3",
                "content": "Review code for PR #234",
                "description": "New authentication feature",
                "due": {"date": "2025-10-31", "is_recurring": False},
                "priority": 3,
                "labels": ["work", "code-review"],
                "project_id": "project1",
                "created_at": "2025-10-30T09:15:00Z"
            },
            {
                "id": "4",
                "content": "Buy groceries",
                "description": "Milk, eggs, bread, vegetables",
                "due": None,
                "priority": 2,
                "labels": ["personal", "errands"],
                "project_id": "project2",
                "created_at": "2025-10-29T18:00:00Z"
            },
            {
                "id": "5",
                "content": "Plan team offsite",
                "description": "Book venue and organize activities",
                "due": {"date": "2025-11-15", "is_recurring": False},
                "priority": 3,
                "labels": ["work", "planning"],
                "project_id": "project1",
                "created_at": "2025-10-20T11:00:00Z"
            },
            {
                "id": "6",
                "content": "Learn new Python framework",
                "description": "Complete tutorial series",
                "due": None,
                "priority": 1,
                "labels": ["learning", "personal"],
                "project_id": "project3",
                "created_at": "2025-10-15T16:00:00Z"
            },
            {
                "id": "7",
                "content": "Submit expense report",
                "description": "Last month's travel expenses",
                "due": {"date": "2025-11-01", "is_recurring": False},
                "priority": 3,
                "labels": ["work", "admin"],
                "project_id": "project1",
                "created_at": "2025-10-27T13:00:00Z"
            },
            {
                "id": "8",
                "content": "Fix production bug",
                "description": "User login timeout issue",
                "due": {"date": "2025-10-31", "is_recurring": False},
                "priority": 4,
                "labels": ["work", "urgent", "bug"],
                "project_id": "project1",
                "created_at": "2025-10-30T15:45:00Z"
            }
        ]

    def normalize_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """
        Normalize task data from different sources into a standard format.

        Args:
            task: Raw task data

        Returns:
            Normalized task dictionary
        """
        return {
            "id": task.get("id"),
            "content": task.get("content", ""),
            "description": task.get("description", ""),
            "due_date": task.get("due", {}).get("date") if task.get("due") else None,
            "priority": task.get("priority", 1),
            "labels": task.get("labels", []),
            "project_id": task.get("project_id"),
            "created_at": task.get("created_at")
        }
