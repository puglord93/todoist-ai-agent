#!/usr/bin/env python3
"""
Run Todoist AI Agent with Claude-fetched data

This script is designed to be called by Claude Code after Claude
fetches tasks from Todoist MCP. The tasks are passed as a JSON string.

Usage:
    python run_with_claude.py '<tasks_json>' [--full]
"""

import sys
import json
from typing import List, Dict, Any
from task_analyzer import TaskAnalyzer
from prioritizer import TaskPrioritizer


def main():
    if len(sys.argv) < 2:
        print("Error: No tasks data provided")
        print("This script should be called with tasks JSON as first argument")
        sys.exit(1)

    # Parse arguments
    tasks_json = sys.argv[1]
    full_report = "--full" in sys.argv

    try:
        # Parse tasks
        tasks = json.loads(tasks_json)

        if not tasks:
            print("No tasks found in your Todoist account!")
            return

        print(f"📥 Received {len(tasks)} tasks from Todoist MCP")
        print()

        # Normalize tasks
        normalized_tasks = []
        for task in tasks:
            normalized = {
                "id": task.get("id"),
                "content": task.get("content", ""),
                "description": task.get("description", ""),
                "due_date": task.get("due", {}).get("date") if task.get("due") else None,
                "priority": task.get("priority", 1),
                "labels": task.get("labels", []),
                "project_id": task.get("project_id"),
                "created_at": task.get("created_at")
            }
            normalized_tasks.append(normalized)

        # Analyze tasks
        print("🔍 Analyzing tasks...")
        analyzer = TaskAnalyzer()
        analyzed_tasks = []
        for task in normalized_tasks:
            analysis = analyzer.analyze_task(task)
            analyzed_tasks.append(analysis)
        print(f"   Analyzed {len(analyzed_tasks)} tasks")
        print()

        # Create focus plan
        print("🎯 Generating focus plan...")
        prioritizer = TaskPrioritizer()
        focus_plan = prioritizer.create_daily_focus_plan(analyzed_tasks, max_tasks=5)
        print()

        # Generate report
        if full_report:
            report = prioritizer.generate_full_report(focus_plan)
        else:
            report = prioritizer.generate_focus_summary(focus_plan)

        print(report)

    except json.JSONDecodeError as e:
        print(f"❌ Error parsing tasks JSON: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
