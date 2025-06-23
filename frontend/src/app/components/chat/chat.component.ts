import { FormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';
import { Component, OnInit, ViewChild, ElementRef, AfterViewChecked, OnDestroy } from '@angular/core';
import { ChatService, Message } from '../../services/chat.service';
import { Subscription } from 'rxjs';
import { StructuredDataViewerComponent } from '../structured-data-viewer/structured-data-viewer.component';

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
  imports: [CommonModule, FormsModule, StructuredDataViewerComponent],
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

  constructor(private chatService: ChatService) {}

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

    const message = this.userInput.trim();
    this.userInput = '';

    try {
      await this.chatService.sendMessage(message);
    } catch (error) {
      console.error('Error sending message:', error);
    }
  }

  startQuickAction(action: QuickAction): void {
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
        return 'bg-green-500 text-white';
      case 'active':
        return 'bg-blue-500 text-white';
      case 'pending':
        return 'bg-gray-200 text-gray-600';
      default:
        return 'bg-gray-200 text-gray-600';
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
    // Update workflow based on actual agent usage
    const hasDetector = this.messages.some(m => m.agent === 'detector');
    const hasPlanner = this.messages.some(m => m.agent === 'planner');
    const hasActionRecommender = this.messages.some(m => m.agent === 'action_recommender');
    const hasFixer = this.messages.some(m => m.agent === 'fixer');
    const hasNotifier = this.messages.some(m => m.agent === 'notifier');

    this.phases[0].status = hasDetector ? 'completed' : 'pending';
    this.phases[1].status = hasDetector ? 'completed' : 'pending'; // Classify is also detector
    this.phases[2].status = hasPlanner ? 'completed' : (hasDetector ? 'active' : 'pending');
    this.phases[3].status = hasActionRecommender ? 'completed' : (hasPlanner ? 'active' : 'pending');
    this.phases[4].status = hasFixer ? 'completed' : (hasActionRecommender ? 'active' : 'pending');
    this.phases[5].status = hasNotifier ? 'completed' : (hasFixer ? 'active' : 'pending');
  }
} 