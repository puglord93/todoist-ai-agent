"""
Smart Scheduler Module

Intelligently infers due dates from task content using natural language processing and AI.
"""

from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
import re
import os
import json
from anthropic import Anthropic
import pytz


class SmartScheduler:
    """AI-powered due date inference and scheduling."""

    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the smart scheduler.

        Args:
            api_key: Anthropic API key (defaults to ANTHROPIC_API_KEY env var)
        """
        self.api_key = api_key or os.getenv("ANTHROPIC_API_KEY")
        self.client = None
        if self.api_key:
            self.client = Anthropic(api_key=self.api_key)
            self.model = "claude-3-5-sonnet-20241022"

        self.today = datetime.now(pytz.UTC)

    def infer_due_date(self, task: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Infer a due date from task content and description.

        Args:
            task: Task dictionary

        Returns:
            Dictionary with due date suggestion or None
        """
        # First try pattern matching for explicit dates
        pattern_result = self._extract_date_from_patterns(task)
        if pattern_result:
            return pattern_result

        # Then try AI-powered inference for implicit dates
        if self.client:
            ai_result = self._infer_date_with_ai(task)
            if ai_result:
                return ai_result

        # Finally, try heuristic-based inference
        return self._infer_date_from_heuristics(task)

    def _extract_date_from_patterns(self, task: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Extract explicit dates from task content using regex patterns.

        Args:
            task: Task dictionary

        Returns:
            Dictionary with extracted date or None
        """
        content = task.get("content", "")
        description = task.get("description", "")
        text = f"{content} {description}".lower()

        patterns = [
            # "tomorrow", "today"
            (r'\b(today|tonight)\b', 0),
            (r'\btomorrow\b', 1),

            # "in X days/weeks"
            (r'\bin (\d+) days?\b', lambda m: int(m.group(1))),
            (r'\bin (\d+) weeks?\b', lambda m: int(m.group(1)) * 7),

            # "next monday/tuesday/etc"
            (r'\bnext (monday|tuesday|wednesday|thursday|friday|saturday|sunday)\b',
             lambda m: self._days_until_weekday(m.group(1), next_week=True)),

            # "this monday/tuesday/etc"
            (r'\bthis (monday|tuesday|wednesday|thursday|friday|saturday|sunday)\b',
             lambda m: self._days_until_weekday(m.group(1), next_week=False)),

            # "on monday/tuesday/etc" (assume this week or next)
            (r'\bon (monday|tuesday|wednesday|thursday|friday|saturday|sunday)\b',
             lambda m: self._days_until_weekday(m.group(1), next_week=False)),

            # "by end of week"
            (r'\bby (end of|eow|end of the) week\b', lambda m: self._days_until_friday()),

            # "by end of month"
            (r'\bby (end of|eom|end of the) month\b',
             lambda m: (self._get_end_of_month() - self.today).days),

            # Specific date formats: MM/DD, DD/MM (ambiguous but we'll try)
            # ISO format: YYYY-MM-DD
            (r'\b(\d{4})-(\d{2})-(\d{2})\b',
             lambda m: self._parse_iso_date(m.group(1), m.group(2), m.group(3))),
        ]

        for pattern, days_offset in patterns:
            match = re.search(pattern, text)
            if match:
                if callable(days_offset):
                    offset = days_offset(match)
                else:
                    offset = days_offset

                if offset is not None:
                    due_date = self.today + timedelta(days=offset)
                    return {
                        "suggested_date": due_date.strftime("%Y-%m-%d"),
                        "confidence": "high",
                        "source": "pattern_match",
                        "extracted_text": match.group(0)
                    }

        return None

    def _infer_date_with_ai(self, task: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Use AI to infer implicit due dates.

        Args:
            task: Task dictionary

        Returns:
            Dictionary with inferred date or None
        """
        content = task.get("content", "")
        description = task.get("description", "")
        labels = task.get("labels", [])

        prompt = f"""You are a scheduling assistant. Analyze this task and suggest a reasonable due date.

Task: "{content}"
Description: "{description or '(none)'}"
Labels: {', '.join(labels) if labels else '(none)'}

Today's date: {self.today.strftime("%Y-%m-%d (%A)")}

Consider:
1. Explicit time references in the task (e.g., "tomorrow", "next week", "by Friday")
2. Urgency implied by words like "urgent", "ASAP", "soon"
3. Task type (e.g., bills are often monthly, meetings have specific dates)
4. Context from description and labels

Return ONLY a JSON object:
{{
  "should_have_due_date": true/false,
  "suggested_date": "YYYY-MM-DD" or null,
  "confidence": "high/medium/low",
  "reasoning": "Brief explanation of why this date makes sense"
}}

If there's no clear timeframe, return {{"should_have_due_date": false, "suggested_date": null}}.
Return only JSON, no other text."""

        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=512,
                messages=[{
                    "role": "user",
                    "content": prompt
                }]
            )

            result_text = response.content[0].text
            result = json.loads(result_text)

            if result.get("should_have_due_date") and result.get("suggested_date"):
                return {
                    "suggested_date": result["suggested_date"],
                    "confidence": result.get("confidence", "medium"),
                    "source": "ai_inference",
                    "reasoning": result.get("reasoning", "")
                }

        except Exception as e:
            print(f"Error inferring date with AI for '{content}': {e}")

        return None

    def _infer_date_from_heuristics(self, task: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Use heuristic rules to suggest due dates.

        Args:
            task: Task dictionary

        Returns:
            Dictionary with suggested date or None
        """
        content = task.get("content", "").lower()
        labels = [label.lower() for label in task.get("labels", [])]

        # Urgent tasks -> tomorrow
        if any(word in content for word in ['urgent', 'asap', 'emergency']):
            return {
                "suggested_date": (self.today + timedelta(days=1)).strftime("%Y-%m-%d"),
                "confidence": "medium",
                "source": "urgency_heuristic",
                "reasoning": "Task marked as urgent"
            }

        # Bills/payments -> end of month
        if any(word in content for word in ['bill', 'payment', 'invoice', 'pay']):
            eom = self._get_end_of_month()
            return {
                "suggested_date": eom.strftime("%Y-%m-%d"),
                "confidence": "low",
                "source": "category_heuristic",
                "reasoning": "Bills typically due end of month"
            }

        # Health appointments -> this week
        if any(word in content for word in ['doctor', 'dentist', 'appointment', 'checkup']):
            return {
                "suggested_date": (self.today + timedelta(days=3)).strftime("%Y-%m-%d"),
                "confidence": "low",
                "source": "category_heuristic",
                "reasoning": "Health appointments typically scheduled soon"
            }

        return None

    def _days_until_weekday(self, weekday_name: str, next_week: bool = False) -> int:
        """
        Calculate days until a specific weekday.

        Args:
            weekday_name: Name of weekday (e.g., "monday")
            next_week: If True, get next week's instance

        Returns:
            Number of days until that weekday
        """
        weekdays = {
            'monday': 0, 'tuesday': 1, 'wednesday': 2, 'thursday': 3,
            'friday': 4, 'saturday': 5, 'sunday': 6
        }

        target_weekday = weekdays.get(weekday_name.lower())
        if target_weekday is None:
            return None

        current_weekday = self.today.weekday()
        days_ahead = target_weekday - current_weekday

        if days_ahead <= 0 or next_week:
            days_ahead += 7

        return days_ahead

    def _days_until_friday(self) -> int:
        """Get days until next Friday."""
        return self._days_until_weekday('friday', next_week=False)

    def _get_end_of_month(self) -> datetime:
        """Get the last day of the current month."""
        next_month = self.today.replace(day=28) + timedelta(days=4)
        return next_month - timedelta(days=next_month.day)

    def _parse_iso_date(self, year: str, month: str, day: str) -> Optional[int]:
        """
        Parse ISO date and return days from today.

        Args:
            year, month, day: Date components as strings

        Returns:
            Days until that date, or None if invalid
        """
        try:
            target_date = datetime(int(year), int(month), int(day), tzinfo=pytz.UTC)
            delta = target_date - self.today
            return delta.days if delta.days >= 0 else None
        except (ValueError, TypeError):
            return None

    def suggest_due_dates_batch(self, tasks: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Suggest due dates for multiple tasks.

        Args:
            tasks: List of tasks

        Returns:
            List of tasks with due date suggestions
        """
        results = []

        for task in tasks:
            # Skip tasks that already have due dates
            if task.get("due_date"):
                continue

            suggestion = self.infer_due_date(task)
            if suggestion:
                results.append({
                    "task_id": task.get("id"),
                    "task_content": task.get("content"),
                    "current_due_date": task.get("due_date"),
                    **suggestion
                })

        return results

    def get_recurring_pattern(self, task: Dict[str, Any]) -> Optional[str]:
        """
        Detect if a task suggests a recurring pattern.

        Args:
            task: Task dictionary

        Returns:
            Recurring pattern string (e.g., "weekly", "monthly") or None
        """
        content = task.get("content", "").lower()
        description = task.get("description", "").lower()
        text = f"{content} {description}"

        patterns = {
            r'\b(daily|every day)\b': 'daily',
            r'\b(weekly|every week)\b': 'weekly',
            r'\b(monthly|every month)\b': 'monthly',
            r'\b(yearly|annually|every year)\b': 'yearly',
            r'\bevery (monday|tuesday|wednesday|thursday|friday|saturday|sunday)\b': 'weekly',
        }

        for pattern, recurrence in patterns.items():
            if re.search(pattern, text):
                return recurrence

        return None
