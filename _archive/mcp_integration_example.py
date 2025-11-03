"""
Example: How to integrate with Todoist MCP Server

This file shows how you would modify todoist_client.py to use
the actual Todoist MCP server when it's available.

This is just an example - the actual implementation will depend
on how your MCP server exposes the Todoist API.
"""

# EXAMPLE 1: If MCP tools are available through Claude's tool system
def fetch_tasks_mcp_example_1(self):
    """
    Example using MCP tools directly (if available in context).
    """
    try:
        # Assuming MCP provides a tool called 'mcp__todoist__get_tasks'
        # The actual tool name will depend on your MCP server setup
        tasks = mcp__todoist__get_tasks()

        # Normalize the tasks to our standard format
        return [self.normalize_task(task) for task in tasks]
    except NameError:
        # MCP tool not available, fall back to mock
        print("⚠️  Todoist MCP not connected. Using mock data.")
        return self._get_mock_tasks()


# EXAMPLE 2: If MCP provides an HTTP API
def fetch_tasks_mcp_example_2(self):
    """
    Example using HTTP requests to MCP server.
    """
    import requests

    try:
        # Replace with your MCP server URL
        response = requests.get('http://localhost:8000/todoist/tasks')

        if response.status_code == 200:
            tasks = response.json()
            return [self.normalize_task(task) for task in tasks]
        else:
            print(f"⚠️  MCP request failed with status {response.status_code}")
            return self._get_mock_tasks()
    except Exception as e:
        print(f"⚠️  Todoist MCP error: {e}. Using mock data.")
        return self._get_mock_tasks()


# EXAMPLE 3: If using Claude Code's MCP integration
def fetch_tasks_mcp_example_3(self):
    """
    Example using environment variable to detect MCP availability.
    """
    import os

    mcp_available = os.getenv('TODOIST_MCP_AVAILABLE', 'false').lower() == 'true'

    if mcp_available:
        # Call your MCP tool here
        # The exact method depends on your setup
        return self._fetch_from_mcp()
    else:
        print("⚠️  Todoist MCP not connected. Using mock data.")
        return self._get_mock_tasks()


# EXAMPLE 4: Update task via MCP
def update_task_mcp_example(self, task_id: str, updates: dict):
    """
    Example of updating a task through MCP.

    Args:
        task_id: The task ID to update
        updates: Dictionary with fields like:
            - 'due_date': '2025-11-05'
            - 'priority': 4
            - 'content': 'Updated task name'
            - 'labels': ['urgent', 'work']
    """
    try:
        # Assuming MCP provides an update tool
        result = mcp__todoist__update_task(task_id=task_id, **updates)
        print(f"✅ Task {task_id} updated successfully")
        return True
    except NameError:
        print(f"⚠️  Todoist MCP not connected. Cannot update task {task_id}")
        return False
    except Exception as e:
        print(f"❌ Error updating task: {e}")
        return False


# STEPS TO INTEGRATE:
#
# 1. Install and configure your Todoist MCP server
# 2. Identify what tools/APIs it provides
# 3. Replace the methods in todoist_client.py with the appropriate calls
# 4. Test with: python main.py (without --mock flag)
# 5. If tasks appear, you're connected!

# COMMON MCP SERVER CONFIGURATIONS:
#
# The MCP server typically needs:
# - Todoist API token (get from todoist.com/app/settings/integrations)
# - Configuration in Claude Code settings
# - Possibly a server URL if running locally
#
# Check the documentation for your specific MCP server implementation.
