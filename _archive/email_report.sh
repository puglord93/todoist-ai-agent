#!/bin/bash
# Email daily Todoist analysis report

cd /Users/jj/todoist-ai-agent
source venv/bin/activate

# Generate report
REPORT=$(python3 fetch_real_tasks.py)

# Send email via macOS mail (if configured)
# Or use a service like SendGrid, Mailgun, etc.

# Option 1: Use macOS mail command (requires mail setup)
echo "$REPORT" | mail -s "Daily Todoist Focus Plan - $(date +%Y-%m-%d)" your-email@example.com

# Option 2: Use Python with Gmail (more reliable)
# Uncomment and configure if needed
# python3 send_email.py "$REPORT"
