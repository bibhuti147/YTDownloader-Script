from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from pytubefix import YouTube
from pytubefix.cli import on_progress
from fastapi.middleware.cors import CORSMiddleware
import io

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://youtube-video-downloader-spa.vercel.app/"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/yurl/{url}")
async def get_video(url: str):
    url = f'https://www.youtube.com/watch?v={url}'

    try:
        yt = YouTube(url, on_progress_callback=on_progress)
        stream = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()
        buffer = io.BytesIO()
        stream.stream_to_buffer(buffer)
        buffer.seek(0)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error downloading video: {str(e)}")
    
    filename = yt.title.replace(" ","_") + ".mp4"

    headers = {
        "Content-Disposition": f"attachment; filename={filename}"
    }

    return StreamingResponse(buffer, media_type="video/mp4",headers=headers)