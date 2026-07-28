# ── Build stage ───────────────────────────────────────────────────────────────
# Use a slim official Python image.  3.12-slim keeps the layer small while
# matching the Python version used in development.
FROM python:3.12-slim

# Set a sane working directory.
WORKDIR /app

# Install Python dependencies first (separate layer — only rebuilds on
# requirements.txt changes, not on every source edit).
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the source.
COPY . .

# The app reads from .env via python-dotenv, but we don't copy a .env file
# into the image — credentials should be injected at runtime via
# environment variables or a mounted .env.  The offline fallback works with
# no credentials at all, so the image is usable out-of-the-box.
#
# Silence any "WATSONX_ENABLED but missing credentials" check at startup by
# ensuring the variable is absent (not "true") unless explicitly overridden.
ENV WATSONX_ENABLED=false
ENV FLASK_DEBUG=false

# Flask listens on 5000 by default.
EXPOSE 5000

# Run with the development server.  For a production deployment swap this
# for gunicorn, but for hackathon / demo use this is fine.
CMD ["python", "app.py"]
