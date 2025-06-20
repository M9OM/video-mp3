import os
import shutil
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
import ffmpeg
from tempfile import NamedTemporaryFile

app = FastAPI()
# CORS middleware to allow requests from frontend

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change to your frontend domain in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/convert-video-to-mp3")
async def convert_video_to_mp3(file: UploadFile = File(...)):
    # Save uploaded video temporarily
    suffix = os.path.splitext(file.filename)[1]
    with NamedTemporaryFile(delete=False, suffix=suffix) as temp_video:
        shutil.copyfileobj(file.file, temp_video)
        video_path = temp_video.name

    # Output MP3 path
    mp3_path = video_path.rsplit(".", 1)[0] + ".mp3"

    try:
        # Convert video to mp3 using ffmpeg
        ffmpeg.input(video_path).output(mp3_path, format='mp3', acodec='libmp3lame', audio_bitrate='192k').run(overwrite_output=True)
    except Exception as e:
        return {"error": f"Failed to convert: {str(e)}"}

    return FileResponse(mp3_path, filename=os.path.basename(mp3_path), media_type="audio/mpeg")
