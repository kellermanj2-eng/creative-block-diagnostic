#!/usr/bin/env bash
# setup.sh — one-command setup for Mac/Linux
# Usage: bash setup.sh
set -e

echo ""
echo "=== Creative Block Diagnostic — setup ==="
echo ""

# ── 1. Create virtual environment ─────────────────────────────────────────────
if [ ! -d ".venv" ]; then
    echo "Creating virtual environment (.venv)..."
    python3 -m venv .venv
else
    echo "Virtual environment already exists — skipping creation."
fi

# ── 2. Activate and install dependencies ──────────────────────────────────────
echo "Installing dependencies from requirements.txt..."
# shellcheck disable=SC1091
source .venv/bin/activate
pip install --quiet -r requirements.txt

# ── 3. Copy .env.example → .env (only if .env doesn't already exist) ──────────
if [ ! -f ".env" ]; then
    cp .env.example .env
    echo "Created .env from .env.example."
    echo "  (watsonx AI personalisation is optional — the app runs fully offline.)"
    echo "  To enable it: edit .env, set WATSONX_ENABLED=true, and fill in your"
    echo "  IBM Cloud credentials."
else
    echo ".env already exists — leaving it unchanged."
fi

# ── Done ──────────────────────────────────────────────────────────────────────
echo ""
echo "=== Setup complete! ==="
echo ""
echo "Next steps:"
echo "  1. Activate the virtual environment:"
echo "       source .venv/bin/activate"
echo "  2. Run the app:"
echo "       python app.py"
echo "  3. Open http://localhost:5000 in your browser."
echo ""
echo "  watsonx AI personalisation is OPTIONAL. The app works fully offline"
echo "  without any credentials."
echo ""
