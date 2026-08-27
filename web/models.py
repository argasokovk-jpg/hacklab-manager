from sqlalchemy import Column, Integer, String, DateTime, Text, Boolean
from sqlalchemy.sql import func
from web.database import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class LabSession(Base):
    __tablename__ = "lab_sessions"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)
    lab_id = Column(Integer, nullable=False)
    container_id = Column(String, nullable=True)
    started_at = Column(DateTime(timezone=True), server_default=func.now())
    finished_at = Column(DateTime(timezone=True), nullable=True)
    is_active = Column(Boolean, default=True)

class ActionLog(Base):
    __tablename__ = "action_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)
    lab_id = Column(Integer, nullable=False)
    command = Column(Text, nullable=False)
    output = Column(Text, nullable=True)
    exit_code = Column(Integer, nullable=True)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())

class LabResult(Base):
    __tablename__ = "lab_results"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)
    lab_id = Column(Integer, nullable=False)
    score = Column(Integer, nullable=True)
    level = Column(String, nullable=True)
    feedback = Column(Text, nullable=True)
    commands_count = Column(Integer, nullable=True)
    duration = Column(Integer, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Achievement(Base):
    __tablename__ = "achievements"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)
    icon = Column(String, nullable=False)
    condition = Column(String, nullable=False)  # например: "lab_completed:1" или "score:80"
    xp_reward = Column(Integer, default=50)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class UserAchievement(Base):
    __tablename__ = "user_achievements"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)
    achievement_id = Column(Integer, nullable=False)
    earned_at = Column(DateTime(timezone=True), server_default=func.now())
