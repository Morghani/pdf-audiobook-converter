import os
import uuid
from fastapi import FastAPI, UploadFile, Form
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from dotenv import load_dotenv
from PyPDF2 import PdfReader
from gtts import gTTS
import openai

load_dotenv()

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
USE_GPT_ONLY = os.getenv("USE_GPT_ONLY", "false").lower() == "true"
DEFAULT_VOICE = os.getenv("DEFAULT_VOICE", "nova")

if OPENAI_API_KEY:
    openai.api_key = OPENAI_API_KEY


def extract_text_from_pdf(file_path):
    reader = PdfReader(file_path)
    return "\n".join(page.extract_text() or "" for page in reader.pages)


def synthesize_with_openai(text, voice):
    response = openai.audio.speech.create(
        model="tts-1",
        voice=voice,
        input=text
    )
    filename = f"generated/{uuid.uuid4()}.mp3"
    with open(filename, "wb") as f:
        f.write(response.content)
    return filename


def synthesize_with_gtts(text):
    tts = gTTS(text)
    filename = f"generated/{uuid.uuid4()}.mp3"
    tts.save(filename)
    return filename


@app.get("/")
async def home():
    return FileResponse("static/index.html")


@app.post("/upload-pdf/")
async def upload_pdf(file: UploadFile, voice: str = Form(DEFAULT_VOICE)):
    contents = await file.read()
    tmp_path = f"tmp_{uuid.uuid4()}.pdf"
    with open(tmp_path, "wb") as f:
        f.write(contents)

    try:
        text = extract_text_from_pdf(tmp_path)
        text = text[:4096]
        if OPENAI_API_KEY and USE_GPT_ONLY:
            audio_path = synthesize_with_openai(text, voice)
        else:
            try:
                audio_path = synthesize_with_openai(text, voice)
            except Exception:
                audio_path = synthesize_with_gtts(text)
    finally:
        os.remove(tmp_path)

    return FileResponse(audio_path, media_type="audio/mpeg", filename="output.mp3")
