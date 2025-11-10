#!/usr/bin/env python3
"""
Example: Using the Task Polish Features Programmatically

This script demonstrates how to use the new AI-powered features
in your own scripts or workflows.
"""

from agent import TodoistAIAgent
from task_polisher import TaskPolisher
from smart_scheduler import SmartScheduler
from mcp_updater import MCPUpdater


def example_1_task_quality_report():
    """Example 1: Generate a task quality report."""
    print("=" * 80)
    print("EXAMPLE 1: Task Quality Report")
    print("=" * 80)

    agent = TodoistAIAgent(use_mock=True)
    report = agent.get_task_quality_report()

    print(f"\nTotal tasks: {report['total_tasks']}")
    print(f"Average quality: {report['average_quality']}%")
    print(f"Tasks needing attention: {report['tasks_needing_attention']}")

    print("\nWorst 3 tasks:")
    for task in report['worst_tasks'][:3]:
        print(f"  - {task['task_content']}: {task['percentage']}%")
        print(f"    Issues: {', '.join(task['issues'])}")


def example_2_polish_single_task():
    """Example 2: Polish a single task."""
    print("\n" + "=" * 80)
    print("EXAMPLE 2: Polish a Single Task")
    print("=" * 80)

    polisher = TaskPolisher()

    task = {
        "id": "test123",
        "content": "call dr",
        "description": "",
        "labels": ["health"]
    }

    result = polisher.polish_task(task)

    print(f"\nOriginal: {result['original_name']}")
    print(f"Polished: {result['suggested_name']}")
    print(f"Description: {result['suggested_description']}")
    print(f"Needs polishing: {result['needs_polishing']}")
    print(f"Reason: {result['polishing_reason']}")


def example_3_infer_due_date():
    """Example 3: Infer due date from task content."""
    print("\n" + "=" * 80)
    print("EXAMPLE 3: Infer Due Date")
    print("=" * 80)

    scheduler = SmartScheduler()

    tasks = [
        {"id": "1", "content": "Pay electricity bill by end of month", "description": ""},
        {"id": "2", "content": "Call dentist tomorrow", "description": ""},
        {"id": "3", "content": "URGENT: Submit report", "description": ""},
        {"id": "4", "content": "Schedule team meeting next Friday", "description": ""},
    ]

    for task in tasks:
        suggestion = scheduler.infer_due_date(task)
        if suggestion:
            print(f"\nTask: {task['content']}")
            print(f"  Suggested date: {suggestion['suggested_date']}")
            print(f"  Confidence: {suggestion['confidence']}")
            print(f"  Source: {suggestion['source']}")


def example_4_batch_polish_and_schedule():
    """Example 4: Batch polish and schedule."""
    print("\n" + "=" * 80)
    print("EXAMPLE 4: Batch Polish and Schedule")
    print("=" * 80)

    agent = TodoistAIAgent(use_mock=True)

    # Get polish suggestions
    print("\n1. Getting polish suggestions...")
    polish_results = agent.polish_tasks(min_quality=50)
    print(f"   Found {len(polish_results)} tasks to polish")

    # Get schedule suggestions
    print("\n2. Getting schedule suggestions...")
    schedule_results = agent.suggest_due_dates()
    print(f"   Found {len(schedule_results)} tasks needing due dates")

    # Show a sample polish suggestion
    if polish_results:
        sample = polish_results[0]
        print(f"\n3. Sample polish suggestion:")
        print(f"   Before: {sample['original_name']}")
        print(f"   After:  {sample['suggested_name']}")

    # Show a sample date suggestion
    if schedule_results:
        sample = schedule_results[0]
        print(f"\n4. Sample date suggestion:")
        print(f"   Task: {sample['task_content']}")
        print(f"   Date: {sample['suggested_date']}")
        print(f"   Reason: {sample.get('reasoning', 'N/A')}")


def example_5_prepare_mcp_updates():
    """Example 5: Prepare updates for MCP."""
    print("\n" + "=" * 80)
    print("EXAMPLE 5: Prepare MCP Updates")
    print("=" * 80)

    # Simulate some approved polish results
    polish_results = [
        {
            "task_id": "task1",
            "original_name": "call john",
            "suggested_name": "Call John about Q4 project review",
            "original_description": "",
            "suggested_description": "Discuss quarterly metrics and roadmap",
            "needs_polishing": True,
            "approved": True  # User approved this
        }
    ]

    # Simulate some schedule results
    schedule_results = [
        {
            "task_id": "task2",
            "task_content": "Submit report",
            "suggested_date": "2025-11-05",
            "confidence": "high",
            "approved": True
        }
    ]

    updater = MCPUpdater()

    # Create update requests
    polish_updates = updater.create_polish_updates(polish_results)
    schedule_updates = updater.create_scheduling_updates(schedule_results)

    all_updates = polish_updates + schedule_updates

    print(f"\nPrepared {len(all_updates)} updates for MCP:")
    for update in all_updates:
        print(f"\n  Task ID: {update['task_id']}")
        print(f"  Updates: {update['updates']}")

    # Generate MCP instructions
    print("\n" + updater.generate_mcp_instructions(all_updates))


def main():
    """Run all examples."""
    print("\n🪄 Task Polish Features - Usage Examples\n")

    try:
        example_1_task_quality_report()
        example_2_polish_single_task()
        example_3_infer_due_date()
        example_4_batch_polish_and_schedule()
        example_5_prepare_mcp_updates()

        print("\n" + "=" * 80)
        print("All examples completed successfully! ✅")
        print("=" * 80)
        print("\nTry modifying these examples for your own use cases.")
        print("See POLISH_FEATURES.md for full API documentation.")

    except ValueError as e:
        print(f"\n❌ Error: {e}")
        print("\nMake sure ANTHROPIC_API_KEY is set:")
        print('  export ANTHROPIC_API_KEY="your-key-here"')
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
