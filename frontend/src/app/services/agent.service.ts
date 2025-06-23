import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders, HttpErrorResponse } from '@angular/common/http';
import { Observable, throwError } from 'rxjs';
import { catchError, map } from 'rxjs/operators';

export interface ADKMessage {
  role: 'user' | 'model';
  parts: Array<{
    text?: string;
    functionCall?: any;
    functionResponse?: any;
  }>;
}

export interface ADKRunRequest {
  newMessage: ADKMessage;
}

export interface ADKEvent {
  content: {
    parts: Array<{
      text?: string;
      functionCall?: any;
      functionResponse?: any;
    }>;
    role: string;
  };
  invocationId: string;
  author: string;
  actions: {
    stateDelta: any;
    artifactDelta: any;
    requestedAuthConfigs: any;
  };
  longRunningToolIds: string[];
  id: string;
  timestamp: number;
}

export interface ADKSession {
  id: string;
  appName: string;
  userId: string;
  state: any;
  events: any[];
  lastUpdateTime: number;
}

@Injectable({
  providedIn: 'root'
})
export class AgentService {
  private baseUrl = 'http://localhost:8000';
  private currentUserId = 'chaospilot_user';
  private currentSessionId = 'chaospilot_session';
  private appName = 'agent_manager';

  constructor(private http: HttpClient) {}

  async runAgentWithPayload(payload: { newMessage: { role: string; parts: { text: string }[] } }): Promise<any> {
    // Only send the payload as provided
    try {
      const response = await this.http.post<ADKEvent[]>(`${this.baseUrl}/run`, payload).toPromise();
      if (response) {
        return this.processADKResponse(response, payload.newMessage.role);
      } else {
        return { result: 'No response from agent' };
      }
    } catch (error) {
      console.error('Error running agent:', error);
      throw error;
    }
  }

  async runAgent(agentName: string, userInput: string): Promise<any> {
    // Legacy method for backward compatibility
    const request: ADKRunRequest = {
      newMessage: {
        role: 'user',
        parts: [{
          text: `Use the ${agentName} agent to: ${userInput}`
        }]
      }
    } as any; // Remove appName, userId, sessionId
    try {
      const response = await this.http.post<ADKEvent[]>(`${this.baseUrl}/run`, request).toPromise();
      if (response) {
        return this.processADKResponse(response, agentName);
      } else {
        return { result: 'No response from agent' };
      }
    } catch (error) {
      console.error('Error running agent:', error);
      throw error;
    }
  }

  async runAgentStreamingWithPayload(payload: { newMessage: { role: string; parts: { text: string }[] } }): Promise<Observable<ADKEvent>> {
    // Only send the payload as provided
    const request = {
      ...payload,
      streaming: false
    };
    return this.http.post<ADKEvent>(`${this.baseUrl}/run_sse`, request).pipe(
      catchError(error => {
        console.error('Error in streaming agent:', error);
        return throwError(error);
      })
    );
  }

  private processADKResponse(events: ADKEvent[], agentName: string): any {
    if (!events || events.length === 0) {
      return { result: 'No response from agent' };
    }

    // Find the final text response
    const finalEvent = events.find(event => 
      event.content.parts.some(part => part.text) && 
      event.author === agentName
    );

    if (finalEvent) {
      const textPart = finalEvent.content.parts.find(part => part.text);
      return {
        result: textPart?.text || 'No text response',
        events: events,
        agent: agentName,
        timestamp: finalEvent.timestamp
      };
    }

    // If no text response, return the last event
    const lastEvent = events[events.length - 1];
    return {
      result: JSON.stringify(lastEvent),
      events: events,
      agent: agentName,
      timestamp: lastEvent.timestamp
    };
  }

  // Helper method to get session info
  async getSessionInfo(): Promise<ADKSession | null> {
    try {
      const sessionUrl = `${this.baseUrl}/apps/${this.appName}/users/${this.currentUserId}/sessions/${this.currentSessionId}`;
      const session = await this.http.get<ADKSession>(sessionUrl).toPromise();
      return session || null;
    } catch (error) {
      console.error('Error getting session info:', error);
      return null;
    }
  }

  // Helper method to delete session
  async deleteSession(): Promise<void> {
    const sessionUrl = `${this.baseUrl}/apps/${this.appName}/users/${this.currentUserId}/sessions/${this.currentSessionId}`;
    await this.http.delete(sessionUrl).toPromise();
  }
} 