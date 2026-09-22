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
import shutil
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
    url = (request.form.get("url") or "").strip()
    bitrate = (request.form.get("bitrate") or "192").strip()

    if not url:
        return jsonify(error="Please paste a video URL."), 400
    if bitrate not in ALLOWED_BITRATES:
        bitrate = "192"
    if not ffmpeg_available():
        return (
            jsonify(
                error="ffmpeg was not found on your PATH. Install it first "
                "(see the README) and restart the app."
            ),
            500,
        )

    ydl_opts = {
        "format": "bestaudio/best",
        # %(title)s is sanitized by yt-dlp into a safe filename.
        "outtmpl": str(DOWNLOAD_DIR / "%(title)s.%(ext)s"),
        "noplaylist": True,  # one URL -> one file for the web UI
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
        return jsonify(error=f"Could not download that URL: {exc}"), 400
    except Exception as exc:  # noqa: BLE001 - surface anything else to the UI
        return jsonify(error=f"Unexpected error: {exc}"), 500

    if not produced.exists():
        return jsonify(error="Conversion finished but no MP3 was produced."), 500

    # Hand the browser a URL it can pull the finished file from.
    return jsonify(
        title=info.get("title", produced.stem),
        filename=produced.name,
        download_url=url_for("download", filename=produced.name),
    )


@app.route("/downloads/<path:filename>")
def download(filename: str):
    """Serve a finished MP3 as an attachment."""
    # send_from_directory rejects path traversal (e.g. ../) for us.
    if not filename.lower().endswith(".mp3"):
        abort(404)
    return send_from_directory(DOWNLOAD_DIR, filename, as_attachment=True)


if __name__ == "__main__":
    # Bind to localhost only - this app is meant to run on your own machine.
    port = int(os.environ.get("PORT", "5000"))
    lock = "on (password required)" if APP_PASSWORD else "off (open)"
    print(f"\n  tube-mp3 running at  http://127.0.0.1:{port}   | login: {lock}\n")
    app.run(host="127.0.0.1", port=port, debug=False)
