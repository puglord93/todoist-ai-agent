#!/bin/bash

# Todoist AI Agent - Daily Briefing Cron Setup (Legacy)
# Interactive script to set up automated daily briefings

# NOTE: This is the legacy setup script. For the new agent-based system,
# use setup_agent_cron.sh instead!

set -e

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Detect script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

echo -e "${BLUE}==========================================${NC}"
echo -e "${BLUE}⚠️  LEGACY SCRIPT WARNING${NC}"
echo -e "${BLUE}==========================================${NC}"
echo ""
echo -e "${YELLOW}This script sets up the LEGACY (non-agent) cron jobs.${NC}"
echo -e "${YELLOW}For the new agent-based system, use:${NC}"
echo -e "${GREEN}  ./setup_agent_cron.sh${NC}"
echo ""
echo "Continue anyway? (y/n)"
read -r -n 1 -r
echo ""

if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Cancelled. Use setup_agent_cron.sh for the agent-based system."
    exit 1
fi

echo ""
echo -e "${BLUE}==========================================${NC}"
echo -e "${BLUE}Todoist AI Agent - Legacy Automation Setup${NC}"
echo -e "${BLUE}==========================================${NC}"
echo ""
echo "This script helps you set up automated cron jobs for:"
echo "  1. Daily briefing (task status reports)"
echo "  2. Auto-polish (automated task improvements)"
echo ""

# Check if virtual environment exists
if [ ! -d "$SCRIPT_DIR/venv" ]; then
    echo -e "${RED}❌ Virtual environment not found at $SCRIPT_DIR/venv${NC}"
    echo -e "${YELLOW}Please run: python3 -m venv venv && source venv/bin/activate && pip install -r requirements.txt${NC}"
    exit 1
fi

echo -e "${GREEN}✅ Virtual environment found${NC}"

# Check if daily_briefing.py exists
if [ ! -f "$SCRIPT_DIR/daily_briefing.py" ]; then
    echo -e "${RED}❌ daily_briefing.py not found${NC}"
    exit 1
fi

echo -e "${GREEN}✅ daily_briefing.py found (legacy)${NC}"
echo ""

# Test the briefing script
echo -e "${BLUE}Testing daily briefing script...${NC}"
if "$SCRIPT_DIR/venv/bin/python3" "$SCRIPT_DIR/daily_briefing.py" --test; then
    echo -e "${GREEN}✅ Test successful!${NC}"
else
    echo -e "${RED}❌ Test failed. Please fix errors before setting up cron.${NC}"
    exit 1
fi

echo ""
echo -e "${BLUE}==========================================${NC}"
echo -e "${BLUE}Which automation do you want to set up?${NC}"
echo -e "${BLUE}==========================================${NC}"
echo ""
echo "1) Daily briefing (task status report)"
echo "2) Auto-polish (automated task improvements)"
echo "3) Both (recommended times: auto-polish at 9:00 AM, briefing at 9:15 AM)"
echo ""
echo "Enter your choice (1-3):"
read -r AUTOMATION_CHOICE

case "$AUTOMATION_CHOICE" in
    1)
        SETUP_BRIEFING=true
        SETUP_AUTO_POLISH=false
        ;;
    2)
        SETUP_BRIEFING=false
        SETUP_AUTO_POLISH=true
        ;;
    3)
        SETUP_BRIEFING=true
        SETUP_AUTO_POLISH=true
        ;;
    *)
        echo -e "${RED}Invalid choice. Exiting.${NC}"
        exit 1
        ;;
esac

echo ""
echo -e "${BLUE}==========================================${NC}"
echo -e "${BLUE}Cron Job Configuration${NC}"
echo -e "${BLUE}==========================================${NC}"
echo ""

# Configure auto-polish if selected
if [ "$SETUP_AUTO_POLISH" = true ]; then
    echo -e "${YELLOW}Auto-polish setup:${NC}"
    echo "What time should auto-polish run?"
    echo "Enter hour (0-23) [default: 9 for 9 AM]:"
    read -r AUTO_POLISH_HOUR
    AUTO_POLISH_HOUR=${AUTO_POLISH_HOUR:-9}

    echo "Enter minute (0-59) [default: 0]:"
    read -r AUTO_POLISH_MINUTE
    AUTO_POLISH_MINUTE=${AUTO_POLISH_MINUTE:-0}

    # Validate input
    if ! [[ "$AUTO_POLISH_HOUR" =~ ^[0-9]+$ ]] || [ "$AUTO_POLISH_HOUR" -lt 0 ] || [ "$AUTO_POLISH_HOUR" -gt 23 ]; then
        echo -e "${RED}Invalid hour. Must be between 0-23.${NC}"
        exit 1
    fi

    if ! [[ "$AUTO_POLISH_MINUTE" =~ ^[0-9]+$ ]] || [ "$AUTO_POLISH_MINUTE" -lt 0 ] || [ "$AUTO_POLISH_MINUTE" -gt 59 ]; then
        echo -e "${RED}Invalid minute. Must be between 0-59.${NC}"
        exit 1
    fi

    # Build auto-polish cron command
    AUTO_POLISH_CRON_CMD="$AUTO_POLISH_MINUTE $AUTO_POLISH_HOUR * * * cd $SCRIPT_DIR && $SCRIPT_DIR/venv/bin/python3 $SCRIPT_DIR/auto_polish.py >> /tmp/todoist_auto_polish.log 2>&1"

    echo ""
    echo -e "${BLUE}Auto-polish cron job:${NC}"
    echo -e "${GREEN}$AUTO_POLISH_CRON_CMD${NC}"
    echo ""
fi

# Configure briefing if selected
if [ "$SETUP_BRIEFING" = true ]; then
    echo -e "${YELLOW}Daily briefing setup:${NC}"
    echo "What time should the briefing run?"
    echo "Enter hour (0-23) [default: 9 for 9 AM]:"
    read -r HOUR
    HOUR=${HOUR:-9}

    echo "Enter minute (0-59) [default: 15]:"
    read -r MINUTE
    MINUTE=${MINUTE:-15}

    # Validate input
    if ! [[ "$HOUR" =~ ^[0-9]+$ ]] || [ "$HOUR" -lt 0 ] || [ "$HOUR" -gt 23 ]; then
        echo -e "${RED}Invalid hour. Must be between 0-23.${NC}"
        exit 1
    fi

    if ! [[ "$MINUTE" =~ ^[0-9]+$ ]] || [ "$MINUTE" -lt 0 ] || [ "$MINUTE" -gt 59 ]; then
        echo -e "${RED}Invalid minute. Must be between 0-59.${NC}"
        exit 1
    fi

    # Build cron command
    BRIEFING_CRON_CMD="$MINUTE $HOUR * * * cd $SCRIPT_DIR && $SCRIPT_DIR/venv/bin/python3 $SCRIPT_DIR/daily_briefing.py >> /tmp/todoist_briefing.log 2>&1"

    echo ""
    echo -e "${BLUE}Daily briefing cron job:${NC}"
    echo -e "${GREEN}$BRIEFING_CRON_CMD${NC}"
    echo ""
fi

# Summary and confirmation
echo ""
echo -e "${BLUE}==========================================${NC}"
echo -e "${BLUE}Summary${NC}"
echo -e "${BLUE}==========================================${NC}"
echo ""

if [ "$SETUP_AUTO_POLISH" = true ]; then
    echo -e "${YELLOW}Auto-polish:${NC} $(printf "%02d:%02d" $AUTO_POLISH_HOUR $AUTO_POLISH_MINUTE) daily"
    echo "  • Improves low-quality tasks automatically"
    echo "  • Logs to: /tmp/todoist_auto_polish.log"
    echo "  • Audit log: ~/todoist_auto_polish.log"
    echo ""
fi

if [ "$SETUP_BRIEFING" = true ]; then
    echo -e "${YELLOW}Daily briefing:${NC} $(printf "%02d:%02d" $HOUR $MINUTE) daily"
    echo "  • Shows overdue, due today, and focus plan"
    echo "  • Saves to: ~/todoist_briefing.txt"
    echo "  • Logs to: /tmp/todoist_briefing.log"
    echo ""
fi

echo "Do you want to add these cron job(s)? (y/n)"
read -r CONFIRM

if [ "$CONFIRM" != "y" ]; then
    echo "Setup cancelled."
    exit 0
fi

# Check for and remove existing jobs
EXISTING_AUTO_POLISH=$(crontab -l 2>/dev/null | grep -F "auto_polish.py" || true)
EXISTING_BRIEFING=$(crontab -l 2>/dev/null | grep -F "daily_briefing.py" || true)

if [ -n "$EXISTING_AUTO_POLISH" ] && [ "$SETUP_AUTO_POLISH" = true ]; then
    echo -e "${YELLOW}⚠️  Removing existing auto-polish cron job${NC}"
    crontab -l 2>/dev/null | grep -v -F "auto_polish.py" | crontab -
fi

if [ -n "$EXISTING_BRIEFING" ] && [ "$SETUP_BRIEFING" = true ]; then
    echo -e "${YELLOW}⚠️  Removing existing briefing cron job${NC}"
    crontab -l 2>/dev/null | grep -v -F "daily_briefing.py" | crontab -
fi

# Add new cron jobs
CRON_ENTRIES=""

if [ "$SETUP_AUTO_POLISH" = true ]; then
    CRON_ENTRIES+="# Todoist AI Agent - Auto-polish low-quality tasks
$AUTO_POLISH_CRON_CMD
"
fi

if [ "$SETUP_BRIEFING" = true ]; then
    CRON_ENTRIES+="# Todoist AI Agent - Daily Morning Briefing
$BRIEFING_CRON_CMD
"
fi

(crontab -l 2>/dev/null; echo "$CRON_ENTRIES") | crontab -

echo ""
echo -e "${GREEN}✅ Cron job(s) added successfully!${NC}"
echo ""
echo -e "${BLUE}==========================================${NC}"
echo -e "${BLUE}Setup Complete!${NC}"
echo -e "${BLUE}==========================================${NC}"
echo ""

if [ "$SETUP_AUTO_POLISH" = true ]; then
    echo -e "${GREEN}Auto-polish will run at $(printf "%02d:%02d" $AUTO_POLISH_HOUR $AUTO_POLISH_MINUTE) every day${NC}"
    echo ""
    echo -e "${YELLOW}⚠️  IMPORTANT: Enable auto-polish in .env:${NC}"
    echo "  AUTO_POLISH_ENABLED=true"
    echo ""
    echo "Test first with:"
    echo "  ${GREEN}$SCRIPT_DIR/venv/bin/python3 $SCRIPT_DIR/auto_polish.py --dry-run${NC}"
    echo ""
fi

if [ "$SETUP_BRIEFING" = true ]; then
    echo -e "${GREEN}Daily briefing will run at $(printf "%02d:%02d" $HOUR $MINUTE) every day${NC}"
    echo ""
    echo "Briefing saved to: ${YELLOW}$(grep BRIEFING_OUTPUT_PATH $SCRIPT_DIR/.env 2>/dev/null | cut -d'=' -f2 || echo "~/todoist_briefing.txt")${NC}"
    echo ""
fi

echo -e "${BLUE}Useful commands:${NC}"
echo "  • View cron jobs: ${GREEN}crontab -l${NC}"
echo "  • Remove all jobs: ${GREEN}crontab -l | grep -v 'todoist' | crontab -${NC}"
if [ "$SETUP_AUTO_POLISH" = true ]; then
    echo "  • View auto-polish logs: ${GREEN}tail -f /tmp/todoist_auto_polish.log${NC}"
    echo "  • Test auto-polish: ${GREEN}$SCRIPT_DIR/venv/bin/python3 $SCRIPT_DIR/auto_polish.py --dry-run${NC}"
fi
if [ "$SETUP_BRIEFING" = true ]; then
    echo "  • View briefing logs: ${GREEN}tail -f /tmp/todoist_briefing.log${NC}"
    echo "  • Test briefing: ${GREEN}$SCRIPT_DIR/venv/bin/python3 $SCRIPT_DIR/daily_briefing.py --test${NC}"
fi
echo ""
