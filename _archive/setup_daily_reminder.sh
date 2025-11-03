#!/bin/bash
# Setup Daily 9am Todoist Review Reminder

echo "Setting up daily 9am Todoist task review reminder..."
echo ""
echo "Choose your preferred method:"
echo ""
echo "1. macOS Calendar (Recommended - Simple)"
echo "2. macOS Shortcuts + Notification"
echo "3. Automated Script (requires setup)"
echo ""
read -p "Enter your choice (1-3): " choice

case $choice in
    1)
        echo ""
        echo "📅 Setting up Calendar Event:"
        echo ""
        echo "To create a 9am daily reminder:"
        echo "1. Open Calendar app (⌘+Space, type 'Calendar')"
        echo "2. Create a new event (⌘+N)"
        echo "3. Set the details:"
        echo "   - Title: 'Review Todoist Tasks'"
        echo "   - Time: 9:00 AM"
        echo "   - Repeat: Daily"
        echo "   - Alert: At time of event"
        echo "4. In the notes, add:"
        echo "   'Open Terminal and ask Claude: Review my Todoist tasks and suggest improvements'"
        echo ""
        echo "When the notification appears at 9am, just:"
        echo "   1. Open Terminal (or Claude Code)"
        echo "   2. Ask me: 'Review my Todoist tasks and suggest improvements'"
        echo ""
        ;;
    2)
        echo ""
        echo "📱 Setting up macOS Shortcut:"
        echo ""
        echo "1. Open Shortcuts app"
        echo "2. Create new shortcut"
        echo "3. Add these actions:"
        echo "   - 'Show Notification'"
        echo "   - Title: 'Review Todoist Tasks'"
        echo "   - Body: 'Time to organize your tasks with Claude!'"
        echo "4. Set automation:"
        echo "   - Automation tab → Create Personal Automation"
        echo "   - Time of Day → 9:00 AM"
        echo "   - Daily"
        echo "   - Run this shortcut"
        echo ""
        echo "Or use this shortcut link (if you have Shortcuts):"
        echo "shortcuts://create-shortcut"
        echo ""
        ;;
    3)
        echo ""
        echo "⚙️  Setting up Automated Script:"
        echo ""
        echo "This will create a LaunchAgent that runs daily at 9am"
        echo ""
        read -p "Create automated script? (y/n): " confirm
        if [[ $confirm == "y" ]]; then
            # Create launch agent plist
            cat > ~/Library/LaunchAgents/com.user.todoist-review.plist << 'EOF'
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.user.todoist-review</string>
    <key>ProgramArguments</key>
    <array>
        <string>/usr/bin/osascript</string>
        <string>-e</string>
        <string>display notification "Time to review your Todoist tasks with Claude!" with title "Todoist AI Agent" sound name "Glass"</string>
    </array>
    <key>StartCalendarInterval</key>
    <dict>
        <key>Hour</key>
        <integer>9</integer>
        <key>Minute</key>
        <integer>0</integer>
    </dict>
    <key>StandardErrorPath</key>
    <string>/tmp/todoist-reminder.err</string>
    <key>StandardOutPath</key>
    <string>/tmp/todoist-reminder.out</string>
</dict>
</plist>
EOF
            # Load the launch agent
            launchctl load ~/Library/LaunchAgents/com.user.todoist-review.plist

            echo "✅ Created LaunchAgent: ~/Library/LaunchAgents/com.user.todoist-review.plist"
            echo "✅ Loaded - will run daily at 9:00 AM"
            echo ""
            echo "You'll get a macOS notification at 9am daily."
            echo "When you see it, open Claude Code and ask:"
            echo "  'Review my Todoist tasks and suggest improvements'"
            echo ""
            echo "To disable: launchctl unload ~/Library/LaunchAgents/com.user.todoist-review.plist"
        fi
        ;;
    *)
        echo "Invalid choice. Exiting."
        exit 1
        ;;
esac

echo ""
echo "🎯 What to do when the reminder triggers:"
echo "   1. Open Terminal or Claude Code"
echo "   2. Navigate to: cd /Users/jj/Code/todoist-ai-agent"
echo "   3. Ask me: 'Review my Todoist tasks and suggest labels and improvements'"
echo ""
echo "Setup complete! 🚀"
