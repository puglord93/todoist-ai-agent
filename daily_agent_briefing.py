"""
Agent-Driven Daily Briefing
Generates intelligent, context-aware morning digests using the planner agent.
"""
import os
import sys
from datetime import datetime, date
from typing import Dict, Any
from dotenv import load_dotenv
from planner_agent import PlannerAgent

# Load environment
load_dotenv()


def send_email(subject: str, body: str, to_email: str = None) -> bool:
    """
    Send email using SMTP.

    Args:
        subject: Email subject
        body: Email body (HTML or plain text)
        to_email: Recipient email (defaults to BRIEFING_EMAIL env var)

    Returns:
        True if successful, False otherwise
    """
    import smtplib
    from email.mime.text import MIMEText
    from email.mime.multipart import MIMEMultipart

    try:
        to_addr = to_email or os.getenv("BRIEFING_EMAIL")
        if not to_addr:
            print(f"📧 [EMAIL] No recipient configured, saving to file instead")
            return save_briefing_to_file(subject, body)

        smtp_host = os.getenv("BRIEFING_SMTP_HOST", "smtp.gmail.com")
        smtp_port = int(os.getenv("BRIEFING_SMTP_PORT", "587"))
        smtp_user = os.getenv("BRIEFING_SMTP_USER")
        smtp_pass = os.getenv("BRIEFING_SMTP_PASS")

        if not smtp_user or not smtp_pass:
            print(f"📧 [EMAIL] SMTP credentials not configured, saving to file")
            return save_briefing_to_file(subject, body)

        # Create message
        msg = MIMEMultipart('alternative')
        msg['Subject'] = subject
        msg['From'] = smtp_user
        msg['To'] = to_addr

        # Attach body
        part1 = MIMEText(body, 'plain')
        part2 = MIMEText(body, 'html')
        msg.attach(part1)
        msg.attach(part2)

        # Send email
        server = smtplib.SMTP(smtp_host, smtp_port)
        server.starttls()
        server.login(smtp_user, smtp_pass)
        server.send_message(msg)
        server.quit()

        print(f"✅ [EMAIL] Sent to {to_addr}")
        return True

    except Exception as e:
        print(f"❌ [EMAIL] Failed: {e}")
        print(f"📄 [FALLBACK] Saving to file instead")
        return save_briefing_to_file(subject, body)


def save_briefing_to_file(subject: str, body: str) -> bool:
    """
    Save briefing to file as fallback.

    Args:
        subject: Email subject
        body: Email body

    Returns:
        True if successful
    """
    try:
        output_path = os.getenv("BRIEFING_OUTPUT_PATH", "~/todoist_briefing.txt")
        output_path = os.path.expanduser(output_path)

        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(f"{subject}\n")
            f.write("=" * 60 + "\n\n")
            f.write(body)

        print(f"✅ [FILE] Saved to {output_path}")
        return True

    except Exception as e:
        print(f"❌ [FILE] Failed to save: {e}")
        return False


def run_daily_briefing(use_mock: bool = False) -> Dict[str, Any]:
    """
    Run the agent-driven daily briefing.

    Args:
        use_mock: If True, use mock data

    Returns:
        Dictionary with briefing results
    """
    today_str = date.today().strftime("%A, %B %d, %Y")
    day_of_week = date.today().weekday()  # 0=Monday, 6=Sunday

    # Get day-specific context
    day_context = ""
    if day_of_week == 0:  # Monday
        day_context = "It's Monday - start of the work week. Focus on strategic planning and setting the tone."
    elif day_of_week == 4:  # Friday
        day_context = "It's Friday - end of the work week. Focus on wrapping up and preparing for next week."
    elif day_of_week in [5, 6]:  # Weekend
        day_context = "It's the weekend. Focus on personal tasks, rest, or important projects without work pressure."
    else:
        day_context = "Regular weekday. Balance urgent tasks with important long-term work."

    # Construct the goal for the agent
    goal = f"""Generate JJ's morning briefing for {today_str}.

{day_context}

The briefing should be:
- Context-aware based on current workload and day of week
- Motivational and encouraging in tone
- Actionable with clear priorities
- Intelligent (not just a list of tasks)

Include insights like:
- Current workload status (overdue, today's tasks, upcoming)
- Key priorities for the day
- Any patterns or observations
- Motivational context appropriate for the day

Make it feel like a thoughtful assistant who knows JJ's work style and preferences. Keep it concise but meaningful."""

    try:
        print("🧠 [AGENT] Initializing planner agent...")
        agent = PlannerAgent(use_mock=use_mock)

        print(f"🎯 [AGENT] Running goal: Generate morning briefing")
        result = agent.handle_request(goal)

        return {
            "success": True,
            "date": today_str,
            "content": result,
            "day_context": day_context,
            "timestamp": datetime.now().isoformat()
        }

    except Exception as e:
        print(f"❌ [AGENT] Failed: {e}")
        print(f"🔄 [FALLBACK] Switching to original daily_briefing.py...")

        # Fallback to original system
        from daily_briefing import TodoistDailyBriefing

        try:
            briefing = TodoistDailyBriefing()
            output = briefing.generate_briefing()

            # Save to file/email
            subject = f"🗓️ Daily Briefing - {today_str} (Fallback)"
            send_email(subject, output)

            return {
                "success": True,
                "fallback": True,
                "date": today_str,
                "content": output,
                "error": str(e)
            }
        except Exception as fallback_error:
            print(f"❌ [FALLBACK] Also failed: {fallback_error}")
            return {
                "success": False,
                "error": str(e),
                "fallback_error": str(fallback_error)
            }


def main():
    """Main entry point for cron job."""
    use_mock = "--mock" in sys.argv

    print("\n" + "=" * 60)
    print("🗓️ AGENT-DRIVEN DAILY BRIEFING")
    print("=" * 60)

    result = run_daily_briefing(use_mock=use_mock)

    if result["success"]:
        today_str = result["date"]
        print(f"\n✅ Briefing generated for {today_str}")

        # Try to send email
        subject = f"🗓️ Daily Briefing - {today_str}"
        body = result["content"]

        if "--email" in sys.argv or os.getenv("BRIEFING_EMAIL"):
            send_email(subject, body)
        else:
            # Just save to file
            output_path = os.getenv("BRIEFING_OUTPUT_PATH", "~/todoist_briefing.txt")
            output_path = os.path.expanduser(output_path)
            save_briefing_to_file(subject, body)

        print("\n" + "=" * 60)
        print("✅ SUCCESS")
        print("=" * 60)
        sys.exit(0)
    else:
        print(f"\n❌ Failed: {result.get('error', 'Unknown error')}")
        print("\n" + "=" * 60)
        print("❌ FAILED")
        print("=" * 60)
        sys.exit(1)


if __name__ == "__main__":
    main()
