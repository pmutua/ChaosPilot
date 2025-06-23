# chaos_commander.py

import os
from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm
import json
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from enum import Enum

from toolbox_core import ToolboxSyncClient
from dotenv import load_dotenv


load_dotenv()

toolbox = ToolboxSyncClient("http://127.0.0.1:5000")
tools = toolbox.load_toolset("action_recommender_toolset")


AZURE_API_KEY = os.getenv("AZURE_API_KEY")
AZURE_API_BASE = os.getenv("AZURE_API_BASE")
AZURE_API_VERSION = os.getenv("AZURE_API_VERSION")


class ActionType(Enum):
    AUTOMATED = "automated"
    SEMI_AUTOMATED = "semi_automated"
    MANUAL = "manual"
    APPROVAL_REQUIRED = "approval_required"


class ActionPriority(Enum):
    IMMEDIATE = "immediate"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class IntelligentActionRecommender:
    """Advanced action recommendation with intelligent automation"""

    def __init__(self):
        self.automation_playbooks = {
            "database_connection_issues": {
                "triggers": [
                    "connection timeout",
                    "connection pool exhausted",
                    "database error",
                ],
                "automated_actions": [
                    {
                        "action": "restart_connection_pool",
                        "description": "Restart database connection pool",
                        "automation_level": ActionType.AUTOMATED,
                        "success_rate": 0.85,
                        "rollback_plan": "restore_previous_pool_config",
                    },
                    {
                        "action": "scale_database_resources",
                        "description": "Scale database CPU/memory if needed",
                        "automation_level": ActionType.SEMI_AUTOMATED,
                        "success_rate": 0.90,
                        "rollback_plan": "scale_down_resources",
                    },
                ],
                "manual_actions": [
                    {
                        "action": "investigate_root_cause",
                        "description": "Investigate underlying database issues",
                        "priority": ActionPriority.HIGH,
                        "estimated_time": "30_minutes",
                    }
                ],
            },
            "api_rate_limiting": {
                "triggers": ["rate limit exceeded", "429 error", "throttling"],
                "automated_actions": [
                    {
                        "action": "adjust_rate_limits",
                        "description": "Temporarily increase rate limits",
                        "automation_level": ActionType.SEMI_AUTOMATED,
                        "success_rate": 0.80,
                        "rollback_plan": "restore_original_limits",
                    },
                    {
                        "action": "enable_caching",
                        "description": "Enable API response caching",
                        "automation_level": ActionType.AUTOMATED,
                        "success_rate": 0.75,
                        "rollback_plan": "disable_caching",
                    },
                ],
                "manual_actions": [
                    {
                        "action": "review_api_usage",
                        "description": "Review API usage patterns",
                        "priority": ActionPriority.MEDIUM,
                        "estimated_time": "1_hour",
                    }
                ],
            },
            "performance_degradation": {
                "triggers": ["high cpu usage", "memory leak", "slow response times"],
                "automated_actions": [
                    {
                        "action": "scale_resources",
                        "description": "Auto-scale application resources",
                        "automation_level": ActionType.AUTOMATED,
                        "success_rate": 0.90,
                        "rollback_plan": "scale_down_resources",
                    },
                    {
                        "action": "restart_services",
                        "description": "Restart problematic services",
                        "automation_level": ActionType.SEMI_AUTOMATED,
                        "success_rate": 0.85,
                        "rollback_plan": "restore_service_state",
                    },
                ],
                "manual_actions": [
                    {
                        "action": "performance_analysis",
                        "description": "Deep performance analysis",
                        "priority": ActionPriority.HIGH,
                        "estimated_time": "2_hours",
                    }
                ],
            },
            "security_incident": {
                "triggers": [
                    "failed login attempts",
                    "suspicious activity",
                    "unauthorized access",
                ],
                "automated_actions": [
                    {
                        "action": "block_suspicious_ips",
                        "description": "Block suspicious IP addresses",
                        "automation_level": ActionType.AUTOMATED,
                        "success_rate": 0.95,
                        "rollback_plan": "unblock_ips",
                    },
                    {
                        "action": "enable_enhanced_monitoring",
                        "description": "Enable enhanced security monitoring",
                        "automation_level": ActionType.AUTOMATED,
                        "success_rate": 0.90,
                        "rollback_plan": "disable_enhanced_monitoring",
                    },
                ],
                "manual_actions": [
                    {
                        "action": "security_audit",
                        "description": "Comprehensive security audit",
                        "priority": ActionPriority.IMMEDIATE,
                        "estimated_time": "4_hours",
                    }
                ],
            },
        }

        self.action_templates = {
            "restart_service": {
                "command": "systemctl restart {service_name}",
                "validation": "check_service_status",
                "timeout": "5_minutes",
                "retry_count": 3,
            },
            "scale_resources": {
                "command": "kubectl scale deployment {deployment} --replicas={replicas}",
                "validation": "check_deployment_status",
                "timeout": "10_minutes",
                "retry_count": 2,
            },
            "update_config": {
                "command": "update_configuration {config_key} {new_value}",
                "validation": "verify_config_change",
                "timeout": "3_minutes",
                "retry_count": 1,
            },
        }

    def analyze_incident_for_actions(self, planner_data: Dict) -> Dict[str, Any]:
        """Analyze incident and recommend intelligent actions"""
        incident_type = planner_data.get("incident_summary", {}).get(
            "incident_type", ""
        )
        priority = planner_data.get("incident_summary", {}).get("priority", "")
        patterns = (
            planner_data.get("incident_summary", {})
            .get("detailed_analysis", {})
            .get("patterns_found", [])
        )

        # Find matching playbook
        playbook = self._find_matching_playbook(patterns, incident_type)

        # Generate action recommendations
        recommendations = self._generate_action_recommendations(
            playbook, priority, patterns
        )

        # Prioritize actions
        prioritized_actions = self._prioritize_actions(recommendations, priority)

        # Add automation context
        automation_context = self._create_automation_context(prioritized_actions)

        return {
            "incident_analysis": {
                "type": incident_type,
                "priority": priority,
                "patterns_detected": len(patterns),
            },
            "recommended_actions": prioritized_actions,
            "automation_context": automation_context,
            "success_probability": self._calculate_success_probability(
                prioritized_actions
            ),
            "estimated_resolution_time": self._estimate_resolution_time(
                prioritized_actions
            ),
            "risk_assessment": self._assess_action_risks(prioritized_actions),
        }

    def _find_matching_playbook(self, patterns: List[Dict], incident_type: str) -> Dict:
        """Find the best matching automation playbook"""
        best_match = None
        highest_score = 0

        for playbook_name, playbook in self.automation_playbooks.items():
            score = 0
            triggers = playbook.get("triggers", [])

            for pattern in patterns:
                message = pattern.get("message", "").lower()
                for trigger in triggers:
                    if trigger.lower() in message:
                        score += 1

            if score > highest_score:
                highest_score = score
                best_match = playbook

        return best_match or self.automation_playbooks.get(
            "performance_degradation", {}
        )

    def _generate_action_recommendations(
        self, playbook: Dict, priority: str, patterns: List[Dict]
    ) -> List[Dict]:
        """Generate intelligent action recommendations"""
        recommendations = []

        # Add automated actions
        automated_actions = playbook.get("automated_actions", [])
        for action in automated_actions:
            action_copy = action.copy()
            action_copy["recommended"] = True
            action_copy["reasoning"] = self._generate_action_reasoning(action, patterns)
            recommendations.append(action_copy)

        # Add manual actions
        manual_actions = playbook.get("manual_actions", [])
        for action in manual_actions:
            action_copy = action.copy()
            action_copy["recommended"] = True
            action_copy["reasoning"] = self._generate_action_reasoning(action, patterns)
            recommendations.append(action_copy)

        # Add contextual actions based on patterns
        contextual_actions = self._generate_contextual_actions(patterns, priority)
        recommendations.extend(contextual_actions)

        return recommendations

    def _generate_action_reasoning(self, action: Dict, patterns: List[Dict]) -> str:
        """Generate intelligent reasoning for action recommendation"""
        action_name = action.get("action", "")

        if "restart" in action_name:
            return "Service restart recommended due to detected instability patterns"
        elif "scale" in action_name:
            return "Resource scaling recommended based on performance degradation indicators"
        elif "investigate" in action_name:
            return (
                "Manual investigation required to identify root cause of complex issues"
            )
        elif "block" in action_name:
            return "Security action required due to detected suspicious activity"
        else:
            return "Action recommended based on incident analysis and best practices"

    def _generate_contextual_actions(
        self, patterns: List[Dict], priority: str
    ) -> List[Dict]:
        """Generate contextual actions based on specific patterns"""
        contextual_actions = []

        for pattern in patterns:
            message = pattern.get("message", "").lower()
            severity = pattern.get("severity", "low")

            if "timeout" in message and severity in ["high", "critical"]:
                contextual_actions.append(
                    {
                        "action": "increase_timeout_limits",
                        "description": "Increase timeout limits for affected services",
                        "automation_level": ActionType.SEMI_AUTOMATED,
                        "priority": ActionPriority.HIGH,
                        "reasoning": "Timeout issues detected with high severity",
                        "estimated_time": "15_minutes",
                    }
                )

            if "memory" in message and "leak" in message:
                contextual_actions.append(
                    {
                        "action": "memory_analysis",
                        "description": "Perform memory leak analysis and cleanup",
                        "automation_level": ActionType.MANUAL,
                        "priority": ActionPriority.HIGH,
                        "reasoning": "Memory leak patterns detected",
                        "estimated_time": "1_hour",
                    }
                )

        return contextual_actions

    def _prioritize_actions(
        self, actions: List[Dict], incident_priority: str
    ) -> List[Dict]:
        """Intelligently prioritize actions based on incident priority and impact"""
        for action in actions:
            # Calculate priority score
            priority_score = 0

            # Base priority from incident
            if incident_priority == "critical":
                priority_score += 100
            elif incident_priority == "high":
                priority_score += 75
            elif incident_priority == "medium":
                priority_score += 50
            else:
                priority_score += 25

            # Automation level bonus
            if action.get("automation_level") == ActionType.AUTOMATED:
                priority_score += 20
            elif action.get("automation_level") == ActionType.SEMI_AUTOMATED:
                priority_score += 15

            # Success rate bonus
            success_rate = action.get("success_rate", 0.5)
            priority_score += int(success_rate * 30)

            # Time efficiency bonus
            estimated_time = action.get("estimated_time", "1_hour")
            if "minutes" in estimated_time:
                priority_score += 10
            elif "hour" in estimated_time:
                priority_score += 5

            action["priority_score"] = priority_score

        # Sort by priority score
        return sorted(actions, key=lambda x: x.get("priority_score", 0), reverse=True)

    def _create_automation_context(self, actions: List[Dict]) -> Dict[str, Any]:
        """Create context for automated execution"""
        automated_actions = [
            a for a in actions if a.get("automation_level") == ActionType.AUTOMATED
        ]
        semi_automated = [
            a for a in actions if a.get("automation_level") == ActionType.SEMI_AUTOMATED
        ]

        return {
            "can_auto_execute": len(automated_actions) > 0,
            "automated_actions_count": len(automated_actions),
            "semi_automated_count": len(semi_automated),
            "execution_plan": self._create_execution_plan(actions),
            "rollback_strategy": self._create_rollback_strategy(actions),
            "monitoring_requirements": self._define_monitoring_requirements(actions),
        }

    def _create_execution_plan(self, actions: List[Dict]) -> List[Dict]:
        """Create detailed execution plan for actions"""
        execution_plan = []

        for i, action in enumerate(actions):
            plan_step = {
                "step_number": i + 1,
                "action": action.get("action"),
                "description": action.get("description"),
                "automation_level": action.get("automation_level"),
                "estimated_time": action.get("estimated_time", "30_minutes"),
                "dependencies": self._identify_dependencies(action, actions),
                "validation_steps": self._create_validation_steps(action),
                "rollback_trigger": self._define_rollback_trigger(action),
            }
            execution_plan.append(plan_step)

        return execution_plan

    def _identify_dependencies(
        self, action: Dict, all_actions: List[Dict]
    ) -> List[str]:
        """Identify dependencies between actions"""
        dependencies = []
        action_name = action.get("action", "")

        # Define dependency rules
        if "scale" in action_name:
            dependencies.append("check_current_resources")
        elif "restart" in action_name:
            dependencies.append("backup_service_state")
        elif "investigate" in action_name:
            dependencies.append("collect_logs")

        return dependencies

    def _create_validation_steps(self, action: Dict) -> List[str]:
        """Create validation steps for action execution"""
        action_name = action.get("action", "")

        if "restart" in action_name:
            return [
                "Verify service is running",
                "Check service health endpoint",
                "Validate recent logs for errors",
            ]
        elif "scale" in action_name:
            return [
                "Confirm resource allocation",
                "Check performance metrics",
                "Verify no resource conflicts",
            ]
        else:
            return [
                "Verify action completion",
                "Check system stability",
                "Monitor for side effects",
            ]

    def _define_rollback_trigger(self, action: Dict) -> Dict[str, Any]:
        """Define conditions that trigger rollback"""
        return {
            "timeout_exceeded": True,
            "validation_failed": True,
            "error_threshold_exceeded": True,
            "performance_degradation": True,
        }

    def _create_rollback_strategy(self, actions: List[Dict]) -> Dict[str, Any]:
        """Create comprehensive rollback strategy"""
        rollback_actions = []

        for action in actions:
            rollback_plan = action.get("rollback_plan")
            if rollback_plan:
                rollback_actions.append(
                    {
                        "original_action": action.get("action"),
                        "rollback_action": rollback_plan,
                        "automation_level": ActionType.AUTOMATED,
                        "estimated_time": "5_minutes",
                    }
                )

        return {
            "rollback_actions": rollback_actions,
            "rollback_trigger_conditions": [
                "Action execution fails",
                "System performance degrades",
                "Error rate increases",
                "Service becomes unavailable",
            ],
            "rollback_timeout": "10_minutes",
        }

    def _define_monitoring_requirements(self, actions: List[Dict]) -> List[str]:
        """Define monitoring requirements for action execution"""
        monitoring_requirements = [
            "Monitor system performance metrics",
            "Track error rates and response times",
            "Watch for resource utilization spikes",
            "Monitor service health endpoints",
        ]

        # Add specific monitoring based on actions
        for action in actions:
            action_name = action.get("action", "")
            if "database" in action_name:
                monitoring_requirements.append("Monitor database connection pool")
            elif "api" in action_name:
                monitoring_requirements.append("Monitor API response times")
            elif "security" in action_name:
                monitoring_requirements.append("Monitor security event logs")

        return monitoring_requirements

    def _calculate_success_probability(self, actions: List[Dict]) -> float:
        """Calculate overall success probability"""
        if not actions:
            return 0.0

        total_probability = 0
        for action in actions:
            success_rate = action.get("success_rate", 0.5)
            total_probability += success_rate

        return total_probability / len(actions)

    def _estimate_resolution_time(self, actions: List[Dict]) -> str:
        """Estimate total resolution time"""
        total_minutes = 0

        for action in actions:
            estimated_time = action.get("estimated_time", "30_minutes")
            if "minutes" in estimated_time:
                minutes = int(estimated_time.split("_")[0])
                total_minutes += minutes
            elif "hour" in estimated_time:
                hours = int(estimated_time.split("_")[0])
                total_minutes += hours * 60

        if total_minutes < 60:
            return f"{total_minutes}_minutes"
        else:
            hours = total_minutes // 60
            minutes = total_minutes % 60
            return f"{hours}_hours_{minutes}_minutes"

    def _assess_action_risks(self, actions: List[Dict]) -> Dict[str, Any]:
        """Assess risks associated with recommended actions"""
        risk_factors = {
            "high_risk_actions": [],
            "medium_risk_actions": [],
            "low_risk_actions": [],
            "overall_risk_level": "low",
        }

        for action in actions:
            action_name = action.get("action", "")
            automation_level = action.get("automation_level")

            # Risk assessment logic
            if "restart" in action_name or "scale" in action_name:
                if automation_level == ActionType.AUTOMATED:
                    risk_factors["high_risk_actions"].append(action_name)
                else:
                    risk_factors["medium_risk_actions"].append(action_name)
            elif "investigate" in action_name:
                risk_factors["low_risk_actions"].append(action_name)
            else:
                risk_factors["medium_risk_actions"].append(action_name)

        # Determine overall risk level
        if risk_factors["high_risk_actions"]:
            risk_factors["overall_risk_level"] = "high"
        elif risk_factors["medium_risk_actions"]:
            risk_factors["overall_risk_level"] = "medium"
        else:
            risk_factors["overall_risk_level"] = "low"

        return risk_factors


# Enhanced action recommender agent
action_recommender_agent = Agent(
    name="action_recommender",
    model=LiteLlm(model="azure/gpt-4o"),
    description="Action recommender using only schema-compliant fields from BigQuery logs.",
    tools=tools,
)


def recommend_actions_from_logs(logs: list) -> dict:
    """
    Recommend actions based on most frequent error/critical messages and agent activity using only available schema fields.
    """
    action_counts = {}
    for log in logs:
        agent_id = log.get("agent_id")
        experiment_id = log.get("experiment_id")
        message = log.get("message")
        severity = log.get("severity")
        if not agent_id or not experiment_id or not message:
            continue
        key = (agent_id, experiment_id, message)
        if key not in action_counts:
            action_counts[key] = {"count": 0, "severities": set()}
        action_counts[key]["count"] += 1
        if severity:
            action_counts[key]["severities"].add(severity)
    # Convert sets to lists for JSON serialization
    for key in action_counts:
        action_counts[key]["severities"] = list(action_counts[key]["severities"])
    # Sort by count and take top 10
    top_actions = sorted(
        action_counts.items(), key=lambda x: x[1]["count"], reverse=True
    )[:10]
    recommendations = [
        {
            "agent_id": k[0],
            "experiment_id": k[1],
            "action_message": k[2],
            "count": v["count"],
            "severities": v["severities"],
        }
        for k, v in top_actions
    ]
    return {
        "action_recommender_summary_generated_at": datetime.utcnow().isoformat() + "Z",
        "top_recommended_actions": recommendations,
    }
