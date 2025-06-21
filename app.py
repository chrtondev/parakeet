from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
from pathlib import Path
import import_docs  # <-- this imports your sort logic

app = Flask(__name__)

BASE_DIR = Path(__file__).resolve().parent
INCOMING_DIR = BASE_DIR / "incoming"

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

    # Sort file immediately
    import_docs.ensure_dirs()
    import_docs.sort_file(filepath)

    return jsonify({"status": "uploaded and sorted", "filename": filename})

@app.route("/")
def index():
    return "DocServer running"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
