#!/usr/bin/env python3
"""
Interactive Task Polish Workflow

Fetches tasks, analyzes them, suggests improvements, and prepares updates.
"""

import argparse
import sys
import json
from typing import List, Dict, Any
from todoist_client import TodoistClient
from task_polisher import TaskPolisher
from smart_scheduler import SmartScheduler
from mcp_updater import MCPUpdater


class InteractivePolishWorkflow:
    """Interactive workflow for polishing Todoist tasks."""

    def __init__(self, use_mock: bool = False):
        """
        Initialize the workflow.

        Args:
            use_mock: Use mock data for testing
        """
        self.client = TodoistClient(use_mock=use_mock)
        self.polisher = TaskPolisher()
        self.scheduler = SmartScheduler()
        self.updater = MCPUpdater()

    def run(self, mode: str = "polish", min_quality: int = 50,
            auto_approve: bool = False) -> Dict[str, Any]:
        """
        Run the interactive polish workflow.

        Args:
            mode: Workflow mode ("polish", "schedule", "both")
            min_quality: Minimum quality score for polishing suggestions
            auto_approve: Auto-approve all suggestions (skip interactive review)

        Returns:
            Results dictionary
        """
        print("🪄 Todoist Task Polish Workflow")
        print("=" * 80)
        print()

        # Step 1: Fetch tasks
        print("📥 Fetching tasks from Todoist...")
        raw_tasks = self.client.fetch_tasks()
        tasks = [self.client.normalize_task(task) for task in raw_tasks]
        print(f"   Found {len(tasks)} tasks\n")

        results = {
            "total_tasks": len(tasks),
            "polish_suggestions": [],
            "schedule_suggestions": [],
            "approved_updates": [],
            "skipped": []
        }

        # Step 2: Identify tasks needing attention
        if mode in ["polish", "both"]:
            print("🔍 Analyzing task quality...")
            needs_polish = self.polisher.identify_tasks_needing_polish(
                tasks, min_quality=min_quality
            )
            print(f"   Found {len(needs_polish)} tasks below quality threshold\n")

            if needs_polish:
                print("✨ Generating polish suggestions...")
                polish_suggestions = self.polisher.polish_tasks_batch(needs_polish)
                results["polish_suggestions"] = polish_suggestions

                # Filter to only those that actually need polishing
                polish_suggestions = [s for s in polish_suggestions
                                     if s.get("needs_polishing", False)]
                print(f"   Generated {len(polish_suggestions)} suggestions\n")

                if polish_suggestions and not auto_approve:
                    print("=" * 80)
                    print("POLISH SUGGESTIONS - REVIEW AND APPROVE")
                    print("=" * 80)
                    results["approved_updates"].extend(
                        self._review_polish_suggestions(polish_suggestions)
                    )

        # Step 3: Suggest due dates
        if mode in ["schedule", "both"]:
            print("\n📅 Checking for tasks needing due dates...")
            tasks_without_dates = [t for t in tasks if not t.get("due_date")]
            print(f"   Found {len(tasks_without_dates)} tasks without due dates\n")

            if tasks_without_dates:
                print("🤖 Inferring due dates...")
                schedule_suggestions = self.scheduler.suggest_due_dates_batch(
                    tasks_without_dates
                )
                results["schedule_suggestions"] = schedule_suggestions
                print(f"   Generated {len(schedule_suggestions)} suggestions\n")

                if schedule_suggestions and not auto_approve:
                    print("=" * 80)
                    print("DUE DATE SUGGESTIONS - REVIEW AND APPROVE")
                    print("=" * 80)
                    results["approved_updates"].extend(
                        self._review_schedule_suggestions(schedule_suggestions)
                    )

        # Step 4: Generate update requests
        if results["approved_updates"]:
            print("\n" + "=" * 80)
            print("GENERATING UPDATE REQUESTS")
            print("=" * 80)

            updates = self._convert_to_updates(results["approved_updates"])

            # Save to file
            self.updater.save_updates_to_file(updates, "pending_updates.json")
            print(f"\n✅ Saved {len(updates)} updates to pending_updates.json")

            # Generate summary
            summary = self.updater.create_summary_report(updates, tasks)
            print("\n" + summary)

            # Show MCP instructions
            print("\n" + "=" * 80)
            print("NEXT STEPS - APPLY UPDATES VIA MCP")
            print("=" * 80)
            print("\nTo apply these updates, ask Claude Code:")
            print('  "Apply the updates from pending_updates.json to Todoist using MCP"')
            print("\nOr manually review: pending_updates.json")

            results["update_file"] = "pending_updates.json"

        else:
            print("\n✨ No updates needed! Your tasks look well-organized.")

        return results

    def _review_polish_suggestions(self, suggestions: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Interactively review polish suggestions.

        Args:
            suggestions: List of polish suggestions

        Returns:
            List of approved suggestions
        """
        approved = []

        for i, suggestion in enumerate(suggestions, 1):
            print(f"\n{'='*80}")
            print(f"SUGGESTION {i}/{len(suggestions)}")
            print(f"{'='*80}")
            print(f"\nTask: {suggestion['original_name']}")
            print(f"Quality Issue: {suggestion.get('polishing_reason', 'Needs improvement')}")
            print(f"\nCurrent Name: {suggestion['original_name']}")
            print(f"Suggested Name: {suggestion['suggested_name']}")

            if suggestion['original_description'] or suggestion['suggested_description']:
                print(f"\nCurrent Description: {suggestion['original_description'] or '(empty)'}")
                print(f"Suggested Description: {suggestion['suggested_description']}")

            if suggestion.get('extracted_priority'):
                print(f"\nExtracted Priority: {suggestion['extracted_priority']}")

            if suggestion.get('extracted_labels'):
                print(f"Suggested Labels: {', '.join(suggestion['extracted_labels'])}")

            # Get user input
            while True:
                choice = input("\nApprove this change? (y/n/q): ").lower().strip()
                if choice in ['y', 'yes']:
                    suggestion['approved'] = True
                    approved.append(suggestion)
                    print("✅ Approved")
                    break
                elif choice in ['n', 'no']:
                    suggestion['approved'] = False
                    print("⏭️  Skipped")
                    break
                elif choice in ['q', 'quit']:
                    print("\n🛑 Exiting review process...")
                    return approved
                else:
                    print("Invalid choice. Please enter y, n, or q.")

        return approved

    def _review_schedule_suggestions(self, suggestions: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Interactively review due date suggestions.

        Args:
            suggestions: List of schedule suggestions

        Returns:
            List of approved suggestions
        """
        approved = []

        for i, suggestion in enumerate(suggestions, 1):
            print(f"\n{'='*80}")
            print(f"DUE DATE SUGGESTION {i}/{len(suggestions)}")
            print(f"{'='*80}")
            print(f"\nTask: {suggestion['task_content']}")
            print(f"Suggested Date: {suggestion['suggested_date']}")
            print(f"Confidence: {suggestion['confidence']}")
            print(f"Reasoning: {suggestion.get('reasoning', suggestion.get('source', 'N/A'))}")

            # Get user input
            while True:
                choice = input("\nApprove this due date? (y/n/q): ").lower().strip()
                if choice in ['y', 'yes']:
                    suggestion['approved'] = True
                    approved.append(suggestion)
                    print("✅ Approved")
                    break
                elif choice in ['n', 'no']:
                    suggestion['approved'] = False
                    print("⏭️  Skipped")
                    break
                elif choice in ['q', 'quit']:
                    print("\n🛑 Exiting review process...")
                    return approved
                else:
                    print("Invalid choice. Please enter y, n, or q.")

        return approved

    def _convert_to_updates(self, approved: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Convert approved suggestions to update format.

        Args:
            approved: List of approved suggestions

        Returns:
            List of update requests
        """
        updates = []

        for item in approved:
            update = {
                "task_id": item["task_id"],
                "updates": {}
            }

            # Polish updates
            if "suggested_name" in item and item.get("approved"):
                if item["suggested_name"] != item.get("original_name"):
                    update["updates"]["content"] = item["suggested_name"]
                if item["suggested_description"] != item.get("original_description", ""):
                    update["updates"]["description"] = item["suggested_description"]
                if item.get("extracted_priority"):
                    update["updates"]["priority"] = item["extracted_priority"]
                if item.get("extracted_labels"):
                    update["updates"]["labels"] = item["extracted_labels"]

            # Schedule updates
            if "suggested_date" in item and item.get("approved"):
                update["updates"]["due_date"] = item["suggested_date"]

            if update["updates"]:
                updates.append(update)

        return updates


def main():
    """Main entry point for CLI."""
    parser = argparse.ArgumentParser(
        description="Interactive task polish workflow",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s                          # Polish tasks interactively
  %(prog)s --mode schedule          # Only suggest due dates
  %(prog)s --mode both              # Polish and schedule
  %(prog)s --quality 60             # Higher quality threshold
  %(prog)s --mock                   # Test with mock data
        """
    )

    parser.add_argument(
        "--mode",
        choices=["polish", "schedule", "both"],
        default="both",
        help="Workflow mode (default: both)"
    )

    parser.add_argument(
        "--quality",
        type=int,
        default=50,
        metavar="N",
        help="Minimum quality score (0-100, default: 50)"
    )

    parser.add_argument(
        "--mock",
        action="store_true",
        help="Use mock data for testing"
    )

    parser.add_argument(
        "--auto-approve",
        action="store_true",
        help="Auto-approve all suggestions (skip interactive review)"
    )

    args = parser.parse_args()

    try:
        workflow = InteractivePolishWorkflow(use_mock=args.mock)
        results = workflow.run(
            mode=args.mode,
            min_quality=args.quality,
            auto_approve=args.auto_approve
        )

        print("\n" + "=" * 80)
        print("WORKFLOW COMPLETE")
        print("=" * 80)
        print(f"Total tasks analyzed: {results['total_tasks']}")
        print(f"Polish suggestions: {len(results.get('polish_suggestions', []))}")
        print(f"Schedule suggestions: {len(results.get('schedule_suggestions', []))}")
        print(f"Approved updates: {len(results.get('approved_updates', []))}")

    except KeyboardInterrupt:
        print("\n\n🛑 Workflow cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
