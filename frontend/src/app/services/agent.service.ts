import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { environment } from '../../environments/environment';
import { ADKRequest, ADKResponse, ADKSession } from './adk-interfaces';
import { BehaviorSubject, Observable } from 'rxjs';
import { v4 as uuidv4 } from 'uuid';

@Injectable({
  providedIn: 'root'
})
export class AgentService {
  private apiUrl = environment.apiUrl
  private appName = 'agent_manager';
  private userId = `u_${uuidv4().slice(0, 8)}`;
  private sessionId = `s_${uuidv4().slice(0, 8)}`;
  private sessionInitialized = false;
  private analysisInProgress = new BehaviorSubject<boolean>(false);
  analysisInProgress$ = this.analysisInProgress.asObservable();

  constructor(private http: HttpClient) {
    // Initialize session when service is created
    this.initializeSession();
  }

  private async initializeSession() {
    if (this.sessionInitialized) return;
    
    try {
      // First, create the session explicitly
      const response = await this.http.post<ADKSession>(
        `${this.apiUrl}/apps/${this.appName}/users/${this.userId}/sessions/${this.sessionId}`,
        {
          state: {
            initialized: true,
            timestamp: new Date().toISOString()
          }
        }
      ).toPromise();

      console.log('Session initialized successfully:', response);
      this.sessionInitialized = true;
    } catch (error: any) {
      console.error('Failed to initialize session:', error);
      // If session exists, mark as initialized
      if (error.error?.detail?.includes('Session already exists')) {
        this.sessionInitialized = true;
      } else {
        throw error;
      }
    }
  }

  // Public method to ensure session is initialized
  public async ensureSession(): Promise<void> {
    if (!this.sessionInitialized) {
      await this.initializeSession();
    }
  }

  public getSessionInfo() {
    return {
      appName: this.appName,
      userId: this.userId,
      sessionId: this.sessionId,
      isInitialized: this.sessionInitialized
    };
  }

  async startAnalysis(): Promise<ADKResponse[]> {
    try {
      this.analysisInProgress.next(true);
      
      // Ensure we have a valid session
      await this.ensureSession();

      // Prepare the request payload
      const request: ADKRequest = {
        appName: this.appName,
        userId: this.userId,
        sessionId: this.sessionId,
        newMessage: {
          role: 'user',
          parts: [{
            text: 'Start system analysis'
          }]
        }
      };

      // Send the analysis request
      const response = await this.http.post<ADKResponse[]>(
        `${this.apiUrl}/run`,
        request
      ).toPromise();

      return response || [];
    } catch (error) {
      console.error('Analysis error:', error);
      throw error;
    } finally {
      this.analysisInProgress.next(false);
    }
  }

  // Method to send a message using the run endpoint
  async sendMessage(message: string): Promise<ADKResponse[]> {
    await this.ensureSession();

    const request: ADKRequest = {
      appName: this.appName,
      userId: this.userId,
      sessionId: this.sessionId,
      newMessage: {
        role: 'user',
        parts: [{
          text: message
        }]
      }
    };

    const response = await this.http.post<ADKResponse[]>(
      `${this.apiUrl}/run`,
      request
    ).toPromise();

    return response || [];
  }

  getAnalysisStatus(): Observable<boolean> {
    return this.analysisInProgress$;
  }
} 