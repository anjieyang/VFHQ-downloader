# VFHQ-downloader

VFHQ-downloader is a Python-based utility designed for the easy downloading and processing of videos from the [VFHQ dataset](https://liangbinxie.github.io/projects/vfhq/).

## Setup

1. Clone the repository or download the source code.
2. Install required Python packages: `pip install -r requirements.txt`.
3. Ensure `yt-dlp` and `aria2c` are installed and accessible in your system's PATH.
4. Download and decompress the [meta_info.zip](https://1drv.ms/u/s!Ag1HH_EDGMqqh2i5sgNyHpcVldos?e=8wKFtV) file in the root directory of the project to obtain the metadata files needed for video processing.

## Usage

1. Ensure the metadata files are located in the `meta_info/` directory.
2. Run `main.py` to start the downloading and processing pipeline.
3. Processed videos will be available in the `data/outputs/` directory.

## Note

This tool is specifically tailored for the VFHQ dataset and require modifications to work with other datasets or video sources.
