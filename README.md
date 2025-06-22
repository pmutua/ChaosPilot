# ChaosPilot - AI-Powered Log Analysis Platform

ChaosPilot is an intelligent log analysis platform that uses AI agents to automatically analyze error, warning, and critical logs, detect patterns, classify incidents, and recommend fixes. **We manage the chaos of production errors through intelligent log analysis.**

## 🎯 **What ChaosPilot Does**

ChaosPilot transforms your log data into actionable insights by managing the chaos of production errors:

- **🔍 AI-Powered Analysis**: Uses LLMs to analyze error, warning, and critical logs for patterns and anomalies
- **📊 Intelligent Classification**: Automatically classifies incidents by severity, impact, and urgency
- **📋 Smart Response Planning**: Generates comprehensive response plans based on log analysis
- **🛠️ Automated Fix Recommendations**: Suggests specific fixes and solutions for detected issues
- **⚡ Safe Auto-Fixing**: Executes automated fixes with rollback capability
- **📢 Smart Alerting**: Manages notifications and escalations intelligently

## 🏗️ **Architecture**

### **Frontend (Angular)**
- Modern, responsive UI with real-time updates
- Agent-based interaction system
- Dashboard with metrics and insights
- Workflow visualization

### **Backend (Google ADK + FastAPI)**
- Google ADK integration for agent orchestration
- RESTful API endpoints with CORS support
- Real-time streaming responses
- Secure session management

### **AI Agents**
1. **🔍 Log Analyzer (detector)** - Analyzes logs for patterns and anomalies
2. **📋 Response Planner (planner)** - Creates detailed response strategies
3. **🛠️ Fix Recommender (action_recommender)** - Suggests specific fixes
4. **⚡ Auto-Fixer (fixer)** - Executes safe automated fixes
5. **📢 Alert Manager (notifier)** - Manages notifications and escalations

## 🚀 **Quick Start**

### **Prerequisites**
- [Google Cloud CLI](https://cloud.google.com/sdk/docs/install-sdk)
- Python 3.8+
- Node.js 16+
- [MCP Toolbox for Databases](https://googleapis.github.io/genai-toolbox/getting-started/local_quickstart/)

### **One-Click Setup**

**Windows:**
```bash
start_chaospilot.bat
```

**Linux/macOS:**
```bash
chmod +x start_chaospilot.sh
./start_chaospilot.sh
```

### **Manual Setup**

1. **Clone the repository**
   ```bash
   git clone https://github.com/pmutua/ChaosPilot
   cd ChaosPilot
   ```

2. **Setup Python environment**
   ```bash
   python -m venv .venv
   # Windows CMD:
   .venv\Scripts\activate.bat
   # Linux/macOS:
   source .venv/bin/activate
   pip install -r requirements.txt
   ```

3. **Setup Frontend**
   ```bash
   cd web
   npm install
   cd ..
   ```

4. **Start the Application**
   ```bash
   # Start MCP Toolbox
   cd mcp-toolbox
   toolbox  # Windows
   ./toolbox --tools-file="tools.yaml"  # Linux/macOS
   
   # Start ADK API Server (with CORS)
   cd agent_manager
   adk api_server app --allow_origins="*"
   
   # Start Frontend
   cd web
   npm start
   ```

## 📚 **Documentation**

- **[📖 Setup & Deployment Guide](docs/setup-and-deployment/HOW_TO_RUN_AND_DEPLOY_THE_APPLICATION.md)** - Complete setup instructions
- **[🔧 ADK Integration Guide](docs/setup-and-deployment/ADK_INTEGRATION_README.md)** - Google ADK API integration details
- **[⚡ Quick Start Guide](QUICK_START.md)** - Fast setup reference
- **[🧪 Integration Testing](test_adk_integration.py)** - Test script for API integration

## 📊 **Features**

### **Real-time Log Analysis**
- Continuous monitoring of error, warning, and critical logs
- Pattern recognition and anomaly detection using BigQuery
- Root cause analysis using AI agents

### **Intelligent Incident Management**
- Automatic incident classification by severity and impact
- Service dependency mapping
- Historical trend analysis

### **Automated Response**
- AI-generated response plans with confidence scoring
- Step-by-step action recommendations
- Safe automated fix execution with rollback capability

### **Comprehensive Dashboard**
- Real-time system metrics and health indicators
- Agent performance analytics
- Recent incidents and resolutions
- Quick action templates for common scenarios

## 🔧 **Configuration**

### **Environment Variables**
```bash
# Google Cloud
GOOGLE_APPLICATION_CREDENTIALS=path/to/credentials.json
PROJECT_ID=your-gcp-project-id

# ADK Configuration
ADK_API_URL=http://localhost:8000
ADK_APP_NAME=agent_manager

# Application
LOG_LEVEL=INFO
ENVIRONMENT=development
```

### **GCP Services Required**
- Cloud Logging
- BigQuery
- Cloud Run
- IAM
- Secret Manager

## 📈 **Usage Examples**

### **Analyzing Error Logs**
1. Navigate to the Log Analysis page
2. Select the "Log Analyzer" agent
3. Provide error logs or describe the issue
4. Get AI-powered analysis with confidence scores

### **Getting Fix Recommendations**
1. Use the "Fix Recommender" agent
2. Share the analyzed logs and issues
3. Get specific fix suggestions with implementation steps

### **Automated Incident Response**
1. The system automatically detects critical issues
2. AI agents generate response plans
3. Safe automated fixes are applied
4. Teams are notified with detailed reports

## 🧪 **Testing**

### **Test API Integration**
```bash
python test_adk_integration.py
```

### **Manual Testing with cURL**
```bash
# Create session
curl -X POST http://localhost:8000/apps/agent_manager/users/test/sessions/test \
  -H "Content-Type: application/json" \
  -d '{"state": {"test": true}}'

# Run detector agent
curl -X POST http://localhost:8000/run \
  -H "Content-Type: application/json" \
  -d '{
    "appName": "agent_manager",
    "userId": "test_user",
    "sessionId": "test_session",
    "newMessage": {
      "role": "user",
      "parts": [{"text": "Use the detector agent to: Analyze logs"}]
    }
  }'
```

## 🚀 **Production Deployment**

### **Deploy to Google Cloud Run**
```bash
# Deploy MCP Toolbox
gcloud run deploy toolbox \
  --image us-central1-docker.pkg.dev/database-toolbox/toolbox/toolbox:latest \
  --service-account cloud-run-svc@YOUR_PROJECT_ID.iam.gserviceaccount.com \
  --region us-central1 \
  --allow-unauthenticated

# Deploy Agent Manager
cd agent_manager
gcloud run deploy agent-manager \
  --source . \
  --service-account cloud-run-svc@YOUR_PROJECT_ID.iam.gserviceaccount.com \
  --region us-central1 \
  --allow-unauthenticated
```

For detailed deployment instructions, see the [Setup & Deployment Guide](docs/setup-and-deployment/HOW_TO_RUN_AND_DEPLOY_THE_APPLICATION.md).

## 🔧 **Troubleshooting**

### **Common Issues**

- **CORS Errors**: Use `adk api_server app --allow_origins="*"`
- **Service Account Issues**: Run the IAM role assignment scripts
- **Billing Errors**: Ensure GCP billing is enabled
- **Agent Not Found**: Verify you're running from the correct directory

For detailed troubleshooting, see the [Setup & Deployment Guide](docs/setup-and-deployment/HOW_TO_RUN_AND_DEPLOY_THE_APPLICATION.md#-troubleshooting).

## 🤝 **Contributing**

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 **License**

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 **Support**

For support and questions:
- Create an issue in the repository
- Check the [documentation](docs/setup-and-deployment/)
- Review the [troubleshooting guide](docs/setup-and-deployment/HOW_TO_RUN_AND_DEPLOY_THE_APPLICATION.md#-troubleshooting)

---

**ChaosPilot** - Managing the chaos of production errors through AI-powered log analysis.

**Quick Links:**
- [🚀 Quick Start](QUICK_START.md)
- [📖 Setup Guide](docs/setup-and-deployment/HOW_TO_RUN_AND_DEPLOY_THE_APPLICATION.md)
- [🔧 ADK Integration](docs/setup-and-deployment/ADK_INTEGRATION_README.md)
- [🧪 Test Integration](test_adk_integration.py)
