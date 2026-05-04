from youtube_transcript_api._errors import TranscriptsDisabled, NoTranscriptFound
import re
import requests
import os

def extract_video_id(url: str) -> str:
    patterns = [
        r"(?:v=|\/)([0-9A-Za-z_-]{11}).*",
        r"(?:youtu\.be\/)([0-9A-Za-z_-]{11})",
        r"(?:embed\/)([0-9A-Za-z_-]{11})",
    ]
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    return None

def get_transcript(url: str) -> dict:
    video_id = extract_video_id(url)

    if not video_id:
        return {"success": False, "error": "Invalid YouTube URL."}

    try:
        api_key = os.environ.get("SUPADATA_API_KEY")
        if not api_key:
            return {"success": False, "error": "SUPADATA_API_KEY not set!"}

        # Supadata se transcript lo
        response = requests.get(
            "https://api.supadata.ai/v1/youtube/transcript",
            params={"url": f"https://www.youtube.com/watch?v={video_id}", "text": True},
            headers={"x-api-key": api_key},
            timeout=30
        )

        if response.status_code != 200:
            error_data = response.json()
            details = error_data.get("details", error_data.get("message", "Unknown error"))
            if "unavailable" in str(details).lower():
                return {"success": False, "error": "⚠️ No transcript found. Please use a lecture video with captions!"}
            elif "live" in str(details).lower():
                return {"success": False, "error": "⚠️ Live streams not supported!"}
            else:
                return {"success": False, "error": f"⚠️ {details}"}

        data = response.json()

        # Transcript text join karo
        content = data.get("content", "")
        if isinstance(content, list):
            full_transcript = " ".join([
                item.get("text", "") if isinstance(item, dict) else str(item)
                for item in content
            ])
        else:
            full_transcript = str(content)

        full_transcript = clean_transcript(full_transcript)

        if not full_transcript.strip():
            return {"success": False, "error": "⚠️ Transcript empty or not available."}

        # Video title lo
        try:
            title_response = requests.get(
                "https://api.supadata.ai/v1/youtube/video",
                params={"url": f"https://www.youtube.com/watch?v={video_id}"},
                headers={"x-api-key": api_key},
                timeout=15
            )
            if title_response.status_code == 200:
                video_title = title_response.json().get("title", f"Video {video_id}")
            else:
                video_title = f"Video {video_id}"
        except:
            video_title = f"Video {video_id}"

        return {
            "success": True,
            "transcript": full_transcript,
            "title": video_title,
            "video_id": video_id,
        }

    except Exception as e:
        return {"success": False, "error": f"⚠️ Error: {str(e)}"}


def clean_transcript(text: str) -> str:
    text = re.sub(r'\[.*?\]', '', text)
    text = re.sub(r'\(.*?\)', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    text = text.replace('♪', '').replace('♫', '')
    return text


def chunk_transcript(transcript: str, chunk_size: int = 500, overlap: int = 50) -> list:
    words = transcript.split()
    chunks = []
    for i in range(0, len(words), chunk_size - overlap):
        chunk = " ".join(words[i:i + chunk_size])
        if chunk:
            chunks.append(chunk)
    return chunks