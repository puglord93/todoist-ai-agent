#!/usr/bin/env python3
"""
Test script for task polishing using OpenAI API standalone
"""

import requests
import os
from dotenv import load_dotenv
from task_polisher import TaskPolisher

# Load environment variables
load_dotenv()

def fetch_todoist_tasks():
    """Fetch tasks from Todoist API"""
    api_token = os.getenv("TODOIST_API_TOKEN")
    headers = {"Authorization": f"Bearer {api_token}"}

    response = requests.get("https://api.todoist.com/rest/v2/tasks", headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error fetching tasks: {response.status_code}")
        return []

def main():
    print("=" * 70)
    print("🤖 TODOIST TASK POLISHER (Standalone with OpenAI)")
    print("=" * 70)
    print()

    # Initialize the task polisher with OpenAI
    print("✅ Initializing OpenAI Task Polisher...")
    polisher = TaskPolisher()
    print(f"   Using model: {polisher.model}")
    print()

    # Fetch tasks from Todoist
    print("📋 Fetching tasks from Todoist...")
    tasks = fetch_todoist_tasks()

    # Filter out tutorial tasks
    tutorial_keywords = ['Download Todoist', 'Capture:', 'Review', 'Complete:', 'Try our',
                         'keyboard shortcuts', 'integrations', 'Settings', 'Subscribe']

    real_tasks = [t for t in tasks if not any(kw in t.get('content', '') for kw in tutorial_keywords)]

    print(f"   Found {len(real_tasks)} real tasks")
    print()

    if not real_tasks:
        print("No tasks to polish!")
        return

    # Find tasks that need polishing
    print("🔍 Analyzing task quality...")
    tasks_needing_polish = polisher.identify_tasks_needing_polish(
        [polisher.todoist_to_internal(t) for t in real_tasks],
        min_quality=60
    )

    print(f"   {len(tasks_needing_polish)} tasks need improvement")
    print()

    if not tasks_needing_polish:
        print("✨ All tasks are well-formatted!")
        return

    # Polish the first task as a demo
    print("=" * 70)
    print("🎨 DEMO: Polishing first low-quality task")
    print("=" * 70)
    print()

    demo_task = tasks_needing_polish[0]
    quality = demo_task["quality_assessment"]

    print(f"📌 Original Task:")
    print(f"   Name: {demo_task.get('content', '')}")
    print(f"   Description: {demo_task.get('description', '(empty)')}")
    print(f"   Quality Score: {quality['percentage']}%")
    print(f"   Issues: {', '.join(quality['issues'])}")
    print()

    print("🤖 Asking AI to polish this task...")
    polished = polisher.polish_task(demo_task)
    print()

    print(f"✨ AI Suggestions:")
    print(f"   Suggested Name: {polished['suggested_name']}")
    print(f"   Suggested Description: {polished['suggested_description']}")
    if polished.get('extracted_priority'):
        print(f"   Suggested Priority: {polished['extracted_priority']}")
    if polished.get('extracted_labels'):
        print(f"   Suggested Labels: {', '.join(polished['extracted_labels'])}")
    print(f"   Reason: {polished['polishing_reason']}")
    print()

    print("=" * 70)
    print("✅ Test completed successfully!")
    print("=" * 70)

def todoist_to_internal(task):
    """Convert Todoist task format to internal format"""
    return {
        "id": task.get("id"),
        "content": task.get("content", ""),
        "description": task.get("description", ""),
        "due_date": task.get("due", {}).get("date") if task.get("due") else None,
        "priority": task.get("priority", 1),
        "labels": task.get("labels", []),
    }

# Add the conversion method to TaskPolisher
TaskPolisher.todoist_to_internal = staticmethod(todoist_to_internal)

if __name__ == "__main__":
    main()
