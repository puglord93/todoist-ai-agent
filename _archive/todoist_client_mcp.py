"""
Todoist Client for MCP Integration

This version is designed to work WITH Claude Code's MCP integration.
When you run the agent through Claude Code, I (Claude) can call the MCP tools
and pass the results to your Python code.
"""

from typing import List, Dict, Any
import json
import sys


class TodoistMCPClient:
    """
    Client that expects task data to be passed in from MCP calls.

    This works by having Claude fetch tasks via MCP and pass them
    to the Python agent, rather than the Python code calling MCP directly.
    """

    def __init__(self):
        """Initialize the MCP client."""
        pass

    def analyze_tasks(self, tasks_json: str) -> None:
        """
        Analyze tasks fetched from Todoist MCP.

        Args:
            tasks_json: JSON string of tasks from MCP

        This will run the full agent analysis on the provided tasks.
        """
        from agent import TodoistAIAgent

        # Parse tasks
        tasks = json.loads(tasks_json)

        # Create a modified agent that uses these tasks
        agent = TodoistAIAgent(use_mock=False)

        # Override the fetch to return our tasks
        agent.client._tasks_cache = tasks

        # Run analysis
        report = agent.generate_report("focus")
        print(report)


def load_tasks_from_stdin():
    """
    Load tasks from stdin (useful for piping).

    Usage:
        echo '[...]' | python todoist_client_mcp.py
    """
    tasks_json = sys.stdin.read()
    client = TodoistMCPClient()
    client.analyze_tasks(tasks_json)


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--stdin":
        load_tasks_from_stdin()
    else:
        print("Usage: python todoist_client_mcp.py --stdin < tasks.json")
        print("Or use the main agent with --mock flag")
