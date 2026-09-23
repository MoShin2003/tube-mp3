# tube-mp3

Paste a video link, get an MP3. It runs on your own computer.

## Setup (Windows)

**How to run a command:** copy the gray box, click in the PowerShell window,
press `Ctrl + V` to paste, then press `Enter`. Wait until it finishes before
doing the next one.

### Step 1: Fork the repo

1. Go to [github.com](https://github.com) and sign in. (No account? Click
   **Sign up** and make a free one.)
2. Go to **https://github.com/MoShin2003/tube-mp3**
3. Click the **Fork** button near the top right.
4. Click the green **Create fork** button.

You now have your own copy at `https://github.com/YOUR-USERNAME/tube-mp3`.

### Step 2: Open PowerShell

Press the **Windows key**, type `PowerShell`, and press `Enter`.

### Step 3: Install the tools

Run these four commands, one at a time. If it asks you to agree to something,
type `Y` and press `Enter`. If a popup asks "Do you want to allow this app to
make changes?", click **Yes**.

```powershell
winget install Python.Python.3.13
```

```powershell
winget install Gyan.FFmpeg
```

```powershell
winget install Git.Git
```

```powershell
winget install DenoLand.Deno
```

When all four are done, **close PowerShell and open it again** (Step 2). The
new tools won't work until you do this.

### Step 4: Check that the tools work

Run each of these. Each one should print a version number. If one says
"not recognized", restart your computer and try again.

```powershell
python --version
```

```powershell
ffmpeg -version
```

```powershell
git --version
```

```powershell
deno --version
```

### Step 5: Download your fork

Go to your home folder:

```powershell
cd ~
```

Download your fork. **Replace `YOUR-USERNAME` with your GitHub username**
before you press Enter:

```powershell
git clone https://github.com/YOUR-USERNAME/tube-mp3.git
```

Go into the new folder:

```powershell
cd tube-mp3
```

### Step 6: Install the app

```powershell
python -m pip install -r requirements.txt
```

### Step 7: Start the app

```powershell
python app.py
```

Now open your web browser and go to **http://127.0.0.1:5000**

Keep the PowerShell window open while you use the app. Closing it turns the app off.

## Using it

1. Paste one or more video links into the box, one per line.
2. Click **Convert to MP3**.
3. The MP3 downloads to your **Downloads** folder. If you converted more than
   one, you get a ZIP file with all of them.

To turn the app off, click the PowerShell window and press `Ctrl + C`.

## Starting it again later

Open PowerShell and run:

```powershell
cd ~\tube-mp3
```

```powershell
python app.py
```

Then go to **http://127.0.0.1:5000**

## Getting updates

1. Go to your fork on GitHub (`https://github.com/YOUR-USERNAME/tube-mp3`).
2. Click **Sync fork**, then **Update branch**.
3. Open PowerShell and run these three commands:

```powershell
cd ~\tube-mp3
```

```powershell
git pull
```

```powershell
python -m pip install --upgrade -r requirements.txt
```

## If something goes wrong

- **"not recognized" or "not found":** close PowerShell and open it again.
  If that doesn't fix it, restart your computer.
- **A video won't convert:** websites change a lot. Do everything in
  [Getting updates](#getting-updates), then try again.
- **The page won't load:** make sure the PowerShell window running
  `python app.py` is still open.
- **"Address already in use":** the app is already running in another
  PowerShell window. Use that one, or close it and start again.

<details>
<summary><b>On a Mac instead?</b></summary>

Do Step 1 (fork) above. Then open **Terminal** (press `Cmd + Space`, type
`Terminal`, press `Enter`) and run these commands one at a time.

Install Homebrew. When it finishes, it may show "Next steps" with a few more
commands. Copy and run those too.

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

Install the tools:

```bash
brew install python ffmpeg git deno
```

Download your fork (replace `YOUR-USERNAME`):

```bash
cd ~
```

```bash
git clone https://github.com/YOUR-USERNAME/tube-mp3.git
```

```bash
cd tube-mp3
```

Set up and install the app:

```bash
python3 -m venv .venv
```

```bash
source .venv/bin/activate
```

```bash
pip install -r requirements.txt
```

Start it. Macs already use port 5000, so this uses 8000:

```bash
PORT=8000 python app.py
```

Open **http://127.0.0.1:8000** in your browser.

**Starting it again later:**

```bash
cd ~/tube-mp3
```

```bash
source .venv/bin/activate
```

```bash
PORT=8000 python app.py
```

**Getting updates:** click **Sync fork** on GitHub, then in Terminal run
`cd ~/tube-mp3`, `source .venv/bin/activate`, `git pull`, and
`pip install --upgrade -r requirements.txt`.

</details>

---

Only download stuff you have the right to download.
