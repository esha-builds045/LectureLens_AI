# 🔬 LectureLens AI — Complete Setup Guide

## 📁 Project Structure
lecturelens/
├── app.py                    # Main Flask app + all API routes
├── requirements.txt          # All Python dependencies
├── Dockerfile               # HuggingFace deployment config
├── .env                     # API keys (NEVER upload this!)
├── .gitignore               # Tells git to ignore .env
├── README.md                # Project documentation
├── SETUP_GUIDE.md           # This file
├── templates/
│   └── index.html           # Complete frontend UI
└── utils/
├── init.py          # Package init
├── transcript_handler.py # YouTube transcript + title extraction
├── embedder.py          # TF-IDF search engine
└── llm_handler.py       # GPT-4o-mini — all AI features

---

## 🔑 API Keys Required

### OpenAI API Key (Only One Required!)
1. Go to: https://platform.openai.com
2. Sign up / Login
3. Click "API Keys" → "Create new secret key"
4. Copy your key (starts with `sk-`)

---

## 🖥️ Local Setup

### Step 1: Install Python
Download from: https://python.org (Python 3.10+)

### Step 2: Download Project
Download and extract the project folder

### Step 3: Create Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Mac/Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 4: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 5: Create `.env` File
Create a file named `.env` in the project root:
OPENAI_API_KEY=sk-your-key-here
SECRET_KEY=lecturelens-secret-2024

### Step 6: Create `.gitignore` File
.env
pycache/
*.pyc
venv/

### Step 7: Run the App
```bash
python app.py
```

### Step 8: Open Browser
http://localhost:7860

---

## 🎯 How to Use

### 1. Process a Video
- Paste any YouTube lecture URL
- Click "Analyze Video"
- Wait for transcript extraction

### 2. Generate Study Material
- Click **Summary** → Generate ✨ → Get comprehensive summary
- Click **Flashcards** → Generate ✨ → Get 10 Q&A cards
- Click **Sticky Notes** → Generate ✨ → Get 8 key point notes
- Click **Flowchart** → Generate ✨ → Get concept map
- Click **Quiz** → Generate ✨ → Get 5 MCQ questions

### 3. Chat with AI
- Type any question about the lecture
- AI answers strictly based on video content
- Previous questions are remembered in conversation

### 4. Export Content
- Click 📄 PDF button on any panel to download
- Click 📋 Copy button to copy to clipboard

### 5. Compare Videos
- Go to Compare tab
- Enter second YouTube URL
- Click Compare ✨

### 6. Change Language
- Click English / اردو / Roman Urdu buttons at top
- All generated content will be in selected language

---

## 🌐 How It Works — Technical Flow
User enters YouTube URL
↓
youtube-transcript-api → extracts captions (free)
↓
yt-dlp → fetches video title (free)
↓
TF-IDF (scikit-learn) → splits into chunks, builds search index (free, local)
↓
User asks question / clicks Generate
↓
TF-IDF → finds most relevant transcript chunks
↓
GPT-4o-mini → generates answer from chunks (paid, ~$0.01/session)
↓
Response shown in UI

---

## 📚 Libraries Explained

| Library | Purpose | Cost |
|---------|---------|------|
| `flask` | Web server + API endpoints | FREE |
| `youtube-transcript-api` | Extract YouTube captions | FREE |
| `yt-dlp` | Fetch video title | FREE |
| `scikit-learn` | TF-IDF text search | FREE |
| `openai` | GPT-4o-mini AI responses | ~$0.01/session |
| `reportlab` | PDF generation | FREE |
| `python-dotenv` | Load .env API keys | FREE |
| `gunicorn` | Production server | FREE |

---

## 🚀 Deploy to HuggingFace Spaces (FREE Hosting)

### Step 1: Create HuggingFace Account
Go to: https://huggingface.co — sign up free

### Step 2: Create New Space
1. Click profile → "New Space"
2. Name: `lecturelens-ai`
3. SDK: **Docker**
4. Visibility: Public (free)
5. Click "Create Space"

### Step 3: Upload Files
Upload all project files EXCEPT `.env` file

### Step 4: Add Secret Key
1. Go to Space → Settings → Repository Secrets
2. Add:
   - Name: `OPENAI_API_KEY`
   - Value: `sk-your-key-here`

### Step 5: Deploy
HuggingFace automatically builds and deploys!

Your app: `https://huggingface.co/spaces/YOUR_USERNAME/lecturelens-ai`

---

## ❌ Common Errors & Fixes

| Error | Fix |
|-------|-----|
| `No transcript found` | Video does not have captions enabled |
| `OPENAI_API_KEY not set` | Check .env file |
| `Module not found` | Run `pip install -r requirements.txt` |
| `Port already in use` | Change port in app.py or kill existing process |
| `Invalid YouTube URL` | Make sure URL has `watch?v=` or `youtu.be/` |

---

## ⚠️ Important Notes

- Never upload `.env` file to GitHub or HuggingFace
- Videos must have captions/subtitles enabled
- Session data resets when server restarts
- Supports English, Hindi, Urdu transcripts
- AI answers strictly based on video content only

---

## 💰 Cost

| Component | Cost |
|-----------|------|
| Everything except OpenAI | FREE |
| OpenAI GPT-4o-mini | ~$0.01 per lecture session |
| HuggingFace hosting | FREE |
| **Total per session** | **~$0.01** |

---

