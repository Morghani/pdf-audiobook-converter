from fastapi import FastAPI, UploadFile, Form
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
import os
from dotenv import load_dotenv
import fitz  # PyMuPDF
from gtts import gTTS
import openai
import uuid

app = FastAPI()
load_dotenv()

# إعدادات
openai.api_key = os.getenv("OPENAI_API_KEY")
USE_GPT_ONLY = os.getenv("USE_GPT_ONLY", "false").lower() == "true"
DEFAULT_VOICE = os.getenv("DEFAULT_VOICE", "nova")

# تخزين الملفات الصوتية المؤقتة
AUDIO_DIR = "generated"
os.makedirs(AUDIO_DIR, exist_ok=True)

# تقديم ملفات الواجهة
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
async def homepage():
    with open("static/index.html", "r", encoding="utf-8") as f:
        return HTMLResponse(content=f.read())

@app.post("/upload-pdf/")
async def upload_pdf(file: UploadFile, voice: str = Form(DEFAULT_VOICE)):
    contents = await file.read()
    doc = fitz.open(stream=contents, filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text()

    word_count = len(text.split())
    if not text.strip():
        return {"error": "PDF has no readable text."}

    filename = f"{AUDIO_DIR}/{uuid.uuid4()}.mp3"

    try:
        if USE_GPT_ONLY:
            response = openai.audio.speech.create(
                model="tts-1",
                voice=voice,
                input=text
            )
            with open(filename, "wb") as f:
                f.write(response.content)
        else:
            raise Exception("Fallback to gTTS")  # Trigger fallback
    except Exception:
        tts = gTTS(text)
        tts.save(filename)

    return FileResponse(filename, media_type="audio/mpeg", filename="output.mp3")
