from typing import NamedTuple

class ClipMeta(NamedTuple):
    video_id: str
    pid: int
    clip_idx: int
    frame_start: int
    frame_end: int
    start_t: float
    end_t: float
    duration_t: float
    height: int
    width: int
    fps: float
    x0: int
    y0: int
    x1: int
    y1: int
