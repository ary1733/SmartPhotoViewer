import subprocess
import logging
from pathlib import Path
import sys

# === Simple logger setup ===
logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger("SmartPhotoConverter")


# === Convert .MOV → .MP4 using FFmpeg ===
def convert_mov_to_mp4(directory: str):
    """
    Converts all .MOV files in the given directory to .MP4 using FFmpeg.
    Example command:
        ffmpeg -i input.MOV -vcodec libx264 -acodec aac output.mp4
    """
    directory = Path(directory)
    mov_files = list(directory.glob("*.MOV"))

    if not mov_files:
        logger.warning("No .MOV files found in directory.")
        return

    for mov_file in mov_files:
        output_file = mov_file.with_suffix(".mp4")
        command = [
            "ffmpeg", "-y", "-i", str(mov_file),
            "-vcodec", "libx264", "-acodec", "aac",
            str(output_file)
        ]
        logger.info(f"🎬 Converting {mov_file.name} → {output_file.name}")

        result = subprocess.run(command, capture_output=True, text=True)

        if result.returncode == 0:
            logger.info(f"✅ Successfully converted: {mov_file.name}")
        else:
            logger.error(f"❌ Failed to convert {mov_file.name}\n{result.stderr}")


# === Convert .HEIC → .JPG using ImageMagick ===
def convert_heic_to_jpg(directory: str):
    """
    Converts all .HEIC files in the given directory to .JPG using ImageMagick.
    Example command:
        magick mogrify -format jpg *.heic
    """
    directory = Path(directory)
    heic_files = list(directory.glob("*.heic"))

    if not heic_files:
        logger.warning("No .HEIC files found in directory.")
        return

    command = ["magick", "mogrify", "-format", "jpg", "*.heic"]
    logger.info(f"🖼️  Converting HEIC → JPG in: {directory}")

    result = subprocess.run(command, cwd=directory, capture_output=True, text=True)

    if result.returncode == 0:
        logger.info(f"✅ Successfully converted HEIC files to JPG in {directory}")
    else:
        logger.error(f"❌ HEIC conversion failed:\n{result.stderr}")


# === Combined runner ===
def run_all(directory: str):
    """
    Runs both conversions in sequence (HEIC→JPG then MOV→MP4).
    """
    logger.info(f"🚀 Starting conversion in: {directory}")
    convert_heic_to_jpg(directory)
    convert_mov_to_mp4(directory)
    logger.info("🎉 All conversions completed.")


# === Entry point ===
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python convert_utils.py <directory_path>")
        sys.exit(1)

    target_dir = sys.argv[1]
    run_all(target_dir)
