# Smart Meeting Notes Generator

Convert meeting audio into transcripts and AI-generated summaries using local Whisper (transcription) and Google Gemini (summaries, free tier).

## Features

- 🎙️ Upload audio files (MP3, WAV, M4A, MP4)
- 📝 Automatic transcription using Whisper (runs locally, free)
- 🤖 AI-generated summaries, key points, and action items
- 💾 SQLite database for meeting history
- 🖥️ Simple Streamlit frontend
- 🚀 FastAPI backend

## Setup

### 1. Create Virtual Environment
Use Python 3.10 (newer versions like 3.14 are not supported by the pinned packages).
```bash
py -3.10 -m venv env
.\env\Scripts\activate  # Windows
pip install -r requirements.txt
```

### 2. Configure Gemini API Key (free)
Get a free key at https://aistudio.google.com/apikey, then copy `backend/.env.example` to `backend/.env` and set:
```
GEMINI_API_KEY=your-key-here
```
Without a key, the app still works but uses a basic keyword-based summary.

You also need [ffmpeg](https://ffmpeg.org/download.html) installed for Whisper to read audio files.

### 3. Run Backend
```bash
cd backend
uvicorn app.main:app --reload --port 8000
```

### 4. Run Frontend
In a second terminal (with the venv activated):
```bash
cd frontend
streamlit run streamlit_app.py
```
Then open http://localhost:8501

## API Endpoints

- `POST /api/upload` - Upload audio file
- `POST /api/transcribe/{meeting_id}` - Transcribe audio
- `POST /api/summarize/{meeting_id}` - Generate summary
- `GET /api/meetings` - List all meetings
- `GET /api/meetings/{meeting_id}` - Get specific meeting
- `DELETE /api/meetings/{meeting_id}` - Delete meeting

## Tech Stack

- **Backend:** FastAPI, SQLAlchemy, Google Gen AI SDK
- **Frontend:** Streamlit
- **Database:** SQLite
- **AI:** Whisper, local (transcription) + Gemini (summarization)

## Project Structure

```
project/
├── backend/          # FastAPI application
├── frontend/         # Streamlit UI
├── data/            # Audio files and database
└── tests/           # Unit tests
```
