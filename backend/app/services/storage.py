"""File storage service"""
import os
import aiofiles
from pathlib import Path
from datetime import datetime


async def save_audio_file(file_content: bytes, filename: str, upload_dir: str) -> str:
    """
    Save uploaded audio file
    
    Args:
        file_content: Audio file bytes
        filename: Original filename
        upload_dir: Directory to save uploads
        
    Returns:
        Path to saved file
    """
    # Create unique filename with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_extension = Path(filename).suffix
    new_filename = f"meeting_{timestamp}{file_extension}"
    
    file_path = Path(upload_dir) / new_filename
    
    # Create directory if it doesn't exist
    file_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Save file
    async with aiofiles.open(file_path, 'wb') as f:
        await f.write(file_content)
    
    return str(file_path)


def validate_audio_file(filename: str, allowed_formats: list) -> bool:
    """
    Validate audio file format
    
    Args:
        filename: File name
        allowed_formats: List of allowed extensions
        
    Returns:
        True if valid, False otherwise
    """
    file_extension = Path(filename).suffix.lower().lstrip('.')
    return file_extension in allowed_formats
