#!/usr/bin/env python3
"""
Demo script to show OpenAI polishing in action
"""

from task_polisher import TaskPolisher

def main():
    print("=" * 70)
    print("🤖 OPENAI TASK POLISHING DEMO")
    print("=" * 70)
    print()

    # Initialize polisher
    polisher = TaskPolisher()
    print(f"✅ Using OpenAI model: {polisher.model}")
    print()

    # Create some sample tasks that need polishing
    sample_tasks = [
        {
            "id": "demo-1",
            "content": "call dentist",
            "description": "",
            "labels": []
        },
        {
            "id": "demo-2",
            "content": "meeting tomorrow",
            "description": "",
            "labels": []
        },
        {
            "id": "demo-3",
            "content": "URGENT buy milk bread eggs",
            "description": "",
            "labels": []
        }
    ]

    for i, task in enumerate(sample_tasks, 1):
        print(f"📌 Task {i}: {task['content']}")
        print("-" * 70)

        print("🤖 Polishing with OpenAI...")
        result = polisher.polish_task(task)

        print(f"   Original: {result['original_name']}")
        print(f"   Polished: {result['suggested_name']}")
        print(f"   Description: {result['suggested_description']}")

        if result.get('extracted_priority'):
            print(f"   Priority: {result['extracted_priority']}")

        if result.get('extracted_labels'):
            print(f"   Labels: {', '.join(result['extracted_labels'])}")

        print(f"   Needs Polish: {result['needs_polishing']}")
        print(f"   Reason: {result['polishing_reason']}")
        print()

    print("=" * 70)
    print("✅ Demo completed!")
    print("=" * 70)

if __name__ == "__main__":
    main()
