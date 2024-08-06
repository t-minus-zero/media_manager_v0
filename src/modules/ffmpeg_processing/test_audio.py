import os
from moviepy.editor import VideoFileClip
from natsort import natsorted

output_fps = 30
video_dir = '../media/input_videos/'

# get list of video files
video_files = natsorted([f for f in os.listdir(video_dir) if f.endswith('.MOV')])  # assuming .MOV files

for i, filename in enumerate(video_files):
    video_clip = VideoFileClip(os.path.join(video_dir, filename))

    # Check if the clip has audio
    if video_clip.audio is None:
        print(f'Video {filename} does not have any audio.')
    else:
        print(f'Video {filename} has audio.')
    
    # Test if a single video clip's audio and video can be extracted and recombined
    if i == 0:
        video_clip.write_videofile('../media/output_video/test.mp4', codec='libx264', audio_codec='aac', fps=output_fps)
