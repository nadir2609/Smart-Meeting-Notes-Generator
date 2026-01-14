"""FastAPI main application"""
import os
from fastapi import FastAPI, File, UploadFile, Depends, HTTPException, Form
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from dotenv import load_dotenv

from app.database import init_db, get_db
from app.models import Meeting, MeetingCreate, MeetingResponse, TranscriptionResponse, SummaryResponse
from app.services.storage import save_audio_file, validate_audio_file
from app.services.transcription import transcribe_audio, save_transcript
from app.services.nlp import clean_transcript, generate_summary

load_dotenv()

app = FastAPI(
    title="Smart Meeting Notes Generator",
    description="Convert meeting audio to transcripts and summaries",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configuration
AUDIO_UPLOAD_DIR = os.getenv("AUDIO_UPLOAD_DIR", "../data/audio")
TRANSCRIPT_DIR = os.getenv("TRANSCRIPT_DIR", "../data/transcripts")
MAX_FILE_SIZE_MB = int(os.getenv("MAX_FILE_SIZE_MB", "25"))
ALLOWED_FORMATS = os.getenv("ALLOWED_AUDIO_FORMATS", "mp3,wav,m4a,mp4").split(",")


@app.on_event("startup")
async def startup_event():
    """Initialize database on startup"""
    await init_db()
    print("✅ Database initialized")


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Smart Meeting Notes Generator API",
        "version": "1.0.0",
        "endpoints": ["/api/upload", "/api/transcribe/{meeting_id}", "/api/summarize/{meeting_id}", "/api/meetings"]
    }


@app.post("/api/upload", response_model=MeetingResponse)
async def upload_audio(
    file: UploadFile = File(...),
    title: str = Form(...),
    db: AsyncSession = Depends(get_db)
):
    """
    Upload audio file and create meeting record
    """
    # Validate file format
    if not validate_audio_file(file.filename, ALLOWED_FORMATS):
        raise HTTPException(
            status_code=400,
            detail=f"Invalid file format. Allowed: {', '.join(ALLOWED_FORMATS)}"
        )
    
    # Read and save file
    file_content = await file.read()
    
    # Check file size
    file_size_mb = len(file_content) / (1024 * 1024)
    if file_size_mb > MAX_FILE_SIZE_MB:
        raise HTTPException(
            status_code=400,
            detail=f"File too large. Max size: {MAX_FILE_SIZE_MB}MB"
        )
    
    # Save audio file
    audio_path = await save_audio_file(file_content, file.filename, AUDIO_UPLOAD_DIR)
    
    # Create meeting record
    meeting = Meeting(
        title=title,
        audio_path=audio_path
    )
    
    db.add(meeting)
    await db.commit()
    await db.refresh(meeting)
    
    return meeting


@app.post("/api/transcribe/{meeting_id}", response_model=TranscriptionResponse)
async def transcribe_meeting(
    meeting_id: int,
    db: AsyncSession = Depends(get_db)
):
    """
    Transcribe audio for a meeting
    """
    # Get meeting
    result = await db.execute(select(Meeting).where(Meeting.id == meeting_id))
    meeting = result.scalar_one_or_none()
    
    if not meeting:
        raise HTTPException(status_code=404, detail="Meeting not found")
    
    if not meeting.audio_path or not os.path.exists(meeting.audio_path):
        raise HTTPException(status_code=404, detail="Audio file not found")
    
    # Transcribe audio
    transcript_data = await transcribe_audio(meeting.audio_path)
    
    # Clean transcript
    cleaned_transcript = clean_transcript(transcript_data["text"])
    
    # Save transcript
    transcript_path = await save_transcript(cleaned_transcript, meeting_id, TRANSCRIPT_DIR)
    
    # Update meeting record
    meeting.transcript_text = cleaned_transcript
    meeting.transcript_path = transcript_path
    meeting.duration = transcript_data.get("duration")
    
    await db.commit()
    
    return TranscriptionResponse(
        meeting_id=meeting_id,
        transcript=cleaned_transcript,
        duration=transcript_data.get("duration")
    )


@app.post("/api/summarize/{meeting_id}", response_model=SummaryResponse)
async def summarize_meeting(
    meeting_id: int,
    db: AsyncSession = Depends(get_db)
):
    """
    Generate summary for a meeting
    """
    # Get meeting
    result = await db.execute(select(Meeting).where(Meeting.id == meeting_id))
    meeting = result.scalar_one_or_none()
    
    if not meeting:
        raise HTTPException(status_code=404, detail="Meeting not found")
    
    if not meeting.transcript_text:
        raise HTTPException(status_code=400, detail="Meeting must be transcribed first")
    
    # Generate summary
    summary_data = await generate_summary(meeting.transcript_text)
    
    # Update meeting record
    meeting.summary = summary_data["summary"]
    meeting.key_points = "\n".join(summary_data["key_points"])
    meeting.action_items = "\n".join(summary_data["action_items"])
    
    await db.commit()
    
    return SummaryResponse(
        meeting_id=meeting_id,
        summary=summary_data["summary"],
        key_points=summary_data["key_points"],
        action_items=summary_data["action_items"]
    )


@app.get("/api/meetings", response_model=list[MeetingResponse])
async def get_meetings(
    skip: int = 0,
    limit: int = 10,
    db: AsyncSession = Depends(get_db)
):
    """
    Get all meetings
    """
    result = await db.execute(
        select(Meeting).offset(skip).limit(limit).order_by(Meeting.created_at.desc())
    )
    meetings = result.scalars().all()
    return meetings


@app.get("/api/meetings/{meeting_id}", response_model=MeetingResponse)
async def get_meeting(
    meeting_id: int,
    db: AsyncSession = Depends(get_db)
):
    """
    Get a specific meeting
    """
    result = await db.execute(select(Meeting).where(Meeting.id == meeting_id))
    meeting = result.scalar_one_or_none()
    
    if not meeting:
        raise HTTPException(status_code=404, detail="Meeting not found")
    
    return meeting


@app.delete("/api/meetings/{meeting_id}")
async def delete_meeting(
    meeting_id: int,
    db: AsyncSession = Depends(get_db)
):
    """
    Delete a meeting
    """
    result = await db.execute(select(Meeting).where(Meeting.id == meeting_id))
    meeting = result.scalar_one_or_none()
    
    if not meeting:
        raise HTTPException(status_code=404, detail="Meeting not found")
    
    await db.delete(meeting)
    await db.commit()
    
    return {"message": "Meeting deleted successfully"}
