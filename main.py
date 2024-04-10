import os
import logging
import multiprocessing
import concurrent.futures
from video_downloader import VideoDownloader
from video_processor import VideoProcessor
from meta_parser import MetaParser
from config import META_DIR, VIDEO_DIR, OUTPUT_DIR, VIDEO_NUM

logging.basicConfig(filename='video_processing.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')


def ensure_directories_exist():
    dirs = [META_DIR, VIDEO_DIR, OUTPUT_DIR]
    for dir in dirs:
        os.makedirs(dir, exist_ok=True)


def process_single_file(meta_file, meta_dir, video_dir, output_dir):
    meta_path = os.path.join(meta_dir, meta_file)
    try:
        meta_info = MetaParser.parse_clip_meta(meta_path)
        video_file = VideoDownloader.download_video(
            video_dir, meta_info)
        if video_file:
            VideoProcessor.crop_video(meta_info, video_file, output_dir)
    except Exception as e:
        logging.error(f"Failed to process {meta_file}: {e}")


def main():
    ensure_directories_exist()

    max_workers = min(32, max(4, multiprocessing.cpu_count() - 1))

    meta_files = [f for f in os.listdir(META_DIR) if f.endswith('.txt')]

    # Number of videos you want to download
    meta_files = meta_files[:VIDEO_NUM]

    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(process_single_file, meta_file, META_DIR, VIDEO_DIR, OUTPUT_DIR)
                   for meta_file in meta_files]
        concurrent.futures.wait(futures)


if __name__ == "__main__":
    main()
