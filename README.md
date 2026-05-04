---
title: LectureLens AI
emoji: 🔬
colorFrom: indigo
colorTo: pink
sdk: docker
pinned: false
---

# 🔬 LectureLens AI — Study Smarter, Learn Deeper

LectureLens AI is an intelligent study assistant that transforms any YouTube lecture into a full learning toolkit. Paste a lecture URL and instantly get summaries, flashcards, sticky notes, quizzes, flowcharts, and an AI-powered Q&A — all in English, Urdu, or Roman Urdu.

---

## ✨ Features

- **📝 Smart Summary** — Structured overview with key concepts, important points, and conclusion
- **🃏 Flashcards** — Auto-generated Q&A cards to test your understanding
- **🗒️ Sticky Notes** — Color-coded bite-sized notes for quick revision
- **🧠 Flowchart** — Visual concept map showing how ideas connect
- **❓ Quiz** — 5 MCQ questions with instant scoring
- **💬 AI Chat** — Ask anything about the lecture and get context-aware answers
- **🔁 Compare Videos** — Side-by-side comparison of two lectures
- **📄 PDF Export** — Download your summary or notes as a PDF
- **🌐 Multilingual** — Supports English, Urdu (اردو), and Roman Urdu

---

## 🚀 How to Use

1. Paste a YouTube lecture URL into the input box
2. Click **Analyze Video** and wait a few seconds
3. Use the tabs to explore Summary, Flashcards, Notes, Quiz, Flowchart, or Chat
4. Switch language using the buttons in the top right corner

> ⚠️ Only educational lecture videos are supported. Cooking, drama, music, and vlog videos will be rejected automatically.

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python, Flask |
| LLM | GPT-4o Mini (OpenAI) |
| Transcript | youtube-transcript-api |
| Search | TF-IDF (scikit-learn) |
| PDF Export | ReportLab |
| Deployment | Hugging Face Spaces (Docker) |

---

## 🌍 Supported Languages

- 🇬🇧 **English**
- 🇵🇰 **Urdu** (اردو)
- 🇵🇰 **Roman Urdu** (e.g., "Yeh concept bohot important hai")

---

## ⚙️ Environment Variables

If you are self-hosting, set the following secrets:

| Variable | Description |
|---|---|
| `OPENAI_API_KEY` | Your OpenAI API key (from platform.openai.com) |
| `SECRET_KEY` | Any random string for Flask session security |

---

## 📌 Limitations

- Only YouTube videos with available captions/transcripts are supported
- Transcript quality depends on the video's auto-generated or manual captions
- Very long videos may be truncated for summarization (first ~6000 characters used)

---

## 👩‍💻 Author

Built By: Esha
[LinkedIn](linkedin.com/in/esha-099241313/)
Feel free to fork, improve, and share!