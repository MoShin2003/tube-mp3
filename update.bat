@echo off
setlocal
cd /d "%~dp0"

echo ============================================
echo    tube-mp3  -  update to the latest version
echo ============================================
echo.

REM Make sure this folder is a git checkout (not a downloaded ZIP).
git rev-parse --is-inside-work-tree >nul 2>&1
if errorlevel 1 (
  echo This folder was not installed with git, so it cannot update itself.
  echo.
  echo To get one-click updates in future, install it once with:
  echo    git clone https://github.com/MoShin2003/tube-mp3.git
  echo.
  echo For now, re-download the latest ZIP from the repo's green "Code" button.
  echo.
  pause
  exit /b 1
)

echo Fetching the latest version...
git pull
if errorlevel 1 (
  echo.
  echo Update failed. If git is not installed, get it with:
  echo    winget install Git.Git
  echo.
  pause
  exit /b 1
)

echo.
echo Up to date. Start the app again with run.bat.
echo.
pause
