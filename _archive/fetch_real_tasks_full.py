#!/usr/bin/env python3
"""
Fetch real tasks from Todoist API and analyze them (FULL REPORT)
"""

import requests
import json
import sys
import os

# Add the project directory to path
sys.path.insert(0, '/Users/jj/todoist-ai-agent')

from task_analyzer import TaskAnalyzer
from prioritizer import TaskPrioritizer

# Todoist API endpoint
TODOIST_API_URL = "https://api.todoist.com/rest/v2/tasks"
API_TOKEN = "1efeeb99887b0753aeeb986c51695e1d51ae680d"

def fetch_tasks():
    """Fetch tasks from Todoist API"""
    headers = {
        "Authorization": f"Bearer {API_TOKEN}"
    }

    response = requests.get(TODOIST_API_URL, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        print(f"❌ Error fetching tasks: {response.status_code}")
        print(response.text)
        return None

def main():
    print("🤖 Todoist AI Agent starting...")
    print()

    # Fetch tasks
    print("📥 Fetching tasks from Todoist...")
    tasks = fetch_tasks()

    if not tasks:
        print("No tasks found or error occurred")
        sys.exit(1)

    print(f"   Found {len(tasks)} tasks")
    print()

    # Show first few raw tasks for inspection
    if tasks:
        print("📋 Sample of your tasks:")
        for i, task in enumerate(tasks[:5], 1):
            print(f"{i}. {task.get('content')} - Priority: {task.get('priority')}, Due: {task.get('due')}, Labels: {task.get('labels')}")
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
    print("🎯 Generating daily focus plan...")
    prioritizer = TaskPrioritizer()
    focus_plan = prioritizer.create_daily_focus_plan(analyzed_tasks, max_tasks=10)
    print()

    # Generate FULL report
    report = prioritizer.generate_full_report(focus_plan)
    print(report)

if __name__ == "__main__":
    main()
