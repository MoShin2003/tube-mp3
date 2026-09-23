@echo off
setlocal
cd /d "%~dp0"

echo ============================================
echo    tube-mp3  -  local video to MP3
echo ============================================
echo.
echo Set a password so only people you share it with can use the app.
echo Leave it blank and the app is open (fine when it is just you).
echo.
set /p TUBE_MP3_PASSWORD="Password (blank = none): "
echo.

REM --upgrade keeps yt-dlp current; old versions stop working with YouTube.
echo Installing / updating dependencies (first run may take a minute)...
python -m pip install --quiet --upgrade -r requirements.txt
if errorlevel 1 (
  echo.
  echo Installing dependencies failed. Check your internet connection.
  echo If "python" was not found, install it with:  winget install Python.Python.3.13
  echo Then close this window, reopen it, and run this file again.
  echo.
  pause
  exit /b 1
)

echo.
echo Open  http://127.0.0.1:5000  in your browser.
echo Close this window to stop the app.
echo.
python app.py
pause
