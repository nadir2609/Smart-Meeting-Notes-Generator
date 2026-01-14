"""Results display component"""
import streamlit as st
from datetime import datetime


def display_meeting_results(meeting_data: dict):
    """
    Display meeting transcript and summary
    
    Args:
        meeting_data: Meeting data from API
    """
    st.subheader("📊 Meeting Analysis")
    
    # Meeting info
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Meeting Title", meeting_data.get("title", "N/A"))
    with col2:
        duration = meeting_data.get("duration")
        if duration:
            minutes = int(duration / 60)
            seconds = int(duration % 60)
            st.metric("Duration", f"{minutes}m {seconds}s")
        else:
            st.metric("Duration", "N/A")
    with col3:
        date_str = meeting_data.get("date", "")
        if date_str:
            date_obj = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
            st.metric("Date", date_obj.strftime("%Y-%m-%d"))
        else:
            st.metric("Date", "N/A")
    
    st.divider()
    
    # Tabs for different sections
    tab1, tab2, tab3, tab4 = st.tabs(["📝 Transcript", "📋 Summary", "🎯 Key Points", "✅ Action Items"])
    
    with tab1:
        transcript = meeting_data.get("transcript_text")
        if transcript:
            st.text_area(
                "Full Transcript",
                value=transcript,
                height=400,
                help="Complete transcript of the meeting"
            )
            
            # Download button
            st.download_button(
                label="⬇️ Download Transcript",
                data=transcript,
                file_name=f"{meeting_data['title']}_transcript.txt",
                mime="text/plain"
            )
        else:
            st.info("Transcript not available yet. Click 'Transcribe Audio' to generate.")
    
    with tab2:
        summary = meeting_data.get("summary")
        if summary:
            st.markdown("### Meeting Summary")
            st.write(summary)
            
            # Download button
            st.download_button(
                label="⬇️ Download Summary",
                data=summary,
                file_name=f"{meeting_data['title']}_summary.txt",
                mime="text/plain"
            )
        else:
            st.info("Summary not available yet. Click 'Generate Summary' to create.")
    
    with tab3:
        key_points = meeting_data.get("key_points")
        if key_points:
            st.markdown("### Key Discussion Points")
            points_list = key_points.split('\n') if isinstance(key_points, str) else key_points
            for i, point in enumerate(points_list, 1):
                if point.strip():
                    st.markdown(f"**{i}.** {point.strip()}")
        else:
            st.info("Key points not available yet. Generate summary first.")
    
    with tab4:
        action_items = meeting_data.get("action_items")
        if action_items:
            st.markdown("### Action Items")
            items_list = action_items.split('\n') if isinstance(action_items, str) else action_items
            for i, item in enumerate(items_list, 1):
                if item.strip():
                    st.checkbox(item.strip(), key=f"action_{i}")
        else:
            st.info("Action items not available yet. Generate summary first.")


def display_meeting_list(meetings: list, api_url: str):
    """
    Display list of past meetings
    
    Args:
        meetings: List of meeting data
        api_url: Backend API URL
    """
    st.subheader("📚 Past Meetings")
    
    if not meetings:
        st.info("No meetings found. Upload an audio file to get started!")
        return
    
    for meeting in meetings:
        with st.expander(f"🎙️ {meeting['title']} - {meeting['date'][:10]}"):
            col1, col2 = st.columns([3, 1])
            
            with col1:
                st.write(f"**ID:** {meeting['id']}")
                st.write(f"**Date:** {meeting['date'][:19]}")
                if meeting.get('duration'):
                    minutes = int(meeting['duration'] / 60)
                    st.write(f"**Duration:** {minutes} minutes")
            
            with col2:
                if st.button("View Details", key=f"view_{meeting['id']}"):
                    st.session_state['selected_meeting_id'] = meeting['id']
                    st.rerun()
                
                if st.button("🗑️ Delete", key=f"delete_{meeting['id']}"):
                    try:
                        response = requests.delete(f"{api_url}/api/meetings/{meeting['id']}")
                        if response.status_code == 200:
                            st.success("Meeting deleted!")
                            st.rerun()
                        else:
                            st.error("Failed to delete meeting")
                    except Exception as e:
                        st.error(f"Error: {str(e)}")
