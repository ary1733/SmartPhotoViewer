from flask import Flask, send_from_directory, jsonify
import os
from pathlib import Path
from convert_utils import run_all  # ✅ the threaded converter we just made
import threading

app = Flask(__name__, static_folder="../frontend", static_url_path="")

# === Directory setup ===
BASE_DIR = Path(__file__).resolve().parent
MEDIA_DIR = (BASE_DIR / "../testmedia").resolve()
CACHE_DIR = (BASE_DIR / "../cache").resolve()
CACHE_DIR.mkdir(exist_ok=True)
WORKERS = 4  # Number of parallel conversion threads

@app.route("/")
def index():
    return send_from_directory(app.static_folder, "index.html")

@app.route("/media/<path:filename>")
def serve_media(filename):
    # 1️⃣ Serve from cache if exists
    cached_path = CACHE_DIR / filename
    if cached_path.exists():
        return send_from_directory(CACHE_DIR, filename)
    # 2️⃣ Fallback to original media
    return send_from_directory(MEDIA_DIR, filename)

@app.route("/list")
def list_media():
    files = os.listdir(MEDIA_DIR)
    # also check cache for converted files
    files.extend(os.listdir(CACHE_DIR))
    # unique files only
    files = list(set(files))
    pairs = []

    for f in files:
        base, ext = os.path.splitext(f)
        ext = ext.lower()

        if ext in [".jpg", ".jpeg"]:
            img_file = f
            video_file = None

            for vext in [".mp4", ".mov", ".MOV"]:
                v_candidate = f"{base}{vext}"
                if (MEDIA_DIR / v_candidate).exists() or (CACHE_DIR / f"{base}.mp4").exists():
                    video_file = f"{base}.mp4" if (CACHE_DIR / f"{base}.mp4").exists() else v_candidate
                    break

            pairs.append({"image": img_file, "video": video_file, "ready": True})
        elif ext in [".mp4"]:
            video_file = f
            img_file = None

            for iext in [".jpg", ".jpeg"]:
                i_candidate = f"{base}{iext}"
                if (MEDIA_DIR / i_candidate).exists() or (CACHE_DIR / f"{base}.jpg").exists():
                    img_file = f"{base}.jpg" if (CACHE_DIR / f"{base}.jpg").exists() else i_candidate
                    break

            if img_file is None:
                pairs.append({"image": img_file, "video": video_file, "ready": False})
            
            # else will already be added in the image section
        elif ext in [".heic", ".mov"]:
            cached_jpg = f"{base}.jpg"
            cached_mp4 = f"{base}.mp4"

            img_ready = (CACHE_DIR / cached_jpg).exists()
            vid_ready = (CACHE_DIR / cached_mp4).exists()

            if ext == ".mov" and not (img_ready and vid_ready):
                pairs.append({
                    "image": None,
                    "video": f,
                    "ready": img_ready and vid_ready
                })
            elif ext in [".heic"] and not img_ready:
                pairs.append({
                    "image": f,
                    "video": None,
                    "ready": img_ready
                })
            # else will be added in the converted sections
    return jsonify(pairs)

# === Background conversion thread ===
# === Background conversion thread ===
def background_convert():
    """Run safe threaded conversions in background at startup"""
    try:
        app.logger.info("🌀 Starting background media conversion...")
        run_all(str(MEDIA_DIR), WORKERS)
        app.logger.info("✅ Initial conversion complete.")
    except Exception as e:
        app.logger.error(f"⚠️ Background conversion failed: {e}")

# === Startup Hooks ===
@app.before_first_request
def start_background_thread():
    thread = threading.Thread(target=background_convert, daemon=True)
    thread.start()

if __name__ == "__main__":
    app.run(port=8000, debug=True, host="0.0.0.0")
