import { Component, OnInit, OnDestroy } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Router, RouterModule } from '@angular/router';
import { AiStateService, AgentState, AutonomousWorkflow, IntelligentInsight } from '../../services/ai-state.service';
import { Subscription } from 'rxjs';
import { AgentService } from '../../services/agent.service';

interface SystemMetric {
  name: string;
  value: string;
  status: 'healthy' | 'warning' | 'critical';
  change: string;
  icon: string;
}

interface RecentIncident {
  id: string;
  title: string;
  severity: 'low' | 'medium' | 'high' | 'critical';
  status: 'resolved' | 'investigating' | 'mitigated';
  timestamp: Date;
  agent: string;
}

interface AgentPerformance {
  name: string;
  icon: string;
  successRate: number;
  avgResponseTime: number;
  totalRuns: number;
  status: 'online' | 'offline' | 'degraded';
}

interface MetricCard {
  title: string;
  value: string | number;
  change: string;
  changeType: 'positive' | 'negative' | 'neutral';
  icon: string;
  color: string;
}

interface RecentActivity {
  id: string;
  type: 'analysis' | 'incident' | 'fix' | 'alert';
  title: string;
  description: string;
  timestamp: Date;
  agent: string;
  severity?: 'low' | 'medium' | 'high' | 'critical';
}

@Component({
  selector: 'app-dashboard',
  standalone: true,
  imports: [CommonModule, RouterModule],
  templateUrl: './dashboard.component.html',
  styleUrls: ['./dashboard.component.scss']
})
export class DashboardComponent implements OnInit, OnDestroy {
  systemMetrics: SystemMetric[] = [
    {
      name: 'Log Volume',
      value: '2.4M',
      status: 'healthy',
      change: '+12%',
      icon: '📊'
    },
    {
      name: 'Error Rate',
      value: '0.8%',
      status: 'healthy',
      change: '-0.3%',
      icon: '⚠️'
    },
    {
      name: 'Critical Alerts',
      value: '3',
      status: 'warning',
      change: '+1',
      icon: '🚨'
    },
    {
      name: 'Auto-Resolved',
      value: '87%',
      status: 'healthy',
      change: '+5%',
      icon: '✅'
    }
  ];

  recentIncidents: RecentIncident[] = [
    {
      id: 'LOG-001',
      title: 'Database connection timeout errors',
      severity: 'high',
      status: 'resolved',
      timestamp: new Date(Date.now() - 2 * 60 * 60 * 1000), // 2 hours ago
      agent: 'detector'
    },
    {
      id: 'LOG-002',
      title: 'API rate limiting warnings',
      severity: 'medium',
      status: 'investigating',
      timestamp: new Date(Date.now() - 30 * 60 * 1000), // 30 minutes ago
      agent: 'detector'
    },
    {
      id: 'LOG-003',
      title: 'Memory leak detected in service',
      severity: 'critical',
      status: 'mitigated',
      timestamp: new Date(Date.now() - 6 * 60 * 60 * 1000), // 6 hours ago
      agent: 'action_recommender'
    }
  ];

  agentPerformance: AgentPerformance[] = [
    {
      name: 'Log Analyzer',
      icon: '🔍',
      successRate: 99.2,
      avgResponseTime: 2.3,
      totalRuns: 156,
      status: 'online'
    },
    {
      name: 'Response Planner',
      icon: '📋',
      successRate: 98.5,
      avgResponseTime: 3.2,
      totalRuns: 67,
      status: 'online'
    },
    {
      name: 'Fix Recommender',
      icon: '🛠️',
      successRate: 96.9,
      avgResponseTime: 4.1,
      totalRuns: 34,
      status: 'online'
    },
    {
      name: 'Auto-Fixer',
      icon: '⚡',
      successRate: 99.8,
      avgResponseTime: 1.1,
      totalRuns: 203,
      status: 'online'
    },
    {
      name: 'Alert Manager',
      icon: '📢',
      successRate: 99.5,
      avgResponseTime: 0.8,
      totalRuns: 145,
      status: 'online'
    }
  ];

  quickActions = [
    {
      title: 'Analyze Logs',
      description: 'Start AI-powered log analysis',
      icon: '🔍',
      route: '/chat',
      color: 'bg-blue-500'
    },
    {
      title: 'View Errors',
      description: 'Browse recent error logs',
      icon: '⚠️',
      route: '/chat',
      color: 'bg-red-500'
    },
    {
      title: 'Incident Report',
      description: 'Generate incident summary',
      icon: '📋',
      route: '/chat',
      color: 'bg-green-500'
    },
    {
      title: 'Performance Review',
      description: 'Analyze system performance',
      icon: '📊',
      route: '/history',
      color: 'bg-purple-500'
    }
  ];

  metrics: MetricCard[] = [
    {
      title: 'Total Errors',
      value: '1,247',
      change: '+12%',
      changeType: 'negative',
      icon: '🚨',
      color: 'bg-red-500'
    },
    {
      title: 'Active Incidents',
      value: '3',
      change: '-2',
      changeType: 'positive',
      icon: '⚠️',
      color: 'bg-yellow-500'
    },
    {
      title: 'Auto-Fixes Applied',
      value: '89',
      change: '+15',
      changeType: 'positive',
      icon: '⚡',
      color: 'bg-green-500'
    },
    {
      title: 'System Uptime',
      value: '99.8%',
      change: '+0.2%',
      changeType: 'positive',
      icon: '📈',
      color: 'bg-blue-500'
    }
  ];

  recentActivities: any[] = [];
  performanceTrends: any[] = [];

  agentStates: AgentState[] = [];
  autonomousWorkflows: AutonomousWorkflow[] = [];
  intelligentInsights: IntelligentInsight[] = [];
  autonomousMode = true;
  proactiveMonitoring = true;
  
  // Performance metrics
  systemHealth = 95;
  responseTime = 245;
  errorRate = 0.2;
  activeIncidents = 2;

  private subscriptions: Subscription[] = [];

  constructor(private aiStateService: AiStateService, private router: Router, private agentService: AgentService) {}

  ngOnInit(): void {
    this.initializeSubscriptions();
    this.generateSampleData();
  }

  ngOnDestroy(): void {
    this.subscriptions.forEach(sub => sub.unsubscribe());
  }

  private initializeSubscriptions(): void {
    this.subscriptions.push(
      this.aiStateService.agentStates$.subscribe(states => {
        this.agentStates = Array.from(states.values());
      }),
      
      this.aiStateService.autonomousWorkflows$.subscribe(workflows => {
        this.autonomousWorkflows = workflows;
      }),
      
      this.aiStateService.intelligentInsights$.subscribe(insights => {
        this.intelligentInsights = insights;
      }),
      
      this.aiStateService.autonomousMode$.subscribe(mode => {
        this.autonomousMode = mode;
      }),
      
      this.aiStateService.proactiveMonitoring$.subscribe(monitoring => {
        this.proactiveMonitoring = monitoring;
      })
    );
  }

  private generateSampleData(): void {
    // Generate sample recent activities
    this.recentActivities = [
      {
        id: 1,
        type: 'incident_detected',
        title: 'Database Connection Issues Detected',
        description: 'Multiple database connection timeouts detected in us-central1 region',
        timestamp: new Date(Date.now() - 5 * 60 * 1000),
        severity: 'high',
        agent: 'Intelligent Detector',
        status: 'investigating'
      },
      {
        id: 2,
        type: 'action_executed',
        title: 'Automated Remediation Executed',
        description: 'Successfully restarted database connection pool',
        timestamp: new Date(Date.now() - 3 * 60 * 1000),
        severity: 'info',
        agent: 'Automated Fixer',
        status: 'completed'
      },
      {
        id: 3,
        type: 'insight_generated',
        title: 'Performance Trend Identified',
        description: 'Response times trending upward, suggesting resource scaling needed',
        timestamp: new Date(Date.now() - 10 * 60 * 1000),
        severity: 'warning',
        agent: 'Strategic Planner',
        status: 'monitoring'
      },
      {
        id: 4,
        type: 'notification_sent',
        title: 'Stakeholder Notification',
        description: 'Sent incident update to on-call team and management',
        timestamp: new Date(Date.now() - 2 * 60 * 1000),
        severity: 'info',
        agent: 'Smart Notifier',
        status: 'completed'
      }
    ];

    // Generate sample performance trends
    this.performanceTrends = [
      { time: '00:00', cpu: 45, memory: 60, response: 180 },
      { time: '02:00', cpu: 52, memory: 65, response: 195 },
      { time: '04:00', cpu: 48, memory: 62, response: 190 },
      { time: '06:00', cpu: 55, memory: 68, response: 210 },
      { time: '08:00', cpu: 68, memory: 75, response: 245 },
      { time: '10:00', cpu: 72, memory: 78, response: 280 },
      { time: '12:00', cpu: 75, memory: 82, response: 320 },
      { time: '14:00', cpu: 78, memory: 85, response: 350 },
      { time: '16:00', cpu: 82, memory: 88, response: 380 },
      { time: '18:00', cpu: 85, memory: 90, response: 420 },
      { time: '20:00', cpu: 88, memory: 92, response: 450 },
      { time: '22:00', cpu: 85, memory: 89, response: 410 }
    ];
  }

  // Utility methods
  getActivityIcon(activity: any): string {
    const iconMap: { [key: string]: string } = {
      'incident_detected': '🔍',
      'action_executed': '⚡',
      'insight_generated': '💡',
      'notification_sent': '📢',
      'automated_fix': '🤖',
      'manual_intervention': '👤'
    };
    return iconMap[activity.type] || '📋';
  }

  getActivityColor(activity: any): string {
    const colorMap: { [key: string]: string } = {
      'critical': 'text-red-600',
      'high': 'text-orange-600',
      'medium': 'text-yellow-600',
      'low': 'text-blue-600',
      'info': 'text-green-600'
    };
    return colorMap[activity.severity] || 'text-gray-600';
  }

  getStatusColor(status: string): string {
    const colorMap: { [key: string]: string } = {
      'completed': 'bg-green-100 text-green-800',
      'investigating': 'bg-blue-100 text-blue-800',
      'monitoring': 'bg-yellow-100 text-yellow-800',
      'failed': 'bg-red-100 text-red-800',
      'pending': 'bg-gray-100 text-gray-800'
    };
    return colorMap[status] || 'bg-gray-100 text-gray-800';
  }

  getSeverityColor(severity: string): string {
    const colorMap: { [key: string]: string } = {
      'critical': 'bg-red-500',
      'high': 'bg-orange-500',
      'medium': 'bg-yellow-500',
      'low': 'bg-blue-500',
      'info': 'bg-green-500'
    };
    return colorMap[severity] || 'bg-gray-500';
  }

  getAgentStatusColor(status: string): string {
    const colorMap: { [key: string]: string } = {
      'idle': 'bg-gray-100 text-gray-600',
      'thinking': 'bg-blue-100 text-blue-600',
      'working': 'bg-yellow-100 text-yellow-600',
      'completed': 'bg-green-100 text-green-600',
      'error': 'bg-red-100 text-red-600'
    };
    return colorMap[status] || 'bg-gray-100 text-gray-600';
  }

  getWorkflowStatusColor(status: string): string {
    const colorMap: { [key: string]: string } = {
      'monitoring': 'bg-blue-100 text-blue-800',
      'detected': 'bg-yellow-100 text-yellow-800',
      'analyzing': 'bg-purple-100 text-purple-800',
      'acting': 'bg-orange-100 text-orange-800',
      'resolved': 'bg-green-100 text-green-800'
    };
    return colorMap[status] || 'bg-gray-100 text-gray-800';
  }

  getInsightTypeIcon(type: string): string {
    const iconMap: { [key: string]: string } = {
      'pattern': '🔍',
      'anomaly': '⚠️',
      'trend': '📈',
      'prediction': '🔮',
      'recommendation': '💡'
    };
    return iconMap[type] || '📋';
  }

  formatTimestamp(timestamp: Date): string {
    const now = new Date();
    const diff = now.getTime() - timestamp.getTime();
    const minutes = Math.floor(diff / (1000 * 60));
    const hours = Math.floor(diff / (1000 * 60 * 60));
    
    if (minutes < 1) return 'Just now';
    if (minutes < 60) return `${minutes}m ago`;
    if (hours < 24) return `${hours}h ago`;
    return timestamp.toLocaleDateString();
  }

  formatDuration(minutes: number): string {
    if (minutes < 60) return `${minutes}m`;
    const hours = Math.floor(minutes / 60);
    const remainingMinutes = minutes % 60;
    return `${hours}h ${remainingMinutes}m`;
  }

  // Autonomous features
  toggleAutonomousMode(): void {
    this.aiStateService.toggleAutonomousMode();
  }

  toggleProactiveMonitoring(): void {
    this.aiStateService.toggleProactiveMonitoring();
  }

  // Performance calculations
  getSystemHealthColor(): string {
    if (this.systemHealth >= 90) return 'text-green-600';
    if (this.systemHealth >= 75) return 'text-yellow-600';
    return 'text-red-600';
  }

  getResponseTimeColor(): string {
    if (this.responseTime <= 200) return 'text-green-600';
    if (this.responseTime <= 400) return 'text-yellow-600';
    return 'text-red-600';
  }

  getErrorRateColor(): string {
    if (this.errorRate <= 0.1) return 'text-green-600';
    if (this.errorRate <= 0.5) return 'text-yellow-600';
    return 'text-red-600';
  }

  // Agent performance
  getActiveAgents(): AgentState[] {
    return this.agentStates.filter(agent => 
      agent.status === 'thinking' || agent.status === 'working'
    );
  }

  getCompletedAgents(): AgentState[] {
    return this.agentStates.filter(agent => agent.status === 'completed');
  }

  getAgentEfficiency(): number {
    const completed = this.getCompletedAgents().length;
    const total = this.agentStates.length;
    return total > 0 ? Math.round((completed / total) * 100) : 0;
  }

  // Autonomous workflow metrics
  getActiveWorkflows(): AutonomousWorkflow[] {
    return this.autonomousWorkflows.filter(workflow => 
      workflow.status !== 'resolved'
    );
  }

  getResolvedWorkflows(): AutonomousWorkflow[] {
    return this.autonomousWorkflows.filter(workflow => 
      workflow.status === 'resolved'
    );
  }

  getWorkflowSuccessRate(): number {
    const resolved = this.getResolvedWorkflows().length;
    const total = this.autonomousWorkflows.length;
    return total > 0 ? Math.round((resolved / total) * 100) : 0;
  }

  // Intelligent insights metrics
  getCriticalInsights(): IntelligentInsight[] {
    return this.intelligentInsights.filter(insight => 
      insight.severity === 'critical' || insight.severity === 'error'
    );
  }

  getActionableInsights(): IntelligentInsight[] {
    return this.intelligentInsights.filter(insight => insight.actionable);
  }

  getInsightDistribution(): { [key: string]: number } {
    const distribution: { [key: string]: number } = {};
    this.intelligentInsights.forEach(insight => {
      distribution[insight.type] = (distribution[insight.type] || 0) + 1;
    });
    return distribution;
  }

  // Performance trends
  getLatestPerformanceMetrics(): any {
    return this.performanceTrends[this.performanceTrends.length - 1];
  }

  getPerformanceTrend(): 'improving' | 'stable' | 'degrading' {
    const recent = this.performanceTrends.slice(-3);
    const avgResponse = recent.reduce((sum, point) => sum + point.response, 0) / recent.length;
    const previous = this.performanceTrends.slice(-6, -3);
    const prevAvgResponse = previous.reduce((sum, point) => sum + point.response, 0) / previous.length;
    
    if (avgResponse < prevAvgResponse - 20) return 'improving';
    if (avgResponse > prevAvgResponse + 20) return 'degrading';
    return 'stable';
  }

  getTrendColor(): string {
    const trend = this.getPerformanceTrend();
    const colorMap: { [key: string]: string } = {
      'improving': 'text-green-600',
      'stable': 'text-blue-600',
      'degrading': 'text-red-600'
    };
    return colorMap[trend] || 'text-gray-600';
  }

  getTrendIcon(): string {
    const trend = this.getPerformanceTrend();
    const iconMap: { [key: string]: string } = {
      'improving': '↗️',
      'stable': '→',
      'degrading': '↘️'
    };
    return iconMap[trend] || '→';
  }

  // Quick actions
  triggerManualAnalysis(): void {
    console.log('Triggering manual analysis...');
    this.agentService.runAgentWithPayload({
      newMessage: {
        role: 'user',
        parts: [
          { text: 'Use the detector agent to: Analyze the latest logs for anomalies' }
        ]
      }
    })
      .then(response => {
        console.log('Analysis started:', response);
        // TODO: Update component state to reflect that analysis is running
      })
      .catch(error => {
        console.error('Failed to start analysis:', error);
      });
  }

  viewDetailedReport(): void {
    // Navigate to detailed report
    console.log('Navigating to detailed report');
  }

  exportData(): void {
    // Export dashboard data
    console.log('Exporting dashboard data');
  }

  // Autonomous action handlers
  executeAutomatedAction(actionId: string): void {
    console.log(`Executing automated action: ${actionId}`);
  }

  approveManualAction(actionId: string): void {
    console.log(`Approving manual action: ${actionId}`);
  }

  dismissInsight(insightId: string): void {
    console.log(`Dismissing insight: ${insightId}`);
  }

  // Real-time updates simulation
  simulateRealTimeUpdate(): void {
    // Simulate real-time metric updates
    this.systemHealth = Math.max(85, Math.min(98, this.systemHealth + (Math.random() - 0.5) * 5));
    this.responseTime = Math.max(150, Math.min(500, this.responseTime + (Math.random() - 0.5) * 20));
    this.errorRate = Math.max(0, Math.min(2, this.errorRate + (Math.random() - 0.5) * 0.1));
  }

  navigateToAction(route: string): void {
    this.router.navigate([route]);
  }

  formatTime(timestamp: Date): string {
    const now = new Date();
    const seconds = Math.floor((now.getTime() - timestamp.getTime()) / 1000);

    let interval = seconds / 31536000;
    if (interval > 1) {
      return Math.floor(interval) + " years ago";
    }
    interval = seconds / 2592000;
    if (interval > 1) {
      return Math.floor(interval) + " months ago";
    }
    interval = seconds / 86400;
    if (interval > 1) {
      return Math.floor(interval) + " days ago";
    }
    interval = seconds / 3600;
    if (interval > 1) {
      return Math.floor(interval) + " hours ago";
    }
    interval = seconds / 60;
    if (interval > 1) {
      return Math.floor(interval) + " minutes ago";
    }
    return Math.floor(seconds) + " seconds ago";
  }

  getStatusBadgeClass(status: 'resolved' | 'investigating' | 'mitigated'): string {
    const baseClasses = 'px-2 py-1 rounded-full text-xs font-medium';
    switch (status) {
      case 'resolved':
        return `${baseClasses} bg-green-100 text-green-800`;
      case 'investigating':
        return `${baseClasses} bg-yellow-100 text-yellow-800`;
      case 'mitigated':
        return `${baseClasses} bg-blue-100 text-blue-800`;
      default:
        return `${baseClasses} bg-gray-100 text-gray-800`;
    }
  }
} 