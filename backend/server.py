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
    """
    List photos & videos (JPG/MP4 only).
    For non-standard formats (.HEIC, .MOV), 
    check if converted version exists in cache/.
    """
    files = os.listdir(MEDIA_DIR)
    pairs = []

    # --- Separate by base name ---
    for f in files:
        base, ext = os.path.splitext(f)
        ext = ext.lower()

        # handle direct usable formats
        if ext in [".jpg", ".jpeg", ".png"]:
            img_file = f
            video_file = None

            # Look for video with same base (either mp4/mov)
            for vext in [".mp4", ".mov"]:
                v_candidate = f"{base}{vext}"
                if (MEDIA_DIR / v_candidate).exists() or (CACHE_DIR / f"{base}.mp4").exists():
                    video_file = f"{base}.mp4" if (CACHE_DIR / f"{base}.mp4").exists() else v_candidate
                    break

            pairs.append({"image": img_file, "video": video_file})

        elif ext in [".heic"]:
            # look for cached JPG
            cached_jpg = f"{base}.jpg"
            if (CACHE_DIR / cached_jpg).exists():
                img_file = cached_jpg
            else:
                continue  # skip if not yet converted
            pairs.append({"image": img_file, "video": None})

        elif ext in [".mov"]:
            # look for cached MP4
            cached_mp4 = f"{base}.mp4"
            if (CACHE_DIR / cached_mp4).exists():
                video_file = cached_mp4
            else:
                continue  # skip if not yet converted

            # try to pair with existing image
            image_file = None
            for iext in [".jpg", ".jpeg", ".png", ".heic"]:
                if (MEDIA_DIR / f"{base}{iext}").exists() or (CACHE_DIR / f"{base}.jpg").exists():
                    image_file = f"{base}.jpg" if (CACHE_DIR / f"{base}.jpg").exists() else f"{base}{iext}"
                    break
            pairs.append({"image": image_file, "video": video_file})

    return jsonify(pairs)

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
