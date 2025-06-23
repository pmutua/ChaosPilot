import { Component, OnInit, OnDestroy } from '@angular/core';
import { CommonModule } from '@angular/common';
import { AiStateService, AutonomousWorkflow, IntelligentInsight, AgentState } from '../../services/ai-state.service';
import { Subscription } from 'rxjs';

@Component({
  selector: 'app-autonomous-monitor',
  standalone: true,
  imports: [CommonModule],
  template: `
    <div class="p-6 bg-gray-50 min-h-screen">
      <h1 class="text-3xl font-bold text-gray-900 mb-6">🤖 Autonomous Monitoring</h1>
      
      <!-- Control Panel -->
      <div class="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
        <div class="bg-white rounded-lg shadow p-6">
          <h3 class="text-lg font-semibold mb-4">Autonomous Mode</h3>
          <button 
            (click)="toggleAutonomousMode()"
            class="w-full px-4 py-2 rounded-lg font-medium transition-colors"
            [class]="autonomousMode ? 'bg-blue-600 text-white' : 'bg-gray-200 text-gray-700'"
          >
            {{ autonomousMode ? 'Enabled' : 'Disabled' }}
          </button>
        </div>
        
        <div class="bg-white rounded-lg shadow p-6">
          <h3 class="text-lg font-semibold mb-4">Active Workflows</h3>
          <div class="text-3xl font-bold text-blue-600">{{ getActiveWorkflows().length }}</div>
        </div>
        
        <div class="bg-white rounded-lg shadow p-6">
          <h3 class="text-lg font-semibold mb-4">Success Rate</h3>
          <div class="text-3xl font-bold text-green-600">{{ getWorkflowSuccessRate() }}%</div>
        </div>
        
        <div class="bg-white rounded-lg shadow p-6">
          <h3 class="text-lg font-semibold mb-4">Insights</h3>
          <div class="text-3xl font-bold text-purple-600">{{ intelligentInsights.length }}</div>
        </div>
      </div>

      <!-- Autonomous Workflows -->
      <div class="bg-white rounded-lg shadow mb-8">
        <div class="p-6 border-b">
          <h3 class="text-lg font-semibold">Autonomous Workflows</h3>
        </div>
        <div class="p-6">
          <div class="space-y-4">
            <div *ngFor="let workflow of autonomousWorkflows" class="border rounded-lg p-4">
              <div class="flex justify-between items-start mb-2">
                <div>
                  <h4 class="font-medium">{{ workflow.name }}</h4>
                  <p class="text-sm text-gray-600">{{ workflow.description }}</p>
                </div>
                <span class="px-2 py-1 rounded text-sm" [class]="getStatusColor(workflow.status)">
                  {{ workflow.status }}
                </span>
              </div>
              <p class="text-sm text-gray-600">{{ workflow.reasoning }}</p>
            </div>
          </div>
        </div>
      </div>

      <!-- Intelligent Insights -->
      <div class="bg-white rounded-lg shadow">
        <div class="p-6 border-b">
          <h3 class="text-lg font-semibold">Intelligent Insights</h3>
        </div>
        <div class="p-6">
          <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            <div *ngFor="let insight of intelligentInsights" class="border rounded-lg p-4">
              <div class="flex items-start space-x-2 mb-2">
                <span class="text-lg">{{ getInsightIcon(insight.type) }}</span>
                <div class="flex-1">
                  <h4 class="font-medium">{{ insight.title }}</h4>
                  <p class="text-sm text-gray-600">{{ insight.description }}</p>
                </div>
              </div>
              <div class="flex items-center space-x-2">
                <span class="px-2 py-1 rounded text-xs" [class]="getSeverityColor(insight.severity)">
                  {{ insight.severity }}
                </span>
                <span class="text-xs text-gray-500">{{ insight.confidence }}% confidence</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  `
})
export class AutonomousMonitorComponent implements OnInit, OnDestroy {
  autonomousMode = true;
  autonomousWorkflows: AutonomousWorkflow[] = [];
  intelligentInsights: IntelligentInsight[] = [];
  agentStates: AgentState[] = [];

  private subscriptions: Subscription[] = [];

  constructor(private aiStateService: AiStateService) {}

  ngOnInit(): void {
    this.subscriptions.push(
      this.aiStateService.autonomousMode$.subscribe(mode => this.autonomousMode = mode),
      this.aiStateService.autonomousWorkflows$.subscribe(workflows => this.autonomousWorkflows = workflows),
      this.aiStateService.intelligentInsights$.subscribe(insights => this.intelligentInsights = insights),
      this.aiStateService.agentStates$.subscribe(states => this.agentStates = Array.from(states.values()))
    );
  }

  ngOnDestroy(): void {
    this.subscriptions.forEach(sub => sub.unsubscribe());
  }

  toggleAutonomousMode(): void {
    this.aiStateService.toggleAutonomousMode();
  }

  getActiveWorkflows(): AutonomousWorkflow[] {
    return this.autonomousWorkflows.filter(w => w.status !== 'resolved');
  }

  getWorkflowSuccessRate(): number {
    const resolved = this.autonomousWorkflows.filter(w => w.status === 'resolved').length;
    const total = this.autonomousWorkflows.length;
    return total > 0 ? Math.round((resolved / total) * 100) : 0;
  }

  getStatusColor(status: string): string {
    const colors: { [key: string]: string } = {
      'monitoring': 'bg-blue-100 text-blue-800',
      'detected': 'bg-yellow-100 text-yellow-800',
      'analyzing': 'bg-purple-100 text-purple-800',
      'acting': 'bg-orange-100 text-orange-800',
      'resolved': 'bg-green-100 text-green-800'
    };
    return colors[status] || 'bg-gray-100 text-gray-800';
  }

  getInsightIcon(type: string): string {
    const icons: { [key: string]: string } = {
      'pattern': '🔍',
      'anomaly': '⚠️',
      'trend': '📈',
      'prediction': '🔮',
      'recommendation': '💡'
    };
    return icons[type] || '📋';
  }

  getSeverityColor(severity: string): string {
    const colors: { [key: string]: string } = {
      'low': 'bg-blue-100 text-blue-800',
      'medium': 'bg-yellow-100 text-yellow-800',
      'high': 'bg-orange-100 text-orange-800',
      'critical': 'bg-red-100 text-red-800'
    };
    return colors[severity] || 'bg-gray-100 text-gray-800';
  }
} 