from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import StreamingResponse
from pytubefix import YouTube
from pytubefix.cli import on_progress
from fastapi.middleware.cors import CORSMiddleware
import io
import traceback

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://youtube-video-downloader-spa.vercel.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/download-video")
async def download_video(request: Request):
    data = await request.json()
    yt_url = data.get("url")
    if not yt_url:
        raise HTTPException(status_code=400, detail="Missing YouTube URL")

    try:
        yt = YouTube(yt_url, on_progress_callback=on_progress, client="WEB", use_po_token=True)
        stream = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()

        if not stream:
            raise HTTPException(status_code=404, detail="No suitable stream found")

        buffer = io.BytesIO()
        stream.stream_to_buffer(buffer)
        buffer.seek(0)

        
        filename = "".join(c if c.isalnum() or c in "._-" else "_" for c in yt.title) + ".mp4"

        headers = {"Content-Disposition": f"attachment; filename={filename}"}
        return StreamingResponse(buffer, media_type="video/mp4", headers=headers)
    
    except Exception as e:
        print("ERROR:", str(e))
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Error downloading video: {str(e)}")