import os
import pandas as pd
import re
from datetime import datetime, timedelta
from tkinter.filedialog import askopenfilename, askdirectory

from moviepy.editor import *

VIDEO_CLIP_TIME_S = 10

if __name__ == "__main__":
    video_path = askopenfilename(title="Select Video")
    video_dir = os.path.dirname(video_path)

    if not video_path or video_path == "":
        raise Exception("Invalid video path")

    timestamps_path = askopenfilename(title="Select Timestamps")

    if not timestamps_path or timestamps_path == "":
        raise Exception("Invalid timestamps path")

    save_dir = askdirectory(title="Select Save Folder")

    if not save_dir or save_dir == "":
        raise Exception("Invalid save folder")

    clip = VideoFileClip(video_path, verbose=False)
    video_filename = os.path.basename(video_path)
    clip_start_time = datetime.strptime(video_filename, "%Y-%m-%d %H-%M-%S.mkv")
    clip_end_time = clip_start_time + timedelta(seconds=clip.duration)

    with open(timestamps_path, "r") as f:
        timestamps_df = pd.read_csv(timestamps_path)
        timestamps_data = timestamps_df.loc[timestamps_df["is_successful_pick"] == False][
            "index"
        ].tolist()

    for timestamp_data in timestamps_data:
        if timestamp_data.strip() == "":
            continue

        event_time = datetime.strptime(
            timestamp_data, "%Y\\%m\\%d_%H:%M:%S"
        )
        event_time_str = event_time.strftime("%Y-%m-%d_%H-%M_%S")

        if event_time < clip_start_time or event_time > clip_end_time:
            print(
                f"!!! Timestamp Not Within This Clip: {timestamp_data} | {event_time_str} !!!"
            )
            continue

        event_time_start = event_time - timedelta(seconds=int(VIDEO_CLIP_TIME_S / 2))
        event_time_end = event_time + timedelta(seconds=int(VIDEO_CLIP_TIME_S / 2))

        if event_time_start < clip_start_time:
            event_time_start = clip_start_time

        if event_time_end > clip_end_time:
            event_time_end = clip_end_time

        time_elapsed_start = int((event_time_start - clip_start_time).total_seconds())
        time_elapsed_end = int((event_time_end - clip_start_time).total_seconds())

        sub_clip: VideoFileClip = clip.subclip(time_elapsed_start, time_elapsed_end)
        sub_clip.write_videofile(os.path.join(save_dir, f"{event_time_str}.mp4"), logger=None)
