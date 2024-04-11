import os
import logging
import multiprocessing
import concurrent.futures
import time
from tqdm import tqdm
from video_downloader import VideoDownloader
from video_processor import VideoProcessor
from meta_parser import MetaParser
from config import META_DIR, VIDEO_DIR, OUTPUT_DIR, VIDEO_NUM

logging.basicConfig(filename='video_processing.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

total_downloads = 0
successful_downloads = 0
failed_downloads = 0


def ensure_directories_exist():
    dirs = [META_DIR, VIDEO_DIR, OUTPUT_DIR]
    for dir in dirs:
        os.makedirs(dir, exist_ok=True)


def process_single_file(meta_file, meta_dir, video_dir, output_dir, progress_bar):
    global total_downloads, successful_downloads, failed_downloads
    meta_path = os.path.join(meta_dir, meta_file)
    try:
        meta_info = MetaParser.parse_clip_meta(meta_path)
        video_file = VideoDownloader.download_video(
            video_dir, meta_info, progress_bar)
        total_downloads += 1
        if video_file:
            VideoProcessor.crop_video(meta_info, video_file, output_dir)
            successful_downloads += 1
        else:
            failed_downloads += 1
    except Exception as e:
        failed_downloads += 1
        logging.error(f"Failed to process {meta_file}: {e}")
    finally:
        progress_bar.update(1)


def main():
    ensure_directories_exist()
    start_time = time.time()

    max_workers = min(32, max(4, multiprocessing.cpu_count() - 1))

    meta_files = [f for f in os.listdir(
        META_DIR) if f.endswith('.txt')][:VIDEO_NUM]
    total_videos = len(meta_files)

    with tqdm(total=total_videos, unit='file') as progress_bar:
        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = [executor.submit(process_single_file, meta_file, META_DIR, VIDEO_DIR, OUTPUT_DIR, progress_bar)
                       for meta_file in meta_files]
            concurrent.futures.wait(futures)

    elapsed_time = time.time() - start_time
    print(f"\nTotal time used: {elapsed_time:.2f} seconds")
    print(f"Total downloads attempted: {total_downloads}")
    print(f"Successful downloads: {successful_downloads}")
    print(f"Failed downloads: {failed_downloads}")


if __name__ == "__main__":
    main()
