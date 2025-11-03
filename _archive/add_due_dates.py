#!/usr/bin/env python3
"""
Add due dates to tasks based on priority and context
"""

import requests
import json
from datetime import datetime, timedelta

TODOIST_API_URL = "https://api.todoist.com/rest/v2/tasks"
API_TOKEN = "1efeeb99887b0753aeeb986c51695e1d51ae680d"

def update_task_due_date(task_id, due_string):
    """Update a task's due date"""
    headers = {
        "Authorization": f"Bearer {API_TOKEN}",
        "Content-Type": "application/json"
    }

    data = {"due_string": due_string}

    response = requests.post(
        f"{TODOIST_API_URL}/{task_id}",
        headers=headers,
        json=data
    )

    return response.status_code in [200, 204]

# Calculate dates
today = datetime.now()
tomorrow = today + timedelta(days=1)
in_2_days = today + timedelta(days=2)
in_3_days = today + timedelta(days=3)
next_week = today + timedelta(days=7)

# Due date assignments
DUE_DATE_UPDATES = {
    "9559828839": {
        "task": "Send follow-up email to Prof Sum",
        "due_string": "today",
        "reasoning": "Priority 4 (Urgent) - Prof is busy, need response soon"
    },

    "9689226453": {
        "task": "Respond to Leonard (CMG Tech) - micro-MIM project",
        "due_string": "tomorrow",
        "reasoning": "Priority 3 - Business communication should be within 24-48 hours"
    },

    "9566684374": {
        "task": "Follow up with DYT on WhatsApp",
        "due_string": "tomorrow",
        "reasoning": "Priority 3 - Follow-ups should be timely"
    },

    "9646027235": {
        "task": "Review Arceus pitch deck",
        "due_string": "in 3 days",
        "reasoning": "Priority 3 - Important but requires deep analysis time"
    },

    "9566714420": {
        "task": "Create 2 LinkedIn posts about VB",
        "due_string": "in 5 days",
        "reasoning": "Priority 2 - Content creation, flexible timeline"
    },

    "9678806227": {
        "task": "Coordinate meeting with SND partners",
        "due_string": "next week",
        "reasoning": "Priority 2 - Meeting coordination needs lead time"
    }
}

def main():
    print("📅 Adding due dates to your tasks...")
    print()

    success_count = 0
    total_tasks = len(DUE_DATE_UPDATES)

    for i, (task_id, info) in enumerate(DUE_DATE_UPDATES.items(), 1):
        print(f"[{i}/{total_tasks}] {info['task']}")
        print(f"   Setting due: {info['due_string']}")
        print(f"   Reasoning: {info['reasoning']}")

        if update_task_due_date(task_id, info['due_string']):
            print(f"   ✅ Updated!\n")
            success_count += 1
        else:
            print(f"   ❌ Failed\n")

    print("=" * 70)
    print(f"✨ Successfully updated {success_count}/{total_tasks} tasks!")
    print()
    print("📊 Due Date Summary:")
    print("   • Today:       1 task  - Prof Sum email")
    print("   • Tomorrow:    2 tasks - CMG Tech, DYT follow-up")
    print("   • In 3 days:   1 task  - Arceus review")
    print("   • In 5 days:   1 task  - LinkedIn posts")
    print("   • Next week:   1 task  - SND meeting")
    print()
    print("🎉 Your tasks now have due dates! Run analysis again to see prioritization.")

if __name__ == "__main__":
    main()
