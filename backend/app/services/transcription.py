"""Local Whisper transcription service (FREE)"""
import os
import asyncio
from pathlib import Path
import whisper
import librosa
from dotenv import load_dotenv

load_dotenv()

# Load Whisper model (cached after first load)
WHISPER_MODEL_NAME = os.getenv("WHISPER_MODEL", "base")
DEVICE = os.getenv("DEVICE", "cpu")

print(f"Loading Whisper model '{WHISPER_MODEL_NAME}' on {DEVICE}...")
model = whisper.load_model(WHISPER_MODEL_NAME, device=DEVICE)
print("✅ Whisper model loaded successfully!")


async def transcribe_audio(audio_file_path: str) -> dict:
    """
    Transcribe audio file using local Whisper model (FREE)
    
    Args:
        audio_file_path: Path to the audio file
        
    Returns:
        dict with 'text' and 'duration' keys
    """
    try:
        # Run transcription in thread pool to avoid blocking
        loop = asyncio.get_event_loop()
        result = await loop.run_in_executor(None, _transcribe_sync, audio_file_path)
        
        return result
    
    except Exception as e:
        raise Exception(f"Transcription failed: {str(e)}")


def _transcribe_sync(audio_file_path: str) -> dict:
    """Synchronous transcription helper"""
    # Get audio duration
    duration = librosa.get_duration(path=audio_file_path)
    
    # Transcribe
    result = model.transcribe(audio_file_path, fp16=False)
    
    return {
        "text": result["text"],
        "duration": duration
    }


async def save_transcript(transcript_text: str, meeting_id: int, transcript_dir: str) -> str:
    """
    Save transcript to a text file
    
    Args:
        transcript_text: The transcript text
        meeting_id: Meeting ID
        transcript_dir: Directory to save transcripts
        
    Returns:
        Path to saved transcript file
    """
    transcript_path = Path(transcript_dir) / f"meeting_{meeting_id}_transcript.txt"
    
    # Create directory if it doesn't exist
    transcript_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Save transcript
    with open(transcript_path, "w", encoding="utf-8") as f:
        f.write(transcript_text)
    
    return str(transcript_path)
