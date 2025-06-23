# ChaosPilot System Architecture

## Overview
ChaosPilot is a full-stack AI platform for log analysis, incident detection, and automated remediation. It leverages Google Agent Development Kit (ADK), Google Cloud services (BigQuery, Logging, AI Platform, Gemini), and a modular multi-agent architecture. The system is designed for security, extensibility, and modern DevOps.

---

## 1. High-Level Architecture

- **Frontend:** Angular SPA (TypeScript, TailwindCSS, RxJS)
- **Backend:** Python (FastAPI, async/await, Google ADK)
- **Agents:** Main agent manager orchestrates multiple ADK-compliant sub-agents (detector, planner, fixer, notifier, action recommender)
- **Data/AI:** Google BigQuery, Cloud Logging, Gemini LLM (Google AI Platform)
- **Authentication:** Supabase (user/session management)
- **DevOps:** Docker, `uv`, `hatch`, GCP deployment scripts

---

## 2. Google Agent Development Kit (ADK) Usage

- **Core Orchestration:**
  - All agent logic is built using ADK's async runtime and event-driven patterns.
  - The main agent manager (`/agent_manager/agent.py`) coordinates sub-agents, each inheriting from ADK base classes.
  - Sub-agents (in `/agent_manager/sub_agents/`) handle specialized tasks (detection, planning, fixing, notification, recommendations).
- **Toolbox Integration:**
  - `/mcp-toolbox/tools.yaml` defines tools and toolsets in ADK schema, enabling dynamic tool invocation and chaining.
- **Schema Compliance:**
  - All tool and agent definitions are kept in sync with ADK's open source schema, ensuring compatibility and reliability.
- **Open Source Contribution:**
  - Refactors and schema corrections to `tools.yaml` and agent code are suitable for upstream contribution to the ADK open source project.

---

## 3. Multi-Agent Orchestration

- **Agent Manager:**
  - Receives user requests and delegates to specialized sub-agents.
- **Agent Handoffs:**
  - Workflows are designed for dynamic agent handoff (e.g., detector → planner → fixer/notifier). If a sub-agent determines another agent is better suited for the next step, it delegates the task.
- **Sub-Agent LLM Access:**
  - Sub-agents can directly invoke Gemini (Google AI Platform) for LLM-powered analysis, classification, and planning, not just the main agent manager.
- **Dynamic Toolsets:**
  - Each agent can invoke tools from the ADK toolbox, with toolsets defined per agent type.
- **Frontend Visualization:**
  - The Angular frontend visualizes multi-agent workflows, showing handoffs, function calls, and responses in the chat UI.

---

## 4. Google Cloud & AI Services (including Gemini)

- **BigQuery:**
  - Stores and queries logs, incident data. Agents use the mcp-toolbox to connect to BigQuery, retrieve logs, and perform analytics and context retrieval.
- **Cloud Logging:**
  - Ingests and manages raw logs. Logs are exported (sunk) from Cloud Logging to BigQuery for structured querying and analysis. Scripts in `/scripts/` support log injection, management, and sink setup.
- **Gemini LLM (Google AI Platform):**
  - Sub-agents and the main agent manager can each call Gemini for advanced log analysis, incident classification, and remediation planning.
  - All LLM calls are backend-only. There is currently no retrieval-augmented generation (RAG) pipeline, embedding generation, or vector similarity search implemented in the codebase. If RAG is implemented in the future, it will follow strict security and privacy guidelines.
- **ADK Toolbox:**
  - All tools and toolsets are defined for use by agents, ensuring schema compliance and dynamic extensibility. The mcp-toolbox provides the interface and schema for agents to interact with BigQuery and other data sources.

---

## 5. Security & Best Practices

- All API keys and secrets are stored in environment variables.
- No direct client access to LLM APIs.
- All communication is over HTTPS.
- Supabase authentication for all sensitive routes.
- Input/output sanitization, rate limiting, and audit logging at every step.

---

## 6. DevOps & Deployment

- **Local Development:** Use `uv` or `hatch` for environment management, run backend with `uvicorn`, frontend with Angular CLI.
- **Production:** Build Docker image, deploy to cloud (GCP, Azure, etc.), use managed DBs and secure secrets.
- **Scripts:** `/scripts` for GCP setup, IAM, log injection, etc.

---

## 7. Example End-to-End Flow

1. User logs in via Supabase (Angular frontend).
2. User triggers an action (e.g., "Analyze Error Logs").
3. Frontend sends authenticated request to FastAPI backend.
4. Backend authenticates and invokes the main ADK agent.
5. Agent manager delegates to the appropriate sub-agent.
6. Sub-agent queries BigQuery (via the mcp-toolbox), retrieves relevant logs, and may send those logs or summaries to Gemini for LLM-powered analysis.
7. Agent handoff is dynamic: if a sub-agent determines another is better suited for the next step, it delegates the task.
8. Backend streams response to frontend, which visualizes the multi-agent workflow.

---

## 8. Google Tech, Open Source, and Published Content

- **Google Tech:**
  - Deep integration with Google Cloud (BigQuery, Logging, AI Platform, Gemini).
  - Full adoption of Google ADK for agent orchestration and tool management.
- **Open Source:**
  - Refactored and schema-corrected `tools.yaml` and agent code are suitable for contribution to the ADK open source project.
- **Published Content:**
  - The project journal (`xREADME.md`) and documentation provide a transparent record of technical decisions, suitable for publication as a case study or blog post.

---

## 9. Summary Table

| Layer      | Tech/Service         | Key Files/Dirs                | Google/ADK Usage                |
|------------|----------------------|-------------------------------|----------------------------------|
| Frontend   | Angular, Tailwind    | `/frontend/src/app/`          | Visualizes multi-agent ADK flows |
| Backend    | FastAPI, ADK, Python | `/main.py`, `/agent_manager/` | ADK async agents, tool orchestration |
| Data/AI    | BigQuery, Gemini     | `/mcp-toolbox/tools.yaml`     | BigQuery queries, Gemini LLM, ADK toolbox |
| Auth       | Supabase             | `/frontend`, `/main.py`       | -                                |
| DevOps     | Docker, uv, hatch    | `/Dockerfile`, `/scripts/`    | GCP deployment scripts           |

---

## 10. Visual Diagram

```
graph TD
  subgraph Frontend (Angular)
    A1["User<br/>Browser"]
    A2["Angular App<br/>(SPA)"]
  end
  subgraph Backend (Python/FastAPI)
    B1["API Gateway<br/>(FastAPI/Uvicorn)"]
    B2["Agent Manager"]
    B3["Sub-Agents<br/>(Detector, Planner, Fixer, etc.)"]
    B4["Session & Auth Service"]
    B6["BigQuery/Logging Service"]
  end
  subgraph Cloud & Data
    C1["Google BigQuery"]
    C2["Google Cloud Logging"]
    C3["Google AI Platform (Gemini)"]
    C4["Supabase<br/>(Auth, DB)"]
  end
  subgraph DevOps
    D1["Docker"]
    D2["CI/CD"]
  end

  A1-->|HTTPS|A2
  A2-->|REST/WebSocket|B1
  B1-->|Auth|B4
  B1-->|Agent Requests|B2
  B2-->|Delegate|B3
  B3-->|Data|B6
  B6-->|Query|C1
  B6-->|Logs|C2
  B2-->|LLM Analysis|C3
  B4-->|User/Session|C4
  B1-->|Streamed Response|A2
  D1-->|Containerize|B1
  D2-->|Deploy|D1
```

---

**Note:**
- There is currently no RAG/embedding/vector similarity service implemented. If this is a future goal, it will be added in a later version and clearly documented as such.

For more details, see the project journal (`xREADME.md`) and codebase documentation. 