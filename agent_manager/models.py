import datetime
from sqlalchemy import Column, Integer, String, DateTime, Text, JSON
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Feedback(Base):
    __tablename__ = "feedback"
    id = Column(Integer, primary_key=True)
    agent_name = Column(String)
    output_id = Column(String)
    user_id = Column(String)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
    feedback_type = Column(String)  # e.g., 'clarity', 'effectiveness'
    feedback_text = Column(Text)
    effectiveness_score = Column(Integer)  # 1-5 scale
    context_json = Column(JSON)
    tools_used = Column(JSON)  # List of tool names


class AgentRegistry(Base):
    __tablename__ = "agent_registry"
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    description = Column(Text)
    default_toolset = Column(JSON)
    capabilities = Column(JSON)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)


class AuditLog(Base):
    __tablename__ = "audit_log"
    id = Column(Integer, primary_key=True)
    event_type = Column(String)  # e.g., 'agent_invocation', 'tool_call', 'feedback'
    agent_name = Column(String)
    tool_name = Column(String, nullable=True)
    user_id = Column(String, nullable=True)
    details = Column(JSON)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)


class IncidentHistory(Base):
    __tablename__ = "incident_history"
    id = Column(Integer, primary_key=True)
    incident_id = Column(String, unique=True)
    summary_json = Column(JSON)
    resolution_json = Column(JSON)
    agent_outputs_json = Column(JSON)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
