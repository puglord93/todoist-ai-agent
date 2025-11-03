"""
Intent Router Module

Uses OpenAI to detect user intent and route to appropriate agent functions.
"""

import os
import json
from typing import Dict, Any, List, Optional, Tuple
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()


class IntentRouter:
    """Routes user natural language requests to appropriate agent functions."""

    def __init__(self, api_key: Optional[str] = None, model: Optional[str] = None):
        """
        Initialize the intent router.

        Args:
            api_key: OpenAI API key (defaults to OPENAI_API_KEY env var)
            model: Model to use (defaults to OPENAI_MODEL env var or gpt-4o-mini)
        """
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY environment variable not set")

        self.client = OpenAI(api_key=self.api_key)
        self.model = model or os.getenv("OPENAI_MODEL", "gpt-4o-mini")
        self.conversation_history: List[Dict[str, str]] = []
        self.last_action_context: Dict[str, Any] = {}

    def detect_intent(self, user_input: str) -> Dict[str, Any]:
        """
        Detect user intent from natural language input.

        Args:
            user_input: User's natural language request

        Returns:
            Dictionary with intent and parameters
        """
        # Define available functions for OpenAI function calling
        functions = [
            {
                "name": "show_tasks",
                "description": "Show tasks (today's tasks, all tasks, or filtered by criteria)",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "filter": {
                            "type": "string",
                            "enum": ["today", "all", "overdue", "upcoming", "no_date"],
                            "description": "Which tasks to show"
                        }
                    },
                    "required": ["filter"]
                }
            },
            {
                "name": "prioritize_tasks",
                "description": "Prioritize tasks and create focus plan using Eisenhower matrix",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "report_type": {
                            "type": "string",
                            "enum": ["focus", "full"],
                            "description": "Type of report to generate"
                        }
                    },
                    "required": []
                }
            },
            {
                "name": "polish_tasks",
                "description": "Show quality report - use ONLY when user asks 'which tasks need polishing?' or 'show me low quality tasks'. Shows analysis without making changes.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "scope": {
                            "type": "string",
                            "enum": ["all", "low_quality", "specific"],
                            "description": "Which tasks to polish"
                        },
                        "min_quality": {
                            "type": "integer",
                            "description": "Minimum quality score (0-100) for low_quality scope"
                        }
                    },
                    "required": ["scope"]
                }
            },
            {
                "name": "schedule_tasks",
                "description": "Suggest or add due dates to tasks",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "scope": {
                            "type": "string",
                            "enum": ["no_date", "all"],
                            "description": "Which tasks need due dates"
                        }
                    },
                    "required": ["scope"]
                }
            },
            {
                "name": "categorize_tasks",
                "description": "Categorize tasks by Eisenhower matrix quadrants",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "quadrant": {
                            "type": "string",
                            "enum": ["Q1", "Q2", "Q3", "Q4", "all"],
                            "description": "Which quadrant to show"
                        }
                    },
                    "required": []
                }
            },
            {
                "name": "get_help",
                "description": "Show available commands and help information",
                "parameters": {
                    "type": "object",
                    "properties": {},
                    "required": []
                }
            },
            {
                "name": "update_task",
                "description": "Update a specific task's properties (name, description, priority, due date, labels)",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "task_identifier": {
                            "type": "string",
                            "description": "Task name or 'first task', 'second task', etc."
                        },
                        "update_type": {
                            "type": "string",
                            "enum": ["name", "description", "priority", "due_date", "labels"],
                            "description": "Type of update to perform"
                        },
                        "new_value": {
                            "type": "string",
                            "description": "New value for the field"
                        }
                    },
                    "required": ["task_identifier", "update_type"]
                }
            },
            {
                "name": "polish_and_apply",
                "description": "Polish and improve tasks - use when user says 'polish [tasks]', 'improve these tasks', 'clean up task names', etc. Applies actual changes with confirmation. Works with: 'these tasks', 'first task', 'all tasks', etc.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "task_identifier": {
                            "type": "string",
                            "description": "Which task(s) to polish: 'these tasks', 'first task', 'all tasks', 'tasks without dates', etc."
                        },
                        "count": {
                            "type": "integer",
                            "description": "Number of tasks to polish (e.g., 3 for 'top 3')"
                        }
                    },
                    "required": ["task_identifier"]
                }
            },
            {
                "name": "manage_labels",
                "description": "View, analyze, or manage task labels (consolidate, remove insignificant labels)",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "action": {
                            "type": "string",
                            "enum": ["view", "analyze", "consolidate", "remove"],
                            "description": "What to do with labels"
                        },
                        "task_identifier": {
                            "type": "string",
                            "description": "Which task(s) to manage labels for (optional, defaults to all)"
                        }
                    },
                    "required": ["action"]
                }
            }
        ]

        # Build context-aware prompt
        messages = self._build_messages(user_input)

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                functions=functions,
                function_call="auto"
            )

            message = response.choices[0].message

            # Check if function was called
            if message.function_call:
                function_name = message.function_call.name
                arguments = json.loads(message.function_call.arguments)

                return {
                    "intent": function_name,
                    "parameters": arguments,
                    "confidence": "high"
                }
            else:
                # No function called - general conversation
                return {
                    "intent": "general_response",
                    "response": message.content,
                    "confidence": "medium"
                }

        except Exception as e:
            print(f"Error detecting intent: {e}")
            return {
                "intent": "error",
                "error": str(e),
                "confidence": "low"
            }

    def _build_messages(self, user_input: str) -> List[Dict[str, str]]:
        """
        Build messages array with conversation history.

        Args:
            user_input: Current user input

        Returns:
            List of message dictionaries
        """
        messages = [
            {
                "role": "system",
                "content": """You are a helpful Todoist task management assistant.
Your job is to understand user requests about their tasks and call the appropriate function.

Context about the user:
- They are a venture builder at ATUM Ventures in Singapore
- They work with deep-tech startups and research institutes
- Their tasks include both work (partnerships, POCs, market validation) and personal items

Available capabilities:
- Show tasks (today, all, overdue, upcoming)
- Prioritize tasks using Eisenhower matrix
- Polish/improve task names and descriptions
- Suggest due dates for tasks
- Categorize tasks by urgency/importance

When the user refers to previous results (like "those tasks" or "the urgent ones"),
use the conversation history to understand what they mean."""
            }
        ]

        # Add conversation history (last 10 messages)
        messages.extend(self.conversation_history[-10:])

        # Add current user input
        messages.append({
            "role": "user",
            "content": user_input
        })

        return messages

    def add_to_history(self, user_input: str, assistant_response: str):
        """
        Add interaction to conversation history.

        Args:
            user_input: User's input
            assistant_response: Assistant's response
        """
        self.conversation_history.append({
            "role": "user",
            "content": user_input
        })
        self.conversation_history.append({
            "role": "assistant",
            "content": assistant_response
        })

        # Keep only last 20 messages (10 interactions)
        if len(self.conversation_history) > 20:
            self.conversation_history = self.conversation_history[-20:]

    def update_context(self, action: str, data: Any):
        """
        Update context about last action taken.

        Args:
            action: Action that was performed
            data: Data associated with the action
        """
        self.last_action_context = {
            "action": action,
            "data": data
        }

    def get_context(self) -> Dict[str, Any]:
        """
        Get current conversation context.

        Returns:
            Context dictionary
        """
        return self.last_action_context

    def clear_history(self):
        """Clear conversation history."""
        self.conversation_history = []
        self.last_action_context = {}
