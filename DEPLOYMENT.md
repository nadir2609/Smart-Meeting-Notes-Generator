# Deployment Guide

## 🚀 Deploy to Render.com (Recommended)

### Prerequisites
- GitHub account with your project pushed
- Render.com account (free)

### Steps

1. **Go to Render Dashboard**
   - Visit https://render.com
   - Sign in with GitHub
   - Authorize Render to access your repository

2. **Deploy Backend**
   - Click "New +" → "Web Service"
   - Connect your `smart-meeting-notes` repository
   - Configure:
     - **Name:** `meeting-notes-backend`
     - **Root Directory:** `backend`
     - **Environment:** `Python 3`
     - **Build Command:** `pip install -r requirements.txt`
     - **Start Command:** `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
   - Environment Variables:
     ```
     WHISPER_MODEL=tiny
     DEVICE=cpu
     DATABASE_URL=sqlite+aiosqlite:///./data/meetings.db
     ```
   - Click "Create Web Service"
   - **Copy the backend URL** (e.g., https://meeting-notes-backend.onrender.com)

3. **Deploy Frontend**
   - Click "New +" → "Web Service"
   - Select same repository
   - Configure:
     - **Name:** `meeting-notes-frontend`
     - **Root Directory:** `frontend`
     - **Environment:** `Python 3`
     - **Build Command:** `pip install -r ../requirements.txt`
     - **Start Command:** `streamlit run streamlit_app.py --server.port $PORT --server.address 0.0.0.0`
   - Environment Variable:
     ```
     API_URL=https://meeting-notes-backend.onrender.com
     ```
   - Click "Create Web Service"

4. **Update Frontend Code**
   - Edit `frontend/streamlit_app.py`
   - Change `API_URL = "http://localhost:8000"` to:
     ```python
     API_URL = os.getenv("API_URL", "http://localhost:8000")
     ```

5. **Test Your App**
   - Visit your frontend URL (e.g., https://meeting-notes-frontend.onrender.com)
   - Upload a short audio file (1-2 minutes)
   - Test transcription and summarization

### ⚠️ Important Notes

- **Cold Starts:** Free tier services sleep after 15 minutes of inactivity. First request may take 30-60 seconds.
- **Model Size:** Use `tiny` or `base` Whisper models on free tier (512MB RAM limit)
- **Audio Length:** Keep audio files under 3 minutes on free tier to avoid timeouts
- **Database:** SQLite works but consider upgrading to PostgreSQL for production

---

## 🤗 Deploy to Hugging Face Spaces (Alternative)

### Steps

1. **Create Space**
   - Go to https://huggingface.co/spaces
   - Click "Create new Space"
   - Choose "Streamlit" SDK
   - Name your space

2. **Upload Files**
   - Clone your space:
     ```bash
     git clone https://huggingface.co/spaces/YOUR_USERNAME/meeting-notes
     cd meeting-notes
     ```
   - Copy all files from `frontend/` to root
   - Copy necessary backend files
   - Create `app.py` (rename `streamlit_app.py` to `app.py`)

3. **Configure**
   - Add `requirements.txt` at root
   - Modify code to run both frontend and backend in same process

4. **Push**
   ```bash
   git add .
   git commit -m "Deploy to Hugging Face"
   git push
   ```

---

## 🌐 Deploy to Railway.app

### Steps

1. **Connect GitHub**
   - Go to https://railway.app
   - Sign in with GitHub
   - Click "New Project" → "Deploy from GitHub repo"

2. **Add Services**
   - Add "backend" service
     - Root directory: `backend`
     - Start command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
   - Add "frontend" service
     - Root directory: `frontend`
     - Start command: `streamlit run streamlit_app.py --server.port $PORT`

3. **Set Environment Variables**
   - Backend: `WHISPER_MODEL=tiny`, `DEVICE=cpu`
   - Frontend: `API_URL=<backend-url>`

4. **Deploy**
   - Railway auto-deploys on push

---

## 💡 Cost Comparison

| Platform | Free Tier | Cold Starts | RAM | Storage |
|----------|-----------|-------------|-----|---------|
| Render | 750h/month | Yes (15min) | 512MB | 1GB |
| Railway | $5 credit/month | No | 512MB | 1GB |
| HF Spaces | Unlimited | No | 2GB | 50GB |
| Streamlit Cloud | Unlimited | No | 1GB | 1GB |

---

## 🔧 Production Recommendations

For serious production use, consider:

1. **Upgrade to Paid Tier** ($7-25/month)
   - No cold starts
   - More RAM (1-4GB)
   - Faster processing

2. **Use PostgreSQL** instead of SQLite
   - Better for concurrent users
   - Render provides free PostgreSQL

3. **Add Redis Caching**
   - Cache transcriptions
   - Faster repeated requests

4. **CDN for Assets**
   - Use Cloudflare or similar
   - Faster page loads

5. **Monitoring**
   - Set up error tracking (Sentry)
   - Performance monitoring
