#!/usr/bin/env python3
"""
Update Todoist task names and descriptions (preserving existing details)
"""

import requests
import json

TODOIST_API_URL = "https://api.todoist.com/rest/v2/tasks"
API_TOKEN = "1efeeb99887b0753aeeb986c51695e1d51ae680d"

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

    return response.status_code in [200, 204]

# Task updates - improved names and polished descriptions
TASK_UPDATES = {
    "9646027235": {
        "name": "Review Arceus pitch deck (tech & market deep dive)",
        "description": """Schedule sit-down meeting with Arceus team for deep dive.

Focus areas:
• Technical architecture and approach
• Business model and market opportunity
• Identify gaps and challenges
• Include team in gap analysis discussions

Approach: Account management style - show value through engagement and interaction, not key driving."""
    },

    "9559828839": {
        "name": "Send follow-up email to Prof Sum (commitment check)",
        "description": """Prof Sum seems very occupied - send email to clarify deliverable conditions.

Key question: Can you commit to this?
• If yes → confirm timeline and next steps
• If no → understand constraints and alternatives

Keep it brief and action-oriented given his schedule."""
    },

    "9566714420": {
        "name": "Create 2 LinkedIn posts about VB",
        "description": """Write and publish two LinkedIn posts about VB.

Post 1: [Define topic/angle]
Post 2: Consider using an infographic format

Ensure posts are:
• Engaging and professional
• Aligned with personal brand
• Include relevant hashtags"""
    },

    "9566684374": {
        "name": "Follow up with DYT on WhatsApp",
        "description": """Send WhatsApp follow-up message to DYT.

Action items:
• [Add context about what you're following up on]
• [Specify expected response or next action]"""
    },

    "9678806227": {
        "name": "Coordinate meeting with SND partners",
        "description": """Schedule connection/meeting with SND regarding partnership opportunities.

Key stakeholders:
• Circular Unite
• SG Enviro
• PUB

Agenda:
• [Define main discussion points]
• [Clarify collaboration opportunities]
• [Next steps and timeline]"""
    },

    "9689226453": {
        "name": "Respond to Leonard (CMG Tech) - micro-MIM project",
        "description": """Reply to Leonard from CMG Tech regarding micro-MIM project proposal.

Points to address:
• Project scope and technical requirements
• Timeline and milestones
• Resource needs and deliverables
• Any questions or clarifications needed

Review their proposal before responding."""
    }
}

def main():
    print("🔄 Updating your Todoist tasks with improved names and descriptions...")
    print()

    success_count = 0
    total_tasks = len(TASK_UPDATES)

    for i, (task_id, updates) in enumerate(TASK_UPDATES.items(), 1):
        print(f"[{i}/{total_tasks}] Updating task {task_id}...")
        print(f"   ✨ New name: {updates['name']}")

        # Update the task
        if update_task(task_id, updates['name'], updates['description']):
            print(f"   ✅ Updated successfully!\n")
            success_count += 1
        else:
            print(f"   ❌ Failed to update\n")

    print("=" * 70)
    print(f"✨ Successfully updated {success_count}/{total_tasks} tasks!")
    print()

    if success_count == total_tasks:
        print("🎉 All tasks updated! Check your Todoist app to see the changes.")
    else:
        print(f"⚠️  {total_tasks - success_count} tasks failed to update. Please check manually.")

    print()
    print("💡 Next steps:")
    print("   1. Open Todoist and review the updated tasks")
    print("   2. Fill in any [...] placeholders with specific details")
    print("   3. Add due dates and priorities for better organization")

if __name__ == "__main__":
    main()
