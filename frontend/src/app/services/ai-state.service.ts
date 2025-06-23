import { Injectable } from '@angular/core';
import { BehaviorSubject, Observable, interval, timer } from 'rxjs';
import { map, switchMap, tap } from 'rxjs/operators';

export interface AgentState {
  id: string;
  name: string;
  status: 'idle' | 'thinking' | 'working' | 'completed' | 'error';
  progress: number;
  message: string;
  data?: any;
  confidence?: number;
  tools?: string[];
  timestamp: Date;
  autonomous?: boolean;
  reasoning?: string;
  nextActions?: string[];
}

export interface AutonomousWorkflow {
  id: string;
  name: string;
  description: string;
  status: 'monitoring' | 'detected' | 'analyzing' | 'acting' | 'resolved';
  priority: 'low' | 'medium' | 'high' | 'critical';
  confidence: number;
  detectedAt: Date;
  resolvedAt?: Date;
  actions: AutonomousAction[];
  reasoning: string;
}

export interface AutonomousAction {
  id: string;
  name: string;
  type: 'automated' | 'semi_automated' | 'manual';
  status: 'pending' | 'executing' | 'completed' | 'failed';
  description: string;
  reasoning: string;
  successProbability: number;
  estimatedTime: string;
  executedAt?: Date;
  result?: any;
}

export interface IntelligentInsight {
  id: string;
  type: 'pattern' | 'anomaly' | 'trend' | 'prediction' | 'recommendation';
  title: string;
  description: string;
  confidence: number;
  severity: 'info' | 'warning' | 'error' | 'critical';
  timestamp: Date;
  data?: any;
  actionable: boolean;
  actions?: string[];
}

@Injectable({
  providedIn: 'root'
})
export class AiStateService {
  private agentStatesSubject = new BehaviorSubject<Map<string, AgentState>>(new Map());
  private autonomousWorkflowsSubject = new BehaviorSubject<AutonomousWorkflow[]>([]);
  private intelligentInsightsSubject = new BehaviorSubject<IntelligentInsight[]>([]);
  private autonomousModeSubject = new BehaviorSubject<boolean>(true);
  private proactiveMonitoringSubject = new BehaviorSubject<boolean>(true);

  public agentStates$ = this.agentStatesSubject.asObservable();
  public autonomousWorkflows$ = this.autonomousWorkflowsSubject.asObservable();
  public intelligentInsights$ = this.intelligentInsightsSubject.asObservable();
  public autonomousMode$ = this.autonomousModeSubject.asObservable();
  public proactiveMonitoring$ = this.proactiveMonitoringSubject.asObservable();

  private autonomousWorkflows: AutonomousWorkflow[] = [];
  private intelligentInsights: IntelligentInsight[] = [];
  private monitoringInterval?: any;

  constructor() {
    this.initializeAutonomousFeatures();
  }

  private initializeAutonomousFeatures(): void {
    // Start proactive monitoring
    this.startProactiveMonitoring();
    
    // Initialize autonomous workflows
    this.initializeAutonomousWorkflows();
    
    // Start intelligent insights generation
    this.startIntelligentInsights();
  }

  // Enhanced Agent State Management
  updateAgentState(agentId: string, updates: Partial<AgentState>): void {
    const currentStates = this.agentStatesSubject.value;
    const currentState = currentStates.get(agentId) || this.createDefaultAgentState(agentId);
    
    const updatedState: AgentState = {
      ...currentState,
      ...updates,
      timestamp: new Date()
    };

    // Add intelligent reasoning for autonomous agents
    if (updates.status === 'thinking' && this.autonomousModeSubject.value) {
      updatedState.reasoning = this.generateReasoning(agentId, updates.data);
      updatedState.nextActions = this.predictNextActions(agentId, updates.data);
    }

    currentStates.set(agentId, updatedState);
    this.agentStatesSubject.next(new Map(currentStates));

    // Trigger autonomous workflows if needed
    this.checkAutonomousTriggers(updatedState);
  }

  private createDefaultAgentState(agentId: string): AgentState {
    return {
      id: agentId,
      name: this.getAgentDisplayName(agentId),
      status: 'idle',
      progress: 0,
      message: 'Ready for analysis',
      timestamp: new Date(),
      autonomous: true
    };
  }

  private getAgentDisplayName(agentId: string): string {
    const nameMap: { [key: string]: string } = {
      'detector': 'Intelligent Detector',
      'planner': 'Strategic Planner',
      'action_recommender': 'Action Recommender',
      'fixer': 'Automated Fixer',
      'notifier': 'Smart Notifier'
    };
    return nameMap[agentId] || agentId;
  }

  private generateReasoning(agentId: string, data?: any): string {
    const reasoningTemplates: { [key: string]: string[] } = {
      'detector': [
        "Analyzing log patterns to identify anomalies and correlations...",
        "Detecting performance degradation patterns and security threats...",
        "Correlating events across multiple services to identify root causes...",
        "Evaluating system health metrics and identifying potential issues..."
      ],
      'planner': [
        "Creating comprehensive incident response plan with automated actions...",
        "Prioritizing actions based on business impact and resource availability...",
        "Developing escalation procedures and communication strategies...",
        "Planning proactive measures to prevent future incidents..."
      ],
      'action_recommender': [
        "Recommending intelligent actions with high success probability...",
        "Identifying automated remediation opportunities...",
        "Prioritizing actions based on impact and effort analysis...",
        "Suggesting preventive measures and monitoring improvements..."
      ],
      'fixer': [
        "Executing automated fixes with rollback capabilities...",
        "Implementing configuration changes and service restarts...",
        "Scaling resources and optimizing performance...",
        "Applying security patches and access controls..."
      ],
      'notifier': [
        "Preparing comprehensive incident notifications...",
        "Determining appropriate stakeholders and communication channels...",
        "Creating detailed status updates and progress reports...",
        "Coordinating with external teams and escalation procedures..."
      ]
    };

    const templates = reasoningTemplates[agentId] || ["Processing data and generating insights..."];
    return templates[Math.floor(Math.random() * templates.length)];
  }

  private predictNextActions(agentId: string, data?: any): string[] {
    const actionPredictions: { [key: string]: string[] } = {
      'detector': [
        "Generate detailed anomaly report",
        "Identify affected services and users",
        "Calculate confidence scores and impact assessment"
      ],
      'planner': [
        "Create incident response timeline",
        "Define escalation procedures",
        "Plan resource allocation and team coordination"
      ],
      'action_recommender': [
        "Prioritize automated actions",
        "Generate execution plan with dependencies",
        "Assess risks and success probabilities"
      ],
      'fixer': [
        "Execute automated remediation",
        "Monitor fix effectiveness",
        "Prepare rollback procedures if needed"
      ],
      'notifier': [
        "Send immediate alerts to stakeholders",
        "Create detailed incident report",
        "Schedule follow-up communications"
      ]
    };

    return actionPredictions[agentId] || ["Continue analysis", "Generate recommendations"];
  }

  // Autonomous Workflow Management
  private initializeAutonomousWorkflows(): void {
    const initialWorkflows: AutonomousWorkflow[] = [
      {
        id: 'auto-monitoring-001',
        name: 'Proactive System Monitoring',
        description: 'Continuously monitors system health and performance metrics',
        status: 'monitoring',
        priority: 'medium',
        confidence: 0.95,
        detectedAt: new Date(),
        actions: [],
        reasoning: 'Automated monitoring workflow to detect issues before they impact users'
      },
      {
        id: 'auto-security-001',
        name: 'Security Threat Detection',
        description: 'Monitors for security threats and suspicious activities',
        status: 'monitoring',
        priority: 'high',
        confidence: 0.90,
        detectedAt: new Date(),
        actions: [],
        reasoning: 'Proactive security monitoring to identify and respond to threats quickly'
      }
    ];

    this.autonomousWorkflows = initialWorkflows;
    this.autonomousWorkflowsSubject.next(this.autonomousWorkflows);
  }

  private checkAutonomousTriggers(agentState: AgentState): void {
    // Check if agent state triggers autonomous workflows
    if (agentState.status === 'completed' && agentState.data) {
      this.triggerAutonomousWorkflow(agentState);
    }
  }

  private triggerAutonomousWorkflow(agentState: AgentState): void {
    const workflow: AutonomousWorkflow = {
      id: `auto-${agentState.id}-${Date.now()}`,
      name: `Autonomous ${agentState.name} Response`,
      description: `Automated response to ${agentState.name} analysis`,
      status: 'detected',
      priority: this.determinePriority(agentState.data),
      confidence: agentState.confidence || 0.8,
      detectedAt: new Date(),
      actions: this.generateAutonomousActions(agentState),
      reasoning: `Automatically triggered based on ${agentState.name} analysis results`
    };

    this.autonomousWorkflows.push(workflow);
    this.autonomousWorkflowsSubject.next([...this.autonomousWorkflows]);

    // Execute autonomous actions
    this.executeAutonomousActions(workflow);
  }

  private determinePriority(data?: any): 'low' | 'medium' | 'high' | 'critical' {
    if (!data) return 'medium';
    
    // Analyze data to determine priority
    const severity = data.severity || data.priority || 'medium';
    return severity as 'low' | 'medium' | 'high' | 'critical';
  }

  private generateAutonomousActions(agentState: AgentState): AutonomousAction[] {
    const actions: AutonomousAction[] = [];

    switch (agentState.id) {
      case 'detector':
        if (agentState.data?.anomalies?.length > 0) {
          actions.push({
            id: `action-${Date.now()}-1`,
            name: 'Investigate Anomalies',
            type: 'automated',
            status: 'pending',
            description: 'Automatically investigate detected anomalies',
            reasoning: 'Anomalies detected require immediate investigation',
            successProbability: 0.85,
            estimatedTime: '5 minutes'
          });
        }
        break;

      case 'planner':
        if (agentState.data?.recommended_actions?.length > 0) {
          actions.push({
            id: `action-${Date.now()}-2`,
            name: 'Execute High-Priority Actions',
            type: 'semi_automated',
            status: 'pending',
            description: 'Execute high-priority actions from response plan',
            reasoning: 'High-priority actions identified for immediate execution',
            successProbability: 0.90,
            estimatedTime: '10 minutes'
          });
        }
        break;

      case 'action_recommender':
        if (agentState.data?.automated_actions?.length > 0) {
          actions.push({
            id: `action-${Date.now()}-3`,
            name: 'Execute Automated Remediation',
            type: 'automated',
            status: 'pending',
            description: 'Execute automated remediation actions',
            reasoning: 'Automated actions available for immediate execution',
            successProbability: 0.95,
            estimatedTime: '3 minutes'
          });
        }
        break;
    }

    return actions;
  }

  private async executeAutonomousActions(workflow: AutonomousWorkflow): Promise<void> {
    for (const action of workflow.actions) {
      if (action.type === 'automated') {
        action.status = 'executing';
        this.updateAutonomousWorkflow(workflow.id);

        // Simulate action execution
        await this.simulateActionExecution(action);

        action.status = 'completed';
        action.executedAt = new Date();
        action.result = { success: true, message: 'Action executed successfully' };
        this.updateAutonomousWorkflow(workflow.id);
      }
    }

    // Update workflow status
    workflow.status = 'resolved';
    workflow.resolvedAt = new Date();
    this.updateAutonomousWorkflow(workflow.id);
  }

  private async simulateActionExecution(action: AutonomousAction): Promise<void> {
    const executionTime = parseInt(action.estimatedTime) * 1000 || 5000;
    await new Promise(resolve => setTimeout(resolve, executionTime));
  }

  private updateAutonomousWorkflow(workflowId: string): void {
    const index = this.autonomousWorkflows.findIndex(w => w.id === workflowId);
    if (index !== -1) {
      this.autonomousWorkflows[index] = { ...this.autonomousWorkflows[index] };
      this.autonomousWorkflowsSubject.next([...this.autonomousWorkflows]);
    }
  }

  // Proactive Monitoring
  private startProactiveMonitoring(): void {
    if (this.monitoringInterval) {
      clearInterval(this.monitoringInterval);
    }

    this.monitoringInterval = setInterval(() => {
      if (this.proactiveMonitoringSubject.value) {
        this.performProactiveMonitoring();
      }
    }, 30000); // Check every 30 seconds
  }

  private performProactiveMonitoring(): void {
    // Simulate proactive monitoring checks
    const monitoringChecks = [
      this.checkSystemHealth(),
      this.checkPerformanceMetrics(),
      this.checkSecurityStatus(),
      this.checkResourceUtilization()
    ];

    Promise.all(monitoringChecks).then(results => {
      results.forEach(result => {
        if (result.insight) {
          this.addIntelligentInsight(result.insight);
        }
      });
    });
  }

  private async checkSystemHealth(): Promise<{ insight?: IntelligentInsight }> {
    // Simulate system health check
    const healthScore = Math.random();
    
    if (healthScore < 0.7) {
      return {
        insight: {
          id: `insight-${Date.now()}-1`,
          type: 'anomaly',
          title: 'System Health Degradation',
          description: 'System health metrics indicate potential issues',
          confidence: 0.85,
          severity: 'warning',
          timestamp: new Date(),
          actionable: true,
          actions: ['Investigate system metrics', 'Check service status']
        }
      };
    }
    return {};
  }

  private async checkPerformanceMetrics(): Promise<{ insight?: IntelligentInsight }> {
    // Simulate performance check
    const responseTime = Math.random() * 1000;
    
    if (responseTime > 800) {
      return {
        insight: {
          id: `insight-${Date.now()}-2`,
          type: 'trend',
          title: 'Performance Degradation Trend',
          description: 'Response times are trending upward',
          confidence: 0.80,
          severity: 'warning',
          timestamp: new Date(),
          actionable: true,
          actions: ['Scale resources', 'Optimize queries']
        }
      };
    }
    return {};
  }

  private async checkSecurityStatus(): Promise<{ insight?: IntelligentInsight }> {
    // Simulate security check
    const securityScore = Math.random();
    
    if (securityScore < 0.8) {
      return {
        insight: {
          id: `insight-${Date.now()}-3`,
          type: 'pattern',
          title: 'Security Pattern Detected',
          description: 'Unusual access patterns detected',
          confidence: 0.75,
          severity: 'error',
          timestamp: new Date(),
          actionable: true,
          actions: ['Review access logs', 'Enhance monitoring']
        }
      };
    }
    return {};
  }

  private async checkResourceUtilization(): Promise<{ insight?: IntelligentInsight }> {
    // Simulate resource check
    const cpuUsage = Math.random() * 100;
    const memoryUsage = Math.random() * 100;
    
    if (cpuUsage > 80 || memoryUsage > 85) {
      return {
        insight: {
          id: `insight-${Date.now()}-4`,
          type: 'prediction',
          title: 'Resource Utilization Warning',
          description: 'High resource utilization may lead to performance issues',
          confidence: 0.90,
          severity: 'warning',
          timestamp: new Date(),
          actionable: true,
          actions: ['Scale resources', 'Optimize processes']
        }
      };
    }
    return {};
  }

  // Intelligent Insights Management
  private startIntelligentInsights(): void {
    // Generate initial insights
    this.generateInitialInsights();
    
    // Set up periodic insight generation
    interval(60000).subscribe(() => {
      if (this.autonomousModeSubject.value) {
        this.generateIntelligentInsights();
      }
    });
  }

  private generateInitialInsights(): void {
    const initialInsights: IntelligentInsight[] = [
      {
        id: 'insight-initial-1',
        type: 'recommendation',
        title: 'Enable Automated Monitoring',
        description: 'Recommendation to enable automated monitoring for better incident detection',
        confidence: 0.95,
        severity: 'info',
        timestamp: new Date(),
        actionable: true,
        actions: ['Enable monitoring', 'Configure alerts']
      },
      {
        id: 'insight-initial-2',
        type: 'pattern',
        title: 'Peak Usage Patterns',
        description: 'Identified peak usage patterns that may require resource scaling',
        confidence: 0.85,
        severity: 'info',
        timestamp: new Date(),
        actionable: true,
        actions: ['Implement auto-scaling', 'Optimize resource allocation']
      }
    ];

    this.intelligentInsights = initialInsights;
    this.intelligentInsightsSubject.next(this.intelligentInsights);
  }

  private generateIntelligentInsights(): void {
    // Generate new insights based on current state
    const newInsights: IntelligentInsight[] = [];
    
    // Analyze agent states for insights
    const agentStates = Array.from(this.agentStatesSubject.value.values());
    const activeAgents = agentStates.filter(agent => agent.status === 'working');
    
    if (activeAgents.length > 2) {
      newInsights.push({
        id: `insight-${Date.now()}-5`,
        type: 'pattern',
        title: 'High Agent Activity',
        description: 'Multiple agents are actively working, indicating complex incident',
        confidence: 0.80,
        severity: 'warning',
        timestamp: new Date(),
        actionable: true,
        actions: ['Prioritize incidents', 'Allocate resources']
      });
    }

    // Add new insights
    newInsights.forEach(insight => this.addIntelligentInsight(insight));
  }

  private addIntelligentInsight(insight: IntelligentInsight): void {
    this.intelligentInsights.unshift(insight);
    
    // Keep only recent insights
    if (this.intelligentInsights.length > 20) {
      this.intelligentInsights = this.intelligentInsights.slice(0, 20);
    }
    
    this.intelligentInsightsSubject.next([...this.intelligentInsights]);
  }

  // Public API Methods
  toggleAutonomousMode(): void {
    const currentMode = this.autonomousModeSubject.value;
    this.autonomousModeSubject.next(!currentMode);
    
    if (!currentMode) {
      this.startProactiveMonitoring();
    } else if (this.monitoringInterval) {
      clearInterval(this.monitoringInterval);
    }
  }

  toggleProactiveMonitoring(): void {
    const currentMode = this.proactiveMonitoringSubject.value;
    this.proactiveMonitoringSubject.next(!currentMode);
  }

  getAgentState(agentId: string): AgentState | undefined {
    return this.agentStatesSubject.value.get(agentId);
  }

  getAllAgentStates(): AgentState[] {
    return Array.from(this.agentStatesSubject.value.values());
  }

  getAutonomousWorkflows(): AutonomousWorkflow[] {
    return this.autonomousWorkflows;
  }

  getIntelligentInsights(): IntelligentInsight[] {
    return this.intelligentInsights;
  }

  clearAgentStates(): void {
    this.agentStatesSubject.next(new Map());
  }

  clearAutonomousWorkflows(): void {
    this.autonomousWorkflows = [];
    this.autonomousWorkflowsSubject.next([]);
  }

  clearIntelligentInsights(): void {
    this.intelligentInsights = [];
    this.intelligentInsightsSubject.next([]);
  }

  // Cleanup
  ngOnDestroy(): void {
    if (this.monitoringInterval) {
      clearInterval(this.monitoringInterval);
    }
  }
}