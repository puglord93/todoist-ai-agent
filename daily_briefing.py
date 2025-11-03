#!/usr/bin/env python3
"""
Daily Briefing Script

Generates a daily task briefing with:
- Today's tasks (overdue, due today, upcoming)
- AI-powered focus plan
- Task quality summary

Can output to console, file, or email.
Designed to run via cron for daily automation.
"""

import os
import sys
from datetime import datetime
from typing import Dict, Any, Optional
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from agent import TodoistAIAgent

# Load environment variables
load_dotenv()


class DailyBriefing:
    """Generate and distribute daily task briefings."""

    def __init__(self):
        """Initialize the briefing generator."""
        self.agent = TodoistAIAgent(use_mock=False)
        self.output_path = os.path.expanduser(
            os.getenv("BRIEFING_OUTPUT_PATH", "~/todoist_briefing.txt")
        )

        # Email settings (optional)
        self.email_to = os.getenv("BRIEFING_EMAIL")
        self.smtp_host = os.getenv("BRIEFING_SMTP_HOST", "smtp.gmail.com")
        self.smtp_port = int(os.getenv("BRIEFING_SMTP_PORT", "587"))
        self.smtp_user = os.getenv("BRIEFING_SMTP_USER")
        self.smtp_pass = os.getenv("BRIEFING_SMTP_PASS")

    def generate_briefing(self) -> str:
        """
        Generate the daily briefing report.

        Returns:
            Formatted briefing text
        """
        now = datetime.now()
        date_str = now.strftime("%A, %B %d, %Y")
        time_str = now.strftime("%I:%M %p")

        # Build the report
        lines = []
        lines.append("=" * 70)
        lines.append(f"📅 TODOIST DAILY BRIEFING - {date_str}")
        lines.append("=" * 70)
        lines.append("")

        # Get today's tasks
        today_data = self.agent.get_today_tasks()

        # Overdue tasks
        if today_data["overdue"]:
            lines.append(f"⚠️  OVERDUE ({len(today_data['overdue'])})")
            lines.append("-" * 70)
            for task in today_data["overdue"]:
                priority = task.get('priority', 1)
                priority_emoji = "🔴" if priority >= 3 else "🟡"
                lines.append(f"{priority_emoji} {task.get('content', '')}")
            lines.append("")

        # Due today
        if today_data["due_today"]:
            lines.append(f"📌 DUE TODAY ({len(today_data['due_today'])})")
            lines.append("-" * 70)
            for task in today_data["due_today"]:
                priority = task.get('priority', 1)
                priority_emoji = "🔴" if priority >= 3 else "🟢"
                lines.append(f"{priority_emoji} {task.get('content', '')}")
            lines.append("")
        else:
            lines.append("📌 DUE TODAY")
            lines.append("-" * 70)
            lines.append("✨ No tasks due today!")
            lines.append("")

        # Upcoming tasks
        if today_data["upcoming"]:
            lines.append(f"📆 UPCOMING (Next 7 days) - {len(today_data['upcoming'])} tasks")
            lines.append("-" * 70)
            for task in today_data["upcoming"][:5]:  # Show first 5
                due_date = task.get('due', {}).get('date', 'No date')
                lines.append(f"   {task.get('content', '')} (Due: {due_date})")
            if len(today_data["upcoming"]) > 5:
                lines.append(f"   ... and {len(today_data['upcoming']) - 5} more")
            lines.append("")

        # Focus plan
        lines.append("🎯 TODAY'S FOCUS PLAN")
        lines.append("-" * 70)
        try:
            top_priorities = self.agent.get_top_priorities(n=5)

            if top_priorities:
                for i, task in enumerate(top_priorities, 1):
                    content = task.get("task_content", "")
                    quadrant = task.get("eisenhower_quadrant", "")
                    # Extract quadrant code (e.g., "Q1" from "Q1: Do First (Urgent, Important)")
                    quadrant_code = quadrant.split(":")[0] if quadrant else ""
                    lines.append(f"{i}. [{quadrant_code}] {content}")
            else:
                lines.append("No prioritized tasks available")
            lines.append("")
        except Exception as e:
            lines.append(f"Error generating focus plan: {e}")
            lines.append("")

        # Task quality summary
        lines.append("📊 TASK QUALITY")
        lines.append("-" * 70)
        try:
            quality_report = self.agent.get_task_quality_report()
            avg_quality = quality_report.get("average_quality", 0)
            worst_tasks = quality_report.get("worst_tasks", [])

            # Count tasks below 50% quality
            needs_polish = len([t for t in worst_tasks if t.get("percentage", 100) < 50])

            lines.append(f"Average quality score: {avg_quality}%")
            lines.append(f"Tasks needing polish: {needs_polish}")

            if needs_polish > 0:
                lines.append("")
                lines.append("💡 Run 'venv/bin/python3 chat.py' and say 'polish my tasks' to improve")
        except Exception as e:
            lines.append(f"Error calculating quality: {e}")

        lines.append("")
        lines.append("=" * 70)
        lines.append(f"Generated at {time_str} by Todoist AI Agent")
        lines.append("=" * 70)

        return "\n".join(lines)

    def save_to_file(self, content: str) -> bool:
        """
        Save briefing to file.

        Args:
            content: Briefing text

        Returns:
            True if successful
        """
        try:
            with open(self.output_path, 'w') as f:
                f.write(content)
            print(f"✅ Briefing saved to: {self.output_path}")
            return True
        except Exception as e:
            print(f"❌ Error saving to file: {e}")
            return False

    def send_email(self, content: str) -> bool:
        """
        Send briefing via email (if configured).

        Args:
            content: Briefing text

        Returns:
            True if successful
        """
        if not all([self.email_to, self.smtp_user, self.smtp_pass]):
            print("⏭️  Email not configured, skipping")
            return False

        try:
            # Create message
            msg = MIMEMultipart()
            msg['From'] = self.smtp_user
            msg['To'] = self.email_to
            msg['Subject'] = f"Todoist Daily Briefing - {datetime.now().strftime('%B %d, %Y')}"

            # Add body
            msg.attach(MIMEText(content, 'plain'))

            # Send email
            with smtplib.SMTP(self.smtp_host, self.smtp_port) as server:
                server.starttls()
                server.login(self.smtp_user, self.smtp_pass)
                server.send_message(msg)

            print(f"✅ Briefing sent to: {self.email_to}")
            return True
        except Exception as e:
            print(f"❌ Error sending email: {e}")
            return False

    def run(self, mode: str = "all"):
        """
        Run the daily briefing.

        Args:
            mode: Output mode - "console", "file", "email", or "all" (default)
        """
        print("🤖 Generating daily briefing...")

        try:
            # Generate briefing
            briefing = self.generate_briefing()

            # Output based on mode
            if mode in ["console", "all"]:
                print("\n" + briefing + "\n")

            if mode in ["file", "all"]:
                self.save_to_file(briefing)

            if mode in ["email", "all"]:
                self.send_email(briefing)

            print("✅ Daily briefing complete!")

        except Exception as e:
            print(f"❌ Error generating briefing: {e}")
            sys.exit(1)


def main():
    """Main entry point."""
    import argparse

    parser = argparse.ArgumentParser(description="Generate daily Todoist briefing")
    parser.add_argument(
        "--mode",
        choices=["console", "file", "email", "all"],
        default="all",
        help="Output mode (default: all)"
    )
    parser.add_argument(
        "--test",
        action="store_true",
        help="Test mode - only output to console"
    )

    args = parser.parse_args()

    # Override mode if test
    if args.test:
        args.mode = "console"

    # Run briefing
    briefing = DailyBriefing()
    briefing.run(mode=args.mode)


if __name__ == "__main__":
    main()
