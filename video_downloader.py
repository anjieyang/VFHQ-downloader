import os
import subprocess
import logging
from config import VIDEO_EXTENSIONS


class VideoDownloader:
    @staticmethod
    def download_video(output_dir, meta_info):
        video_path = os.path.join(
            output_dir, f"vid_{meta_info.video_id}")

        command = [
            "yt-dlp",
            f"https://www.youtube.com/watch?v={meta_info.video_id}",
            "--output", f"{video_path}.%(ext)s",
            "-f", "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best",
            "--external-downloader", "aria2c",
            "--external-downloader-args", "-x 8 -s 8 -k 1M --console-log-level=warn --quiet=true",
            "--progress"
        ]

        try:
            subprocess.check_call(command)
            # Check for the downloaded file and return the path if found
            for ext in VIDEO_EXTENSIONS:
                if os.path.isfile(video_path + ext):
                    downloaded_file = video_path + ext
                    logging.info(f'Successfully downloaded video for ID {
                                 meta_info.video_id} to {downloaded_file}')
                    return downloaded_file
        except subprocess.CalledProcessError as e:
            logging.error(f'Failed to download video for ID {
                          meta_info.video_id}: {e}')
        except Exception as e:
            logging.error(f'Unexpected error occurred while downloading video for ID {
                          meta_info.video_id}: {e}')

        return None
