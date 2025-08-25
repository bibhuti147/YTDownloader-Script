from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from pytubefix import YouTube
from pytubefix.cli import on_progress
import os

app = FastAPI()

app.mount("/videos", StaticFiles(directory="Download"), name="videos")


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/yurl/{url}")
def get_video(url: str):
    url = f'https://www.youtube.com/watch?v={url}'
    yt = YouTube(url, on_progress_callback=on_progress)
    stream = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()
    os.makedirs("Download", exist_ok=True)
    filepath = stream.download("Download")
    
    filename = os.path.basename(filepath)
     
    video_url = f"/videos/{filename}"
    
    return {"video_url": video_url}