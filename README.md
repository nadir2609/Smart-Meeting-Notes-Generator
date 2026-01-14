# Smart Meeting Notes Generator

Convert meeting audio into transcripts and AI-generated summaries using OpenAI Whisper and GPT.

## Features

- 🎙️ Upload audio files (MP3, WAV, M4A, MP4)
- 📝 Automatic transcription using OpenAI Whisper
- 🤖 AI-generated summaries, key points, and action items
- 💾 SQLite database for meeting history
- 🖥️ Simple Streamlit frontend
- 🚀 FastAPI backend

## Setup

### 1. Create Virtual Environment
```bash
python -m venv env
.\env\Scripts\activate  # Windows
pip install -r requirements.txt
```

### 2. Configure OpenAI API Key
Copy `.env.example` to `.env` in the backend folder and add your OpenAI API key:
```
OPENAI_API_KEY=sk-your-key-here
```

### 3. Run Backend
```bash
cd backend
uvicorn app.main:app --reload --port 8000
```

### 4. Run Frontend
```bash
streamlit run frontend/streamlit_app.py
```

## API Endpoints

- `POST /api/upload` - Upload audio file
- `POST /api/transcribe/{meeting_id}` - Transcribe audio
- `POST /api/summarize/{meeting_id}` - Generate summary
- `GET /api/meetings` - List all meetings
- `GET /api/meetings/{meeting_id}` - Get specific meeting
- `DELETE /api/meetings/{meeting_id}` - Delete meeting

## Tech Stack

- **Backend:** FastAPI, SQLAlchemy, OpenAI API
- **Frontend:** Streamlit
- **Database:** SQLite
- **AI:** OpenAI Whisper (transcription) + GPT-4 (summarization)

## Project Structure

```
project/
├── backend/          # FastAPI application
├── frontend/         # Streamlit UI
├── data/            # Audio files and database
└── tests/           # Unit tests
```
