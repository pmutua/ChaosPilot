import { Injectable } from '@angular/core';
import { v4 as uuidv4 } from 'uuid';

@Injectable({ providedIn: 'root' })
export class SessionService {
  private sessionId: string;

  constructor() {
    this.sessionId = localStorage.getItem('sessionId') || uuidv4();
    localStorage.setItem('sessionId', this.sessionId);
  }

  getSessionId(): string {
    return this.sessionId;
  }
} 