import { Component, Input, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';

interface AgentMeta {
  name: string;
  key: string;
  icon: string;
  description: string;
  status: 'online' | 'offline';
}

interface WorkflowPhase {
  id: string;
  name: string;
  description: string;
  icon: string;
  status: string;
  agents: string[];
}

@Component({
  standalone: true,
  imports: [CommonModule],
  selector: 'app-workflow-tracker',
  templateUrl: './workflow-tracker.component.html',
  styleUrls: ['./workflow-tracker.component.scss']
})
export class WorkflowTrackerComponent {
  @Input() agentMeta: AgentMeta[] = [];
  @Input() currentAgent: string = '';

  phases: WorkflowPhase[] = [
    {
      id: 'analyze',
      name: 'Analyze',
      description: 'AI analyzes error, warning, and critical logs',
      icon: '🔍',
      status: 'completed',
      agents: ['log_analyzer']
    },
    {
      id: 'classify',
      name: 'Classify',
      description: 'Classify incidents by severity and impact',
      icon: '📊',
      status: 'active',
      agents: ['incident_classifier']
    },
    {
      id: 'plan',
      name: 'Plan',
      description: 'Generate response strategies and action plans',
      icon: '📋',
      status: 'pending',
      agents: ['response_planner']
    },
    {
      id: 'recommend',
      name: 'Recommend',
      description: 'Suggest specific fixes and solutions',
      icon: '🛠️',
      status: 'pending',
      agents: ['fix_recommender']
    },
    {
      id: 'execute',
      name: 'Execute',
      description: 'Apply fixes with safety checks',
      icon: '⚡',
      status: 'pending',
      agents: ['auto_fixer']
    },
    {
      id: 'notify',
      name: 'Notify',
      description: 'Alert teams and stakeholders',
      icon: '📢',
      status: 'pending',
      agents: ['alert_manager']
    }
  ];

  isActive(agentKey: string): boolean {
    return this.currentAgent === agentKey;
  }

  isCompleted(agentKey: string): boolean {
    if (!this.currentAgent) return false;
    const currentIndex = this.agentMeta.findIndex(a => a.key === this.currentAgent);
    const phaseIndex = this.agentMeta.findIndex(a => a.key === agentKey);
    return phaseIndex < currentIndex;
  }
}