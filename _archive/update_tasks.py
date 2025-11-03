#!/usr/bin/env python3
"""
Update Todoist task names and descriptions
"""

import requests
import json

# Todoist API endpoint
TODOIST_API_URL = "https://api.todoist.com/rest/v2/tasks"
API_TOKEN = "1efeeb99887b0753aeeb986c51695e1d51ae680d"

def get_task(task_id):
    """Get a specific task"""
    headers = {"Authorization": f"Bearer {API_TOKEN}"}
    response = requests.get(f"{TODOIST_API_URL}/{task_id}", headers=headers)
    return response.json() if response.status_code == 200 else None

def update_task(task_id, new_content=None, new_description=None):
    """Update a task's content and/or description"""
    headers = {
        "Authorization": f"Bearer {API_TOKEN}",
        "Content-Type": "application/json"
    }

    data = {}
    if new_content:
        data["content"] = new_content
    if new_description:
        data["description"] = new_description

    response = requests.post(
        f"{TODOIST_API_URL}/{task_id}",
        headers=headers,
        json=data
    )

    return response.status_code == 204

# Task updates with improved names and descriptions
TASK_UPDATES = {
    "9646027235": {
        "name": "Review Arceus pitch deck (tech & market analysis)",
        "description": "Go through Arceus' complete pitch deck focusing on:\n- Technical approach and architecture\n- Market analysis and opportunity\n- Competitive landscape\n- Investment potential"
    },
    "9559828839": {
        "name": "Send follow-up email to Prof Sum",
        "description": "Draft and send a compelling follow-up email to Prof Sum.\n\nKey points to include:\n- Reference to previous conversation\n- Clear ask or next steps\n- Value proposition"
    },
    "9566714420": {
        "name": "Create 2 LinkedIn posts about VB",
        "description": "Write and publish two LinkedIn posts about VB.\n\nPost 1: [Topic/angle for first post]\nPost 2: [Topic/angle for second post]\n\nEnsure posts are engaging, professional, and aligned with personal brand."
    },
    "9566684374": {
        "name": "Follow up with DYT on WhatsApp",
        "description": "Send WhatsApp message to DYT for follow-up.\n\nContext: [Add context about what you're following up on]\nAction needed: [Specify what response or action you need]"
    },
    "9678806227": {
        "name": "Schedule connection with SND",
        "description": "Reach out to SND to schedule a meeting or call.\n\nPurpose: [Add purpose of meeting]\nPreferred timing: [Add any time preferences]\nTopics to discuss: [List key discussion points]"
    },
    "9689226453": {
        "name": "Respond to Leonard (CMG Tech) re: micro-MIM project",
        "description": "Reply to Leonard from CMG Tech regarding the micro-MIM project.\n\nKey points to address:\n- Project timeline and scope\n- Technical requirements\n- Next steps and deliverables\n- Any questions or clarifications needed"
    }
}

def main():
    print("🔄 Updating your Todoist tasks...")
    print()

    success_count = 0

    for task_id, updates in TASK_UPDATES.items():
        # First, get current task to show before/after
        current_task = get_task(task_id)

        if not current_task:
            print(f"❌ Could not find task {task_id}")
            continue

        print("─" * 70)
        print(f"📝 Task: {current_task.get('content')}")
        print(f"   Old description: {current_task.get('description', '(none)')[:50]}...")
        print()
        print(f"   ✨ New name: {updates['name']}")
        print(f"   ✨ New description: {updates['description'][:80]}...")
        print()

        # Update the task
        if update_task(task_id, updates['name'], updates['description']):
            print("   ✅ Updated successfully!")
            success_count += 1
        else:
            print("   ❌ Failed to update")

        print()

    print("=" * 70)
    print(f"✨ Updated {success_count}/{len(TASK_UPDATES)} tasks successfully!")
    print()
    print("💡 Tip: Check your Todoist app to see the changes!")

if __name__ == "__main__":
    main()
