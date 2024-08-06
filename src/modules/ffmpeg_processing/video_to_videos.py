import os
import json
from moviepy.editor import VideoFileClip

input_file = '../media/output_video/videos_mushup.MOV'
times_file = '../media/output_videos/times.json'
output_dir = '../media/output_videos/'

# load the video
video = VideoFileClip(input_file)

# load the timestamps
with open(times_file, 'r') as f:
    times = json.load(f)

# cut and save clips based on the timestamps
for i, time in enumerate(times):
    clip = video.subclip(time[0], time[1])
    clip_filename = f'clip_{i+1}.mp4'
    clip.write_videofile(os.path.join(output_dir, clip_filename), codec='libx264', audio_codec='aac', fps=video.fps)
