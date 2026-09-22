# tube-mp3

A tiny **local** web app that turns video URLs into MP3s. Run it on your own
computer, open `http://127.0.0.1:5000`, paste one or more URLs, click convert,
and the MP3s download to your machine. That's it.

**Made for sound, not video.** It ignores the picture entirely and grabs the
best available audio for each link, then encodes to MP3 — default **320 kbps**
for crisp, clear sound. Paste a whole list of URLs at once and grab them all
in one **ZIP**.

It's a thin wrapper around two mature open-source tools:

- **[yt-dlp](https://github.com/yt-dlp/yt-dlp)** — downloads the best audio stream from a URL
- **[ffmpeg](https://ffmpeg.org/)** — transcodes that stream into an `.mp3` (with metadata)

> ⚠️ **Use responsibly.** Only download content you have the right to
> download — your own uploads, Creative Commons / public-domain material, or
> content the rights-holder has given you permission to grab. Downloading
> copyrighted material you don't have rights to, or in a way that breaks a
> site's Terms of Service, may be against the law where you live. You are
> responsible for what you convert.

---

## Quick start on Windows (no coding tools needed)

You do **not** need VS Code or any editor — just Windows and PowerShell.

1. Install Python and ffmpeg (one time). In PowerShell:
   ```powershell
   winget install Python.Python.3.12
   winget install Gyan.FFmpeg
   ```
   Then **close and reopen PowerShell** so the installs are picked up.
2. Get the code: on this repo's page click the green **Code** button →
   **Download ZIP**, then extract it. (Or `git clone` if you have git.)
3. **Double-click `run.bat`.** It asks for a password (leave it blank if
   it's just you), installs what it needs the first time, and starts the app.
4. Open **http://127.0.0.1:5000** in your browser.

> If `python` isn't found, use `py` instead, or re-run the winget install and
> reopen PowerShell.

## Quick start on macOS / Linux

```bash
brew install ffmpeg            # Linux: sudo apt install ffmpeg
git clone https://github.com/MoShin2003/tube-mp3.git
cd tube-mp3
pip install -r requirements.txt
python app.py
```
Open **http://127.0.0.1:5000**. Want a different port? `PORT=8000 python app.py`

Paste **one URL per line** to convert several at once. Each finished file
downloads in your browser and is also saved to the `downloads/` folder; when
you convert two or more, you also get a one-click **"Download all as ZIP"**
button. Pick the sound quality from the dropdown — **320 kbps** (default) is
the crispest.

---

## Password protection

The app can require a password before anyone can use it. It's **off by
default** (simplest when it's just you on localhost) and turns on the moment
you set the `TUBE_MP3_PASSWORD` environment variable:

- **Windows:** `run.bat` prompts you for it — just type one in.
- **macOS / Linux:**
  ```bash
  TUBE_MP3_PASSWORD="pick-something" python app.py
  ```

With a password set, everyone sees a login page first. This is what makes it
safe to share a guest link (below). The password is **never stored in the
repo** — it only lives in the environment variable while the app is running.

---

## Let a friend use it — the guest link

Your friend needs **nothing but a web browser**. You run the app on your
machine and hand them a temporary public link that points at it.

1. Start the app **with a password** (`run.bat`, or the env-var command above).
2. Install Cloudflare's free tunnel tool (one time):
   ```powershell
   winget install Cloudflare.cloudflared
   ```
   (macOS: `brew install cloudflared`.)
3. Make the link. On Windows, **double-click `share.bat`**; on macOS/Linux:
   ```bash
   cloudflared tunnel --url http://localhost:5000
   ```
   A link like `https://something.trycloudflare.com` appears.
4. Send your friend **the link + the password**. They open it, type the
   password, paste a video URL, click convert — the MP3 downloads to *their*
   computer. Everything else happens on your machine, behind the scenes.

**Keep it safe:**
- Always set a password before sharing — the link is public, the password is
  what keeps strangers out.
- The link only works while **your** machine is on and the app + tunnel are
  running. Close `share.bat` to switch the guest link off.
- Your machine and internet connection do the downloading, so the free
  `trycloudflare.com` link is best for occasional use with people you trust.

### The other option: your friend runs his own copy

If he'd rather not depend on your machine being on, he can just do the
**Quick start** above himself — **fork** the repo (his own GitHub copy to
tinker with) or **clone/Download ZIP** (just to use it). Same steps, runs on
his own localhost, uses his own connection. No password or tunnel needed.

---

## How it works

```
Browser  ──URL──▶  Flask (app.py)  ──▶  yt-dlp  ──▶  ffmpeg  ──▶  .mp3
   ▲                                                                │
   └──────────────────────  download link  ◀───────────────────────┘
```

The server binds to `127.0.0.1` only, so it isn't reachable from outside your
machine unless you deliberately expose it with a tunnel.

## Project layout

```
tube-mp3/
├── app.py               # Flask app: routes + optional login + yt-dlp/ffmpeg glue
├── templates/
│   ├── index.html       # the converter page
│   └── login.html       # password page (shown only when a password is set)
├── run.bat              # Windows: double-click to start the app
├── share.bat            # Windows: double-click to create a guest link
├── downloads/           # finished MP3s land here (git-ignored)
├── requirements.txt
├── LICENSE
└── README.md
```

## License

MIT — see [LICENSE](LICENSE).
