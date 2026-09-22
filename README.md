# tube-mp3

![Python](https://img.shields.io/badge/python-3.9%2B-blue)
![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey)
![License](https://img.shields.io/badge/license-MIT-green)

**A lightweight, self-hosted web app that converts video links into
high-quality MP3s — right on your own computer.**

Paste one or more video URLs, click convert, and tube-mp3 downloads the best
available audio for each and saves it as an MP3. No account, no cloud service,
nothing tracked — it runs entirely on your machine and is built on two trusted
open-source projects, [yt-dlp](https://github.com/yt-dlp/yt-dlp) and
[ffmpeg](https://ffmpeg.org/).

---

## Features

- 🎧 **Audio-first** — always grabs the best available audio for each video; the picture is ignored.
- ✨ **High quality** — up to **320 kbps** MP3 (the default), with lower options for smaller files.
- 📋 **Batch mode** — paste many URLs at once, one per line, and convert them all in a single click.
- 📦 **One-click ZIP** — download an entire batch together as a single archive.
- 🔒 **Optional password** — lock the app behind a login page before you share it.
- 🔗 **Shareable** — hand a friend a private link; they use it from any browser and install nothing.
- 💻 **Cross-platform** — Windows, macOS, and Linux.
- 🗂️ **Local & private** — every file stays on your computer.

---

## Requirements

| Tool | Purpose | Notes |
|------|---------|-------|
| **Python 3.9+** | runs the app | [python.org](https://www.python.org/downloads/) |
| **ffmpeg** | extracts & encodes audio | [ffmpeg.org](https://ffmpeg.org/download.html) |
| **git** *(recommended)* | one-command updates | optional, but makes updating trivial |

---

## Installation

### Windows

1. **Install the tools.** Open **PowerShell** and run:
   ```powershell
   winget install Python.Python.3.12
   winget install Gyan.FFmpeg
   winget install Git.Git
   ```
   Then **close and reopen PowerShell** so the new tools are detected. Verify:
   ```powershell
   python --version
   ffmpeg -version
   ```

2. **Download the app** (with git, so updates are one click later):
   ```powershell
   cd ~\Documents
   git clone https://github.com/MoShin2003/tube-mp3.git
   cd tube-mp3
   ```

3. **Start it** — double-click **`run.bat`** in the `tube-mp3` folder.
   It asks for a password (leave blank if it's just you), installs
   dependencies on first run, and launches the app.

4. Open **http://127.0.0.1:5000** in your browser.

> **No git?** You can instead use the green **Code → Download ZIP** button on
> the repo page and extract it — but you'll have to re-download to update.
> Installing with `git clone` is recommended.

### macOS / Linux

```bash
# 1. Install ffmpeg
brew install ffmpeg            # Linux (Debian/Ubuntu): sudo apt install ffmpeg

# 2. Get the app
git clone https://github.com/MoShin2003/tube-mp3.git
cd tube-mp3

# 3. Install dependencies and run
pip install -r requirements.txt
python app.py
```

Open **http://127.0.0.1:5000**. Use a different port with `PORT=8000 python app.py`.

---

## Using the app

1. Open **http://127.0.0.1:5000**.
2. Paste one or more video URLs into the box — **one per line**:
   ```
   https://example.com/video-one
   https://example.com/video-two
   https://example.com/video-three
   ```
3. Choose the **sound quality** (default **320 kbps** — the crispest).
4. Click **Convert to MP3**.

Each track appears in a list with a ✓ and its own download link. Convert two
or more and you also get a **⬇ Download all as ZIP** button that grabs the
whole batch at once. Every file is saved to the `downloads/` folder as well,
so you always keep a copy on disk.

---

## Password protection

The app can require a password before anyone can use it. It is **off by
default** (simplest when you're the only user) and turns on the moment you set
the `TUBE_MP3_PASSWORD` environment variable:

- **Windows:** `run.bat` prompts you for a password on startup — just type one.
- **macOS / Linux:**
  ```bash
  TUBE_MP3_PASSWORD="choose-a-password" python app.py
  ```

With a password set, everyone sees a login page first. The password is **never
stored in the repository** — it only exists in the environment while the app
runs. This is what makes it safe to share a link (below).

---

## Sharing with a friend

Your friend needs **nothing but a web browser**. You run the app on your
machine and give them a temporary private link that points to it.

1. Start the app **with a password** (see above).
2. Install Cloudflare's free tunnel tool once:
   ```
   winget install Cloudflare.cloudflared      # macOS: brew install cloudflared
   ```
3. Create the link:
   - **Windows:** double-click **`share.bat`**.
   - **macOS / Linux:** `cloudflared tunnel --url http://localhost:5000`

   A public link like `https://something.trycloudflare.com` appears.
4. Send your friend **the link and the password**. They open it, sign in,
   paste URLs, and convert — the MP3s download to *their* computer.

**Notes:** the link only works while your machine is on and the app + tunnel
are running; close `share.bat` to switch it off. Always set a password before
sharing. The free link's address changes each time you start it.

---

## Updating

- **Installed with git (recommended):** double-click **`update.bat`**, or run
  `git pull` in the project folder. Restart the app and you're on the latest.
- **Installed via ZIP:** download the ZIP again and replace your folder.

---

## Troubleshooting

| Problem | Fix |
|---------|-----|
| `ffmpeg` "not recognized" / "not found" | Close and reopen your terminal after installing ffmpeg so it's on the PATH. On Windows, occasionally a full sign-out is needed. |
| `python` not found | Reopen your terminal after installing Python. On Windows, try `py` instead of `python`. |
| Windows "publisher could not be verified" popup | Normal for any downloaded `.bat` file. The scripts are plain text — open them in Notepad to read them — then click **Run**. |
| "Address already in use" | The app is already running, or the port is taken. Close the other window, or start on another port: `PORT=8000 python app.py`. |
| A single link fails in a batch | The others still convert. The failing link shows an ✗ with the reason — usually the URL is private, region-locked, or unsupported. |

---

## How it works

```
Browser  ──URLs──▶  Flask (app.py)  ──▶  yt-dlp  ──▶  ffmpeg  ──▶  .mp3 (+ .zip)
   ▲                                                                    │
   └──────────────────────────  download  ◀────────────────────────────┘
```

`yt-dlp` selects and downloads the best audio stream for each URL; `ffmpeg`
encodes it to MP3 and tags it. The server binds to `127.0.0.1` only, so it is
not reachable from outside your machine unless you deliberately expose it with
a tunnel.

## Project structure

```
tube-mp3/
├── app.py               # Flask app: routes, optional login, yt-dlp/ffmpeg glue
├── templates/
│   ├── index.html       # the converter page
│   └── login.html       # password page (shown only when a password is set)
├── run.bat              # Windows: double-click to start the app
├── share.bat            # Windows: double-click to create a guest link
├── update.bat           # Windows: double-click to update (git pull)
├── downloads/           # finished MP3s and ZIPs (git-ignored)
├── requirements.txt
├── LICENSE
└── README.md
```

---

## Responsible use

Only download content you have the right to download — your own uploads,
Creative Commons or public-domain material, or content the rights-holder has
given you permission to grab. Downloading copyrighted material you don't have
rights to, or in a way that violates a site's Terms of Service, may be illegal
where you live. **You are responsible for what you convert.**

## License

Released under the [MIT License](LICENSE).
