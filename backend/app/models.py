"""Database models and Pydantic schemas"""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field
from sqlalchemy import Column, Integer, String, DateTime, Float, Text
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


# SQLAlchemy ORM Models
class Meeting(Base):
    """Meeting database model"""
    __tablename__ = "meetings"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    date = Column(DateTime, default=datetime.utcnow)
    audio_path = Column(String(500), nullable=False)
    transcript_path = Column(String(500), nullable=True)
    transcript_text = Column(Text, nullable=True)
    summary = Column(Text, nullable=True)
    key_points = Column(Text, nullable=True)
    action_items = Column(Text, nullable=True)
    duration = Column(Float, nullable=True)  # in seconds
    created_at = Column(DateTime, default=datetime.utcnow)


# Pydantic Schemas for API
class MeetingCreate(BaseModel):
    """Schema for creating a new meeting"""
    title: str = Field(..., min_length=1, max_length=255)


class MeetingResponse(BaseModel):
    """Schema for meeting response"""
    id: int
    title: str
    date: datetime
    audio_path: str
    transcript_path: Optional[str] = None
    transcript_text: Optional[str] = None
    summary: Optional[str] = None
    key_points: Optional[str] = None
    action_items: Optional[str] = None
    duration: Optional[float] = None
    created_at: datetime

    class Config:
        from_attributes = True


class TranscriptionResponse(BaseModel):
    """Schema for transcription response"""
    meeting_id: int
    transcript: str
    duration: Optional[float] = None


class SummaryResponse(BaseModel):
    """Schema for summary response"""
    meeting_id: int
    summary: str
    key_points: list[str]
    action_items: list[str]
