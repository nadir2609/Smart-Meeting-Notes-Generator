"""File upload component"""
import streamlit as st
import requests
from typing import Optional


def upload_audio_file(api_url: str) -> Optional[dict]:
    """
    Handle audio file upload
    
    Args:
        api_url: Backend API URL
        
    Returns:
        Meeting data if upload successful
    """
    st.subheader("📁 Upload Audio File")
    
    # File uploader
    uploaded_file = st.file_uploader(
        "Choose an audio file",
        type=["mp3", "wav", "m4a", "mp4", "webm"],
        help="Supported formats: MP3, WAV, M4A, MP4, WebM (Max 25MB)"
    )
    
    # Meeting title input
    meeting_title = st.text_input(
        "Meeting Title",
        placeholder="e.g., Q1 Planning Meeting",
        help="Give your meeting a descriptive title"
    )
    
    # Upload button
    if st.button("🚀 Upload & Process", type="primary", disabled=not uploaded_file or not meeting_title):
        if uploaded_file and meeting_title:
            with st.spinner("Uploading audio file..."):
                try:
                    # Prepare file for upload
                    files = {"file": (uploaded_file.name, uploaded_file, uploaded_file.type)}
                    data = {"title": meeting_title}
                    
                    # Upload to backend
                    response = requests.post(
                        f"{api_url}/api/upload",
                        files=files,
                        data=data,
                        timeout=60
                    )
                    
                    if response.status_code == 200:
                        meeting_data = response.json()
                        st.success(f"✅ File uploaded successfully! Meeting ID: {meeting_data['id']}")
                        return meeting_data
                    else:
                        st.error(f"❌ Upload failed: {response.json().get('detail', 'Unknown error')}")
                        return None
                        
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")
                    return None
    
    return None
