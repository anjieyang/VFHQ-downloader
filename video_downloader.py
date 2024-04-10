import os
import subprocess
import logging
from config import VIDEO_EXTENSIONS


class VideoDownloader:
    @staticmethod
    def download_video(output_dir, meta_info):
        video_path = os.path.join(
            output_dir, f"clip_{meta_info.video_id}_{meta_info.pid}")
        postprocessor_args = f"ffmpeg:-ss {
            meta_info.start_t} -to {meta_info.end_t}"

        command = [
            "yt-dlp",
            f"https://www.youtube.com/watch?v={meta_info.video_id}",
            "--output", f"{video_path}.%(ext)s",
            "-f", "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best",
            "--external-downloader", "aria2c",
            "--external-downloader-args", "-x 8 -s 8 -k 1M --console-log-level=warn --quiet=true",
            "--progress",
            "--postprocessor-args", postprocessor_args
        ]

        try:
            subprocess.check_call(command)
            # Check for the downloaded file and return the path if found
            for ext in VIDEO_EXTENSIONS:
                if os.path.isfile(video_path + ext):
                    downloaded_file = video_path + ext
                    logging.info(f'Successfully downloaded video clip for ID {
                                 meta_info.video_id}_{meta_info.pid} to {downloaded_file}')
                    return downloaded_file
        except subprocess.CalledProcessError as e:
            logging.error(f'Failed to download video clip for ID {
                          meta_info.video_id}_{meta_info.pid}: {e}')
        except Exception as e:
            logging.error(f'Unexpected error occurred while downloading video clip for ID {
                          meta_info.video_id}_{meta_info.pid}: {e}')

        return None
