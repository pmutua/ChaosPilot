import { Component, Input } from '@angular/core';
import { CommonModule } from '@angular/common';

@Component({
  standalone: true,
  imports: [CommonModule],
  selector: 'app-structured-data-viewer',
  template: `
    <div *ngIf="data" class="bg-white border border-gray-200 rounded-lg p-4 mt-3">
      <div class="flex items-center justify-between mb-3">
        <h4 class="text-sm font-medium text-gray-900">📊 Analysis Details</h4>
        <span *ngIf="confidence" 
              [class]="getConfidenceColor(confidence)"
              class="text-xs font-medium">
          {{ formatConfidence(confidence) }} confidence
        </span>
      </div>
      
      <!-- Detector Data -->
      <div *ngIf="agentName === 'detector'" class="space-y-3">
        <div *ngIf="data.total_error_logs !== undefined" class="flex justify-between items-center">
          <span class="text-sm text-gray-600">Total Error Logs:</span>
          <span class="text-sm font-medium">{{ data.total_error_logs }}</span>
        </div>
        
        <div *ngIf="data.errors_grouped_by_severity" class="space-y-2">
          <span class="text-sm text-gray-600">Severity Breakdown:</span>
          <div class="grid grid-cols-2 gap-2">
            <div *ngFor="let severity of getSeverityEntries(data.errors_grouped_by_severity)" 
                 class="flex justify-between items-center p-2 bg-gray-50 rounded">
              <span class="text-xs">{{ severity.key }}</span>
              <span class="text-xs font-medium">{{ severity.value }}</span>
            </div>
          </div>
        </div>
        
        <div *ngIf="data.recent_errors && data.recent_errors.length > 0" class="space-y-2">
          <span class="text-sm text-gray-600">Recent Critical Issues:</span>
          <div class="space-y-1">
            <div *ngFor="let error of data.recent_errors.slice(0, 3)" 
                 class="p-2 bg-red-50 rounded border-l-4 border-red-400">
              <div class="text-xs font-medium">{{ error.failure_type }}</div>
              <div class="text-xs text-gray-600">{{ error.severity }} - {{ error.region }}</div>
              <div class="text-xs text-gray-500">{{ formatTimestamp(error.timestamp) }}</div>
            </div>
          </div>
        </div>
      </div>
      
      <!-- Planner Data -->
      <div *ngIf="agentName === 'planner'" class="space-y-3">
        <div *ngIf="data.summary" class="space-y-2">
          <span class="text-sm text-gray-600">Summary:</span>
          <div class="grid grid-cols-2 gap-2">
            <div *ngIf="data.summary.critical_services_detected !== undefined" 
                 class="flex justify-between items-center p-2 bg-gray-50 rounded">
              <span class="text-xs">Critical Services:</span>
              <span class="text-xs font-medium">{{ data.summary.critical_services_detected ? 'Yes' : 'No' }}</span>
            </div>
            <div *ngIf="data.summary.total_error_events !== undefined" 
                 class="flex justify-between items-center p-2 bg-gray-50 rounded">
              <span class="text-xs">Total Errors:</span>
              <span class="text-xs font-medium">{{ data.summary.total_error_events }}</span>
            </div>
          </div>
        </div>
        
        <div *ngIf="data.immediate_recovery_actions && data.immediate_recovery_actions.length > 0" class="space-y-2">
          <span class="text-sm text-gray-600">Immediate Actions:</span>
          <div class="space-y-1">
            <div *ngFor="let action of data.immediate_recovery_actions.slice(0, 3)" 
                 class="p-2 bg-yellow-50 rounded border-l-4 border-yellow-400">
              <div class="text-xs font-medium">{{ action.action }}</div>
              <div class="text-xs text-gray-600">{{ action.urgency }} priority</div>
              <div class="text-xs text-gray-500">Risk: {{ action.risk_assessment }}</div>
            </div>
          </div>
        </div>
      </div>
      
      <!-- Action Recommender Data -->
      <div *ngIf="agentName === 'action_recommender'" class="space-y-3">
        <div *ngIf="data.recovery_tasks && data.recovery_tasks.length > 0" class="space-y-2">
          <span class="text-sm text-gray-600">Recommended Tasks:</span>
          <div class="space-y-1">
            <div *ngFor="let task of data.recovery_tasks.slice(0, 3)" 
                 class="p-2 bg-blue-50 rounded border-l-4 border-blue-400">
              <div class="text-xs font-medium">{{ task.description }}</div>
              <div class="text-xs text-gray-600">{{ task.priority }} priority</div>
              <div *ngIf="task.estimated_time_minutes" class="text-xs text-gray-500">
                ⏱️ {{ task.estimated_time_minutes }} minutes
              </div>
            </div>
          </div>
        </div>
      </div>
      
      <!-- Raw JSON Toggle -->
      <details class="mt-3 pt-3 border-t border-gray-100">
        <summary class="cursor-pointer text-xs text-gray-500 hover:text-gray-700">
          🔍 View Raw JSON
        </summary>
        <pre class="mt-2 p-2 bg-gray-50 rounded text-xs overflow-x-auto">{{ data | json }}</pre>
      </details>
    </div>
  `,
  styles: []
})
export class StructuredDataViewerComponent {
  @Input() data: any;
  @Input() agentName: string = '';
  @Input() confidence: number | null = null;

  getConfidenceColor(confidence: number): string {
    if (confidence >= 0.8) return 'text-green-600';
    if (confidence >= 0.6) return 'text-yellow-600';
    return 'text-red-600';
  }

  formatConfidence(confidence: number): string {
    return `${Math.round(confidence * 100)}%`;
  }

  getSeverityEntries(severityData: any): Array<{key: string, value: any}> {
    return Object.entries(severityData).map(([key, value]) => ({ key, value }));
  }

  formatTimestamp(timestamp: string): string {
    if (!timestamp) return '';
    try {
      const date = new Date(timestamp);
      return date.toLocaleString();
    } catch {
      return timestamp;
    }
  }
} 