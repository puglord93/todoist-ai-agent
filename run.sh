#!/bin/bash
# Helper script to run the Todoist AI Agent

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Activate virtual environment
source "$SCRIPT_DIR/venv/bin/activate"

# Run the agent with all passed arguments
python3 "$SCRIPT_DIR/main.py" "$@"
