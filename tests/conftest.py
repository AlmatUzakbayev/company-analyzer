import os

# app.py creates the Gemini client at import time, so a placeholder key is needed; no request is sent
os.environ.setdefault("GOOGLE_API_KEY", "test-key")
