import os

# Bot configuration
TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")

# Storage configuration
STORAGE_PATH = os.path.abspath("storage")  # Use absolute path

# Allowed file types
ALLOWED_EXTENSIONS = {
    '.pdf',
    '.jpg', '.jpeg', '.png',
    '.mp4', '.avi', '.mov'
}

# Maximum file size (in bytes)
MAX_FILE_SIZE = 50 * 1024 * 1024  # 50MB