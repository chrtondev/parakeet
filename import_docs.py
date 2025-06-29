# import_docs.py

import os
import shutil
import datetime
import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
INCOMING_DIR = BASE_DIR / "incoming"
LOG_FILE = BASE_DIR / "logs" / "import_log.json"

EXT_MAP = {
    ".txt": "txt",
    ".md": "md",
    ".pdf": "pdf",
    ".png": "images",
    ".jpg": "images",
    ".jpeg": "images",
    ".gif": "images"
}

def ensure_dirs():
    for folder in ["incoming", "txt", "md", "pdf", "images", "misc", "logs"]:
        (BASE_DIR / folder).mkdir(parents=True, exist_ok=True)

def log_entry(file, dest_folder):
    entry = {
        "file": file,
        "dest": dest_folder,
        "timestamp": datetime.datetime.now().isoformat()
    }
    if not LOG_FILE.exists():
        with open(LOG_FILE, "w") as f:
            json.dump([], f)
    with open(LOG_FILE, "r+") as f:
        data = json.load(f)
        data.append(entry)
        f.seek(0)
        json.dump(data, f, indent=2)

def sort_file(file_path: Path):
    ext = file_path.suffix.lower()
    folder = EXT_MAP.get(ext, "misc")
    dest = BASE_DIR / folder / file_path.name
    shutil.move(str(file_path), str(dest))
    log_entry(file_path.name, folder)
