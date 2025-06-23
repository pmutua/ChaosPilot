# Project Story: ChaosPilot – AI-Powered Log Analysis

## Inspiration

As someone who has spent years working in software engineering, I've seen firsthand how overwhelming and time-consuming it can be to sift through endless logs during incidents. I've been on-call and faced the daunting task of finding the root cause of a production outage—often buried in thousands of lines of logs. The frustration of manual log analysis, the pressure to restore service quickly, and the risk of missing critical patterns inspired me to imagine a better way.

The real spark came when I saw a post on Reddit: someone asked if there was an AI tool that could analyze logs and surface actionable insights. That question resonated deeply with my own experience and the pain points I've seen across teams. I realized that with the rise of LLMs and cloud-native architectures, it was finally possible to build a tool that could automate the chaos of log analysis and incident response.

## About the Project

ChaosPilot is my answer to the modern log analysis problem. It's a full-stack, AI-powered platform that:
- Ingests and analyzes logs in real time, currently connected with BigQuery and it's possible to connect with other data sources via the [MCP Toolbox for databases](https://googleapis.github.io/genai-toolbox/getting-started/introduction/).
    > This solution was originally named “Gen AI Toolbox for Databases” as its initial development.
- Detects patterns, anomalies, and root causes
- Classifies incidents by severity and impact
- Generates actionable response plans and fix recommendations
- Provides a beautiful, interactive dashboard for teams

I wanted to build something that not only saves engineers time, but also empowers them to respond faster and with more confidence during high-stress incidents.

## 🛠️ How I Built It

- **Frontend:** Angular, TypeScript, TailwindCSS for a modern, responsive UI
- **Backend:** Python, FastAPI, Google ADK for orchestrating AI agents and workflows
- **Authentication:** Supabase for secure user management
- **Data/AI:** Google ADK agents (detector, planner, fixer, etc.), BigQuery analytics
- **DevOps:** Docker, GCP, and modern Python dependency management (`uv`, `hatch`)

I focused on building a seamless integration between the UI and backend, ensuring that every agent response—whether plain text, markdown, or structured JSON—was rendered clearly and usefully for the end user. I also prioritized security, making sure only authenticated users could access sensitive dashboards and data.

## 📚 What I Learned

- How to design and implement a full-stack AI product from scratch
- Advanced Angular and TypeScript patterns for dynamic, reactive UIs
- Secure authentication and route protection with Supabase
- Orchestrating multi-agent workflows and handling diverse response types (text, markdown, JSON)
- Best practices in async Python, API design, and frontend-backend contract alignment
- The importance of clear documentation and project journaling for future maintainers and employers
- **Learning the Agent Development Kit (ADK):** I had to go through many resources, documentation, and community posts to understand and implement the ADK. It was a steep learning curve, but it opened my eyes to the power of building autonomous, agent-based systems. I realized that with the right tools, we can create systems that not only react, but proactively manage and optimize complex environments.

## ⚡ Challenges Faced

- Handling the wide variety of log formats and agent response types (sometimes plain text, sometimes deeply nested JSON)
- Ensuring the UI was both beautiful and functional, even as the backend evolved
- Debugging authentication flows and making sure session management was robust
- Building a system that could scale from a hackathon prototype to a production-ready tool
- **Deployment Issues:** Deploying a multi-service, cloud-native stack (with ADK, FastAPI, Supabase, and the MCP Toolbox) was a real challenge. I faced CORS issues, service account permission errors, and the usual headaches of getting everything to work smoothly on GCP and Docker. Each deployment hurdle taught me more about cloud infrastructure and the importance of automation and clear documentation.

## 💡 Final Thoughts

ChaosPilot is more than just a hackathon project—it's a reflection of my passion for solving real engineering problems with modern technology. I built it for every engineer who's ever felt lost in a sea of logs, and for every team that wants to move faster and smarter in the face of chaos.

If you're reading this as a future employer or collaborator, know that I bring not just technical skills, but also empathy for the user and a drive to build tools that make a real difference.
