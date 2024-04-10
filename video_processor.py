import os
from moviepy.editor import VideoFileClip
import logging
from clip_meta import ClipMeta


class VideoProcessor:
    @staticmethod
    def crop_video(clip_meta: ClipMeta, video_file, output_path):
        if not video_file:
            logging.info(f"No video file provided for {clip_meta.video_id}.")
            return

        safe_video_id = 'anjie' + \
            clip_meta.video_id[1:] if clip_meta.video_id.startswith(
                "-") else clip_meta.video_id
        clip = VideoFileClip(video_file)
        trimmed_clip = clip.subclip(clip_meta.start_t, clip_meta.end_t)
        cropped_clip = trimmed_clip.crop(
            x1=clip_meta.x0, y1=clip_meta.y0, x2=clip_meta.x1, y2=clip_meta.y1)

        output_file = os.path.join(output_path, f"{safe_video_id}.mp4")
        cropped_clip.write_videofile(
            output_file, codec="libx264", preset="ultrafast", audio_codec="aac", threads=4)

        clip.close()
        os.rename(output_file, os.path.join(
            output_path, f"{clip_meta.video_id}.mp4"))
