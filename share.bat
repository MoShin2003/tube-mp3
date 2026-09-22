@echo off
setlocal
cd /d "%~dp0"

echo ============================================
echo    tube-mp3  -  create a guest link
echo ============================================
echo.
echo This makes a public https link that points at the app running on
echo THIS computer, so a friend can use it from their browser.
echo.
echo Before you run this:
echo   1. Start the app first with run.bat (and set a password!).
echo   2. Have cloudflared installed:  winget install Cloudflare.cloudflared
echo.
echo A link like  https://something.trycloudflare.com  will appear below.
echo Send that link (and the password) to your friend.
echo Close this window to shut the guest link off again.
echo.
cloudflared tunnel --url http://localhost:5000
if errorlevel 1 (
  echo.
  echo Could not run "cloudflared". Install it with:  winget install Cloudflare.cloudflared
  echo Then close this window, reopen it, and run this file again.
  echo.
)
pause
