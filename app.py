from flask import Flask, request, jsonify
import os
from werkzeug.utils import secure_filename
import subprocess
from pathlib import Path

app = Flask(__name__)

BASE_DIR = Path(__file__).resolve().parent
INCOMING_DIR = BASE_DIR / "incoming"

# --- Upload endpoint ---
@app.route("/upload", methods=["POST"])
def upload_file():
    if 'file' not in request.files:
        return "No file part", 400
    file = request.files['file']
    if file.filename == '':
        return "No selected file", 400
    filename = secure_filename(file.filename)
    filepath = INCOMING_DIR / filename
    file.save(str(filepath))

    # Run the import_docs.py script to sort the file
    subprocess.run(["python3", str(BASE_DIR / "import_docs.py")])

    return jsonify({"status": "uploaded", "filename": filename})

# --- Basic health check ---
@app.route("/")
def index():
    return "DocServer running"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
