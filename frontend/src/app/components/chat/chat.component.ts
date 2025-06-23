import { FormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';
import { Component, OnInit, ViewChild, ElementRef, AfterViewChecked, OnDestroy } from '@angular/core';
import { ChatService, Message } from '../../services/chat.service';
import { Subscription } from 'rxjs';
import { GoogleAdkService } from '../../services/google-adk.service';
import { MarkdownPipe } from '../../pipes/markdown.pipe';

interface QuickAction {
  title: string;
  description: string;
  prompt: string;
  agent: string;
  icon: string;
}

interface WorkflowPhase {
  id: string;
  name: string;
  description: string;
  icon: string;
  status: 'completed' | 'active' | 'pending';
  number: number;
}

@Component({
  standalone: true,
  imports: [CommonModule, FormsModule, MarkdownPipe],
  selector: 'app-chat',
  templateUrl: './chat.component.html',
  styleUrls: ['./chat.component.scss']
})
export class ChatComponent implements OnInit, AfterViewChecked, OnDestroy {
  @ViewChild('messagesContainer') private messagesContainer!: ElementRef;

  messages: Message[] = [];
  userInput: string = '';
  isLoading: boolean = false;
  showWorkflowTracker: boolean = true;
  private subscriptions: Subscription[] = [];

  phases: WorkflowPhase[] = [
    {
      id: 'analyze',
      name: 'Analyze',
      description: 'AI analyzes error, warning, and critical logs',
      icon: '🔍',
      status: 'pending',
      number: 1
    },
    {
      id: 'classify',
      name: 'Classify',
      description: 'Classify incidents by severity and impact',
      icon: '📊',
      status: 'pending',
      number: 2
    },
    {
      id: 'plan',
      name: 'Plan',
      description: 'Generate response strategies and action plans',
      icon: '📋',
      status: 'pending',
      number: 3
    },
    {
      id: 'recommend',
      name: 'Recommend',
      description: 'Suggest specific fixes and solutions',
      icon: '🛠️',
      status: 'pending',
      number: 4
    },
    {
      id: 'execute',
      name: 'Execute',
      description: 'Apply fixes with safety checks',
      icon: '⚡',
      status: 'pending',
      number: 5
    },
    {
      id: 'notify',
      name: 'Notify',
      description: 'Alert teams and stakeholders',
      icon: '📢',
      status: 'pending',
      number: 6
    }
  ];

  quickActions: QuickAction[] = [
    {
      title: 'Analyze Error Logs',
      description: 'Start AI analysis of recent error logs',
      prompt: 'Analyze the recent error logs and identify any patterns or anomalies that need attention.',
      agent: 'detector',
      icon: '🔍'
    },
    {
      title: 'Classify Incident',
      description: 'Classify a new incident based on log data',
      prompt: 'Classify this incident based on the log data provided. Determine severity, impact, and urgency.',
      agent: 'detector',
      icon: '📊'
    },
    {
      title: 'Generate Fix Plan',
      description: 'Create a response plan for detected issues',
      prompt: 'Based on the log analysis, create a detailed response plan with step-by-step actions.',
      agent: 'planner',
      icon: '📋'
    },
    {
      title: 'Recommend Fixes',
      description: 'Get specific fix recommendations',
      prompt: 'Analyze the logs and recommend specific fixes for the identified issues.',
      agent: 'action_recommender',
      icon: '🛠️'
    },
    {
      title: 'Correlate Logs',
      description: 'Find related logs across services',
      prompt: 'Correlate these logs across different services to identify related issues and dependencies.',
      agent: 'detector',
      icon: '🔗'
    },
    {
      title: 'Performance Review',
      description: 'Analyze performance patterns',
      prompt: 'Analyze the performance patterns in these logs and identify any bottlenecks or optimization opportunities.',
      agent: 'detector',
      icon: '📈'
    }
  ];

  constructor(private chatService: ChatService, private googleAdkService: GoogleAdkService) {}

  ngOnInit(): void {
    this.subscriptions.push(
      this.chatService.messages$.subscribe(messages => {
        this.messages = messages;
        this.updateWorkflowProgress();
      })
    );

    this.subscriptions.push(
      this.chatService.isLoading$.subscribe(isLoading => {
        this.isLoading = isLoading;
      })
    );
  }

  ngOnDestroy(): void {
    this.subscriptions.forEach(sub => sub.unsubscribe());
  }

  ngAfterViewChecked(): void {
    this.scrollToBottom();
  }

  async sendMessage(): Promise<void> {
    if (!this.userInput.trim() || this.isLoading) return;
    const input = this.userInput.trim();
    this.userInput = '';
    await this.chatService.sendMessage(input);
  }

  startQuickAction(action: QuickAction): void {
    if (this.isLoading) return;
    this.userInput = action.prompt;
    this.sendMessage();
  }

  onEnterPress(event: KeyboardEvent): void {
    if (event.key === 'Enter' && !event.shiftKey) {
      event.preventDefault();
      this.sendMessage();
    }
  }

  toggleWorkflowTracker(): void {
    this.showWorkflowTracker = !this.showWorkflowTracker;
  }

  trackByMessage(index: number, message: Message): number {
    return index;
  }

  getPhaseStatusClass(status: string): string {
    switch (status) {
      case 'completed':
        return 'bg-green-100 text-green-600';
      case 'active':
        return 'bg-blue-100 text-blue-600';
      default:
        return 'bg-gray-100 text-gray-600';
    }
  }

  getConfidenceColor(confidence: number): string {
    if (confidence >= 0.8) return 'text-green-600';
    if (confidence >= 0.6) return 'text-yellow-600';
    return 'text-red-600';
  }

  formatConfidence(confidence: number): string {
    return `${Math.round(confidence * 100)}%`;
  }

  private scrollToBottom(): void {
    try {
      this.messagesContainer.nativeElement.scrollTop = this.messagesContainer.nativeElement.scrollHeight;
    } catch (err) {}
  }

  private updateWorkflowProgress(): void {
    // Reset all phases to pending
    this.phases.forEach(phase => phase.status = 'pending');

    // Update phase status based on messages
    let lastActivePhase = '';
    this.messages.forEach(message => {
      if (message.agent) {
        const phase = this.getPhaseForAgent(message.agent);
        if (phase) {
          if (lastActivePhase && lastActivePhase !== phase.id) {
            const lastPhase = this.phases.find(p => p.id === lastActivePhase);
            if (lastPhase) lastPhase.status = 'completed';
          }
          const currentPhase = this.phases.find(p => p.id === phase.id);
          if (currentPhase) currentPhase.status = 'active';
          lastActivePhase = phase.id;
        }
      }
    });
  }

  private getPhaseForAgent(agent: string): WorkflowPhase | null {
    const agentPhaseMap: { [key: string]: string } = {
      'detector': 'analyze',
      'enhanced_detector': 'analyze',
      'planner': 'plan',
      'action_recommender': 'recommend',
      'fixer': 'execute',
      'notifier': 'notify'
    };

    const phaseId = agentPhaseMap[agent];
    return phaseId ? this.phases.find(p => p.id === phaseId) || null : null;
  }

  getTableKeys(data: any[]): string[] {
    return data && data.length ? Object.keys(data[0]) : [];
  }
} 