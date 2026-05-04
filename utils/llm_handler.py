import os
import json
import re
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

class LLMHandler:
    def __init__(self):
        api_key = os.environ.get("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY environment variable not set!")
        self.client = OpenAI(api_key=api_key)
        self.model = "gpt-4o-mini"

    def _call_llm(self, system_prompt: str, user_prompt: str, max_tokens: int = 2000) -> str:
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            max_tokens=max_tokens,
            temperature=0.3
        )
        return response.choices[0].message.content

    def _get_language_instruction(self, language: str) -> str:
        instructions = {
            "english": "Respond in clear, simple English.",
            "urdu": "صرف اردو میں جواب دیں۔ آسان اردو استعمال کریں۔",
            "roman_urdu": "Sirf Roman Urdu mein jawab do. English bilkul mat use karo. Jaise: 'Yeh topic bohot important hai kyunki...'"
        }
        return instructions.get(language, instructions["english"])

    def answer_question(self, question: str, context: str, language: str, video_title: str, history: list = []) -> str:
        lang_instruction = self._get_language_instruction(language)

        system_prompt = f"""You are LectureLens AI, an intelligent study assistant.
You ONLY answer based on the video transcript provided.
If the answer is not in the transcript, say "This information is not covered in the video."
{lang_instruction}"""

        messages = [{"role": "system", "content": system_prompt}]

        for msg in history[-6:]:
            messages.append({"role": msg["role"], "content": msg["content"]})

        messages.append({
            "role": "user",
            "content": f"""Video: "{video_title}"
Relevant transcript:
{context}
Question: {question}"""
        })

        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            max_tokens=2000,
            temperature=0.3
        )
        return response.choices[0].message.content

    def summarize(self, transcript: str, language: str, video_title: str) -> str:
        lang_instruction = self._get_language_instruction(language)
        transcript_excerpt = transcript[:6000]

        system_prompt = f"""You are LectureLens AI, an expert at creating educational summaries.
{lang_instruction}
Create well-structured, comprehensive summaries that help students understand key concepts."""

        user_prompt = f"""Create a detailed summary of this lecture: "{video_title}"

Transcript:
{transcript_excerpt}

Please include:
1. Main Topic Overview
2. Key Concepts Covered (with brief explanations)
3. Important Points to Remember
4. Conclusion

Format it clearly with headings."""

        return self._call_llm(system_prompt, user_prompt, max_tokens=2500)

    def generate_flashcards(self, transcript: str, language: str, video_title: str) -> list:
        lang_instruction = self._get_language_instruction(language)
        transcript_excerpt = transcript[:5000]

        system_prompt = f"""You are LectureLens AI. Generate educational flashcards.
{lang_instruction}
IMPORTANT: Return ONLY valid JSON, no other text.
Format: [{{"question": "...", "answer": "..."}}]"""

        user_prompt = f"""Create 10 flashcards from this lecture: "{video_title}"

Transcript:
{transcript_excerpt}

Return ONLY a JSON array of flashcards with "question" and "answer" fields.
Make questions test understanding, not just memory."""

        response = self._call_llm(system_prompt, user_prompt, max_tokens=2000)

        try:
            json_match = re.search(r'\[.*\]', response, re.DOTALL)
            if json_match:
                cards = json.loads(json_match.group())
                return cards
        except:
            pass

        return [{"question": "What is the main topic of this lecture?",
                 "answer": "Please refer to the summary for the main topics covered."}]

    def generate_notes(self, transcript: str, language: str, video_title: str) -> list:
        lang_instruction = self._get_language_instruction(language)
        transcript_excerpt = transcript[:5000]

        system_prompt = f"""You are LectureLens AI. Generate concise sticky notes for studying.
{lang_instruction}
IMPORTANT: Return ONLY valid JSON, no other text.
Format: [{{"title": "...", "content": "...", "color": "yellow|blue|green|pink|purple"}}]"""

        user_prompt = f"""Create 8 sticky notes from this lecture: "{video_title}"

Transcript:
{transcript_excerpt}

Return ONLY a JSON array. Each note should have:
- title: short topic name (3-5 words)
- content: key information (2-3 sentences)
- color: one of yellow, blue, green, pink, purple"""

        response = self._call_llm(system_prompt, user_prompt, max_tokens=2000)

        try:
            json_match = re.search(r'\[.*\]', response, re.DOTALL)
            if json_match:
                notes = json.loads(json_match.group())
                return notes
        except:
            pass

        return [{"title": "Key Point", "content": "Process the video to see notes.", "color": "yellow"}]

    def generate_flowchart(self, transcript: str, language: str, video_title: str) -> dict:
        lang_instruction = self._get_language_instruction(language)
        transcript_excerpt = transcript[:5000]

        system_prompt = f"""You are LectureLens AI. Generate flowchart data for lecture content.
{lang_instruction}
IMPORTANT: Return ONLY valid JSON, no other text.
Format: {{"title": "...", "nodes": [{{"id": "1", "label": "...", "type": "start|process|decision|end"}}], "edges": [{{"from": "1", "to": "2", "label": ""}}]}}"""

        user_prompt = f"""Create a flowchart showing the main concepts and flow of: "{video_title}"

Transcript:
{transcript_excerpt}

Return ONLY a JSON object with nodes and edges showing how concepts connect.
Use 8-12 nodes maximum."""

        response = self._call_llm(system_prompt, user_prompt, max_tokens=2000)

        try:
            json_match = re.search(r'\{.*\}', response, re.DOTALL)
            if json_match:
                flowchart = json.loads(json_match.group())
                return flowchart
        except:
            pass

        return {
            "title": video_title,
            "nodes": [
                {"id": "1", "label": "Video Start", "type": "start"},
                {"id": "2", "label": "Main Content", "type": "process"},
                {"id": "3", "label": "Key Concepts", "type": "process"},
                {"id": "4", "label": "Conclusion", "type": "end"}
            ],
            "edges": [
                {"from": "1", "to": "2", "label": ""},
                {"from": "2", "to": "3", "label": ""},
                {"from": "3", "to": "4", "label": ""}
            ]
        }

    def generate_quiz(self, transcript: str, language: str, video_title: str) -> list:
        lang_instruction = self._get_language_instruction(language)
        transcript_excerpt = transcript[:5000]

        system_prompt = f"""You are LectureLens AI. Generate MCQ quiz questions.
{lang_instruction}
IMPORTANT: Return ONLY a valid JSON array. No markdown, no backticks, no explanation.
Exact format: [{{"question":"...","options":["A) ...","B) ...","C) ...","D) ..."],"correct":"A"}}]"""

        user_prompt = f"""Create 5 MCQ questions from: "{video_title}"
Transcript: {transcript_excerpt}
Return ONLY JSON array, nothing else."""

        try:
            response = self._call_llm(system_prompt, user_prompt, max_tokens=2000)
            clean = re.sub(r'```json|```', '', response).strip()
            try:
                return json.loads(clean)
            except:
                json_match = re.search(r'\[.*\]', clean, re.DOTALL)
                if json_match:
                    return json.loads(json_match.group())
        except Exception as e:
            print(f"Quiz error: {str(e)}")
        return []

    def compare_videos(self, transcript1: str, title1: str, transcript2: str, title2: str, language: str) -> str:
        lang_instruction = self._get_language_instruction(language)
        system_prompt = f"""You are LectureLens AI. Compare two lecture videos.
{lang_instruction}"""
        user_prompt = f"""Compare these two lectures:

Video 1: "{title1}"
{transcript1[:3000]}

Video 2: "{title2}"
{transcript2[:3000]}

Include:
1. Common Topics
2. Unique Points in Video 1
3. Unique Points in Video 2
4. Which is better for beginners?"""
        return self._call_llm(system_prompt, user_prompt, max_tokens=2000)

    def check_educational(self, transcript: str, title: str = "") -> bool:

        # Only clearly non-educational, specific reject keywords (removed ambiguous ones like 'tail', 'subscribe', 'game', 'travel', etc.)
        reject_keywords = [
            'recipe', 'ingredient', 'tablespoon', 'teaspoon',
            'karahi', 'biryani', 'gosht', 'daal',
            'pakana', 'namak', 'mirch', 'aata', 'maida',
            'drama serial', 'tv episode', 'breaking news',
            'song lyrics', 'music video', 'singer',
            'makeup tutorial', 'skincare routine', 'fashion haul',
            'funny prank', 'prank video', 'comedy skit',
            'gameplay', 'game review', 'streamer',
            'reaction video', 'review karte hain',
        ]

        accept_keywords = [
            'lecture', 'lesson', 'chapter', 'topic', 'concept', 'definition',
            'theory', 'algorithm', 'programming', 'code', 'function',
            'mathematics', 'math', 'physics', 'chemistry', 'biology',
            'history', 'geography', 'economics', 'psychology',
            'tutorial', 'course', 'university', 'college', 'school',
            'exam', 'assignment', 'hypothesis', 'equation', 'formula',
            'theorem', 'proof', 'data', 'analysis', 'research',
            'python', 'javascript', 'machine learning', 'artificial intelligence',
            'database', 'network', 'compiler', 'accounting', 'finance',
            'explain', 'understand', 'learn', 'study', 'education',
            'parh', 'seekhna', 'samajhna', 'taleem', 'ilm',
            'class', 'teacher', 'student', 'syllabus', 'notes',
        ]

        text = (transcript[:3000] + " " + title).lower()

        reject_count = sum(1 for kw in reject_keywords if kw in text)
        accept_count = sum(1 for kw in accept_keywords if kw in text)

        # Only reject if clearly non-educational AND no educational signals present
        if reject_count >= 3 and accept_count == 0:
            return False

        # Accept if any educational signal exists
        if accept_count >= 1:
            return True

        # Fall back to LLM — skip intro by starting at char 500, use more context
        try:
            system_prompt = """Strict classifier. Return ONLY 'yes' or 'no'.
'yes' for: university lecture, school lesson, coding tutorial, academic subject, professional skill training, educational explainer.
'no' for: cooking recipe, drama, music video, vlog, breaking news, cartoon, gameplay, fashion haul, comedy prank."""
            user_prompt = f"Title: {title}\nTranscript: {transcript[500:2500]}\nIs this educational? yes or no only."
            response = self._call_llm(system_prompt, user_prompt, max_tokens=5)
            return 'yes' in response.lower().strip()
        except:
            # Default to True if classifier fails — better to allow than wrongly block
            return True