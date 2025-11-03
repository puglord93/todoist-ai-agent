#!/usr/bin/env python3
"""
Add priorities to tasks based on urgency and importance
"""

import requests
import json

TODOIST_API_URL = "https://api.todoist.com/rest/v2/tasks"
API_TOKEN = "1efeeb99887b0753aeeb986c51695e1d51ae680d"

def update_task_priority(task_id, priority):
    """Update a task's priority"""
    headers = {
        "Authorization": f"Bearer {API_TOKEN}",
        "Content-Type": "application/json"
    }

    data = {"priority": priority}

    response = requests.post(
        f"{TODOIST_API_URL}/{task_id}",
        headers=headers,
        json=data
    )

    return response.status_code in [200, 204]

# Priority assignments based on urgency and importance analysis
# Priority 4 = Urgent & Important
# Priority 3 = Important
# Priority 2 = Moderate
# Priority 1 = Low

PRIORITY_UPDATES = {
    "9559828839": {
        "task": "Send follow-up email to Prof Sum",
        "priority": 4,
        "reasoning": "Email to professor - time-sensitive, waiting on commitment decision, blocks other work"
    },

    "9689226453": {
        "task": "Respond to Leonard (CMG Tech) - micro-MIM project",
        "priority": 3,
        "reasoning": "Business communication - important for project progression, professional relationship"
    },

    "9646027235": {
        "task": "Review Arceus pitch deck",
        "priority": 3,
        "reasoning": "Investment/business opportunity - important for decision making, requires deep analysis"
    },

    "9566684374": {
        "task": "Follow up with DYT on WhatsApp",
        "priority": 3,
        "reasoning": "Follow-up communication - keeps momentum, maintains relationship"
    },

    "9678806227": {
        "task": "Coordinate meeting with SND partners",
        "priority": 2,
        "reasoning": "Partnership coordination - important but can be scheduled flexibly"
    },

    "9566714420": {
        "task": "Create 2 LinkedIn posts about VB",
        "priority": 2,
        "reasoning": "Content creation - valuable for visibility but not blocking other work"
    }
}

def main():
    print("🎯 Adding priorities to your tasks based on urgency/importance...")
    print()

    success_count = 0
    total_tasks = len(PRIORITY_UPDATES)

    for i, (task_id, info) in enumerate(PRIORITY_UPDATES.items(), 1):
        priority = info["priority"]
        priority_label = {4: "P1 (Urgent)", 3: "P2 (High)", 2: "P3 (Medium)", 1: "P4 (Low)"}

        print(f"[{i}/{total_tasks}] {info['task']}")
        print(f"   Setting priority: {priority_label[priority]}")
        print(f"   Reasoning: {info['reasoning']}")

        if update_task_priority(task_id, priority):
            print(f"   ✅ Updated!\n")
            success_count += 1
        else:
            print(f"   ❌ Failed\n")

    print("=" * 70)
    print(f"✨ Successfully updated {success_count}/{total_tasks} tasks!")
    print()
    print("📊 Priority Summary:")
    print("   • Priority 4 (Urgent):     1 task  - Prof Sum email")
    print("   • Priority 3 (High):       3 tasks - CMG Tech, Arceus, DYT")
    print("   • Priority 2 (Medium):     2 tasks - SND meeting, LinkedIn posts")
    print()
    print("🎉 Your tasks are now prioritized! Check Todoist to see the changes.")

if __name__ == "__main__":
    main()
