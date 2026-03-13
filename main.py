import os
from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, JSONResponse
from transmission_rpc import Client

app = FastAPI()
templates = Jinja2Templates(directory="templates")

TRANSMISSION_HOST = os.getenv("TRANSMISSION_HOST", "localhost")
TRANSMISSION_PORT = int(os.getenv("TRANSMISSION_PORT", "9091"))
# DOWNLOAD_DIR = os.getenv("DOWNLOAD_DIR", "/mnt/usbdrive")
# DOWNLOAD_DIR = os.getenv("DOWNLOAD_DIR", "/home/sergio/Downloads/torrents")
def get_client():
    return Client(host=TRANSMISSION_HOST, port=TRANSMISSION_PORT, username='sergio', password='a')


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/add")
async def add_torrent(link: str = Form(...)):
    try:
        client = get_client()
        # client.add_torrent(link, download_dir=DOWNLOAD_DIR)
        client.add_torrent(link)
        return JSONResponse({"status": "ok", "message": "Torrent added successfully."})
    except Exception as e:
        return JSONResponse({"status": "error", "message": str(e)}, status_code=500)


@app.get("/torrents")
async def list_torrents():
    try:
        client = get_client()
        torrents = client.get_torrents()
        result = []
        for t in torrents:
            result.append({
                "id": t.id,
                "name": t.name,
                "status": t.status,
                "progress": round(t.progress, 1),
                "size": t.total_size,
                "download_speed": t.rate_download,
            })
        return JSONResponse({"status": "ok", "torrents": result})
    except Exception as e:
        return JSONResponse({"status": "error", "message": str(e)}, status_code=500)


@app.delete("/torrent/{torrent_id}")
async def remove_torrent(torrent_id: int, delete_data: bool = False):
    try:
        client = get_client()
        client.remove_torrent(torrent_id, delete_data=delete_data)
        return JSONResponse({"status": "ok", "message": "Torrent removed."})
    except Exception as e:
        return JSONResponse({"status": "error", "message": str(e)}, status_code=500)
