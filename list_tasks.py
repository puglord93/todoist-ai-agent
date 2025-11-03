#!/usr/bin/env python3
"""
List all Todoist tasks for editing
"""

import requests
import json
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Todoist API endpoint
TODOIST_API_URL = "https://api.todoist.com/rest/v2/tasks"
API_TOKEN = os.getenv("TODOIST_API_TOKEN")

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
        return None

def main():
    print("📋 Fetching your Todoist tasks...")
    print()

    tasks = fetch_tasks()

    if not tasks:
        print("No tasks found")
        return

    # Filter out Todoist onboarding/tutorial tasks
    real_tasks = []
    tutorial_keywords = ['Download Todoist', 'Capture:', 'Review', 'Complete:', 'Try our',
                         'keyboard shortcuts', 'integrations', 'Settings', 'Subscribe',
                         'Customize', 'Explore', 'Want to start', 'Take our quiz',
                         'Add Todoist to', 'Create Labels', 'Connect your calendar',
                         'Add your first task', 'Upcoming', 'CSV upload']

    for task in tasks:
        content = task.get('content', '')
        is_tutorial = any(keyword in content for keyword in tutorial_keywords)
        if not is_tutorial:
            real_tasks.append(task)

    print(f"Found {len(real_tasks)} real tasks (excluding {len(tasks) - len(real_tasks)} tutorial tasks)")
    print()
    print("=" * 70)
    print("YOUR TASKS:")
    print("=" * 70)

    for i, task in enumerate(real_tasks, 1):
        task_id = task.get('id')
        content = task.get('content', '')
        priority = task.get('priority', 1)
        due = task.get('due')
        labels = task.get('labels', [])

        print(f"\n{i}. {content}")
        print(f"   ID: {task_id}")
        print(f"   Priority: {priority} (1=low, 4=urgent)")
        print(f"   Due: {due.get('date') if due else 'No due date'}")
        print(f"   Labels: {', '.join(labels) if labels else 'No labels'}")

    print("\n" + "=" * 70)
    print(f"\nTotal: {len(real_tasks)} tasks need organizing!")

if __name__ == "__main__":
    main()
