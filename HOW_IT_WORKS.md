# How ChaosPilot Works: Step-by-Step Script

This document provides a clear, step-by-step walkthrough of how the ChaosPilot application operates, from user interaction in the frontend to agent orchestration and AI analysis in the backend. Use this as a guide for onboarding, demos, or understanding the system flow.

---

## 1. User Login & Authentication

- The user navigates to the ChaosPilot web app (Angular frontend).
- The app prompts the user to log in using Supabase authentication.
- Upon successful login, the user is granted access to the dashboard, chat, history, and settings.

---

## 2. Initiating an AI Workflow (Example: Analyze Error Logs)

- The user sees a set of quick action buttons (e.g., "Analyze Error Logs", "Classify Incident", "Generate Fix Plan").
- The user clicks "Analyze Error Logs".
- The frontend sends an authenticated request to the backend (FastAPI server) to start the analysis workflow.

---

## 3. Backend Agent Orchestration

- The backend receives the request and verifies the user's authentication (via Supabase).
- The main agent manager (using Google ADK) is invoked.
- The agent manager delegates the task to the appropriate sub-agent (e.g., the detector agent for log analysis).

---

## 4. Data Query & AI Analysis

- The sub-agent queries Google BigQuery for recent error logs.
- The relevant logs or summaries are prepared for analysis.
- The backend sends the prepared data to the selected LLM (Gemini or Azure OpenAI) for advanced analysis and insights.
- The LLM returns its analysis (e.g., detected patterns, incident classification, recommendations).

---

## 5. Multi-Agent Workflow (if needed)

- If the workflow requires further steps (e.g., generating a fix plan, recommending fixes), the agent manager hands off the task to other sub-agents (planner, fixer, etc.).
- Each sub-agent may query data, invoke tools, or call the LLM as needed.
- The results from each agent are collected and organized.

---

## 6. Streaming Results to the Frontend

- The backend streams the results of the agent workflow back to the frontend.
- The Angular app dynamically updates the chat UI, displaying:
  - Markdown-formatted analysis and reports
  - Structured data (tables, JSON)
  - Agent handoffs and function calls
  - Status updates and loading indicators

---

## 7. User Experience & Further Actions

- The user reviews the AI-generated analysis and recommendations in the chat interface.
- The user can trigger additional actions (e.g., request a fix plan, escalate an incident, review history).
- All sensitive actions and data remain protected by authentication and backend-only processing.

---

## 8. Security & Best Practices

- All LLM/API calls are made from the backend only; the client never interacts directly with AI services.
- All communication is over HTTPS.
- User sessions and permissions are managed by Supabase.
- Logs and sensitive data are never exposed to the client or external services.

---

## 9. Summary Flow Diagram

```
User (Browser)
   │
   ▼
Angular Frontend (UI, Auth, Chat)
   │  (REST API call)
   ▼
FastAPI Backend (Python, ADK)
   │
   ├─► Agent Manager (Orchestrates sub-agents)
   │      │
   │      ├─► Detector Agent (queries BigQuery)
   │      ├─► Planner Agent (generates plans)
   │      └─► Fixer/Notifier Agents (as needed)
   │
   └─► LLM (Gemini/Azure) for analysis
   │
   ▼
Backend streams results
   │
   ▼
Angular Frontend (renders chat, tables, reports)
```

---

For more details, see the architecture and project journal files. 