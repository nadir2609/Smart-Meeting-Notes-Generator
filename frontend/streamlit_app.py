"""Smart Meeting Notes Generator - Streamlit Frontend"""
import os
import streamlit as st
import requests
from datetime import datetime
from components.file_uploader import upload_audio_file
from components.results_display import display_meeting_results, display_meeting_list

# Page configuration
st.set_page_config(
    page_title="Smart Meeting Notes Generator",
    page_icon="🎙️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Backend API URL (supports both local and deployed environments)
API_URL = os.getenv("API_URL", "http://localhost:8000")

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        color: #1f77b4;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.2rem;
        text-align: center;
        color: #666;
        margin-bottom: 2rem;
    }
    .stButton>button {
        width: 100%;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'current_meeting' not in st.session_state:
    st.session_state['current_meeting'] = None
if 'selected_meeting_id' not in st.session_state:
    st.session_state['selected_meeting_id'] = None

# Header
st.markdown('<div class="main-header">🎙️ Smart Meeting Notes</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">AI-Powered Meeting Transcription & Summarization (100% FREE)</div>', unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.title("⚙️ Settings")
    
    # API Status Check
    try:
        response = requests.get(f"{API_URL}/", timeout=2)
        if response.status_code == 200:
            st.success("✅ Backend Connected")
        else:
            st.error("❌ Backend Error")
    except:
        st.error("❌ Backend Offline")
        st.warning("Start backend: `cd backend && uvicorn app.main:app --reload`")
    
    st.divider()
    
    # Navigation
    st.subheader("📑 Navigation")
    page = st.radio(
        "Select Page",
        ["🎙️ New Meeting", "📚 Meeting History"],
        label_visibility="collapsed"
    )
    
    st.divider()
    
    # Info
    st.subheader("ℹ️ About")
    st.info("""
    **Features:**
    - 🎤 Upload audio files
    - 📝 AI transcription (Whisper)
    - 📊 Smart summaries (Gemini)
    - 🎯 Key points extraction
    - ✅ Action items detection
    
    **FREE** - Gemini free-tier API key
    """)

# Main content
if page == "🎙️ New Meeting":
    # Two-column layout
    col1, col2 = st.columns([1, 1])
    
    with col1:
        # Upload section
        meeting_data = upload_audio_file(API_URL)
        
        if meeting_data:
            st.session_state['current_meeting'] = meeting_data
    
    with col2:
        # Processing section
        if st.session_state['current_meeting']:
            meeting = st.session_state['current_meeting']
            
            st.subheader("🔄 Processing")
            
            # Transcription
            if not meeting.get('transcript_text'):
                if st.button("📝 Transcribe Audio", type="primary", use_container_width=True):
                    with st.spinner("Transcribing audio... This may take a few minutes."):
                        try:
                            response = requests.post(
                                f"{API_URL}/api/transcribe/{meeting['id']}",
                                timeout=600  # 10 minutes timeout
                            )
                            
                            if response.status_code == 200:
                                transcript_data = response.json()
                                st.success("✅ Transcription complete!")
                                
                                # Update meeting data
                                meeting['transcript_text'] = transcript_data['transcript']
                                meeting['duration'] = transcript_data.get('duration')
                                st.session_state['current_meeting'] = meeting
                                st.rerun()
                            else:
                                st.error(f"❌ Transcription failed: {response.json().get('detail', 'Unknown error')}")
                        except requests.Timeout:
                            st.error("❌ Transcription timed out. Try with a shorter audio file.")
                        except Exception as e:
                            st.error(f"❌ Error: {str(e)}")
            else:
                st.success("✅ Transcription completed")
            
            # Summarization
            if meeting.get('transcript_text') and not meeting.get('summary'):
                if st.button("🤖 Generate Summary", type="primary", use_container_width=True):
                    with st.spinner("Generating summary..."):
                        try:
                            response = requests.post(
                                f"{API_URL}/api/summarize/{meeting['id']}",
                                timeout=300  # 5 minutes timeout
                            )
                            
                            if response.status_code == 200:
                                summary_data = response.json()
                                st.success("✅ Summary generated!")
                                
                                # Update meeting data
                                meeting['summary'] = summary_data['summary']
                                meeting['key_points'] = '\n'.join(summary_data['key_points'])
                                meeting['action_items'] = '\n'.join(summary_data['action_items'])
                                st.session_state['current_meeting'] = meeting
                                st.rerun()
                            else:
                                st.error(f"❌ Summary generation failed: {response.json().get('detail', 'Unknown error')}")
                        except Exception as e:
                            st.error(f"❌ Error: {str(e)}")
            elif meeting.get('summary'):
                st.success("✅ Summary generated")
        else:
            st.info("👈 Upload an audio file to get started")
    
    # Results section (full width)
    if st.session_state['current_meeting'] and st.session_state['current_meeting'].get('transcript_text'):
        st.divider()
        display_meeting_results(st.session_state['current_meeting'])

elif page == "📚 Meeting History":
    # Fetch all meetings
    try:
        response = requests.get(f"{API_URL}/api/meetings", timeout=5)
        
        if response.status_code == 200:
            meetings = response.json()
            
            # Check if user selected a meeting from the list
            if st.session_state.get('selected_meeting_id'):
                # Fetch selected meeting details
                meeting_response = requests.get(
                    f"{API_URL}/api/meetings/{st.session_state['selected_meeting_id']}",
                    timeout=5
                )
                
                if meeting_response.status_code == 200:
                    meeting = meeting_response.json()
                    
                    # Back button
                    if st.button("← Back to List"):
                        st.session_state['selected_meeting_id'] = None
                        st.rerun()
                    
                    st.divider()
                    display_meeting_results(meeting)
                else:
                    st.error("Failed to load meeting details")
                    st.session_state['selected_meeting_id'] = None
            else:
                # Display meeting list
                display_meeting_list(meetings, API_URL)
        else:
            st.error("Failed to fetch meetings")
    except Exception as e:
        st.error(f"Error: {str(e)}")

# Footer
st.divider()
st.markdown("""
<div style="text-align: center; color: #666; padding: 1rem;">
    Made with ❤️ using Streamlit, FastAPI, Whisper & Gemini | Free & Open Source
</div>
""", unsafe_allow_html=True)
