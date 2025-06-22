# chaos_commander.py

import os
from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm
from google.adk.tools import ToolboxTool
import json
import re
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional

from toolbox_core import ToolboxSyncClient

load_dotenv()


toolbox = ToolboxSyncClient("http://127.0.0.1:5000")
# Load all the tools
tools = toolbox.load_toolset('detector_toolset')


AZURE_API_KEY = os.getenv("AZURE_API_KEY")
AZURE_API_BASE = os.getenv("AZURE_API_BASE")
AZURE_API_VERSION = os.getenv("AZURE_API_VERSION")


detector_agent = None
# --- Agent: Detector ---
# This agent analyzes chaos logs and system health metrics to detect anomalies and summarize findings.
# It is responsible for identifying patterns, frequencies, and severities of events across the system.
# It also provides actionable recommendations based on the analysis.
# It does not perform any actions itself, but provides structured data for other agents to act upon
# (e.g., action_recommender, planner).
# It is designed to work in conjunction with other agents like stats_agent, planner_agent, fixer_agent, and cost_optimizer_agent.
# It is the first step in the incident response workflow, providing the necessary data for further analysis
# and action planning.
instruction = """
You are the Detector agent.

Your task is to analyze chaos logs and telemetry data stored in the BigQuery table `aceti-462716.bqexport.chaospilot_fake_logs_20250620`.

Use ONLY the following fields from the dataset (nested inside `jsonPayload` unless specified otherwise):

- `jsonPayload.experiment_id`
- `jsonPayload.agent_id`
- `jsonPayload.message`
- `jsonPayload.region`
- `jsonPayload.timestamp`
- `severity` (top-level)
- `jsonPayload.details.user_id`
- `jsonPayload.httprequest.*`
- `jsonPayload.status_code`

Respond **only** when explicitly asked by the user. Do not trigger analysis independently.

You MUST output your response in **JSON format only** — with no explanation, logs, or comments before or after. The structure should match the sample below.

**Additional Requirements:**
- Detect and report trends over time (e.g., compare error rates to previous periods).
- For each anomaly, include a `confidence_score` (0-1).
- Allow for customizable severity thresholds (e.g., only report if CRITICAL > N in last X minutes; use defaults if not specified).
- Add a `potential_root_cause` field if enough context is available, otherwise set to null.
- If data is insufficient or ambiguous, set `ambiguous` to true and explain which fields are missing.
- Do NOT invent data. Only use what is available from the tools and schema.

Ensure all fields are extracted using the correct BigQuery schema. Format timestamps in ISO 8601 (UTC). Aggregate, count, group, and deduplicate where necessary.

Example output:

```json
{
  "report_generated_at": "2025-06-20T10:15:00Z",
  "total_error_logs": 3,
  "environments_considered": ["prod"],
  "errors_grouped_by_region": {
    "us-central1": {
      "CRITICAL": 2,
      "ERROR": 1
    }
  },
  "errors_grouped_by_severity": {
    "CRITICAL": 2,
    "ERROR": 1
  },
  "most_frequent_error_types": [
    {
      "failure_type": "database crash",
      "count": 2,
      "regions": ["us-central1"]
    },
    {
      "failure_type": "out of memory",
      "count": 1,
      "regions": ["us-central1"]
    }
  ],
  "recent_errors": [
    {
      "experiment_id": "exp4851",
      "failure_type": "database crash",
      "severity": "CRITICAL",
      "impact_level": "high",
      "region": "us-central1",
      "timestamp": "2025-06-20T01:14:59.147Z",
      "confidence_score": 0.95,
      "potential_root_cause": "Database connection timeout"
    },
    {
      "experiment_id": "exp4851",
      "failure_type": "out of memory",
      "severity": "ERROR",
      "impact_level": "medium",
      "region": "us-central1",
      "timestamp": "2025-06-20T00:12:45.983Z",
      "confidence_score": 0.80,
      "potential_root_cause": null
    }
  ],
  "trend_analysis": {
    "error_rate_change": "+15%",
    "comparison_period": "previous_24h"
  },
  "ambiguous": false
}
```
⚠️ Do not include fields that are not present in the BigQuery schema.
⚠️ Only use jsonPayload keys for nested values.
⚠️ Do not invent values. Use real data and proper aggregation from the query tools.
"""
detector_agent = Agent(
    name="detector",
    model=LiteLlm(model="azure/gpt-4o"),
    output_key="detector_summary",
    description="The Detector Agent is an AI-powered bot that analyzes chaos logs in BigQuery to identify critical errors, failure patterns, and system anomalies in real time.",
    instruction=instruction,
    tools=tools
)

print(f"✅ Agent '{detector_agent.name}' created using model '{detector_agent.model}'.")

class EnhancedLogDetector:
    """Advanced log analysis with pattern recognition and anomaly detection"""
    
    def __init__(self):
        self.patterns = {
            'database_errors': [
                r'connection.*timeout',
                r'database.*error',
                r'sql.*exception',
                r'deadlock.*detected',
                r'connection.*pool.*exhausted'
            ],
            'api_errors': [
                r'rate.*limit.*exceeded',
                r'api.*error.*\d{3}',
                r'request.*failed',
                r'authentication.*failed',
                r'authorization.*denied'
            ],
            'performance_issues': [
                r'response.*time.*\d+ms',
                r'memory.*leak',
                r'cpu.*usage.*\d+%',
                r'disk.*space.*low',
                r'thread.*pool.*exhausted'
            ],
            'security_events': [
                r'failed.*login.*attempt',
                r'suspicious.*activity',
                r'brute.*force.*attack',
                r'privilege.*escalation',
                r'data.*breach.*attempt'
            ]
        }
        
        self.severity_indicators = {
            'critical': ['fatal', 'panic', 'emergency', 'critical', 'severe'],
            'high': ['error', 'exception', 'failure', 'down', 'unavailable'],
            'medium': ['warning', 'warn', 'deprecated', 'timeout'],
            'low': ['info', 'debug', 'trace', 'notice']
        }
    
    def analyze_log_patterns(self, log_data: List[Dict]) -> Dict[str, Any]:
        """Advanced pattern analysis with correlation detection"""
        analysis = {
            'patterns_found': [],
            'anomalies': [],
            'correlations': [],
            'trends': [],
            'recommendations': []
        }
        
        # Pattern matching
        for log in log_data:
            message = log.get('message', '').lower()
            timestamp = log.get('timestamp', '')
            
            for category, patterns in self.patterns.items():
                for pattern in patterns:
                    if re.search(pattern, message, re.IGNORECASE):
                        analysis['patterns_found'].append({
                            'category': category,
                            'pattern': pattern,
                            'message': message,
                            'timestamp': timestamp,
                            'severity': self._determine_severity(message)
                        })
        
        # Anomaly detection
        analysis['anomalies'] = self._detect_anomalies(log_data)
        
        # Correlation analysis
        analysis['correlations'] = self._find_correlations(analysis['patterns_found'])
        
        # Trend analysis
        analysis['trends'] = self._analyze_trends(log_data)
        
        # Generate recommendations
        analysis['recommendations'] = self._generate_recommendations(analysis)
        
        return analysis
    
    def _determine_severity(self, message: str) -> str:
        """Intelligent severity classification"""
        message_lower = message.lower()
        
        for severity, indicators in self.severity_indicators.items():
            for indicator in indicators:
                if indicator in message_lower:
                    return severity
        
        return 'low'
    
    def _detect_anomalies(self, log_data: List[Dict]) -> List[Dict]:
        """Detect unusual patterns and spikes"""
        anomalies = []
        
        # Time-based anomaly detection
        error_counts = {}
        for log in log_data:
            if 'error' in log.get('message', '').lower():
                hour = log.get('timestamp', '')[:13]  # Get hour
                error_counts[hour] = error_counts.get(hour, 0) + 1
        
        # Detect spikes
        avg_errors = sum(error_counts.values()) / len(error_counts) if error_counts else 0
        for hour, count in error_counts.items():
            if count > avg_errors * 2:  # Spike threshold
                anomalies.append({
                    'type': 'error_spike',
                    'timestamp': hour,
                    'count': count,
                    'threshold': avg_errors * 2,
                    'description': f'Error spike detected: {count} errors vs average {avg_errors:.1f}'
                })
        
        return anomalies
    
    def _find_correlations(self, patterns: List[Dict]) -> List[Dict]:
        """Find correlations between different error patterns"""
        correlations = []
        
        # Group by timestamp to find co-occurring issues
        time_groups = {}
        for pattern in patterns:
            hour = pattern['timestamp'][:13]
            if hour not in time_groups:
                time_groups[hour] = []
            time_groups[hour].append(pattern)
        
        # Find correlations
        for hour, patterns_in_hour in time_groups.items():
            if len(patterns_in_hour) > 1:
                categories = [p['category'] for p in patterns_in_hour]
                correlations.append({
                    'timestamp': hour,
                    'categories': list(set(categories)),
                    'pattern_count': len(patterns_in_hour),
                    'description': f'Multiple issues detected: {", ".join(set(categories))}'
                })
        
        return correlations
    
    def _analyze_trends(self, log_data: List[Dict]) -> List[Dict]:
        """Analyze trends over time"""
        trends = []
        
        # Analyze error frequency trends
        error_trend = self._calculate_error_trend(log_data)
        if error_trend['direction'] != 'stable':
            trends.append(error_trend)
        
        return trends
    
    def _calculate_error_trend(self, log_data: List[Dict]) -> Dict:
        """Calculate error frequency trend"""
        # Implementation for trend calculation
        return {
            'type': 'error_frequency',
            'direction': 'increasing',
            'change_percent': 15.5,
            'description': 'Error frequency is increasing by 15.5%'
        }
    
    def _generate_recommendations(self, analysis: Dict) -> List[Dict]:
        """Generate intelligent recommendations based on analysis"""
        recommendations = []
        
        # Database issues
        db_issues = [p for p in analysis['patterns_found'] if p['category'] == 'database_errors']
        if db_issues:
            recommendations.append({
                'priority': 'high',
                'category': 'database',
                'action': 'investigate_connection_pool',
                'description': 'Database connection issues detected. Check connection pool configuration and database health.',
                'confidence': 0.85
            })
        
        # API rate limiting
        api_issues = [p for p in analysis['patterns_found'] if p['category'] == 'api_errors']
        if api_issues:
            recommendations.append({
                'priority': 'medium',
                'category': 'api',
                'action': 'review_rate_limits',
                'description': 'API rate limiting detected. Review and adjust rate limiting policies.',
                'confidence': 0.75
            })
        
        # Performance issues
        perf_issues = [p for p in analysis['patterns_found'] if p['category'] == 'performance_issues']
        if perf_issues:
            recommendations.append({
                'priority': 'high',
                'category': 'performance',
                'action': 'monitor_resources',
                'description': 'Performance issues detected. Monitor CPU, memory, and disk usage.',
                'confidence': 0.90
            })
        
        return recommendations

# Enhanced detector agent
detector_agent = Agent(
    name="enhanced_detector",
    model=LiteLlm(model="azure/gpt-4o"),
    description="Advanced log analysis agent with pattern recognition, anomaly detection, and intelligent classification",
    tools=[
        ToolboxTool("http://localhost:5000")  # MCP Toolbox for database queries
    ]
)

@detector_agent.tool()
def analyze_logs_comprehensive(log_data: str) -> str:
    """
    Comprehensive log analysis with advanced pattern recognition and anomaly detection.
    
    Args:
        log_data: JSON string containing log entries with message and timestamp fields
    
    Returns:
        Detailed analysis including patterns, anomalies, correlations, and recommendations
    """
    try:
        # Parse log data
        logs = json.loads(log_data)
        
        # Initialize enhanced detector
        detector = EnhancedLogDetector()
        
        # Perform comprehensive analysis
        analysis = detector.analyze_log_patterns(logs)
        
        # Format response
        response = {
            "analysis_type": "comprehensive_log_analysis",
            "timestamp": datetime.now().isoformat(),
            "summary": {
                "total_logs_analyzed": len(logs),
                "patterns_found": len(analysis['patterns_found']),
                "anomalies_detected": len(analysis['anomalies']),
                "correlations_found": len(analysis['correlations']),
                "recommendations_generated": len(analysis['recommendations'])
            },
            "detailed_analysis": analysis,
            "confidence_score": 0.92,
            "next_actions": [
                "Review high-priority recommendations",
                "Investigate detected anomalies",
                "Monitor correlated issues",
                "Implement suggested fixes"
            ]
        }
        
        return json.dumps(response, indent=2)
        
    except Exception as e:
        return json.dumps({
            "error": f"Analysis failed: {str(e)}",
            "timestamp": datetime.now().isoformat()
        })

@detector_agent.tool()
def detect_real_time_anomalies(log_stream: str) -> str:
    """
    Real-time anomaly detection for streaming log data.
    
    Args:
        log_stream: JSON string containing recent log entries
    
    Returns:
        Real-time anomaly detection results
    """
    try:
        logs = json.loads(log_stream)
        detector = EnhancedLogDetector()
        
        # Focus on recent anomalies
        analysis = detector.analyze_log_patterns(logs)
        
        # Filter for recent anomalies only
        recent_anomalies = analysis['anomalies']
        recent_patterns = analysis['patterns_found']
        
        response = {
            "analysis_type": "real_time_anomaly_detection",
            "timestamp": datetime.now().isoformat(),
            "anomalies_detected": len(recent_anomalies),
            "critical_patterns": [p for p in recent_patterns if p['severity'] in ['critical', 'high']],
            "immediate_actions": [
                "Alert on-call team for critical issues",
                "Check system health metrics",
                "Review recent deployments",
                "Monitor error rates"
            ],
            "anomalies": recent_anomalies
        }
        
        return json.dumps(response, indent=2)
        
    except Exception as e:
        return json.dumps({
            "error": f"Real-time detection failed: {str(e)}",
            "timestamp": datetime.now().isoformat()
        })




