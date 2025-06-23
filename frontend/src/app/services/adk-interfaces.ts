export interface ADKMessagePart {
  text?: string;
  functionCall?: {
    id: string;
    args: Record<string, any>;
    name: string;
  };
  functionResponse?: {
    id: string;
    name: string;
    response: {
      status: string;
      result?: any;
      report?: string;
    };
  };
}

export interface ADKMessage {
  role: 'user' | 'model';
  parts: ADKMessagePart[];
}

export interface ADKRequest {
  appName: string;
  userId: string;
  sessionId: string;
  newMessage: ADKMessage;
  streaming?: boolean;
}

export interface ADKActions {
  stateDelta: Record<string, any>;
  artifactDelta: Record<string, any>;
  requestedAuthConfigs: Record<string, any>;
  transferToAgent?: string;
}

export interface ADKResponse {
  content: {
    parts: ADKMessagePart[];
    role: 'model' | 'user';
  };
  invocationId: string;
  author: string;
  actions: ADKActions;
  longRunningToolIds?: string[];
  id: string;
  timestamp: number;
}

export interface ADKSession {
  id: string;
  sessionId: string;
  appName: string;
  userId: string;
  state: {
    state: Record<string, any>;
  };
  events: ADKResponse[];
  lastUpdateTime: number;
  messages?: any[];
}

export interface AgentAnalysisResult {
  responses: ADKResponse[];
  status: 'running' | 'completed' | 'error';
  startTime: number;
  endTime?: number;
  error?: string;
} 