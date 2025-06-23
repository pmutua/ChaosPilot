import { Injectable } from '@angular/core';

@Injectable({ providedIn: 'root' })
export class FeedbackService {
  private apiBase = 'http://localhost:8000';

  async submitFeedback(feedback: any): Promise<any> {
    const response = await fetch(`${this.apiBase}/feedback`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(feedback)
    });
    if (!response.ok) {
      const errorText = await response.text();
      throw new Error(`Feedback submission failed: ${errorText}`);
    }
    return await response.json();
  }

  async getFeedback(agentName: string): Promise<any[]> {
    const response = await fetch(`${this.apiBase}/feedback/${agentName}`);
    if (!response.ok) {
      const errorText = await response.text();
      throw new Error(`Failed to fetch feedback: ${errorText}`);
    }
    return await response.json();
  }
} 