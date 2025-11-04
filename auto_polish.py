#!/usr/bin/env python3
"""
Auto Polish Script

Automatically polishes low-quality tasks on schedule.
Designed for cron automation with safety features:
- Quality threshold filtering
- Rate limiting (max tasks per run)
- Audit logging with rollback data
- Dry-run mode for testing
"""

import os
import sys
import json
from datetime import datetime
from typing import Dict, Any, List, Optional
from dotenv import load_dotenv

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from agent import TodoistAIAgent
from todoist_client import TodoistClient
from task_updater import TaskUpdater

# Load environment variables
load_dotenv()


class AutoPolisher:
    """Automated task polishing with safety features."""

    def __init__(self, dry_run: bool = False):
        """
        Initialize the auto polisher.

        Args:
            dry_run: If True, preview changes without applying
        """
        self.agent = TodoistAIAgent(use_mock=False)
        self.client = TodoistClient(use_mock=False)
        self.updater = TaskUpdater()
        self.dry_run = dry_run

        # Configuration from environment
        self.enabled = os.getenv("AUTO_POLISH_ENABLED", "false").lower() == "true"
        self.quality_threshold = int(os.getenv("AUTO_POLISH_QUALITY_THRESHOLD", "40"))
        self.max_tasks = int(os.getenv("AUTO_POLISH_MAX_TASKS", "5"))
        self.log_path = os.path.expanduser(
            os.getenv("AUTO_POLISH_LOG_PATH", "~/todoist_auto_polish.log")
        )

    def run(self) -> Dict[str, Any]:
        """
        Run the auto-polish workflow.

        Returns:
            Results dictionary with statistics
        """
        results = {
            "timestamp": datetime.now().isoformat(),
            "dry_run": self.dry_run,
            "enabled": self.enabled,
            "tasks_analyzed": 0,
            "tasks_below_threshold": 0,
            "tasks_polished": 0,
            "tasks_updated": 0,
            "errors": [],
            "changes": []
        }

        # Check if enabled
        if not self.enabled and not self.dry_run:
            print("⏭️  Auto-polish is disabled (AUTO_POLISH_ENABLED=false)")
            print("   Run with --dry-run to test, or enable in .env")
            return results

        print("🤖 Auto Polish - Automated Task Improvement")
        print("=" * 70)
        print(f"Mode: {'DRY RUN (preview only)' if self.dry_run else 'LIVE (will apply changes)'}")
        print(f"Quality threshold: {self.quality_threshold}%")
        print(f"Max tasks per run: {self.max_tasks}")
        print()

        try:
            # Step 1: Get task quality report
            print("📊 Analyzing task quality...")
            quality_report = self.agent.get_task_quality_report()
            results["tasks_analyzed"] = quality_report["total_tasks"]

            # Step 2: Filter tasks below threshold
            worst_tasks = quality_report.get("worst_tasks", [])
            tasks_below_threshold = [
                t for t in worst_tasks
                if t.get("percentage", 100) < self.quality_threshold
            ]
            results["tasks_below_threshold"] = len(tasks_below_threshold)

            print(f"   Total tasks: {results['tasks_analyzed']}")
            print(f"   Below {self.quality_threshold}% quality: {len(tasks_below_threshold)}")
            print()

            if not tasks_below_threshold:
                print("✨ No tasks need polishing! All tasks meet quality threshold.")
                self._log_results(results)
                return results

            # Step 3: Limit to max_tasks
            tasks_to_polish = tasks_below_threshold[:self.max_tasks]
            if len(tasks_below_threshold) > self.max_tasks:
                print(f"⚠️  Limiting to {self.max_tasks} tasks (found {len(tasks_below_threshold)})")
                print(f"   Remaining tasks will be processed in next run")
                print()

            # Step 4: Get full task data for selected tasks
            print(f"🔍 Fetching full task data for {len(tasks_to_polish)} tasks...")
            raw_tasks = self.client.fetch_tasks()
            normalized_tasks = [self.client.normalize_task(task) for task in raw_tasks]

            # Map task IDs to full task objects
            task_map = {t.get("id"): t for t in normalized_tasks}
            tasks_to_polish_full = []
            for quality_task in tasks_to_polish:
                task_id = quality_task.get("task_id")
                if task_id in task_map:
                    tasks_to_polish_full.append(task_map[task_id])

            # Step 5: Generate polish suggestions
            print("✨ Generating AI polish suggestions...")
            polish_suggestions = self.agent.polisher.polish_tasks_batch(tasks_to_polish_full)

            # Filter to only those that actually need polishing
            polish_suggestions = [
                s for s in polish_suggestions
                if s.get("needs_polishing", False)
            ]
            results["tasks_polished"] = len(polish_suggestions)

            print(f"   Generated {len(polish_suggestions)} polish suggestions")
            print()

            if not polish_suggestions:
                print("✨ All tasks are already well-formatted!")
                self._log_results(results)
                return results

            # Step 6: Preview and apply changes
            print("=" * 70)
            print("POLISH CHANGES" + (" (PREVIEW ONLY)" if self.dry_run else ""))
            print("=" * 70)
            print()

            for i, suggestion in enumerate(polish_suggestions, 1):
                task_id = suggestion["task_id"]
                task = task_map.get(task_id)
                if not task:
                    continue

                print(f"[{i}/{len(polish_suggestions)}] {suggestion['original_name']}")
                print(f"Quality: {quality_report['worst_tasks'][i-1]['percentage']}%")
                print(f"Reason: {suggestion.get('polishing_reason', 'Needs improvement')}")
                print()

                # Build updates dictionary
                updates = {}
                if suggestion["suggested_name"] != suggestion["original_name"]:
                    updates["content"] = suggestion["suggested_name"]
                if suggestion["suggested_description"] != suggestion.get("original_description", ""):
                    updates["description"] = suggestion["suggested_description"]

                # Create preview
                preview = self.updater.create_update_preview(task, updates)
                print(self.updater.format_preview(preview))
                print()

                # Apply update (if not dry run)
                if updates and not self.dry_run:
                    success = self.client.update_task(task_id, updates)
                    if success:
                        results["tasks_updated"] += 1
                        change_record = {
                            "timestamp": datetime.now().isoformat(),
                            "task_id": task_id,
                            "before": {
                                "name": suggestion["original_name"],
                                "description": suggestion.get("original_description", "")
                            },
                            "after": {
                                "name": suggestion["suggested_name"],
                                "description": suggestion["suggested_description"]
                            },
                            "quality_before": quality_report['worst_tasks'][i-1]['percentage']
                        }
                        results["changes"].append(change_record)
                        print("✅ Updated successfully")
                    else:
                        error_msg = f"Failed to update task: {suggestion['original_name']}"
                        results["errors"].append(error_msg)
                        print(f"❌ {error_msg}")
                elif updates:
                    print("⏭️  Skipped (dry-run mode)")

                print("-" * 70)
                print()

            # Step 7: Summary
            print("=" * 70)
            print("AUTO POLISH SUMMARY")
            print("=" * 70)
            print(f"Tasks analyzed: {results['tasks_analyzed']}")
            print(f"Below threshold: {results['tasks_below_threshold']}")
            print(f"Polish suggestions: {results['tasks_polished']}")
            if not self.dry_run:
                print(f"Successfully updated: {results['tasks_updated']}")
                print(f"Errors: {len(results['errors'])}")
            else:
                print("\n💡 This was a dry run. Set AUTO_POLISH_ENABLED=true to apply changes.")
            print()

            # Step 8: Log results
            self._log_results(results)

        except Exception as e:
            error_msg = f"Error during auto-polish: {e}"
            results["errors"].append(error_msg)
            print(f"❌ {error_msg}")
            import traceback
            traceback.print_exc()

        return results

    def _log_results(self, results: Dict[str, Any]) -> None:
        """
        Log results to audit file.

        Args:
            results: Results dictionary
        """
        try:
            # Create log entry
            log_entry = {
                "timestamp": results["timestamp"],
                "dry_run": results["dry_run"],
                "enabled": results["enabled"],
                "summary": {
                    "tasks_analyzed": results["tasks_analyzed"],
                    "tasks_below_threshold": results["tasks_below_threshold"],
                    "tasks_polished": results["tasks_polished"],
                    "tasks_updated": results["tasks_updated"],
                    "errors": results["errors"]
                },
                "changes": results["changes"]
            }

            # Append to log file
            with open(self.log_path, 'a') as f:
                f.write(json.dumps(log_entry, indent=2))
                f.write("\n" + "="*70 + "\n")

            if results["changes"]:
                print(f"📝 Audit log updated: {self.log_path}")

        except Exception as e:
            print(f"⚠️  Warning: Failed to write log: {e}")


def main():
    """Main entry point."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Automatically polish low-quality Todoist tasks",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --dry-run           # Preview changes without applying
  %(prog)s                     # Apply changes (if AUTO_POLISH_ENABLED=true)
  %(prog)s --force             # Apply changes even if disabled in config

Configuration (in .env):
  AUTO_POLISH_ENABLED=true           # Enable auto-polishing
  AUTO_POLISH_QUALITY_THRESHOLD=40   # Only polish tasks below 40%%
  AUTO_POLISH_MAX_TASKS=5            # Max 5 tasks per run
  AUTO_POLISH_LOG_PATH=~/todoist_auto_polish.log

Safety Features:
  - Only polishes tasks below quality threshold
  - Rate limited to max tasks per run
  - Detailed audit logging with rollback data
  - Dry-run mode for safe testing
        """
    )

    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview changes without applying (ignores AUTO_POLISH_ENABLED)"
    )

    parser.add_argument(
        "--force",
        action="store_true",
        help="Force run even if AUTO_POLISH_ENABLED=false"
    )

    args = parser.parse_args()

    # Override enabled check if force flag set
    if args.force:
        os.environ["AUTO_POLISH_ENABLED"] = "true"

    # Run auto polisher
    polisher = AutoPolisher(dry_run=args.dry_run)
    results = polisher.run()

    # Exit with error code if there were errors
    if results["errors"]:
        sys.exit(1)


if __name__ == "__main__":
    main()
