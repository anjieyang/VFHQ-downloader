import os
import subprocess
import logging
from config import VIDEO_EXTENSIONS

class VideoDownloader:
    @staticmethod
    def download_video(output_dir, video_id):
        video_path = os.path.join(output_dir, f"vid_{video_id}")
        downloaded_file = None

        out_paths = [video_path + ext for ext in VIDEO_EXTENSIONS]
        existing_files = [out_path for out_path in out_paths if os.path.isfile(out_path)]
        if existing_files:
            logging.info(f'File already exists for video ID {video_id}')
            return existing_files[0]

        try:
            command = [
                "yt-dlp",
                f"https://www.youtube.com/watch?v={video_id}",
                "--output", f"{video_path}.%(ext)s",
                "-f", "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best",
                "--external-downloader", "aria2c",
                "--external-downloader-args", "-x 8 -s 8 -k 1M --console-log-level=warn --quiet=true",
                "--progress" 
            ]
            subprocess.check_call(command)

            for ext in VIDEO_EXTENSIONS:
                if os.path.isfile(video_path + ext):
                    downloaded_file = video_path + ext
                    break

            if downloaded_file:
                logging.info(f'Successfully downloaded video ID {video_id} to {downloaded_file}')
                return downloaded_file

        except subprocess.CalledProcessError as e:
            logging.error(f'Failed to download video ID {video_id}: {e}')
        except Exception as e:
            logging.error(f'Unexpected error occurred while downloading video ID {video_id}: {e}')

        if downloaded_file and os.path.exists(downloaded_file):
            os.remove(downloaded_file)
            logging.info(f'Deleted incomplete video file: {downloaded_file}')

        return None
