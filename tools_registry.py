"""
Tools Registry - Exposes modules as OpenAI-compatible tools
"""
from typing import Dict, List, Any, Optional
from agent import TodoistAIAgent


class ToolsRegistry:
    """Registry of all available tools for the agent to use."""

    def __init__(self, use_mock: bool = False):
        """Initialize the tools registry."""
        self.agent = TodoistAIAgent(use_mock=use_mock)

    def get_tools(self) -> List[Dict[str, Any]]:
        """
        Get all available tools in OpenAI function calling format.

        Returns:
            List of tool definitions
        """
        return [
            self._fetch_tasks_tool(),
            self._analyze_tasks_tool(),
            self._polish_tasks_tool(),
            self._schedule_due_dates_tool(),
            self._update_tasks_tool(),
            self._prioritize_tasks_tool(),
            self._categorize_tasks_tool(),
            self._get_daily_briefing_tool(),
            self._get_task_quality_report_tool(),
            self._generate_focus_plan_tool(),
            self._suggest_updates_tool(),
            self._get_user_profile_tool(),
            self._update_user_profile_tool(),
        ]

    def _fetch_tasks_tool(self) -> Dict[str, Any]:
        """Fetch tasks from Todoist with optional filters."""
        return {
            "type": "function",
            "function": {
                "name": "fetch_tasks",
                "description": "Fetch tasks from Todoist with optional filtering. Use this to get current tasks before analysis.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "filter": {
                            "type": "string",
                            "enum": ["all", "today", "overdue", "upcoming", "no_date"],
                            "description": "Filter tasks by status. Defaults to 'all'."
                        }
                    },
                    "required": []
                }
            }
        }

    def _analyze_tasks_tool(self) -> Dict[str, Any]:
        """Analyze tasks for urgency, importance, and priority using Eisenhower Matrix."""
        return {
            "type": "function",
            "function": {
                "name": "analyze_tasks",
                "description": "Analyze tasks for urgency, importance, and priority. Returns scored analysis with Eisenhower quadrant classification.",
                "parameters": {
                    "type": "object",
                    "properties": {},
                    "required": []
                }
            }
        }

    def _polish_tasks_tool(self) -> Dict[str, Any]:
        """Polish and improve task names and descriptions using AI."""
        return {
            "type": "function",
            "function": {
                "name": "polish_tasks",
                "description": "Polish and improve task names and descriptions using AI. Returns suggestions for better formatting, clarity, and completeness.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "scope": {
                            "type": "string",
                            "enum": ["all", "low_quality", "specific"],
                            "description": "Which tasks to polish. 'low_quality' finds tasks scoring < 50% quality."
                        },
                        "min_quality": {
                            "type": "integer",
                            "description": "Minimum quality threshold (0-100) for low_quality scope. Default: 50"
                        },
                        "task_ids": {
                            "type": "array",
                            "items": {"type": "string"},
                            "description": "Specific task IDs to polish (for 'specific' scope)"
                        }
                    },
                    "required": ["scope"]
                }
            }
        }

    def _schedule_due_dates_tool(self) -> Dict[str, Any]:
        """Infer and suggest due dates for tasks without dates."""
        return {
            "type": "function",
            "function": {
                "name": "schedule_due_dates",
                "description": "Infer and suggest due dates for tasks using AI. Works best on tasks without existing due dates.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "scope": {
                            "type": "string",
                            "enum": ["all", "no_date", "specific"],
                            "description": "Which tasks to schedule. 'no_date' filters tasks without due dates."
                        },
                        "task_ids": {
                            "type": "array",
                            "items": {"type": "string"},
                            "description": "Specific task IDs to schedule (for 'specific' scope)"
                        }
                    },
                    "required": ["scope"]
                }
            }
        }

    def _update_tasks_tool(self) -> Dict[str, Any]:
        """Update tasks with new names, descriptions, priorities, or due dates."""
        return {
            "type": "function",
            "function": {
                "name": "update_tasks",
                "description": "Update one or more tasks with new values. Always shows preview before applying changes.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "updates": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "task_id": {"type": "string", "description": "Task ID to update"},
                                    "content": {"type": "string", "description": "New task name (optional)"},
                                    "description": {"type": "string", "description": "New task description (optional)"},
                                    "priority": {"type": "integer", "description": "New priority 1-4 (optional)"},
                                    "due_date": {"type": "string", "description": "New due date YYYY-MM-DD (optional)"},
                                    "labels": {"type": "array", "items": {"type": "string"}, "description": "New labels (optional)"}
                                },
                                "required": ["task_id"]
                            },
                            "description": "List of task updates to apply"
                        },
                        "preview_only": {
                            "type": "boolean",
                            "description": "If True, only show previews without applying changes. Default: True"
                        }
                    },
                    "required": ["updates", "preview_only"]
                }
            }
        }

    def _prioritize_tasks_tool(self) -> Dict[str, Any]:
        """Prioritize tasks and generate a focus plan using Eisenhower Matrix."""
        return {
            "type": "function",
            "function": {
                "name": "prioritize_tasks",
                "description": "Prioritize all tasks and generate a focus plan. Returns top priorities and categorized by Eisenhower quadrants.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "max_tasks": {
                            "type": "integer",
                            "description": "Maximum number of tasks in focus plan. Default: 5"
                        }
                    },
                    "required": []
                }
            }
        }

    def _categorize_tasks_tool(self) -> Dict[str, Any]:
        """Categorize tasks by Eisenhower matrix quadrants."""
        return {
            "type": "function",
            "function": {
                "name": "categorize_tasks",
                "description": "Categorize all tasks by Eisenhower matrix quadrants (Q1-Q4).",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "quadrant": {
                            "type": "string",
                            "enum": ["Q1", "Q2", "Q3", "Q4", "all"],
                            "description": "Which quadrant to return, or 'all' for all quadrants. Default: 'all'"
                        }
                    },
                    "required": []
                }
            }
        }

    def _get_daily_briefing_tool(self) -> Dict[str, Any]:
        """Generate a comprehensive daily briefing with overdue, due today, and priorities."""
        return {
            "type": "function",
            "function": {
                "name": "get_daily_briefing",
                "description": "Generate a comprehensive daily briefing with task overview, priorities, and recommendations.",
                "parameters": {
                    "type": "object",
                    "properties": {},
                    "required": []
                }
            }
        }

    def _get_task_quality_report_tool(self) -> Dict[str, Any]:
        """Get a quality report showing which tasks need improvement."""
        return {
            "type": "function",
            "function": {
                "name": "get_task_quality_report",
                "description": "Analyze task quality and identify tasks needing improvement. Returns quality scores and suggestions.",
                "parameters": {
                    "type": "object",
                    "properties": {},
                    "required": []
                }
            }
        }

    def _generate_focus_plan_tool(self) -> Dict[str, Any]:
        """Generate a realistic daily/weekly focus plan."""
        return {
            "type": "function",
            "function": {
                "name": "generate_focus_plan",
                "description": "Generate a realistic focus plan for today or the week based on current tasks and priorities.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "timeframe": {
                            "type": "string",
                            "enum": ["today", "week"],
                            "description": "Timeframe for the focus plan. Default: 'today'"
                        },
                        "max_tasks": {
                            "type": "integer",
                            "description": "Maximum number of tasks to include. Default: 5"
                        }
                    },
                    "required": []
                }
            }
        }

    def _suggest_updates_tool(self) -> Dict[str, Any]:
        """Get AI-suggested updates for tasks (priorities, due dates, etc.)."""
        return {
            "type": "function",
            "function": {
                "name": "suggest_updates",
                "description": "Get AI-suggested updates for tasks like adding due dates or adjusting priorities.",
                "parameters": {
                    "type": "object",
                    "properties": {},
                    "required": []
                }
            }
        }

    def _get_user_profile_tool(self) -> Dict[str, Any]:
        """Get user's preferences and work patterns."""
        return {
            "type": "function",
            "function": {
                "name": "get_user_profile",
                "description": "Get user's preferences, work patterns, and historical behavior for personalization.",
                "parameters": {
                    "type": "object",
                    "properties": {},
                    "required": []
                }
            }
        }

    def _update_user_profile_tool(self) -> Dict[str, Any]:
        """Update user's preferences based on feedback."""
        return {
            "type": "function",
            "function": {
                "name": "update_user_profile",
                "description": "Update user's preferences based on their actions and feedback.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "preferences": {
                            "type": "object",
                            "description": "Dictionary of preference updates",
                            "properties": {
                                "work_hours": {"type": "string", "description": "e.g., '09:00-18:00'"},
                                "max_deep_tasks_per_day": {"type": "integer", "description": "Maximum deep work tasks per day"},
                                "likes_batching": {"type": "boolean", "description": "Whether user prefers batching similar tasks"},
                                "prefers_mornings_for_deep_work": {"type": "boolean", "description": "Whether user prefers mornings for deep work"},
                                "avoid_evenings_for_admin": {"type": "boolean", "description": "Whether to avoid scheduling admin in evenings"},
                                "timezone": {"type": "string", "description": "User's timezone"},
                                "polish_aggressiveness": {"type": "string", "enum": ["conservative", "moderate", "aggressive"], "description": "How aggressively to polish tasks"},
                                "typical_task_completion_rate": {"type": "number", "description": "Historical task completion rate (0-1)"}
                            }
                        }
                    },
                    "required": ["preferences"]
                }
            }
        }

    # Tool Execution Methods

    def execute_tool(self, tool_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute a tool by name with given arguments.

        Args:
            tool_name: Name of the tool to execute
            arguments: Arguments to pass to the tool

        Returns:
            Result of the tool execution
        """
        method = getattr(self, f"_execute_{tool_name}", None)
        if not method:
            return {"error": f"Tool '{tool_name}' not found"}

        try:
            return method(**arguments)
        except Exception as e:
            return {"error": f"Error executing {tool_name}: {str(e)}"}

    # Individual tool execution methods

    def _execute_fetch_tasks(self, filter: str = "all") -> Dict[str, Any]:
        """Execute fetch_tasks tool."""
        tasks = self.agent.get_tasks_filtered(filter)
        return {
            "status": "success",
            "count": len(tasks),
            "filter": filter,
            "tasks": tasks
        }

    def _execute_analyze_tasks(self) -> Dict[str, Any]:
        """Execute analyze_tasks tool."""
        results = self.agent.run_analysis()
        return {
            "status": "success",
            "analyzed_count": len(results["analyzed_tasks"]),
            "analyzed_tasks": results["analyzed_tasks"]
        }

    def _execute_polish_tasks(self, scope: str, min_quality: int = 50, task_ids: Optional[List[str]] = None) -> Dict[str, Any]:
        """Execute polish_tasks tool."""
        tasks = None
        if scope == "specific" and task_ids:
            all_tasks = self.agent.client.fetch_tasks()
            tasks = [t for t in all_tasks if str(t.get("id")) in task_ids]

        results = self.agent.polish_tasks(tasks, min_quality)
        return {
            "status": "success",
            "polished_count": len(results),
            "results": results
        }

    def _execute_schedule_due_dates(self, scope: str, task_ids: Optional[List[str]] = None) -> Dict[str, Any]:
        """Execute schedule_due_dates tool."""
        tasks = None
        if scope == "specific" and task_ids:
            all_tasks = self.agent.client.fetch_tasks()
            tasks = [t for t in all_tasks if str(t.get("id")) in task_ids]

        results = self.agent.suggest_due_dates(tasks)
        return {
            "status": "success",
            "scheduled_count": len(results),
            "suggestions": results
        }

    def _execute_update_tasks(self, updates: List[Dict[str, Any]], preview_only: bool = True) -> Dict[str, Any]:
        """Execute update_tasks tool."""
        if preview_only:
            # Just return previews
            previews = []
            for update in updates:
                task_id = update["task_id"]
                all_tasks = self.agent.client.fetch_tasks()
                task = next((t for t in all_tasks if str(t.get("id")) == str(task_id)), None)
                if task:
                    preview = self.agent.task_updater.create_update_preview(task, update)
                    previews.append(preview)
            return {
                "status": "success",
                "preview_only": True,
                "update_count": len(updates),
                "previews": previews
            }
        else:
            # Apply updates
            results = []
            for update in updates:
                task_id = update["task_id"]
                update_copy = update.copy()
                del update_copy["task_id"]
                success = self.agent.client.update_task(task_id, update_copy)
                results.append({"task_id": task_id, "success": success})
            return {
                "status": "success",
                "preview_only": False,
                "update_count": len(updates),
                "results": results
            }

    def _execute_prioritize_tasks(self, max_tasks: int = 5) -> Dict[str, Any]:
        """Execute prioritize_tasks tool."""
        focus_plan = self.agent.prioritizer.create_daily_focus_plan(
            self.agent.run_analysis()["analyzed_tasks"],
            max_tasks=max_tasks
        )
        return {
            "status": "success",
            "max_tasks": max_tasks,
            "focus_plan": focus_plan
        }

    def _execute_categorize_tasks(self, quadrant: str = "all") -> Dict[str, Any]:
        """Execute categorize_tasks tool."""
        result = self.agent.categorize_by_quadrant(quadrant)
        return {
            "status": "success",
            "quadrant": quadrant,
            "result": result
        }

    def _execute_get_daily_briefing(self) -> Dict[str, Any]:
        """Execute get_daily_briefing tool."""
        today_tasks = self.agent.get_today_tasks()
        focus_plan = self.agent.get_top_priorities(5)
        quality_report = self.agent.get_task_quality_report()

        return {
            "status": "success",
            "date": today_tasks["today"],
            "summary": {
                "overdue_count": len(today_tasks["overdue"]),
                "due_today_count": len(today_tasks["due_today"]),
                "upcoming_count": len(today_tasks["upcoming"]),
                "no_date_count": len(today_tasks["no_date"]),
                "total_tasks": today_tasks["total"]
            },
            "focus_plan": focus_plan,
            "quality_report": quality_report
        }

    def _execute_get_task_quality_report(self) -> Dict[str, Any]:
        """Execute get_task_quality_report tool."""
        report = self.agent.get_task_quality_report()
        return {
            "status": "success",
            "report": report
        }

    def _execute_generate_focus_plan(self, timeframe: str = "today", max_tasks: int = 5) -> Dict[str, Any]:
        """Execute generate_focus_plan tool."""
        results = self.agent.run_analysis()
        focus_plan = self.agent.prioritizer.create_daily_focus_plan(
            results["analyzed_tasks"],
            max_tasks=max_tasks
        )

        return {
            "status": "success",
            "timeframe": timeframe,
            "max_tasks": max_tasks,
            "focus_plan": focus_plan
        }

    def _execute_suggest_updates(self) -> Dict[str, Any]:
        """Execute suggest_updates tool."""
        suggestions = self.agent.suggest_updates()
        return {
            "status": "success",
            "suggestion_count": len(suggestions),
            "suggestions": suggestions
        }

    def _execute_get_user_profile(self) -> Dict[str, Any]:
        """Execute get_user_profile tool."""
        from pathlib import Path
        import json

        profile_file = Path.home() / ".todoist_agent_profile.json"

        default_profile = {
            "work_hours": "09:00-18:00",
            "timezone": "Asia/Singapore",
            "max_deep_tasks_per_day": 3,
            "likes_batching": True,
            "prefers_mornings_for_deep_work": True,
            "avoid_evenings_for_admin": True,
            "polish_aggressiveness": "moderate",
            "typical_task_completion_rate": 0.75,
            "preferred_focus_blocks": ["09:00-11:00", "14:00-16:00"],
            "task_history": []
        }

        if profile_file.exists():
            try:
                profile = json.loads(profile_file.read_text())
                # Merge with defaults
                for key, value in default_profile.items():
                    if key not in profile:
                        profile[key] = value
                return {
                    "status": "success",
                    "profile": profile
                }
            except Exception as e:
                return {
                    "status": "error",
                    "error": f"Error reading profile: {str(e)}",
                    "profile": default_profile
                }

        return {
            "status": "success",
            "profile": default_profile
        }

    def _execute_update_user_profile(self, preferences: Dict[str, Any]) -> Dict[str, Any]:
        """Execute update_user_profile tool."""
        from pathlib import Path
        import json

        profile_file = Path.home() / ".todoist_agent_profile.json"

        # Get current profile
        current_profile = self._execute_get_user_profile()["profile"]

        # Update with new preferences
        current_profile.update(preferences)

        # Save back
        try:
            profile_file.write_text(json.dumps(current_profile, indent=2))
            return {
                "status": "success",
                "updated_keys": list(preferences.keys()),
                "profile": current_profile
            }
        except Exception as e:
            return {
                "status": "error",
                "error": f"Error saving profile: {str(e)}"
            }
