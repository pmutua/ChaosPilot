import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { BehaviorSubject, Observable } from 'rxjs';
import { ADKMessage, ADKRequest, ADKResponse, ADKSession } from './adk-interfaces';

const API_BASE_URL = 'http://localhost:8000';
const APP_NAME = 'agent_manager';
const USER_ID = 'chaospilot_user';
const SESSION_STORAGE_KEY = 'adk_sessions';

@Injectable({ providedIn: 'root' })
export class GoogleAdkService {
  private currentSession$ = new BehaviorSubject<ADKSession | null>(null);
  private loading$ = new BehaviorSubject<boolean>(false);
  private sessions$ = new BehaviorSubject<ADKSession[]>([]);

  constructor(private http: HttpClient) {
    this.restoreSessions();
  }

  get currentSession(): Observable<ADKSession | null> { return this.currentSession$.asObservable(); }
  get loading(): Observable<boolean> { return this.loading$.asObservable(); }
  get sessions(): Observable<ADKSession[]> { return this.sessions$.asObservable(); }

  private restoreSessions() {
    const sessions = JSON.parse(localStorage.getItem(SESSION_STORAGE_KEY) || '[]');
    this.sessions$.next(sessions);
    if (sessions.length > 0) {
      this.currentSession$.next(sessions[0]);
    }
  }

  private persistSessions() {
    localStorage.setItem(SESSION_STORAGE_KEY, JSON.stringify(this.sessions$.getValue()));
  }

  private getOrCreateSessionId(): string {
    let sessionId = localStorage.getItem('adk_session_id');
    if (!sessionId) {
      sessionId = this.generateSessionId();
      localStorage.setItem('adk_session_id', sessionId);
    }
    return sessionId;
  }

  private generateSessionId(): string {
    return 'sess-' + Math.random().toString(36).substr(2, 9);
  }

  private addOrUpdateSession(session: ADKSession): void {
    const sessions = this.sessions$.getValue();
    const idx = sessions.findIndex(s => s.id === session.id);
    if (idx >= 0) {
      sessions[idx] = { ...sessions[idx], ...session };
    } else {
      sessions.unshift(session);
    }
    this.sessions$.next(sessions);
    this.currentSession$.next(sessions[0]);
    this.persistSessions();
  }

  private updateSessionWithMessage(sessionId: string, message: ADKMessage, response: ADKResponse): void {
    const sessions = this.sessions$.getValue();
    const idx = sessions.findIndex(s => s.id === sessionId);
    if (idx >= 0) {
      sessions[idx].messages = sessions[idx].messages || [];
      sessions[idx].messages.push({ ...message, timestamp: Date.now(), response });
      this.sessions$.next(sessions);
      this.persistSessions();
    }
  }

  private handleError(error: any): void {
    // Add user-friendly error handling here
    console.error('GoogleAdkService error:', error);
  }

  // --- OpenAPI-compliant methods below ---

  async createOrResumeSession(state: any = {}): Promise<ADKSession> {
    const sessionId = this.getOrCreateSessionId();
    const url = `${API_BASE_URL}/apps/${APP_NAME}/users/${USER_ID}/sessions/${sessionId}`;
    const payload = { state };
    try {
      const session = await this.http.post<ADKSession>(url, payload).toPromise();
      if (!session) throw new Error('Session creation failed');
      this.addOrUpdateSession(session);
      return session;
    } catch (error: any) {
      // Extra logging for debugging
      console.error('Session creation error:', {
        error,
        sessionId,
        appName: APP_NAME,
        url,
        payload
      });
      // If session already exists, fetch it instead
      if (error.status === 400 && error.error?.detail?.includes('Session already exists')) {
        const existing = await this.http.get<ADKSession>(url).toPromise();
        if (!existing) throw new Error('Session exists but could not be fetched');
        this.addOrUpdateSession(existing);
        return existing;
      }
      this.handleError(error);
      throw error;
    }
  }

  async sendMessage(message: ADKMessage): Promise<ADKResponse> {
    this.loading$.next(true);
    const sessionId = this.getOrCreateSessionId();
    const payload: ADKRequest = {
      appName: APP_NAME,
      userId: USER_ID,
      sessionId,
      newMessage: message
    };
    try {
      await this.createOrResumeSession();
      const response = await this.http.post<ADKResponse>(`${API_BASE_URL}/run`, payload).toPromise();
      if (!response) throw new Error('No response from agent');
      this.updateSessionWithMessage(sessionId, message, response);
      return response;
    } catch (error) {
      this.handleError(error);
      throw error;
    } finally {
      this.loading$.next(false);
    }
  }

  async getSessionInfo(): Promise<ADKSession> {
    const sessionId = this.getOrCreateSessionId();
    const url = `${API_BASE_URL}/apps/${APP_NAME}/users/${USER_ID}/sessions/${sessionId}`;
    const session = await this.http.get<ADKSession>(url).toPromise();
    if (!session) throw new Error('Session not found');
    return session;
  }

  async listSessions(): Promise<ADKSession[]> {
    const url = `${API_BASE_URL}/apps/${APP_NAME}/users/${USER_ID}/sessions`;
    const result = await this.http.get<ADKSession[]>(url).toPromise();
    return result ?? [];
  }

  async deleteSession(sessionId: string): Promise<void> {
    const url = `${API_BASE_URL}/apps/${APP_NAME}/users/${USER_ID}/sessions/${sessionId}`;
    await this.http.delete(url).toPromise();
    // Remove from local state
    const sessions = this.sessions$.getValue().filter(s => s.id !== sessionId);
    this.sessions$.next(sessions);
    if (this.currentSession$.getValue()?.id === sessionId) {
      this.currentSession$.next(sessions[0] || null);
    }
    this.persistSessions();
  }

  switchToSession(sessionId: string): void {
    const session = this.sessions$.getValue().find(s => s.id === sessionId) || null;
    this.currentSession$.next(session);
  }

  endCurrentSession(): void {
    const sessions = this.sessions$.getValue();
    const current = this.currentSession$.getValue();
    if (current) {
      const updated = sessions.filter(s => s.id !== current.id);
      this.sessions$.next(updated);
      this.currentSession$.next(updated[0] || null);
      this.persistSessions();
    }
  }
} 