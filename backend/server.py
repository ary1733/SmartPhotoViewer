from flask import Flask, send_from_directory, request, jsonify
import os

app = Flask(__name__, static_folder="../frontend", static_url_path="")
MEDIA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../media")
@app.route("/")
def index():
    return send_from_directory(app.static_folder, "index.html")

@app.route("/media/<path:filename>")
def serve_media(filename):
    return send_from_directory(MEDIA_DIR, filename)

@app.route("/list")
def list_media():
    files = os.listdir(MEDIA_DIR)
    photos = [f for f in files if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
    videos = [f for f in files if f.lower().endswith(('.mov', '.mp4'))]
    pairs = []
    for img in photos:
        base = os.path.splitext(img)[0]
        video = next((v for v in videos if os.path.splitext(v)[0] == base), None)
        pairs.append({"image": img, "video": video})
    return jsonify(pairs)

if __name__ == "__main__":
    app.run(port=8000, debug=True, host="0.0.0.0")
