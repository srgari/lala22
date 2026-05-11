# Plan: Add "Refresh" Button (Reconnect + Restart All Torrents)

## What it does

When Transmission is restarted (e.g. after a Pi reboot), all torrents end up in "stopped" state. This button lets you reconnect to the server and kick all torrents back into action in one click.

---

## Files to change

- `main.py`
- `templates/index.html`

---

## 1. `main.py` — New endpoint

Append after the existing endpoints:

```python
@app.post("/restart-all")
async def restart_all():
    try:
        client = get_client()
        torrents = client.get_torrents()
        ids = [t.id for t in torrents]
        if ids:
            client.start_torrent(ids)
        return JSONResponse({"status": "ok", "message": f"Restarted {len(ids)} torrent(s)."})
    except Exception as e:
        return JSONResponse({"status": "error", "message": str(e)}, status_code=500)
```

- The `get_client()` call is the reconnect step — if Transmission is unreachable it throws and the error message shows in the UI.
- `start_torrent(ids)` accepts a list and starts them all at once.

---

## 2. `templates/index.html`

### A. CSS (add after `.btn-remove:hover`)

```css
.btn-refresh {
  padding: 0.5rem 1rem;
  background: none;
  border: 1px solid #444;
  color: #e0e0e0;
  border-radius: 6px;
  cursor: pointer;
  font-size: 0.88rem;
  margin-bottom: 1rem;
}
.btn-refresh:hover { border-color: #888; color: #fff; }
```

### B. HTML (add after `</form>`, before `<div id="message">`)

```html
<button id="refresh-btn" class="btn-refresh">Refresh</button>
```

### C. JavaScript (add before the `fetchTorrents()` call at the bottom)

```js
async function restartAll() {
  try {
    const res = await fetch('/restart-all', { method: 'POST' });
    const data = await res.json();
    setMessage(data.message, data.status);
    if (data.status === 'ok') fetchTorrents();
  } catch (e) {
    setMessage('Failed to contact server.', 'err');
  }
}

document.getElementById('refresh-btn').addEventListener('click', restartAll);
```

---

## Expected behaviour

| Scenario | Result |
|---|---|
| Transmission reachable, torrents exist | Starts all torrents, shows "Restarted N torrent(s).", refreshes table |
| Transmission reachable, no torrents | Shows "Restarted 0 torrent(s)." — harmless |
| Transmission unreachable | Red error message shown |
