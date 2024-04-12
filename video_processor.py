import os
from moviepy.editor import VideoFileClip
import logging
from clip_meta import ClipMeta


class VideoProcessor:
    @staticmethod
    def crop_video(clip_meta: ClipMeta, video_file, output_path):
        safe_video_id = 'anjie' + \
            clip_meta.video_id[1:] if clip_meta.video_id.startswith(
                "-") else clip_meta.video_id

        final_output_file = os.path.join(
            output_path, f"{clip_meta.video_id}_{clip_meta.pid}.mp4")

        if os.path.exists(final_output_file):
            logging.info(
                f"File {final_output_file} already exists. Skipping processing.")
            return

        if not video_file:
            logging.info(f"No video file provided for {
                         clip_meta.video_id}_{clip_meta.pid}.")
            return

        clip = VideoFileClip(video_file)
        trimmed_clip = clip.subclip(clip_meta.start_t, clip_meta.end_t)
        cropped_clip = trimmed_clip.crop(
            x1=clip_meta.x0, y1=clip_meta.y0, x2=clip_meta.x1, y2=clip_meta.y1)

        output_file = os.path.join(
            output_path, f"{safe_video_id}_{clip_meta.pid}.mp4")
        cropped_clip.write_videofile(
            output_file, codec="libx264", preset="ultrafast", audio_codec="aac", threads=4, logger=None)
        clip.close()

        os.rename(output_file, final_output_file)
        logging.info(f"Video processed and saved as {final_output_file}")
