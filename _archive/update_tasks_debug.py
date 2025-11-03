#!/usr/bin/env python3
"""
Debug version - update with error details
"""

import requests
import json

TODOIST_API_URL = "https://api.todoist.com/rest/v2/tasks"
API_TOKEN = "1efeeb99887b0753aeeb986c51695e1d51ae680d"

def update_task_debug(task_id, new_content=None, new_description=None):
    """Update a task with debug output"""
    headers = {
        "Authorization": f"Bearer {API_TOKEN}",
        "Content-Type": "application/json"
    }

    data = {}
    if new_content:
        data["content"] = new_content
    if new_description:
        data["description"] = new_description

    print(f"   Sending update: {data}")

    response = requests.post(
        f"{TODOIST_API_URL}/{task_id}",
        headers=headers,
        json=data
    )

    print(f"   Response status: {response.status_code}")
    if response.status_code != 204:
        print(f"   Response body: {response.text}")

    return response.status_code == 204

# Test with just one task
task_id = "9646027235"
new_name = "Review Arceus pitch deck (tech & market deep dive)"
new_desc = "Test description"

print(f"Testing update for task {task_id}...")
update_task_debug(task_id, new_name, new_desc)
