#!/usr/bin/env python3
"""
Quick CLI tool to see today's tasks
Usage: ./today.py or venv/bin/python3 today.py
"""

import requests
import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

def main():
    # Get today's date
    today = datetime.now().strftime("%Y-%m-%d")

    # Fetch tasks
    token = os.getenv("TODOIST_API_TOKEN")
    response = requests.get(
        "https://api.todoist.com/rest/v2/tasks",
        headers={"Authorization": f"Bearer {token}"}
    )

    if response.status_code != 200:
        print(f"❌ Error fetching tasks: {response.status_code}")
        return

    tasks = response.json()

    # Filter tutorial tasks
    tutorial_keywords = ['Download Todoist', 'Capture:', 'Review', 'Complete:']
    real_tasks = [t for t in tasks if not any(kw in t.get('content', '') for kw in tutorial_keywords)]

    # Categorize tasks
    overdue = []
    due_today = []
    upcoming = []

    for task in real_tasks:
        due_date = task.get('due', {}).get('date') if task.get('due') else None
        if due_date:
            if due_date < today:
                overdue.append(task)
            elif due_date == today:
                due_today.append(task)
            elif due_date > today:
                upcoming.append(task)

    # Print results
    print()
    print("=" * 70)
    print(f"📅 TODAY'S TASKS - {today}")
    print("=" * 70)
    print()

    if overdue:
        print(f"⚠️  OVERDUE ({len(overdue)}):")
        print("-" * 70)
        for task in overdue:
            priority_emoji = "🔴" if task.get('priority', 1) >= 3 else "🟡"
            print(f"{priority_emoji} {task['content']}")
            if task.get('labels'):
                print(f"   Labels: {', '.join(task['labels'])}")
        print()

    if due_today:
        print(f"📌 DUE TODAY ({len(due_today)}):")
        print("-" * 70)
        for task in due_today:
            priority_emoji = "🔴" if task.get('priority', 1) >= 3 else "🟢"
            print(f"{priority_emoji} {task['content']}")
            if task.get('labels'):
                print(f"   Labels: {', '.join(task['labels'])}")
        print()
    else:
        print("✨ No tasks due today!")
        print()

    if upcoming:
        print(f"📆 UPCOMING (Next 7 days):")
        print("-" * 70)
        upcoming_week = [t for t in upcoming if t.get('due', {}).get('date', '') <= datetime.now().strftime("%Y-%m-%d")[:8] + str(int(today[-2:]) + 7).zfill(2)][:5]
        for task in upcoming_week:
            due_date = task.get('due', {}).get('date')
            print(f"   {task['content']} (Due: {due_date})")
        print()

    print("=" * 70)
    print(f"Total active tasks: {len(real_tasks)}")
    print("=" * 70)
    print()

if __name__ == "__main__":
    main()
