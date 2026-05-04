from flask import Flask, request, jsonify, render_template, session
from utils.transcript_handler import get_transcript
from utils.embedder import EmbeddingHandler
from utils.llm_handler import LLMHandler
import os
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from io import BytesIO
from flask import send_file
import uuid
from dotenv import load_dotenv 
load_dotenv()                   

from flask import Flask, request, jsonify, render_template, session
# ... baaki code same rehega

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "lecturelens-secret-2024")

embedding_handler = EmbeddingHandler()
llm_handler = LLMHandler()

# In-memory session store (use Redis in production)
sessions = {}

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/process", methods=["POST"])
def process_video():
    data = request.get_json()
    url = data.get("url", "").strip()
    
    if not url:
        return jsonify({"error": "YouTube URL required"}), 400
    
    try:
        # Extract transcript
        transcript_data = get_transcript(url)
        if not transcript_data["success"]:
            return jsonify({"error": transcript_data["error"]}), 400
        
        transcript_text = transcript_data["transcript"]
        video_title = transcript_data.get("title", "YouTube Video")
        
        # Create embeddings and store
        session_id = str(uuid.uuid4())
        is_educational = llm_handler.check_educational(transcript_text, video_title)
        if not is_educational:
           return jsonify({
        "error": "⚠️ This video does not appear to be an educational lecture. Please provide a study or lecture video!"
    }), 400
        embedding_handler.process_and_store(transcript_text, session_id)
        
        # Store session info
        sessions[session_id] = {
           "transcript": transcript_text,
           "title": video_title,
           "url": url,
           "messages": []  # ✅ Chat history yahan save hogi
}
        
        
        return jsonify({
            "success": True,
            "session_id": session_id,
            "title": video_title,
            "transcript": transcript_text,
            "transcript_length": len(transcript_text),
            # "video_id": video_id, 
            "message": "Video processed successfully!"
        })
        
 
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/chat", methods=["POST"])
def chat():
    data = request.get_json()
    session_id = data.get("session_id")
    question = data.get("question", "").strip()
    language = data.get("language", "english")
    
    if not session_id or session_id not in sessions:
        return jsonify({"error": "Invalid session. Please process a video first."}), 400
    
    if not question:
        return jsonify({"error": "Question cannot be empty"}), 400
    
    try:
        # Retrieve relevant chunks
        relevant_chunks = embedding_handler.retrieve(question, session_id)
        
        # History mein question add karo
        sessions[session_id]["messages"].append({
            "role": "user",
            "content": question
        })

        # Generate answer
        answer = llm_handler.answer_question(
            question=question,
            context=relevant_chunks,
            language=language,
            video_title=sessions[session_id]["title"],
            history=sessions[session_id]["messages"]
        )

        # History mein answer save karo
        sessions[session_id]["messages"].append({
            "role": "assistant",
            "content": answer
        })
        
        return jsonify({"success": True, "answer": answer})
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/summarize", methods=["POST"])
def summarize():
    data = request.get_json()
    session_id = data.get("session_id")
    language = data.get("language", "english")
    
    if not session_id or session_id not in sessions:
        return jsonify({"error": "Invalid session"}), 400
    
    try:
        transcript = sessions[session_id]["transcript"]
        title = sessions[session_id]["title"]
        summary = llm_handler.summarize(transcript, language, title)
        return jsonify({"success": True, "summary": summary})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/flashcards", methods=["POST"])
def flashcards():
    data = request.get_json()
    session_id = data.get("session_id")
    language = data.get("language", "english")
    
    if not session_id or session_id not in sessions:
        return jsonify({"error": "Invalid session"}), 400
    
    try:
        transcript = sessions[session_id]["transcript"]
        title = sessions[session_id]["title"]
        cards = llm_handler.generate_flashcards(transcript, language, title)
        return jsonify({"success": True, "flashcards": cards})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/notes", methods=["POST"])
def sticky_notes():
    data = request.get_json()
    session_id = data.get("session_id")
    language = data.get("language", "english")
    
    if not session_id or session_id not in sessions:
        return jsonify({"error": "Invalid session"}), 400
    
    try:
        transcript = sessions[session_id]["transcript"]
        title = sessions[session_id]["title"]
        notes = llm_handler.generate_notes(transcript, language, title)
        return jsonify({"success": True, "notes": notes})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/flowchart", methods=["POST"])
def flowchart():
    data = request.get_json()
    session_id = data.get("session_id")
    language = data.get("language", "english")
    
    if not session_id or session_id not in sessions:
        return jsonify({"error": "Invalid session"}), 400
    
    try:
        transcript = sessions[session_id]["transcript"]
        title = sessions[session_id]["title"]
        flowchart_data = llm_handler.generate_flowchart(transcript, language, title)
        return jsonify({"success": True, "flowchart": flowchart_data})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    



@app.route("/api/quiz", methods=["POST"])
def quiz():
    data = request.get_json()
    session_id = data.get("session_id")
    language = data.get("language", "english")
    if not session_id or session_id not in sessions:
        return jsonify({"error": "Invalid session"}), 400
    try:
        transcript = sessions[session_id]["transcript"]
        title = sessions[session_id]["title"]
        questions = llm_handler.generate_quiz(transcript, language, title)
        if not questions:
            return jsonify({"error": "Could not generate quiz. Try again!"}), 400
        return jsonify({"success": True, "questions": questions})
   
    except Exception as e:
         print(f"QUIZ ROUTE ERROR: {str(e)}")
         return jsonify({"error": str(e)}), 500
    
@app.route("/api/compare", methods=["POST"])
def compare():
    data = request.get_json()
    session_id = data.get("session_id")
    url2 = data.get("url2", "").strip()
    language = data.get("language", "english")

    if not session_id or session_id not in sessions:
        return jsonify({"error": "Invalid session"}), 400
    if not url2:
        return jsonify({"error": "Second URL required"}), 400

    try:
        transcript2 = get_transcript(url2)
        if not transcript2["success"]:
            return jsonify({"error": transcript2["error"]}), 400

        transcript1 = sessions[session_id]["transcript"]
        title1 = sessions[session_id]["title"]
        title2 = transcript2["title"]

        result = llm_handler.compare_videos(
            transcript1, title1,
            transcript2["transcript"], title2,
            language
        )
        return jsonify({"success": True, "comparison": result})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/export", methods=["POST"])
def export_pdf():
    data = request.get_json()
    session_id = data.get("session_id")
    content = data.get("content", "")
    title = data.get("title", "LectureLens Export")

    if not session_id or session_id not in sessions:
        return jsonify({"error": "Invalid session"}), 400

    try:
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter)
        styles = getSampleStyleSheet()
        story = []

        story.append(Paragraph(title, styles['Title']))
        story.append(Spacer(1, 20))

        for line in content.split('\n'):
            if line.strip():
                story.append(Paragraph(line, styles['Normal']))
                story.append(Spacer(1, 6))

        doc.build(story)
        buffer.seek(0)

        return send_file(
            buffer,
            as_attachment=True,
            download_name="lecturelens_export.pdf",
            mimetype='application/pdf'
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=7860)
