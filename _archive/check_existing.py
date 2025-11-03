#!/usr/bin/env python3
"""
Check existing task descriptions before updating
"""

import requests
import json

TODOIST_API_URL = "https://api.todoist.com/rest/v2/tasks"
API_TOKEN = "1efeeb99887b0753aeeb986c51695e1d51ae680d"

def get_task(task_id):
    """Get a specific task"""
    headers = {"Authorization": f"Bearer {API_TOKEN}"}
    response = requests.get(f"{TODOIST_API_URL}/{task_id}", headers=headers)
    return response.json() if response.status_code == 200 else None

TASK_IDS = [
    "9646027235",
    "9559828839",
    "9566714420",
    "9566684374",
    "9678806227",
    "9689226453"
]

def main():
    print("📋 Checking existing task details...")
    print("=" * 70)

    for task_id in TASK_IDS:
        task = get_task(task_id)
        if task:
            print(f"\n📌 {task.get('content')}")
            print(f"   ID: {task_id}")
            desc = task.get('description', '')
            if desc:
                print(f"   Current description: {desc}")
            else:
                print(f"   Current description: (empty)")
            print()

if __name__ == "__main__":
    main()
