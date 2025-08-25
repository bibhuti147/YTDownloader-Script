from fastapi import FastAPI
from pytubefix import YouTube
from pytubefix.cli import on_progress 

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/yurl/{url}")
def get_video(url: str):
    url = f'https://www.youtube.com/watch?v={url}'
    yt = YouTube(url, on_progress_callback=on_progress)
    stream = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()
    stream.download('./Download') 