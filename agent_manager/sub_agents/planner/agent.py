# chaos_commander.py

import os
from datetime import datetime, timedelta
from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm
from google.adk.tools import ToolboxTool
import json
from typing import Dict, List, Any, Optional
from enum import Enum
from dotenv import load_dotenv

from toolbox_core import ToolboxSyncClient

load_dotenv()

toolbox = ToolboxSyncClient("http://127.0.0.1:5000")
tools = toolbox.load_toolset('planner_toolset')

AZURE_API_KEY = os.getenv("AZURE_API_KEY")
AZURE_API_BASE = os.getenv("AZURE_API_BASE")
AZURE_API_VERSION = os.getenv("AZURE_API_VERSION")

class IncidentPriority(Enum):
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"

class IncidentType(Enum):
    DATABASE_FAILURE = "database_failure"
    API_DEGRADATION = "api_degradation"
    PERFORMANCE_ISSUE = "performance_issue"
    SECURITY_BREACH = "security_breach"
    INFRASTRUCTURE_FAILURE = "infrastructure_failure"
    NETWORK_ISSUE = "network_issue"

class IntelligentIncidentPlanner:
    """Advanced incident response planning with intelligent reasoning"""
    
    def __init__(self):
        self.response_templates = {
            IncidentType.DATABASE_FAILURE: {
                "immediate_actions": [
                    "Check database connectivity and health",
                    "Verify connection pool status",
                    "Review recent database changes",
                    "Check for deadlocks or long-running queries"
                ],
                "mitigation_steps": [
                    "Implement connection retry logic",
                    "Add database health monitoring",
                    "Optimize query performance",
                    "Set up database failover"
                ],
                "prevention_measures": [
                    "Regular database maintenance",
                    "Performance monitoring alerts",
                    "Connection pool optimization",
                    "Query optimization reviews"
                ]
            },
            IncidentType.API_DEGRADATION: {
                "immediate_actions": [
                    "Check API endpoint health",
                    "Review rate limiting policies",
                    "Analyze response times",
                    "Check authentication services"
                ],
                "mitigation_steps": [
                    "Implement circuit breakers",
                    "Add API caching",
                    "Optimize response times",
                    "Scale API resources"
                ],
                "prevention_measures": [
                    "API performance monitoring",
                    "Load testing",
                    "Rate limit optimization",
                    "Caching strategies"
                ]
            },
            IncidentType.PERFORMANCE_ISSUE: {
                "immediate_actions": [
                    "Monitor CPU and memory usage",
                    "Check disk space",
                    "Review application logs",
                    "Analyze resource bottlenecks"
                ],
                "mitigation_steps": [
                    "Scale resources horizontally",
                    "Optimize code performance",
                    "Implement caching",
                    "Add resource monitoring"
                ],
                "prevention_measures": [
                    "Regular performance testing",
                    "Resource monitoring alerts",
                    "Code optimization reviews",
                    "Capacity planning"
                ]
            }
        }
        
        self.escalation_matrix = {
            IncidentPriority.CRITICAL: {
                "response_time": "5 minutes",
                "escalation_level": "immediate",
                "stakeholders": ["oncall", "management", "stakeholders"],
                "communication_channels": ["slack", "email", "phone"]
            },
            IncidentPriority.HIGH: {
                "response_time": "15 minutes",
                "escalation_level": "within_1_hour",
                "stakeholders": ["oncall", "management"],
                "communication_channels": ["slack", "email"]
            },
            IncidentPriority.MEDIUM: {
                "response_time": "1 hour",
                "escalation_level": "within_4_hours",
                "stakeholders": ["oncall"],
                "communication_channels": ["slack"]
            },
            IncidentPriority.LOW: {
                "response_time": "4 hours",
                "escalation_level": "within_24_hours",
                "stakeholders": ["oncall"],
                "communication_channels": ["slack"]
            }
        }
    
    def analyze_incident_context(self, detector_data: Dict) -> Dict[str, Any]:
        """Intelligent analysis of incident context and impact"""
        analysis = {
            "incident_type": self._classify_incident(detector_data),
            "priority": self._determine_priority(detector_data),
            "impact_assessment": self._assess_impact(detector_data),
            "root_cause_hypothesis": self._generate_root_cause_hypothesis(detector_data),
            "affected_services": self._identify_affected_services(detector_data),
            "business_impact": self._assess_business_impact(detector_data)
        }
        
        return analysis
    
    def _classify_incident(self, detector_data: Dict) -> str:
        """Classify incident type based on patterns"""
        patterns = detector_data.get('detailed_analysis', {}).get('patterns_found', [])
        
        for pattern in patterns:
            category = pattern.get('category', '')
            if 'database' in category:
                return IncidentType.DATABASE_FAILURE.value
            elif 'api' in category:
                return IncidentType.API_DEGRADATION.value
            elif 'performance' in category:
                return IncidentType.PERFORMANCE_ISSUE.value
            elif 'security' in category:
                return IncidentType.SECURITY_BREACH.value
        
        return IncidentType.INFRASTRUCTURE_FAILURE.value
    
    def _determine_priority(self, detector_data: Dict) -> str:
        """Determine incident priority based on severity and impact"""
        patterns = detector_data.get('detailed_analysis', {}).get('patterns_found', [])
        
        critical_count = sum(1 for p in patterns if p.get('severity') == 'critical')
        high_count = sum(1 for p in patterns if p.get('severity') == 'high')
        
        if critical_count > 0:
            return IncidentPriority.CRITICAL.value
        elif high_count > 2:
            return IncidentPriority.HIGH.value
        elif high_count > 0:
            return IncidentPriority.MEDIUM.value
        else:
            return IncidentPriority.LOW.value
    
    def _assess_impact(self, detector_data: Dict) -> Dict[str, Any]:
        """Assess technical and business impact"""
        patterns = detector_data.get('detailed_analysis', {}).get('patterns_found', [])
        anomalies = detector_data.get('detailed_analysis', {}).get('anomalies', [])
        
        return {
            "affected_users": self._estimate_affected_users(patterns),
            "service_degradation": self._assess_service_degradation(patterns),
            "data_risk": self._assess_data_risk(patterns),
            "recovery_time_estimate": self._estimate_recovery_time(patterns, anomalies)
        }
    
    def _generate_root_cause_hypothesis(self, detector_data: Dict) -> List[Dict]:
        """Generate intelligent root cause hypotheses"""
        patterns = detector_data.get('detailed_analysis', {}).get('patterns_found', [])
        correlations = detector_data.get('detailed_analysis', {}).get('correlations', [])
        
        hypotheses = []
        
        # Database-related hypotheses
        db_patterns = [p for p in patterns if p.get('category') == 'database_errors']
        if db_patterns:
            hypotheses.append({
                "hypothesis": "Database connection pool exhaustion",
                "confidence": 0.85,
                "evidence": [p.get('message') for p in db_patterns],
                "investigation_steps": [
                    "Check connection pool metrics",
                    "Review database load",
                    "Analyze connection patterns"
                ]
            })
        
        # API-related hypotheses
        api_patterns = [p for p in patterns if p.get('category') == 'api_errors']
        if api_patterns:
            hypotheses.append({
                "hypothesis": "API rate limiting or authentication issues",
                "confidence": 0.75,
                "evidence": [p.get('message') for p in api_patterns],
                "investigation_steps": [
                    "Check API rate limits",
                    "Verify authentication tokens",
                    "Review API endpoint health"
                ]
            })
        
        return hypotheses
    
    def _identify_affected_services(self, detector_data: Dict) -> List[str]:
        """Identify services affected by the incident"""
        patterns = detector_data.get('detailed_analysis', {}).get('patterns_found', [])
        services = set()
        
        for pattern in patterns:
            message = pattern.get('message', '').lower()
            if 'api' in message:
                services.add('api_gateway')
            if 'database' in message or 'sql' in message:
                services.add('database')
            if 'auth' in message or 'login' in message:
                services.add('authentication')
            if 'payment' in message:
                services.add('payment_processing')
        
        return list(services)
    
    def _assess_business_impact(self, detector_data: Dict) -> Dict[str, Any]:
        """Assess business impact of the incident"""
        priority = self._determine_priority(detector_data)
        
        impact_levels = {
            IncidentPriority.CRITICAL.value: {
                "customer_experience": "severely_impacted",
                "revenue_impact": "high",
                "reputation_risk": "high",
                "compliance_risk": "high"
            },
            IncidentPriority.HIGH.value: {
                "customer_experience": "moderately_impacted",
                "revenue_impact": "medium",
                "reputation_risk": "medium",
                "compliance_risk": "medium"
            },
            IncidentPriority.MEDIUM.value: {
                "customer_experience": "slightly_impacted",
                "revenue_impact": "low",
                "reputation_risk": "low",
                "compliance_risk": "low"
            },
            IncidentPriority.LOW.value: {
                "customer_experience": "minimal_impact",
                "revenue_impact": "minimal",
                "reputation_risk": "minimal",
                "compliance_risk": "minimal"
            }
        }
        
        return impact_levels.get(priority, impact_levels[IncidentPriority.LOW.value])
    
    def _estimate_affected_users(self, patterns: List[Dict]) -> str:
        """Estimate number of affected users"""
        total_errors = len(patterns)
        if total_errors > 100:
            return "large_scale"
        elif total_errors > 50:
            return "medium_scale"
        elif total_errors > 10:
            return "small_scale"
        else:
            return "limited_scale"
    
    def _assess_service_degradation(self, patterns: List[Dict]) -> str:
        """Assess level of service degradation"""
        critical_count = sum(1 for p in patterns if p.get('severity') == 'critical')
        if critical_count > 5:
            return "severe_degradation"
        elif critical_count > 2:
            return "moderate_degradation"
        elif critical_count > 0:
            return "minor_degradation"
        else:
            return "no_degradation"
    
    def _assess_data_risk(self, patterns: List[Dict]) -> str:
        """Assess data security and integrity risk"""
        security_patterns = [p for p in patterns if p.get('category') == 'security_events']
        if security_patterns:
            return "high_risk"
        else:
            return "low_risk"
    
    def _estimate_recovery_time(self, patterns: List[Dict], anomalies: List[Dict]) -> str:
        """Estimate recovery time based on incident complexity"""
        complexity_score = len(patterns) + len(anomalies)
        if complexity_score > 20:
            return "4-8_hours"
        elif complexity_score > 10:
            return "2-4_hours"
        elif complexity_score > 5:
            return "1-2_hours"
        else:
            return "30_minutes_1_hour"
    
    def create_response_plan(self, incident_analysis: Dict) -> Dict[str, Any]:
        """Create comprehensive incident response plan"""
        incident_type = incident_analysis.get('incident_type')
        priority = incident_analysis.get('priority')
        
        # Get response template
        template = self.response_templates.get(IncidentType(incident_type), {})
        escalation = self.escalation_matrix.get(IncidentPriority(priority), {})
        
        plan = {
            "incident_id": f"INC-{datetime.now().strftime('%Y%m%d-%H%M%S')}",
            "created_at": datetime.now().isoformat(),
            "incident_summary": incident_analysis,
            "response_plan": {
                "immediate_actions": template.get('immediate_actions', []),
                "mitigation_steps": template.get('mitigation_steps', []),
                "prevention_measures": template.get('prevention_measures', [])
            },
            "escalation_procedure": escalation,
            "communication_plan": {
                "stakeholders": escalation.get('stakeholders', []),
                "channels": escalation.get('communication_channels', []),
                "update_frequency": self._determine_update_frequency(priority)
            },
            "success_criteria": self._define_success_criteria(incident_type),
            "automated_actions": self._suggest_automated_actions(incident_analysis)
        }
        
        return plan
    
    def _determine_update_frequency(self, priority: str) -> str:
        """Determine update frequency based on priority"""
        frequencies = {
            IncidentPriority.CRITICAL.value: "every_15_minutes",
            IncidentPriority.HIGH.value: "every_30_minutes",
            IncidentPriority.MEDIUM.value: "every_hour",
            IncidentPriority.LOW.value: "every_4_hours"
        }
        return frequencies.get(priority, "every_hour")
    
    def _define_success_criteria(self, incident_type: str) -> List[str]:
        """Define success criteria for incident resolution"""
        criteria = {
            IncidentType.DATABASE_FAILURE.value: [
                "Database connectivity restored",
                "All queries executing successfully",
                "Connection pool healthy",
                "No deadlocks detected"
            ],
            IncidentType.API_DEGRADATION.value: [
                "API response times normalized",
                "All endpoints responding",
                "Rate limiting functioning properly",
                "Authentication working correctly"
            ],
            IncidentType.PERFORMANCE_ISSUE.value: [
                "Resource usage within normal limits",
                "Application response times improved",
                "No memory leaks detected",
                "System stability restored"
            ]
        }
        return criteria.get(incident_type, ["Incident resolved", "Service restored", "Monitoring stable"])
    
    def _suggest_automated_actions(self, incident_analysis: Dict) -> List[Dict]:
        """Suggest automated actions for incident response"""
        incident_type = incident_analysis.get('incident_type')
        priority = incident_analysis.get('priority')
        
        actions = []
        
        if incident_type == IncidentType.DATABASE_FAILURE.value:
            actions.extend([
                {
                    "action": "restart_database_connections",
                    "description": "Automatically restart database connection pool",
                    "automation_level": "semi_automated",
                    "requires_approval": True
                },
                {
                    "action": "scale_database_resources",
                    "description": "Automatically scale database resources if needed",
                    "automation_level": "fully_automated",
                    "requires_approval": False
                }
            ])
        
        if priority in [IncidentPriority.CRITICAL.value, IncidentPriority.HIGH.value]:
            actions.append({
                "action": "send_emergency_notifications",
                "description": "Send emergency notifications to on-call team",
                "automation_level": "fully_automated",
                "requires_approval": False
            })
        
        return actions

# Enhanced planner agent
planner_agent = Agent(
    name="intelligent_planner",
    model=LiteLlm(model="azure/gpt-4o"),
    description="Intelligent incident response planner with automated reasoning and proactive mitigation strategies",
    tools=tools
)

@planner_agent.tool()
def create_intelligent_response_plan(detector_data: str) -> str:
    """
    Create intelligent incident response plan with automated reasoning.
    
    Args:
        detector_data: JSON string containing detector analysis results
    
    Returns:
        Comprehensive incident response plan with automated actions
    """
    try:
        # Parse detector data
        detector_analysis = json.loads(detector_data)
        
        # Initialize intelligent planner
        planner = IntelligentIncidentPlanner()
        
        # Analyze incident context
        incident_analysis = planner.analyze_incident_context(detector_analysis)
        
        # Create response plan
        response_plan = planner.create_response_plan(incident_analysis)
        
        return json.dumps(response_plan, indent=2)
        
    except Exception as e:
        return json.dumps({
            "error": f"Planning failed: {str(e)}",
            "timestamp": datetime.now().isoformat()
        })

@planner_agent.tool()
def suggest_proactive_measures(historical_data: str) -> str:
    """
    Suggest proactive measures based on historical incident data.
    
    Args:
        historical_data: JSON string containing historical incident data
    
    Returns:
        Proactive measures and prevention strategies
    """
    try:
        historical_incidents = json.loads(historical_data)
        
        # Analyze patterns and suggest proactive measures
        proactive_measures = {
            "monitoring_improvements": [
                "Implement predictive alerting based on trends",
                "Add anomaly detection for resource usage",
                "Set up automated health checks",
                "Create dashboards for key metrics"
            ],
            "infrastructure_improvements": [
                "Implement auto-scaling policies",
                "Add redundancy for critical services",
                "Set up automated backups",
                "Implement circuit breakers"
            ],
            "process_improvements": [
                "Create runbooks for common incidents",
                "Implement automated incident response",
                "Set up post-incident reviews",
                "Create knowledge base for solutions"
            ],
            "priority": "high",
            "estimated_effort": "2-4_weeks",
            "expected_impact": "reduce_incidents_by_60%"
        }
        
        return json.dumps(proactive_measures, indent=2)
        
    except Exception as e:
        return json.dumps({
            "error": f"Proactive analysis failed: {str(e)}",
            "timestamp": datetime.now().isoformat()
        })
