@echo off
REM setup.bat — one-command setup for Windows
REM Usage: setup.bat

echo.
echo === Creative Block Diagnostic — setup ===
echo.

REM ── 1. Create virtual environment ─────────────────────────────────────────────
IF NOT EXIST ".venv\" (
    echo Creating virtual environment ^(.venv^)...
    python -m venv .venv
    IF ERRORLEVEL 1 (
        echo ERROR: Failed to create virtual environment.
        echo Make sure Python 3.11+ is installed and on your PATH.
        exit /b 1
    )
) ELSE (
    echo Virtual environment already exists -- skipping creation.
)

REM ── 2. Install dependencies ────────────────────────────────────────────────────
echo Installing dependencies from requirements.txt...
call .venv\Scripts\activate.bat
pip install --quiet -r requirements.txt
IF ERRORLEVEL 1 (
    echo ERROR: pip install failed.
    exit /b 1
)

REM ── 3. Copy .env.example → .env (only if .env doesn't already exist) ──────────
IF NOT EXIST ".env" (
    copy .env.example .env >nul
    echo Created .env from .env.example.
    echo   ^(watsonx AI personalisation is optional -- the app runs fully offline.^)
    echo   To enable it: edit .env, set WATSONX_ENABLED=true, and fill in your
    echo   IBM Cloud credentials.
) ELSE (
    echo .env already exists -- leaving it unchanged.
)

REM ── Done ──────────────────────────────────────────────────────────────────────
echo.
echo === Setup complete! ===
echo.
echo Next steps:
echo   1. Activate the virtual environment:
echo        .venv\Scripts\activate
echo   2. Run the app:
echo        python app.py
echo   3. Open http://localhost:5000 in your browser.
echo.
echo   watsonx AI personalisation is OPTIONAL. The app works fully offline
echo   without any credentials.
echo.
