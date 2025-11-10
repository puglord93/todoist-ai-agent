#!/usr/bin/env python3
"""
Apply polish updates to Todoist tasks via API
"""

import requests
import json

# Todoist API configuration
TODOIST_API_URL = "https://api.todoist.com/rest/v2/tasks"
API_TOKEN = "1efeeb99887b0753aeeb986c51695e1d51ae680d"

def update_task(task_id, updates):
    """Update a task via Todoist API"""
    headers = {
        "Authorization": f"Bearer {API_TOKEN}",
        "Content-Type": "application/json"
    }

    url = f"{TODOIST_API_URL}/{task_id}"
    response = requests.post(url, headers=headers, json=updates)

    if response.status_code == 200:
        return True, response.json()
    else:
        return False, response.text

# Define all updates
updates = [
    # Task 1: Prof Sum email - just add labels and description
    {
        "task_id": "9559828839",
        "updates": {
            "labels": ["email", "follow-up", "academic", "urgent"],
            "description": "Follow up with Prof Sum regarding his commitment decision. Need confirmation on his availability and interest level."
        }
    },

    # Task 2: LinkedIn posts - expand VB and add description
    {
        "task_id": "9566714420",
        "updates": {
            "content": "Create 2 LinkedIn posts about VB project",
            "labels": ["content-creation", "linkedin", "social-media", "vb-project", "marketing"],
            "description": "Draft 2 engaging LinkedIn posts about the VB project:\n1. Project overview and vision\n2. Recent milestones and achievements\n\nReview and schedule for posting."
        }
    },

    # Task 3: SND partners meeting - add purpose and labels
    {
        "task_id": "9678806227",
        "updates": {
            "content": "Schedule meeting with SND partners - Q4 collaboration planning",
            "labels": ["meeting", "coordination", "partnerships", "snd", "business"],
            "description": "Send calendar invite to SND partners.\nAgenda:\n- Q4 collaboration opportunities\n- Project updates\n- Resource allocation\n\nPropose 2-3 time slots."
        }
    },

    # Task 4: Leonard CMG Tech - add labels and description
    {
        "task_id": "9689226453",
        "updates": {
            "content": "Respond to Leonard (CMG Tech) - micro-MIM project status",
            "labels": ["email", "response", "cmg-tech", "micro-mim", "project", "urgent"],
            "description": "Reply to Leonard's inquiry about micro-MIM project.\nKey points to address:\n- Current project status\n- Timeline updates\n- Next steps\n\nReview his previous email before responding."
        }
    },

    # Task 5: DYT WhatsApp - clarify and add context
    {
        "task_id": "9566684374",
        "updates": {
            "content": "Follow up with DYT on WhatsApp regarding pending response",
            "labels": ["follow-up", "messaging", "dyt", "communication", "urgent"],
            "description": "Check in with DYT for update on pending matter.\nIf no response, consider alternative contact method."
        }
    },

    # Task 6: LinkedIn password - shorten and add due date
    {
        "task_id": "9693822068",
        "updates": {
            "content": "Audit LinkedIn security - update password and review connected apps",
            "labels": ["security", "personal", "linkedin", "account-management"],
            "description": "Security audit steps:\n1. Change LinkedIn password\n2. Review Settings → Security → Connected apps\n3. Disconnect any suspicious or unused apps\n4. Verify 2FA is enabled",
            "due_string": "Nov 4"
        }
    },

    # Task 7: Joseph dog info - add clarity and due date
    {
        "task_id": "9693822143",
        "updates": {
            "content": "Send dog ownership documentation to Joseph",
            "labels": ["email", "personal", "joseph", "pets"],
            "description": "Compile and send to Joseph:\n- Vaccination records\n- Microchip information\n- Care instructions\n- Vet contact details",
            "due_string": "Nov 3"
        }
    }
]

print("🪄 Applying Polish Updates to Todoist Tasks...")
print("=" * 80)

success_count = 0
failed_updates = []

for i, update_info in enumerate(updates, 1):
    task_id = update_info["task_id"]
    updates_data = update_info["updates"]

    print(f"\n{i}/7 Updating task {task_id}...")
    print(f"    Changes: {', '.join(updates_data.keys())}")

    success, result = update_task(task_id, updates_data)

    if success:
        print(f"    ✅ Updated successfully!")
        success_count += 1
    else:
        print(f"    ❌ Failed: {result}")
        failed_updates.append((task_id, result))

print("\n" + "=" * 80)
print(f"✅ Successfully updated: {success_count}/7 tasks")

if failed_updates:
    print(f"❌ Failed updates: {len(failed_updates)}")
    for task_id, error in failed_updates:
        print(f"   - Task {task_id}: {error}")

print("\n🎉 Polish complete! Check your Todoist to see the improvements.")
