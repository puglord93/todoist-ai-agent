#!/bin/bash
# Setup script for agent-driven daily briefing cron job

echo "============================================================"
echo "🗓️  AGENT-DRIVEN DAILY BRIEFING SETUP"
echo "============================================================"
echo ""
echo "This will set up an intelligent, context-aware daily briefing"
echo "that uses AI to generate personalized morning digests."
echo ""
echo "The briefing will:"
echo "  • Adapt to your workload and day of week"
echo "  • Provide motivational, intelligent insights"
echo "  • Send email or save to file"
echo "  • Fall back to original system if needed"
echo ""
read -p "Continue? (y/n) " -n 1 -r
echo ""

if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Cancelled."
    exit 1
fi

echo ""
echo "📧 Email Configuration"
echo "----------------------"
echo "Do you want to receive the briefing via email?"
read -p "Enable email? (y/n) " -n 1 -r
echo ""

if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo ""
    echo "Enter email details:"
    read -p "Your email address: " recipient
    read -p "SMTP server (default: smtp.gmail.com): " smtp_host
    smtp_host=${smtp_host:-smtp.gmail.com}

    read -p "SMTP port (default: 587): " smtp_port
    smtp_port=${smtp_port:-587}

    read -p "SMTP username (your email): " smtp_user
    read -s -p "SMTP password/app password: " smtp_pass
    echo ""

    # Update .env file
    echo ""
    echo "📝 Updating .env file..."

    # Backup original
    cp .env .env.backup.$(date +%Y%m%d_%H%M%S) 2>/dev/null || true

    # Update email settings
    if grep -q "BRIEFING_EMAIL=" .env 2>/dev/null; then
        sed -i "s|BRIEFING_EMAIL=.*|BRIEFING_EMAIL=$recipient|" .env
        sed -i "s|BRIEFING_SMTP_HOST=.*|BRIEFING_SMTP_HOST=$smtp_host|" .env
        sed -i "s|BRIEFING_SMTP_PORT=.*|BRIEFING_SMTP_PORT=$smtp_port|" .env
        sed -i "s|BRIEFING_SMTP_USER=.*|BRIEFING_SMTP_USER=$smtp_user|" .env
        sed -i "s|BRIEFING_SMTP_PASS=.*|BRIEFING_SMTP_PASS=$smtp_pass|" .env
    else
        cat >> .env << EOF

# Email settings (configured by setup script)
BRIEFING_EMAIL=$recipient
BRIEFING_SMTP_HOST=$smtp_host
BRIEFING_SMTP_PORT=$smtp_port
BRIEFING_SMTP_USER=$smtp_user
BRIEFING_SMTP_PASS=$smtp_pass
EOF
    fi

    echo "✅ Email configured!"
else
    echo "📝 Email disabled - briefing will be saved to file"
    echo "   Default location: ~/todoist_briefing.txt"
fi

echo ""
echo "⏰ Schedule Configuration"
echo "-------------------------"
echo "When would you like to receive the briefing?"
echo "  1) 8:00 AM (recommended)"
echo "  2) 7:00 AM"
echo "  3) 9:00 AM"
echo "  4) Custom time"
read -p "Select (1-4): " -n 1 -r
echo ""

case $REPLY in
    1) hour="8" ;;
    2) hour="7" ;;
    3) hour="9" ;;
    4)
        read -p "Enter hour (0-23): " hour
        ;;
    *)
        hour="8"
        ;;
esac

# Get absolute path to script
SCRIPT_PATH=$(realpath daily_agent_briefing.py)
PROJECT_DIR=$(dirname "$SCRIPT_PATH")

echo ""
echo "🔧 Creating cron job..."
echo "   Schedule: $hour:00 every day"
echo "   Script: $SCRIPT_PATH"

# Create cron command
CRON_CMD="0 $hour * * * cd $PROJECT_DIR && python daily_agent_briefing.py >> ~/todoist_briefing_cron.log 2>&1"

# Add to crontab
(crontab -l 2>/dev/null; echo "$CRON_CMD") | crontab -

echo "✅ Cron job created!"

echo ""
echo "📋 Testing the briefing..."
echo "Would you like to test the briefing now?"
read -p "Run test? (y/n) " -n 1 -r
echo ""

if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo ""
    echo "🧪 Running test (using mock data)..."
    python daily_agent_briefing.py --mock
    echo ""
    echo "Check the output above to see how it looks!"
fi

echo ""
echo "============================================================"
echo "✅ SETUP COMPLETE!"
echo "============================================================"
echo ""
echo "Your agent-driven daily briefing is now configured!"
echo ""
echo "📅 Schedule: Every day at $hour:00"
echo "📧 Email: $([ -n "$recipient" ] && echo "Enabled - $recipient" || echo "Disabled - saving to file")"
echo ""
echo "Commands:"
echo "  • Test briefing:           python daily_agent_briefing.py --mock"
echo "  • View cron jobs:          crontab -l"
echo "  • Remove cron job:         crontab -r"
echo "  • View log:                tail -f ~/todoist_briefing_cron.log"
echo ""
echo "The briefing will be intelligent and adaptive, changing"
echo "based on your workload, day of week, and preferences!"
echo ""
