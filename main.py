#!/usr/bin/env python3
"""
Todoist AI Agent - Main Entry Point

Command-line interface for running the Todoist AI agent.
"""

import argparse
import sys
from agent import TodoistAIAgent


def main():
    """Main entry point for the CLI."""
    parser = argparse.ArgumentParser(
        description="AI-powered Todoist task manager and prioritizer",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s                    # Run with default focus report
  %(prog)s --full             # Generate full report with all quadrants
  %(prog)s --top 3            # Show top 3 priorities only
  %(prog)s --quadrant Q1      # Show tasks in Q1 (Do First)
  %(prog)s --suggest          # Get task update suggestions
  %(prog)s --mock             # Use mock data for testing
        """
    )

    parser.add_argument(
        "--full",
        action="store_true",
        help="Generate full report with all Eisenhower quadrants"
    )

    parser.add_argument(
        "--top",
        type=int,
        metavar="N",
        help="Show only top N priority tasks"
    )

    parser.add_argument(
        "--quadrant",
        choices=["Q1", "Q2", "Q3", "Q4"],
        help="Show tasks in specific Eisenhower quadrant"
    )

    parser.add_argument(
        "--suggest",
        action="store_true",
        help="Generate task update suggestions"
    )

    parser.add_argument(
        "--mock",
        action="store_true",
        help="Use mock data instead of real Todoist API (for testing)"
    )

    args = parser.parse_args()

    # Initialize agent
    agent = TodoistAIAgent(use_mock=args.mock)

    try:
        # Handle different modes
        if args.suggest:
            # Show update suggestions
            print("💡 Analyzing tasks for suggestions...\n")
            suggestions = agent.suggest_updates()

            if not suggestions:
                print("✨ No suggestions at this time. Your tasks look well-organized!")
            else:
                print(f"Found {len(suggestions)} suggestions:\n")
                for i, suggestion in enumerate(suggestions, 1):
                    print(f"{i}. {suggestion['task_content']}")
                    print(f"   Suggestion: {suggestion['suggestion']}")
                    print(f"   Reason: {suggestion['reason']}")
                    print()

        elif args.top:
            # Show top N priorities
            top_tasks = agent.get_top_priorities(args.top)
            print(f"🎯 TOP {args.top} PRIORITIES\n")
            print("=" * 60)

            for i, task in enumerate(top_tasks, 1):
                print(f"\n{i}. {task['task_content']}")
                print(f"   Priority Score: {task['priority_score']}/100")
                print(f"   Quadrant: {task['eisenhower_quadrant']}")

                if task["days_until_due"] is not None:
                    if task["is_overdue"]:
                        print(f"   Due: ⚠️ OVERDUE")
                    elif task["days_until_due"] == 0:
                        print(f"   Due: 📅 TODAY")
                    elif task["days_until_due"] == 1:
                        print(f"   Due: 📅 TOMORROW")
                    else:
                        print(f"   Due: In {task['days_until_due']} days")

                if task["recommendations"]:
                    print(f"   💡 {task['recommendations'][0]}")

            print("\n" + "=" * 60)

        elif args.quadrant:
            # Show tasks in specific quadrant
            tasks = agent.get_tasks_by_quadrant(args.quadrant)
            quadrant_names = {
                "Q1": "DO FIRST (Urgent & Important)",
                "Q2": "SCHEDULE (Important, Not Urgent)",
                "Q3": "DELEGATE (Urgent, Not Important)",
                "Q4": "CONSIDER (Neither Urgent nor Important)"
            }

            print(f"📊 {args.quadrant}: {quadrant_names[args.quadrant]}\n")
            print("=" * 60)

            if not tasks:
                print("\nNo tasks in this quadrant")
            else:
                for i, task in enumerate(tasks, 1):
                    print(f"\n{i}. {task['task_content']}")
                    print(f"   Score: {task['priority_score']}/100")

                    if task["days_until_due"] is not None:
                        if task["is_overdue"]:
                            print(f"   Due: ⚠️ OVERDUE")
                        elif task["days_until_due"] == 0:
                            print(f"   Due: TODAY")
                        else:
                            print(f"   Due: {task['days_until_due']} days")

                    if task["labels"]:
                        print(f"   Labels: {', '.join(task['labels'])}")

            print("\n" + "=" * 60)

        else:
            # Generate report (focus or full)
            report_type = "full" if args.full else "focus"
            report = agent.generate_report(report_type)
            print(report)

    except KeyboardInterrupt:
        print("\n\nOperation cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
