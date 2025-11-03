#!/bin/bash

# Todoist AI Agent - Daily Briefing Cron Setup
# Interactive script to set up automated daily briefings

set -e

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Detect script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

echo -e "${BLUE}======================================${NC}"
echo -e "${BLUE}Todoist AI Agent - Daily Briefing Setup${NC}"
echo -e "${BLUE}======================================${NC}"
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

echo -e "${GREEN}✅ daily_briefing.py found${NC}"
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
echo -e "${BLUE}======================================${NC}"
echo -e "${BLUE}Cron Job Configuration${NC}"
echo -e "${BLUE}======================================${NC}"
echo ""

# Ask for schedule time
echo -e "${YELLOW}What time should the briefing run?${NC}"
echo "Enter hour (0-23) [default: 7 for 7 AM]:"
read -r HOUR
HOUR=${HOUR:-7}

echo "Enter minute (0-59) [default: 0]:"
read -r MINUTE
MINUTE=${MINUTE:-0}

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
CRON_CMD="$MINUTE $HOUR * * * cd $SCRIPT_DIR && $SCRIPT_DIR/venv/bin/python3 $SCRIPT_DIR/daily_briefing.py >> /tmp/todoist_briefing.log 2>&1"

echo ""
echo -e "${BLUE}Cron job to be added:${NC}"
echo -e "${GREEN}$CRON_CMD${NC}"
echo ""

# Check if cron job already exists
EXISTING_CRON=$(crontab -l 2>/dev/null | grep -F "daily_briefing.py" || true)

if [ -n "$EXISTING_CRON" ]; then
    echo -e "${YELLOW}⚠️  Existing Todoist briefing cron job found:${NC}"
    echo "$EXISTING_CRON"
    echo ""
    echo "Do you want to replace it? (y/n)"
    read -r REPLACE
    if [ "$REPLACE" != "y" ]; then
        echo "Setup cancelled."
        exit 0
    fi

    # Remove existing job
    crontab -l 2>/dev/null | grep -v -F "daily_briefing.py" | crontab -
    echo -e "${GREEN}✅ Removed existing cron job${NC}"
fi

# Add new cron job
echo "Do you want to add this cron job? (y/n)"
read -r CONFIRM

if [ "$CONFIRM" = "y" ]; then
    # Add to crontab
    (crontab -l 2>/dev/null; echo "# Todoist AI Agent - Daily Morning Briefing"; echo "$CRON_CMD") | crontab -
    echo -e "${GREEN}✅ Cron job added successfully!${NC}"
    echo ""
    echo -e "${BLUE}======================================${NC}"
    echo -e "${BLUE}Setup Complete!${NC}"
    echo -e "${BLUE}======================================${NC}"
    echo ""
    echo -e "${GREEN}Your daily briefing will run at $(printf "%02d:%02d" $HOUR $MINUTE) every day.${NC}"
    echo ""
    echo "Briefing will be saved to: ${YELLOW}$(grep BRIEFING_OUTPUT_PATH $SCRIPT_DIR/.env 2>/dev/null | cut -d'=' -f2 || echo "~/todoist_briefing.txt")${NC}"
    echo ""
    echo "Logs will be saved to: ${YELLOW}/tmp/todoist_briefing.log${NC}"
    echo ""
    echo -e "${BLUE}Useful commands:${NC}"
    echo "  • View current cron jobs: ${GREEN}crontab -l${NC}"
    echo "  • Remove this cron job: ${GREEN}crontab -l | grep -v daily_briefing.py | crontab -${NC}"
    echo "  • View logs: ${GREEN}tail -f /tmp/todoist_briefing.log${NC}"
    echo "  • Test manually: ${GREEN}$SCRIPT_DIR/venv/bin/python3 $SCRIPT_DIR/daily_briefing.py --test${NC}"
    echo ""
    echo -e "${YELLOW}💡 Tip: To access from Windows, use: ssh your-mac 'cat ~/todoist_briefing.txt'${NC}"
    echo ""
else
    echo "Setup cancelled."
    exit 0
fi
