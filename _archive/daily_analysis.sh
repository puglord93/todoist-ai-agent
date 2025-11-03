#!/bin/bash
# Daily Todoist Analysis - Auto-run script

# Change to project directory
cd /Users/jj/todoist-ai-agent

# Activate virtual environment
source venv/bin/activate

# Run analysis and save to file
OUTPUT_FILE="daily_reports/analysis_$(date +%Y-%m-%d).txt"
mkdir -p daily_reports

echo "==================================" > "$OUTPUT_FILE"
echo "Todoist Analysis - $(date)" >> "$OUTPUT_FILE"
echo "==================================" >> "$OUTPUT_FILE"
echo "" >> "$OUTPUT_FILE"

# Run the analysis
python3 fetch_real_tasks.py >> "$OUTPUT_FILE" 2>&1

# Optional: Display in terminal if running manually
cat "$OUTPUT_FILE"

# Optional: Send notification (macOS)
osascript -e 'display notification "Your daily Todoist analysis is ready!" with title "Todoist AI Agent"'

echo ""
echo "Report saved to: $OUTPUT_FILE"
