#!/usr/bin/env python3
"""tube-mp3 - a tiny local web app that converts a video URL to an MP3.

Everything runs on your own machine (localhost). It is a thin, friendly
wrapper around two mature open-source tools:

  * yt-dlp - downloads the best audio stream from a URL
  * ffmpeg - transcodes that stream into an .mp3 (with metadata)

Optional password gate:
  Set the TUBE_MP3_PASSWORD environment variable and the app shows a login
  page before anyone can use it. Leave it unset and the app is open (handy
  when you're the only one using it on localhost). The password matters most
  when you expose the app to a friend through a tunnel (see the README).

Responsible use: only download content you have the right to download -
your own uploads, Creative Commons / public-domain material, or content
the rights-holder has given you permission to download.
"""
from __future__ import annotations

import hmac
import os
import re
import shutil
import time
import zipfile
from pathlib import Path

import yt_dlp
from flask import (
    Flask,
    abort,
    jsonify,
    redirect,
    render_template,
    request,
    send_from_directory,
    session,
    url_for,
)

app = Flask(__name__)
# Signs the login cookie. Random per start is fine - a restart just means
# everyone logs in again.
app.secret_key = os.environ.get("SECRET_KEY") or os.urandom(24)

# Optional password. Empty/unset => the app is open (no login).
APP_PASSWORD = os.environ.get("TUBE_MP3_PASSWORD", "").strip()

# MP3 bitrates (kbps) the UI is allowed to request.
ALLOWED_BITRATES = {"128", "192", "256", "320"}

# Finished files land here, so you keep a copy on disk as well as in the
# browser download. This folder is git-ignored.
DOWNLOAD_DIR = Path(__file__).resolve().parent / "downloads"
DOWNLOAD_DIR.mkdir(exist_ok=True)


def ffmpeg_available() -> bool:
    """True if an `ffmpeg` binary is on the PATH."""
    return shutil.which("ffmpeg") is not None


def split_urls(raw: str) -> list[str]:
    """Turn a blob of pasted text into a clean list of URLs.

    Accepts URLs separated by new lines, spaces, or commas, and keeps only
    the ones that look like http(s) links.
    """
    parts = re.split(r"[\s,]+", (raw or "").strip())
    return [p for p in parts if p.lower().startswith(("http://", "https://"))]


def convert_one(url: str, bitrate: str) -> dict:
    """Download the best audio for one URL and encode it to MP3.

    Returns a result dict describing success or failure - it never raises,
    so one bad link in a batch can't sink the rest.
    """
    ydl_opts = {
        # bestaudio => yt-dlp automatically picks the highest-quality audio
        # source available for THIS video; video is ignored entirely.
        "format": "bestaudio/best",
        # %(title)s is sanitized by yt-dlp into a safe filename.
        "outtmpl": str(DOWNLOAD_DIR / "%(title)s.%(ext)s"),
        "noplaylist": True,  # one URL -> one file
        "quiet": True,
        "no_warnings": True,
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": bitrate,
            },
            {"key": "FFmpegMetadata"},
        ],
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            # After FFmpegExtractAudio the real output ends in .mp3.
            produced = Path(ydl.prepare_filename(info)).with_suffix(".mp3")
    except yt_dlp.utils.DownloadError as exc:
        return {"url": url, "ok": False, "error": f"Could not download: {exc}"}
    except Exception as exc:  # noqa: BLE001 - surface anything else to the UI
        return {"url": url, "ok": False, "error": f"Unexpected error: {exc}"}

    if not produced.exists():
        return {"url": url, "ok": False, "error": "No MP3 was produced."}

    return {
        "url": url,
        "ok": True,
        "title": info.get("title", produced.stem),
        "filename": produced.name,
        "download_url": url_for("download", filename=produced.name),
    }


@app.before_request
def require_login():
    """Gate every page behind the password, when one is configured."""
    if not APP_PASSWORD:
        return None  # no password set -> app is open
    if request.endpoint in ("login", "static"):
        return None  # let the login page and static assets through
    if session.get("authed"):
        return None  # already logged in
    return redirect(url_for("login"))


@app.route("/login", methods=["GET", "POST"])
def login():
    if not APP_PASSWORD:
        return redirect(url_for("index"))
    error = None
    if request.method == "POST":
        supplied = request.form.get("password") or ""
        # Constant-time compare so the password can't be guessed by timing.
        if hmac.compare_digest(supplied, APP_PASSWORD):
            session["authed"] = True
            return redirect(url_for("index"))
        error = "Wrong password. Try again."
    return render_template("login.html", error=error)


@app.route("/")
def index():
    return render_template(
        "index.html",
        ffmpeg_ok=ffmpeg_available(),
        locked=bool(APP_PASSWORD),
    )


@app.route("/convert", methods=["POST"])
def convert():
    # Accept the new multi-line "urls" field, and still accept an old single
    # "url" field for safety.
    raw = request.form.get("urls") or request.form.get("url") or ""
    bitrate = (request.form.get("bitrate") or "320").strip()
    if bitrate not in ALLOWED_BITRATES:
        bitrate = "320"

    urls = split_urls(raw)
    if not urls:
        return jsonify(error="Please paste at least one video URL (http/https)."), 400
    if not ffmpeg_available():
        return (
            jsonify(
                error="ffmpeg was not found on your PATH. Install it first "
                "(see the README) and restart the app."
            ),
            500,
        )

    # Convert each link in turn; a failure on one doesn't stop the others.
    results = [convert_one(u, bitrate) for u in urls]
    succeeded = [r for r in results if r["ok"]]

    # When 2+ tracks succeed, bundle them so the whole batch is one download.
    zip_url = None
    if len(succeeded) >= 2:
        zip_name = f"tube-mp3_batch_{int(time.time())}.zip"
        # MP3s are already compressed, so store (no re-compression) is fastest.
        with zipfile.ZipFile(DOWNLOAD_DIR / zip_name, "w", zipfile.ZIP_STORED) as zf:
            for r in succeeded:
                path = DOWNLOAD_DIR / r["filename"]
                if path.exists():
                    zf.write(path, arcname=r["filename"])
        zip_url = url_for("download", filename=zip_name)

    return jsonify(
        results=results,
        zip_url=zip_url,
        ok_count=len(succeeded),
        fail_count=len(results) - len(succeeded),
    )


@app.route("/downloads/<path:filename>")
def download(filename: str):
    """Serve a finished MP3 (or a batch .zip) as an attachment."""
    # send_from_directory rejects path traversal (e.g. ../) for us.
    if not filename.lower().endswith((".mp3", ".zip")):
        abort(404)
    return send_from_directory(DOWNLOAD_DIR, filename, as_attachment=True)


if __name__ == "__main__":
    # Bind to localhost only - this app is meant to run on your own machine.
    port = int(os.environ.get("PORT", "5000"))
    lock = "on (password required)" if APP_PASSWORD else "off (open)"
    print(f"\n  tube-mp3 running at  http://127.0.0.1:{port}   | login: {lock}\n")
    app.run(host="127.0.0.1", port=port, debug=False)
