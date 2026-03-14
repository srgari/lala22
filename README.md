# Torrent Manager

This is Sergio's personal torrent management web app, built for fun as his first vibe-coding project. He described what he wanted; I (Claude Code) wrote the code. He watched in mild disbelief. It went well.

So far, he's happy with how it's evolving — and it's now deployed and running on the Raspberry Pi.

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
├── .dockerignore          # Keeps venv and cache out of the image
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

> **Note on download directory:** Transmission's download folder is configured directly on the host machine via `settings.json` — not via the app. On the Raspberry Pi, `download-dir` is set to `/mnt/usbdrive` in Transmission's config.

> **Note on authentication:** `rpc-authentication-required` must be set to `false` in Transmission's `settings.json` (Transmission must be stopped before editing the file, otherwise it overwrites changes on exit).

In `docker-compose.yml`, the container uses `network_mode: host` so it can reach a Transmission daemon running on the host machine directly.

---

## Running It

### Prerequisites

- Docker and Docker Compose installed
- Your user added to the `docker` group (`sudo usermod -aG docker <user>`, then log out/in)
- Transmission daemon running and accessible (port 9091)

### Start the container

```bash
docker compose up --build
```

The `--build` flag ensures any code changes are picked up. The web interface will be available at `http://localhost:8000`.

### Development (without Docker)

```bash
pip install -r requirements.txt
uvicorn main:app --reload
```

This binds to `localhost` only. To make the app visible to other devices on the network (e.g. when running on the Raspberry Pi and accessing from another machine), bind to `0.0.0.0`:

```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

The site will then be reachable at `http://<machine-ip>:8000` from any device on the same network. Drop `--reload` in production — it's for development only.

---

## Installing Transmission (daemon + CLI only)

Installing the full `transmission` package pulls in GTK dependencies that can conflict with existing desktop packages. Install only what's needed:

```bash
sudo apt install transmission-daemon transmission-cli
```

- `transmission-daemon` — the background service that handles downloads
- `transmission-cli` — command-line tools (optional but useful for troubleshooting)

This avoids the GUI and its dependencies entirely.

After installing, **stop the daemon before editing its config**, or it will overwrite your changes on exit:

```bash
sudo systemctl stop transmission-daemon
sudo nano /etc/transmission-daemon/settings.json
sudo systemctl start transmission-daemon
```

Key settings to change in `settings.json`:

| Setting | Value |
|---|---|
| `"rpc-authentication-required"` | `false` |
| `"download-dir"` | `"/mnt/usbdrive"` (or wherever you want) |
| `"rpc-whitelist-enabled"` | `false` (if accessing from other machines on LAN) |

---

## Deployment: Raspberry Pi 3

Running on a Raspberry Pi 3 (currently `192.168.0.178` — dynamic, but stable as long as the Pi stays on) connected to a USB drive mounted at `/mnt/usbdrive`. Transmission runs on the Pi with `download-dir` set to `/mnt/usbdrive`, and the Docker container talks to it over localhost.

### Mounting the USB drive

The USB drive must be mounted at `/mnt/usbdrive` before Transmission starts, or downloads will fall back to the SD card. To mount it automatically on boot, add an entry to `/etc/fstab`:

```bash
# Find the drive's UUID
sudo blkid

# Add to /etc/fstab (replace UUID and fstype as appropriate)
UUID=XXXX-XXXX  /mnt/usbdrive  exfat  defaults,nofail  0  0
```

The `nofail` option prevents the Pi from hanging at boot if the drive isn't connected.

### Accessing downloaded files via Samba

Samba is installed on the Pi so downloaded files can be browsed from other machines on the LAN (Windows, Mac, or Linux file manager).

```bash
sudo apt install samba
```

Add a share to `/etc/samba/smb.conf`:

```ini
[usbdrive]
path = /mnt/usbdrive
browseable = yes
read only = yes
guest ok = yes
```

Then restart Samba:

```bash
sudo systemctl restart smbd
```

The share will appear on the network as `\\192.168.0.178\usbdrive` (or `smb://192.168.0.178/usbdrive` on Mac/Linux).

---

## Lessons Learned

- `transmission_rpc` cannot reliably set a custom `download_dir` on Linux — Transmission ignores or rejects it due to permission constraints.
- Editing `settings.json` directly also failed to redirect downloads on Linux Mint Cinnamon.
- The working solution: set `download-dir` to `/mnt/usbdrive` directly in Transmission's `settings.json` on the Raspberry Pi. This works fine on Raspberry Pi OS.
- `rpc-authentication-required` must be `false` in `settings.json`. Remember to stop Transmission before editing — it overwrites the file on exit.

---

## Current Status

- [x] FastAPI backend working
- [x] Web UI built and looking decent
- [x] Docker container confirmed working
- [x] Transmission download confirmed working (default folder)
- [x] Deployed and running on Raspberry Pi 3 (downloads to `/mnt/usbdrive`)
- [ ] Sergio has actually read all the code he asked Claude to write

---

*Built with Claude Code. I asked, it built. I'm not sure how I feel about that, but I like the result.*
