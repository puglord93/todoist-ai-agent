# Daily 9am Todoist Review Reminder Setup

## Quick Setup (Choose One Method)

### 🌟 Method 1: macOS Calendar (RECOMMENDED - 2 minutes)

**Easiest and most reliable method:**

1. **Open Calendar app**
   - Press `⌘ + Space`
   - Type "Calendar"
   - Press Enter

2. **Create new event**
   - Press `⌘ + N` (or click the `+` button)

3. **Fill in details:**
   ```
   Title: Review Todoist Tasks
   Date: Today
   Time: 9:00 AM - 9:15 AM
   Repeat: Every Day
   Alert: At time of event (or 5 minutes before)
   ```

4. **Add to Notes section:**
   ```
   Open Claude Code and ask:
   "Review my Todoist tasks and suggest improvements"
   ```

5. **Save** (⌘ + S)

**Done!** You'll get a notification every day at 9am.

---

### 📱 Method 2: Automated macOS Notification

**Run the setup script:**

```bash
cd /Users/jj/Code/todoist-ai-agent
./setup_daily_reminder.sh
```

Choose option **3** for automated notification.

This creates a LaunchAgent that shows a macOS notification at 9am daily.

**To test it immediately:**
```bash
osascript -e 'display notification "Time to review your Todoist tasks with Claude!" with title "Todoist AI Agent" sound name "Glass"'
```

**To disable later:**
```bash
launchctl unload ~/Library/LaunchAgents/com.user.todoist-review.plist
```

---

### ⚡ Method 3: macOS Shortcuts (if you use Shortcuts app)

1. Open **Shortcuts** app
2. Click `+` to create new shortcut
3. Add action: **Show Notification**
   - Title: `Review Todoist Tasks`
   - Body: `Time to organize with Claude!`
4. Click the `ⓘ` info button
5. Enable **Show in Menu Bar** (optional)
6. Go to **Automation** tab
7. Click `+` → **Time of Day**
8. Set to **9:00 AM**, **Daily**
9. Choose your shortcut

---

## What to Do When Reminder Triggers

When you see the 9am notification:

1. **Open Terminal** (or keep Claude Code running)

2. **Navigate to project:**
   ```bash
   cd /Users/jj/Code/todoist-ai-agent
   ```

3. **Ask me one of these:**
   ```
   "Review my Todoist tasks and suggest improvements"

   "Fetch my Todoist tasks and suggest labels for them"

   "Show me my 5 worst quality tasks and how to improve them"

   "Check my Todoist tasks - which ones need due dates?"
   ```

4. **Review suggestions** and approve the ones you like

5. **I'll apply them** via MCP to your Todoist

**Takes ~5 minutes daily!**

---

## Pro Tips

### Morning Routine Template

Ask me this every morning:

```
"Good morning! Please:
1. Fetch my Todoist tasks
2. Show tasks due today and overdue
3. Identify any vague task names
4. Suggest labels for unlabeled tasks
5. Recommend due dates for tasks without them"
```

### Quick Commands

Create Terminal aliases in `~/.zshrc`:

```bash
# Add these to ~/.zshrc
alias todoist-review='cd /Users/jj/Code/todoist-ai-agent && echo "Ask Claude: Review my tasks"'
alias todoist-polish='cd /Users/jj/Code/todoist-ai-agent && ./interactive_polish.py'
```

Then just type `todoist-review` in any terminal!

---

## Troubleshooting

**Calendar notification not appearing?**
- Check System Settings → Notifications → Calendar
- Make sure "Allow Notifications" is enabled

**LaunchAgent not working?**
```bash
# Check if loaded
launchctl list | grep todoist

# View logs
cat /tmp/todoist-reminder.out
cat /tmp/todoist-reminder.err

# Reload
launchctl unload ~/Library/LaunchAgents/com.user.todoist-review.plist
launchctl load ~/Library/LaunchAgents/com.user.todoist-review.plist
```

**Want to change the time?**
- Calendar: Just edit the event
- LaunchAgent: Edit `~/Library/LaunchAgents/com.user.todoist-review.plist` and change `<integer>9</integer>` to your preferred hour

---

## My Recommendation

**Use Method 1 (Calendar)** because:
- ✅ Most reliable
- ✅ Works even if computer is asleep/wakes up
- ✅ Easy to snooze if you're busy
- ✅ Can see it on your phone (if iCloud Calendar sync is on)
- ✅ Can adjust time easily
- ✅ No technical setup needed

Set it up once, and you'll never forget to review your tasks! 🎯
