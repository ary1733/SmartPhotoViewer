import subprocess
import logging
from pathlib import Path
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed

# === Simple logger setup ===
logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger("SmartPhotoConverter")


# === Utility ===
def get_cache_dir(base_dir: Path) -> Path:
    cache_dir = base_dir.parent / "cache"
    cache_dir.mkdir(exist_ok=True)
    return cache_dir


# === Worker functions ===
def convert_mov(mov_file: Path, cache_dir: Path):
    output_file = cache_dir / (mov_file.stem + ".mp4")
    if output_file.exists():
        return f"⚡ Skipped {mov_file.name} (cached)"

    cmd = [
        "ffmpeg", "-y", "-i", str(mov_file),
        "-vcodec", "libx264", "-acodec", "aac",
        str(output_file)
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode == 0:
        return f"✅ {mov_file.name} → {output_file.name}"
    else:
        return f"❌ {mov_file.name} failed: {result.stderr.strip()}"


def convert_heic(heic_file: Path, cache_dir: Path):
    output_file = cache_dir / (heic_file.stem + ".jpg")
    if output_file.exists():
        return f"⚡ Skipped {heic_file.name} (cached)"

    cmd = ["magick", str(heic_file), str(output_file)]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode == 0:
        return f"✅ {heic_file.name} → {output_file.name}"
    else:
        return f"❌ {heic_file.name} failed: {result.stderr.strip()}"


# === Parallel conversion ===
def convert_mov_to_mp4(directory: Path, workers: int = 4):
    cache_dir = get_cache_dir(directory)
    mov_files = list(directory.glob("*.MOV"))
    if not mov_files:
        logger.warning("No .MOV files found.")
        return

    logger.info(f"🎬 Converting {len(mov_files)} MOV files with {workers} threads...")
    with ThreadPoolExecutor(max_workers=workers) as executor:
        futures = [executor.submit(convert_mov, f, cache_dir) for f in mov_files]
        for future in as_completed(futures):
            logger.info(future.result())


def convert_heic_to_jpg(directory: Path, workers: int = 4):
    cache_dir = get_cache_dir(directory)
    heic_files = list(directory.glob("*.heic"))
    if not heic_files:
        logger.warning("No .HEIC files found.")
        return

    logger.info(f"🖼️ Converting {len(heic_files)} HEIC files with {workers} threads...")
    with ThreadPoolExecutor(max_workers=workers) as executor:
        futures = [executor.submit(convert_heic, f, cache_dir) for f in heic_files]
        for future in as_completed(futures):
            logger.info(future.result())


def generate_thumbnails(directory: Path, workers: int = 4):
    cache_dir = get_cache_dir(directory)
    video_files = list(directory.glob("*.mov")) + list(directory.glob("*.mp4"))
    logger.info(f"Found {len(video_files)} video files for thumbnail generation.")
    if not video_files:
        logger.info("No video files found for thumbnail generation.")
        return
    need_thumbnails = []
    for video_file in video_files:
        base = video_file.stem
        cache_thumb = cache_dir / f"{base}.jpg"
        if not cache_thumb.exists() and not any((directory / f"{base}{ext}").exists() for ext in [".jpg", ".jpeg", ".png", ".heic"]):
            need_thumbnails.append(video_file)
    def create_thumbnail(video_file: Path):
        base = video_file.stem
        thumb_file = cache_dir / f"{base}.jpg"
        if thumb_file.exists():
            return f"⚡ Skipped thumbnail for {video_file.name} (cached)"

        try:
            ffmpeg_cmd = [
                "ffmpeg", "-y",
                "-i", str(video_file),
                "-ss", "00:00:00.5",
                "-vframes", "1",
                str(thumb_file),
            ]
            subprocess.run(ffmpeg_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            return f"🎞️ Created thumbnail via ffmpeg for {video_file.name}"
        except Exception as e:
            return f"❌ Thumbnail generation failed for {video_file.name}: {e}"

    logger.info(f"🖼️ Generating thumbnails for {len(need_thumbnails)} videos with {workers} threads...")
    with ThreadPoolExecutor(max_workers=workers) as executor:
        futures = [executor.submit(create_thumbnail, f) for f in need_thumbnails]
        for future in as_completed(futures):
            logger.info(future.result())

# === Combined runner ===
def run_all(directory: str, workers: int = 4):
    directory = Path(directory)
    logger.info(f"🚀 Starting safe parallel conversion in: {directory}")
    convert_heic_to_jpg(directory, workers)
    convert_mov_to_mp4(directory, workers)
    generate_thumbnails(directory, workers)
    logger.info("🎉 All conversions completed safely in cache.")


# === CLI Entry point ===
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Safe multi-threaded converter for SmartPhotoViewer")
    parser.add_argument("directory", help="Path to media directory")
    parser.add_argument("--workers", type=int, default=4, help="Number of parallel threads (default: 4)")
    args = parser.parse_args()

    run_all(args.directory, args.workers)
