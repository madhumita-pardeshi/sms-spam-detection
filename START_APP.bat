@echo off
setlocal
cd /d "%~dp0"

if not exist "spam_model.pkl" (
  echo ERROR: Project files are incomplete or still inside the ZIP.
  echo Right-click the ZIP, choose Extract All, then run START_APP.bat in the extracted folder.
  pause
  exit /b 1
)
if not exist "tfidf_vectorizer.pkl" (
  echo ERROR: tfidf_vectorizer.pkl is missing. Extract the complete project ZIP first.
  pause
  exit /b 1
)

where py >nul 2>nul
if %errorlevel%==0 (
  py -3 -m venv .venv
) else (
  where python >nul 2>nul
  if errorlevel 1 (
    echo ERROR: Python was not found. Install Python 3.12 or newer and select Add Python to PATH.
    pause
    exit /b 1
  )
  python -m venv .venv
)
if errorlevel 1 (
  echo ERROR: Could not create the Python environment.
  pause
  exit /b 1
)

call .venv\Scripts\activate.bat
echo Installing project packages. This can take a few minutes the first time...
python -m pip install --upgrade pip
if errorlevel 1 goto install_failed
python -m pip install -r requirements.txt
if errorlevel 1 goto install_failed

echo TextShield is running. Keep this window open; press Ctrl+C to stop it.
python app.py
goto finished

:install_failed
echo.
echo Package installation failed. Check your internet connection and Python installation,
echo then run START_APP.bat again. Read README.md for manual setup instructions.
pause

:finished
endlocal
