import os
from clip_meta import ClipMeta

class MetaParser:
    @staticmethod
    def parse_clip_meta(clip_meta_path):
        with open(clip_meta_path, "r") as clip_meta_file:
            clip_name = os.path.splitext(os.path.basename(clip_meta_path))[0]
            for line in clip_meta_file:
                if line.startswith("H"):
                    clip_height = int(line.strip().split(" ")[-1])
                elif line.startswith("W"):
                    clip_width = int(line.strip().split(" ")[-1])
                elif line.startswith("FPS"):
                    clip_fps = float(line.strip().split(" ")[-1])
                elif line.startswith("CROP"):
                    clip_crop_bbox = line.strip().split(" ")[-4:]
                    x0, y0, x1, y1 = map(int, clip_crop_bbox)

            _, videoid, pid, clip_idx, frame_rlt = clip_name.split("+")
            pid = int(pid.split("P")[1])
            clip_idx = int(clip_idx.split("C")[1])
            frame_start, frame_end = map(int, frame_rlt.replace("F", "").split("-"))

            start_t = round(frame_start / clip_fps, 5)
            end_t = round(frame_end / clip_fps, 5)
            duration_t = end_t - start_t

            return ClipMeta(
                video_id=videoid, pid=pid, clip_idx=clip_idx, frame_start=frame_start,
                frame_end=frame_end, start_t=start_t, end_t=end_t, duration_t=duration_t,
                height=clip_height, width=clip_width, fps=clip_fps, x0=x0, y0=y0, x1=x1, y1=y1,
            )
