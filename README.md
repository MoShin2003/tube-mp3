# tube-mp3

A tiny **local** web app that turns a video URL into an MP3. You run it on
your own computer, open `http://127.0.0.1:5000` in your browser, paste a URL,
and get an MP3 back.

It's a thin wrapper around two mature open-source tools:

- **[yt-dlp](https://github.com/yt-dlp/yt-dlp)** — downloads the best audio stream from a URL
- **[ffmpeg](https://ffmpeg.org/)** — transcodes that stream into an `.mp3` (with metadata)

> ⚠️ **Use responsibly.** Only download content you have the right to
> download — your own uploads, Creative Commons / public-domain material, or
> content the rights-holder has given you permission to grab. Downloading
> copyrighted material you don't have rights to, or content in a way that
> breaks a site's Terms of Service, may be against the law where you live.
> You are responsible for what you convert.

---

## Setup

You need **Python 3.9+** and **ffmpeg** installed.

### 1. Install ffmpeg

- **macOS** (Homebrew): `brew install ffmpeg`
- **Windows** (winget): `winget install Gyan.FFmpeg` — or `choco install ffmpeg`
- **Linux** (Debian/Ubuntu): `sudo apt install ffmpeg`

Check it worked: `ffmpeg -version`

### 2. Get the code and install dependencies

```bash
git clone https://github.com/MoShin2003/tube-mp3.git
cd tube-mp3

# (recommended) use a virtual environment
python3 -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate

pip install -r requirements.txt
```

### 3. Run it

```bash
python app.py
```

Then open **http://127.0.0.1:5000** in your browser. Paste a URL, pick a
quality, hit **Convert to MP3**. Finished files download in your browser and
are also saved to the `downloads/` folder.

Want a different port? `PORT=8000 python app.py`

---

## Can my friend use it too?

**Yes — the easy, correct way is for your friend to run his own copy.** This
app is designed to run locally on each person's machine.

**Option A — he clones or forks the repo (recommended).**
He installs ffmpeg, clones the repo (or forks it first if he wants his own
copy on GitHub), runs `pip install -r requirements.txt`, then `python app.py`.
Now it's running on *his* localhost. This is the whole point of it being a
small local tool: no server to host, no bandwidth through your machine, and
downloads use *his* internet connection, not yours.

- **Fork** = he gets his own GitHub copy he can change freely. Good if he
  wants to tinker.
- **Clone** = he just grabs the code and runs it. Good if he only wants to use it.

Either way the setup is the same three steps above.

**Option B — expose your running port to him (not recommended).**
You *can* run it on your machine and hand him a temporary public link to your
port with a tunneling tool (e.g. `ngrok http 5000` or Cloudflare Tunnel). It
works, but it's the worse choice for a tool like this because:

- Your computer has to stay on and running the app the whole time.
- All his downloads flow through **your** machine and **your** IP/bandwidth.
- You're exposing a service on your machine to the public internet, which is a
  security risk you have to manage (anyone with the link can use it).

For two friends converting the odd file, **Option A wins every time.** Save the
tunnel idea for when you actually want one shared always-on instance — and if
you get there, put it behind real auth first.

---

## How it works

```
Browser (localhost)  ──URL──▶  Flask (app.py)  ──▶  yt-dlp  ──▶  ffmpeg  ──▶  .mp3
       ▲                                                                        │
       └────────────────────────  download link  ◀────────────────────────────┘
```

The server binds to `127.0.0.1` only, so it isn't reachable from outside your
machine by default.

## Project layout

```
tube-mp3/
├── app.py               # Flask app: routes + yt-dlp/ffmpeg glue
├── templates/
│   └── index.html       # the single-page UI
├── downloads/           # finished MP3s land here (git-ignored)
├── requirements.txt
├── LICENSE
└── README.md
```

## License

MIT — see [LICENSE](LICENSE).
