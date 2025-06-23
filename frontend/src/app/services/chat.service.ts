import { Injectable } from '@angular/core';
import { BehaviorSubject, Observable } from 'rxjs';
import { AgentService } from './agent.service';
import { ADKResponse, ADKMessagePart, ADKActions } from './adk-interfaces';

export interface Message {
  role: 'user' | 'assistant' | 'thinking' | 'transfer' | 'error';
  content: string;
  agent?: string;
  timestamp: Date;
  structuredData?: any;
  confidence?: number;
  toolsUsed?: string[];
  showRawData?: boolean;
}

@Injectable({
  providedIn: 'root'
})
export class ChatService {
  public messages$ = new BehaviorSubject<Message[]>([]);
  public aiResponse$ = new BehaviorSubject<string>('');
  public isLoading$ = new BehaviorSubject<boolean>(false);
  public currentAgent$ = new BehaviorSubject<string>('');

  private agentWorkflow = [
    { name: 'detector', displayName: 'Log Analyzer', icon: '🔍' },
    { name: 'planner', displayName: 'Response Planner', icon: '📋' },
    { name: 'action_recommender', displayName: 'Fix Recommender', icon: '🛠️' },
    { name: 'fixer', displayName: 'Auto-Fixer', icon: '⚡' },
    { name: 'notifier', displayName: 'Alert Manager', icon: '📢' }
  ];

  constructor(private agentService: AgentService) {}

  async initSession(): Promise<void> {
    try {
      this.isLoading$.next(true);
      await this.agentService.ensureSession();
    } catch (err: any) {
      console.error('Session initialization failed:', err);
      this.addMessage('error', 'Error: Could not start a session with the backend.');
    } finally {
      this.isLoading$.next(false);
    }
  }

  async sendMessage(userInput: string, agent?: string): Promise<void> {
    this.isLoading$.next(true);

    const userMessage: Message = {
      role: 'user',
      content: userInput,
      timestamp: new Date()
    };
    this.messages$.next([...this.messages$.getValue(), userMessage]);

    try {
      await this.agentService.ensureSession();
      const response = await this.agentService.sendMessage(userInput);
      
      if (Array.isArray(response)) {
        response.forEach((adkResp: any) => {
          if (adkResp.content && Array.isArray(adkResp.content.parts)) {
            adkResp.content.parts.forEach((part: any) => {
              if (typeof part.text === 'string') {
                // Check for JSON code block
                const jsonMatch = part.text.match(/```json\n([\s\S]*?)```/);
                let structuredData = undefined;
                if (jsonMatch) {
                  try {
                    structuredData = JSON.parse(jsonMatch[1]);
                  } catch {}
                }
                this.addMessage(
                  'assistant',
                  part.text,
                  adkResp.author,
                  structuredData,
                  undefined,
                  undefined,
                  new Date(adkResp.timestamp * 1000)
                );
              } else if (part.functionCall && part.functionCall.name) {
                this.addMessage(
                  'transfer',
                  `Transferring to ${part.functionCall.args?.agent_name || part.functionCall.name}...`,
                  adkResp.author,
                  undefined,
                  undefined,
                  undefined,
                  new Date(adkResp.timestamp * 1000)
                );
              } else if (part.functionResponse && part.functionResponse.name) {
                this.addMessage(
                  'transfer',
                  `Transfer to ${part.functionResponse.name.replace('transfer_to_', '')} complete.`,
                  adkResp.author,
                  undefined,
                  undefined,
                  undefined,
                  new Date(adkResp.timestamp * 1000)
                );
              } else if (part.functionResponse && part.functionResponse.response) {
                let structuredData = undefined;
                const result = part.functionResponse.response.result;
                if (typeof result === 'string' && result.trim().startsWith('[')) {
                  try {
                    structuredData = JSON.parse(result);
                  } catch {}
                }
                this.addMessage(
                  'assistant',
                  '', // No text, just structured data
                  adkResp.author,
                  structuredData,
                  undefined,
                  undefined,
                  new Date(adkResp.timestamp * 1000)
                );
              } else if (typeof part === 'object') {
                this.addMessage(
                  'assistant',
                  '',
                  adkResp.author,
                  part,
                  undefined,
                  undefined,
                  new Date(adkResp.timestamp * 1000)
                );
              }
            });
          }
        });
      }
    } catch (err: any) {
      console.error('Error processing message:', err);
      this.addMessage('error', `Error: ${err.message || 'Failed to process request'}`);
    } finally {
      this.isLoading$.next(false);
    }
  }

  private determineAgentFromInput(input: string): string {
    const lowerInput = input.toLowerCase();
    
    if (lowerInput.includes('analyze') || lowerInput.includes('log') || lowerInput.includes('error') || lowerInput.includes('detect')) {
      return 'detector';
    }
    if (lowerInput.includes('plan') || lowerInput.includes('strategy') || lowerInput.includes('recovery')) {
      return 'planner';
    }
    if (lowerInput.includes('recommend') || lowerInput.includes('action') || lowerInput.includes('fix')) {
      return 'action_recommender';
    }
    if (lowerInput.includes('execute') || lowerInput.includes('apply') || lowerInput.includes('run')) {
      return 'fixer';
    }
    if (lowerInput.includes('notify') || lowerInput.includes('alert') || lowerInput.includes('escalate')) {
      return 'notifier';
    }
    
    // Default to detector for general analysis
    return 'detector';
  }

  private parseAgentResponse(result: any, agentName: string): ADKResponse {
    let content = '';
    let structuredData = null;
    let confidence = null;
    let toolsUsed = [];

    // Handle ADK API response format
    if (result.events && Array.isArray(result.events)) {
      // Extract content from the final text response
      const textEvents = result.events.filter((event: any) => 
        event.content && event.content.parts && 
        event.content.parts.some((part: any) => part.text)
      );

      if (textEvents.length > 0) {
        const finalTextEvent = textEvents[textEvents.length - 1];
        const textPart = finalTextEvent.content.parts.find((part: any) => part.text);
        content = textPart?.text || result.result;
      } else {
        content = result.result;
      }

      // Extract function calls and responses for tools used
      const functionEvents = result.events.filter((event: any) => 
        event.content && event.content.parts && 
        event.content.parts.some((part: any) => part.functionCall || part.functionResponse)
      );

      functionEvents.forEach((event: any) => {
        event.content.parts.forEach((part: any) => {
          if (part.functionCall && part.functionCall.name) {
            toolsUsed.push(part.functionCall.name);
          }
        });
      });

      // Try to extract structured data from function responses
      const functionResponseEvents = result.events.filter((event: any) => 
        event.content && event.content.parts && 
        event.content.parts.some((part: any) => part.functionResponse)
      );

      if (functionResponseEvents.length > 0) {
        const lastFunctionResponse = functionResponseEvents[functionResponseEvents.length - 1];
        const responsePart = lastFunctionResponse.content.parts.find((part: any) => part.functionResponse);
        if (responsePart && responsePart.functionResponse.response) {
          try {
            structuredData = responsePart.functionResponse.response;
          } catch (e) {
            // If not JSON, use as is
            structuredData = responsePart.functionResponse.response;
          }
        }
      }
    } else {
      // Fallback to original parsing logic
      if (typeof result.result === 'string') {
        content = result.result;
        // Try to parse JSON from string
        try {
          structuredData = JSON.parse(result.result);
        } catch (e) {
          // Not JSON, use as plain text
        }
      } else if (result.result && typeof result.result === 'object') {
        structuredData = result.result;
        content = this.formatStructuredResponse(result.result, agentName);
      }
    }

    // Extract confidence and tools if available
    if (structuredData) {
      confidence = structuredData.confidence_score || structuredData.confidence || null;
      if (result.tools_used) {
        toolsUsed = result.tools_used;
      }
    }

    // Return a valid ADKResponse object
    return {
      content: { parts: [{ text: content || 'Analysis completed' }], role: 'model' },
      invocationId: '',
      author: agentName,
      actions: { stateDelta: {}, artifactDelta: {}, requestedAuthConfigs: {} },
      id: '',
      timestamp: Math.floor(Date.now() / 1000),
      longRunningToolIds: []
    };
  }

  private formatStructuredResponse(data: any, agentName: string): string {
    switch (agentName) {
      case 'detector':
        return this.formatDetectorResponse(data);
      case 'planner':
        return this.formatPlannerResponse(data);
      case 'action_recommender':
        return this.formatActionRecommenderResponse(data);
      default:
        return JSON.stringify(data, null, 2);
    }
  }

  private formatDetectorResponse(data: any): string {
    if (!data) return 'No analysis data available';
    
    let summary = `🔍 **Log Analysis Complete**\n\n`;
    
    if (data.total_error_logs !== undefined) {
      summary += `📊 **Total Errors**: ${data.total_error_logs}\n`;
    }
    
    if (data.errors_grouped_by_severity) {
      summary += `⚠️ **Severity Breakdown**:\n`;
      Object.entries(data.errors_grouped_by_severity).forEach(([severity, count]) => {
        summary += `   • ${severity}: ${count}\n`;
      });
    }
    
    if (data.recent_errors && data.recent_errors.length > 0) {
      summary += `🚨 **Recent Critical Issues**:\n`;
      data.recent_errors.slice(0, 3).forEach((error: any) => {
        summary += `   • ${error.failure_type} (${error.severity}) - ${error.region}\n`;
      });
    }
    
    if (data.confidence_score !== undefined) {
      summary += `\n🎯 **Confidence**: ${Math.round(data.confidence_score * 100)}%`;
    }
    
    return summary;
  }

  private formatPlannerResponse(data: any): string {
    if (!data) return 'No recovery plan available';
    
    let summary = `📋 **Recovery Plan Generated**\n\n`;
    
    if (data.summary) {
      summary += `📊 **Summary**:\n`;
      if (data.summary.critical_services_detected !== undefined) {
        summary += `   • Critical Services: ${data.summary.critical_services_detected ? 'Yes' : 'No'}\n`;
      }
      if (data.summary.total_error_events !== undefined) {
        summary += `   • Total Errors: ${data.summary.total_error_events}\n`;
      }
    }
    
    if (data.immediate_recovery_actions && data.immediate_recovery_actions.length > 0) {
      summary += `⚡ **Immediate Actions**:\n`;
      data.immediate_recovery_actions.slice(0, 3).forEach((action: any) => {
        summary += `   • ${action.action} (${action.urgency} priority)\n`;
      });
    }
    
    if (data.confidence_score !== undefined) {
      summary += `\n🎯 **Plan Confidence**: ${Math.round(data.confidence_score * 100)}%`;
    }
    
    return summary;
  }

  private formatActionRecommenderResponse(data: any): string {
    if (!data) return 'No action recommendations available';
    
    let summary = `🛠️ **Action Recommendations**\n\n`;
    
    if (data.recovery_tasks && data.recovery_tasks.length > 0) {
      summary += `📋 **Recommended Tasks**:\n`;
      data.recovery_tasks.slice(0, 3).forEach((task: any) => {
        summary += `   • ${task.description} (${task.priority} priority)\n`;
        if (task.estimated_time_minutes) {
          summary += `     ⏱️ Estimated time: ${task.estimated_time_minutes} minutes\n`;
        }
      });
    }
    
    return summary;
  }

  private getNextAgentInWorkflow(currentAgent: string): string | null {
    const currentIndex = this.agentWorkflow.findIndex(agent => agent.name === currentAgent);
    if (currentIndex >= 0 && currentIndex < this.agentWorkflow.length - 1) {
      return this.agentWorkflow[currentIndex + 1].name;
    }
    return null;
  }

  private getAgentDisplayName(agentName: string): string {
    const agent = this.agentWorkflow.find(a => a.name === agentName);
    return agent ? agent.displayName : agentName;
  }

  private addMessage(
    role: Message['role'], 
    content: string, 
    agent?: string, 
    structuredData?: any, 
    confidence?: number, 
    toolsUsed?: string[],
    timestamp?: Date
  ): void {
    const msg: Message = {
      role,
      content,
      agent: agent ?? '',
      timestamp: timestamp || new Date(),
      structuredData,
      confidence,
      toolsUsed
    };
    this.messages$.next([...this.messages$.getValue(), msg]);
  }

  clearMessages(): void {
    this.messages$.next([]);
  }

  getAgentWorkflow() {
    return this.agentWorkflow;
  }

  streamAgentResponseSSE(payload: any): Observable<any> {
    return new Observable(observer => {
      // Ensure session before making the request
      this.agentService.ensureSession().then(() => {
        const sessionInfo = this.agentService.getSessionInfo();
        const fullPayload = {
          ...sessionInfo,
          ...payload
        };

        fetch('http://localhost:8000/run', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(fullPayload)
        })
          .then(async response => {
            if (!response.ok) throw new Error('Network response was not ok');
            const data = await response.json();
            observer.next(data);
            observer.complete();
          })
          .catch(error => {
            observer.error(error);
          });
      }).catch(error => {
        observer.error(error);
      });
    });
  }
} 