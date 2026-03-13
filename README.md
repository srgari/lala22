# Torrent Manager

This is Sergio's personal torrent management web app, built for fun as his first vibe-coding project. He described what he wanted; I (Claude Code) wrote the code. He watched in mild disbelief. It went well.

So far, he's happy with how it's evolving — but he's stubborn: he's going to stop, read every line, and actually understand what was built before going further. Priorities first though — README today (also written by me, let's be honest), make Transmission work tomorrow, then deploy to the Raspberry Pi, *then* study time.

---

## What It Does

A minimal dark-themed web interface that lets you:

- Paste a **magnet link** or torrent URL and kick off a download
- See all active torrents with **name, status, progress bar, speed, and size**
- **Remove** a torrent with one click
- The list auto-refreshes every 5 seconds, no page reload needed

Under the hood, the UI talks to a **FastAPI** backend, which talks to **Transmission** (a torrent client) via its RPC interface.

---

## Stack

| Layer | Technology |
|---|---|
| Web UI | HTML + CSS + vanilla JS |
| Backend API | Python / FastAPI |
| ASGI server | Uvicorn |
| Torrent engine | Transmission (external daemon) |
| RPC bridge | `transmission-rpc` Python library |
| Templating | Jinja2 |
| Container | Docker + Docker Compose |

---

## Project Structure

```
lala22/
├── main.py                # FastAPI app — all the API endpoints
├── requirements.txt       # Python dependencies
├── Dockerfile             # Container image definition
├── docker-compose.yml     # Service orchestration
└── templates/
    └── index.html         # The entire frontend (one file, dark mode, clean)
```

---

## How It Works

### API Endpoints

| Method | Path | What it does |
|---|---|---|
| `GET` | `/` | Serves the web UI |
| `POST` | `/add` | Adds a torrent (form field: `link`) |
| `GET` | `/torrents` | Returns list of all torrents as JSON |
| `DELETE` | `/torrent/{id}` | Removes a torrent by ID |

### Configuration

The app is configured via environment variables:

| Variable | Default | Description |
|---|---|---|
| `TRANSMISSION_HOST` | `localhost` | Host where Transmission is running |
| `TRANSMISSION_PORT` | `9091` | Transmission RPC port |
| `DOWNLOAD_DIR` | `/mnt/usbdrive` | Where downloaded files go |

In `docker-compose.yml`, the container uses `network_mode: host` so it can reach a Transmission daemon running on the host machine directly.

---

## Running It

### Prerequisites

- Docker and Docker Compose installed
- Transmission daemon running and accessible (port 9091)

### Start the container

```bash
docker compose up --build
```

The web interface will be available at `http://localhost:8000`.

### Development (without Docker)

```bash
pip install -r requirements.txt
uvicorn main:app --reload
```

---

## Target Deployment: Raspberry Pi 3

The end goal is to run this on a Raspberry Pi 3 (`192.168.0.178`) connected to a USB drive mounted at `/mnt/usbdrive`. Transmission will run on the Pi, and downloads will go straight to the USB drive.

**Status:** work in progress. Transmission integration needs to be sorted out first, then the container gets deployed to the Pi.

---

## Current Status

- [x] FastAPI backend working
- [x] Web UI built and looking decent
- [x] Docker container defined
- [ ] Transmission download confirmed working
- [ ] Deployed and running on Raspberry Pi 3
- [ ] Sergio has actually read all the code he asked Claude to write

---

*Built with Claude Code. I asked, it built. I'm not sure how I feel about that, but I like the result.*
