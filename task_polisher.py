"""
Task Polisher Module

Uses AI to enhance task names, descriptions, and extract metadata from task content.
"""

from typing import Dict, Any, List, Optional
import os
import json
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class TaskPolisher:
    """AI-powered task name and description enhancement."""

    def __init__(self, api_key: Optional[str] = None, model: Optional[str] = None):
        """
        Initialize the task polisher.

        Args:
            api_key: OpenAI API key (defaults to OPENAI_API_KEY env var)
            model: Model to use (defaults to OPENAI_MODEL env var or gpt-4o-mini)
        """
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY environment variable not set")

        self.client = OpenAI(api_key=self.api_key)
        self.model = model or os.getenv("OPENAI_MODEL", "gpt-4o-mini")

    def polish_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """
        Polish a single task by improving its name and description.

        Args:
            task: Task dictionary with 'content' and optional 'description'

        Returns:
            Dictionary with polishing suggestions
        """
        current_name = task.get("content", "")
        current_description = task.get("description", "")
        labels = task.get("labels", [])

        prompt = self._build_polish_prompt(current_name, current_description, labels)

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                max_tokens=1024,
                messages=[{
                    "role": "user",
                    "content": prompt
                }],
                response_format={"type": "json_object"}
            )

            result_text = response.choices[0].message.content
            result = json.loads(result_text)

            return {
                "task_id": task.get("id"),
                "original_name": current_name,
                "original_description": current_description,
                "suggested_name": result.get("polished_name", current_name),
                "suggested_description": result.get("polished_description", current_description),
                "extracted_priority": result.get("extracted_priority"),
                "extracted_labels": result.get("extracted_labels", []),
                "needs_polishing": result.get("needs_polishing", False),
                "polishing_reason": result.get("reason", "")
            }

        except Exception as e:
            print(f"Error polishing task '{current_name}': {e}")
            return {
                "task_id": task.get("id"),
                "original_name": current_name,
                "original_description": current_description,
                "suggested_name": current_name,
                "suggested_description": current_description,
                "needs_polishing": False,
                "error": str(e)
            }

    def polish_tasks_batch(self, tasks: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Polish multiple tasks.

        Args:
            tasks: List of task dictionaries

        Returns:
            List of polishing suggestion dictionaries
        """
        results = []
        for task in tasks:
            result = self.polish_task(task)
            results.append(result)

        return results

    def _build_polish_prompt(self, name: str, description: str, labels: List[str]) -> str:
        """
        Build the AI prompt for task polishing.

        Args:
            name: Current task name
            description: Current task description
            labels: Current labels

        Returns:
            Prompt string
        """
        return f"""You are a productivity assistant helping to polish task names and descriptions.

Current task:
- Name: "{name}"
- Description: "{description or '(empty)'}"
- Labels: {', '.join(labels) if labels else '(none)'}

Please analyze this task and provide improvements. Return ONLY a JSON object with:

{{
  "needs_polishing": true/false,
  "reason": "Brief explanation of why this task needs improvement (or why it's already good)",
  "polished_name": "Improved task name - should be clear, specific, and start with action verb",
  "polished_description": "Enhanced description with context, steps, or relevant details",
  "extracted_priority": 1-4 or null (1=lowest, 4=highest priority if mentioned in task),
  "extracted_labels": ["list", "of", "suggested", "labels"]
}}

Guidelines:
1. Task names should start with clear action verbs (e.g., "Call", "Write", "Review", "Schedule")
2. Add specific context (e.g., "call john" → "Call John about Q4 project review")
3. Extract implicit information (e.g., "dentist" → "Dentist appointment for cleaning")
4. Keep it concise but meaningful
5. Only suggest changes if the current version is vague or unclear
6. Extract priority hints from words like "urgent", "ASAP", "important"
7. Suggest labels based on content (e.g., "work", "personal", "health", "urgent")

Return only the JSON, no other text."""

    def get_quality_score(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """
        Calculate a quality score for a task.

        Args:
            task: Task dictionary

        Returns:
            Quality assessment dictionary
        """
        score = 0
        max_score = 100
        issues = []

        content = task.get("content", "")
        description = task.get("description", "")

        # Check for action verb (simple heuristic)
        action_verbs = ['call', 'email', 'write', 'review', 'schedule', 'plan',
                       'create', 'update', 'fix', 'send', 'prepare', 'finish',
                       'complete', 'buy', 'order', 'book', 'submit', 'research']

        has_action_verb = any(content.lower().startswith(verb) for verb in action_verbs)
        if has_action_verb:
            score += 25
        else:
            issues.append("No clear action verb at the start")

        # Check length (not too short, not too long)
        if 10 <= len(content) <= 80:
            score += 20
        elif len(content) < 10:
            issues.append("Task name too vague (too short)")
        else:
            issues.append("Task name too long")

        # Check for description
        if description and len(description) > 10:
            score += 20
        else:
            issues.append("Missing or minimal description")

        # Check for due date
        if task.get("due_date"):
            score += 15
        else:
            issues.append("No due date set")

        # Check for priority
        if task.get("priority", 1) > 1:
            score += 10
        else:
            issues.append("No priority set")

        # Check for labels
        if task.get("labels"):
            score += 10
        else:
            issues.append("No labels for categorization")

        return {
            "task_id": task.get("id"),
            "task_content": content,
            "quality_score": score,
            "max_score": max_score,
            "percentage": round((score / max_score) * 100, 1),
            "issues": issues,
            "needs_attention": score < 50
        }

    def identify_tasks_needing_polish(self, tasks: List[Dict[str, Any]],
                                     min_quality: int = 50) -> List[Dict[str, Any]]:
        """
        Identify tasks that need polishing based on quality score.

        Args:
            tasks: List of tasks
            min_quality: Minimum quality percentage (0-100)

        Returns:
            List of tasks needing attention
        """
        needs_polish = []

        for task in tasks:
            quality = self.get_quality_score(task)
            if quality["percentage"] < min_quality:
                needs_polish.append({
                    **task,
                    "quality_assessment": quality
                })

        return sorted(needs_polish,
                     key=lambda x: x["quality_assessment"]["percentage"])
