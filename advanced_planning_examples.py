"""
Advanced Planning Examples - Complex multi-step workflows

These examples show how the planner agent handles complex, goal-driven scenarios
that would be difficult to implement with hardcoded flows.
"""
from planner_agent import PlannerAgent
from typing import Dict, Any


class AdvancedPlanningScenarios:
    """
    Examples of complex planning scenarios handled by the agent.
    """

    def __init__(self, use_mock: bool = False):
        """Initialize with a planner agent."""
        self.agent = PlannerAgent(use_mock=use_mock)

    def scenario_1_overwhelmed_backlog(self):
        """
        Scenario: User is overwhelmed by a large backlog.
        The agent must: assess situation, create realistic plan, clean up.
        """
        print("\n" + "=" * 70)
        print("SCENARIO 1: Overwhelmed by Backlog")
        print("=" * 70)

        user_goal = (
            "I have 50+ tasks in my backlog and I'm overwhelmed. "
            "I'm not sure what to focus on. Help me create a realistic plan "
            "for this week and clean up the mess."
        )

        response = self.agent.handle_request(user_goal)
        return response

    def scenario_2_monday_morning_planning(self):
        """
        Scenario: Monday morning - start the week right.
        The agent must: get overview, prioritize, schedule strategically.
        """
        print("\n" + "=" * 70)
        print("SCENARIO 2: Monday Morning Planning")
        print("=" * 70)

        context = {
            "day_of_week": "monday",
            "time": "morning",
            "energy_level": "high",
            "context": "Start of week, time to plan strategically"
        }

        user_goal = (
            "It's Monday morning and I want to plan my week strategically. "
            "I'm in a good energy state and ready to tackle important work. "
            "Help me create a focus plan that balances urgent tasks with "
            "important long-term projects."
        )

        response = self.agent.handle_request(user_goal, context)
        return response

    def scenario_3_procrastination_help(self):
        """
        Scenario: User has important tasks but keeps procrastinating.
        The agent must: identify root causes, break down tasks, add urgency.
        """
        print("\n" + "=" * 70)
        print("SCENARIO 3: Breaking Through Procrastination")
        print("=" * 70)

        user_goal = (
            "I keep procrastinating on important tasks. I have a quarterly report "
            "due in 2 weeks that I haven't started, and I'm avoiding it. "
            "Help me break this down into manageable steps and create a schedule "
            "that will get me to finish on time."
        )

        response = self.agent.handle_request(user_goal)
        return response

    def scenario_4_energy_based_planning(self):
        """
        Scenario: Plan based on energy levels throughout the day.
        The agent must: use profile to match tasks to energy.
        """
        print("\n" + "=" * 70)
        print("SCENARIO 4: Energy-Based Task Planning")
        print("=" * 70)

        user_goal = (
            "I want to plan my day based on energy levels. I have deep work tasks, "
            "admin tasks, and communication tasks. Since I prefer mornings for deep work, "
            "help me create a schedule that matches tasks to my natural energy patterns."
        )

        response = self.agent.handle_request(user_goal)
        return response

    def scenario_5_pre_meeting_prep(self):
        """
        Scenario: Prepare for an important meeting.
        The agent must: identify what to review, create checklist.
        """
        print("\n" + "=" * 70)
        print("SCENARIO 5: Pre-Meeting Preparation")
        print("=" * 70)

        user_goal = (
            "I have an important investor meeting tomorrow afternoon. "
            "Help me identify what I need to review or prepare, check if my tasks "
            "are polished and professional, and create a checklist for tomorrow."
        )

        response = self.agent.handle_request(user_goal)
        return response

    def scenario_6_end_of_day_wrap_up(self):
        """
        Scenario: End of day - what's left, what's next.
        The agent must: assess day's progress, plan tomorrow, cleanup.
        """
        print("\n" + "=" * 70)
        print("SCENARIO 6: End of Day Wrap-up")
        print("=" * 70)

        user_goal = (
            "It's 5pm and I'm wrapping up my workday. Help me see what I accomplished "
            "today, what still needs attention, and what I should focus on tomorrow morning."
        )

        response = self.agent.handle_request(user_goal)
        return response

    def scenario_7_quarterly_planning(self):
        """
        Scenario: Quarterly planning - big picture view.
        The agent must: categorize by impact, identify themes, plan sprints.
        """
        print("\n" + "=" * 70)
        print("SCENARIO 7: Quarterly Planning")
        print("=" * 70)

        user_goal = (
            "I'm planning for next quarter. I want to see all my tasks categorized by "
            "impact and importance, identify recurring themes, and create a strategic "
            "plan with weekly focus areas."
        )

        response = self.agent.handle_request(user_goal)
        return response

    def scenario_8_calendar_integration_thinking(self):
        """
        Scenario: Thinking about calendar, not just task list.
        The agent must: think in time blocks, not just tasks.
        """
        print("\n" + "=" * 70)
        print("SCENARIO 8: Time-Block Thinking")
        print("=" * 70)

        user_goal = (
            "I want to think in terms of time blocks rather than just task lists. "
            "Help me identify how much time each priority will take and create a "
            "realistic schedule for this week with estimated durations."
        )

        response = self.agent.handle_request(user_goal)
        return response


def run_all_scenarios(use_mock: bool = True):
    """
    Run all scenarios to demonstrate agent capabilities.

    Args:
        use_mock: If True, use mock data
    """
    scenarios = AdvancedPlanningScenarios(use_mock=use_mock)

    print("\n" + "=" * 70)
    print("🚀 ADVANCED PLANNING SCENARIOS")
    print("=" * 70)
    print("\nThese examples show goal-driven, adaptive planning.")
    print("Watch how the agent:")
    print("  • Understands the user's goal")
    print("  • Fetches relevant data")
    print("  • Creates multi-step plans")
    print("  • Adapts to context")
    print("  • Provides actionable output")
    print("=" * 70)

    scenario_list = [
        ("Overwhelmed Backlog", scenarios.scenario_1_overwhelmed_backlog),
        ("Monday Morning Planning", scenarios.scenario_2_monday_morning_planning),
        ("Breaking Procrastination", scenarios.scenario_3_procrastination_help),
        ("Energy-Based Planning", scenarios.scenario_4_energy_based_planning),
        ("Pre-Meeting Prep", scenarios.scenario_5_pre_meeting_prep),
        ("End of Day Wrap-up", scenarios.scenario_6_end_of_day_wrap_up),
        ("Quarterly Planning", scenarios.scenario_7_quarterly_planning),
        ("Time-Block Thinking", scenarios.scenario_8_calendar_integration_thinking),
    ]

    for i, (name, scenario_func) in enumerate(scenario_list, 1):
        try:
            print(f"\n\n{'='*70}")
            print(f"Running Scenario {i}/{len(scenario_list)}: {name}")
            print(f"{'='*70}\n")

            scenario_func()

            if i < len(scenario_list):
                print("\n" + "-" * 70)
                print("Press Enter to continue to next scenario...")
                input()

        except KeyboardInterrupt:
            print("\n\n⏹️  Stopped by user")
            break
        except Exception as e:
            print(f"\n❌ Error in scenario {name}: {e}")
            import traceback
            traceback.print_exc()

    print("\n\n" + "=" * 70)
    print("✅ All scenarios completed!")
    print("=" * 70)


if __name__ == "__main__":
    import sys

    use_mock = "--mock" in sys.argv
    run_all_scenarios(use_mock=use_mock)
