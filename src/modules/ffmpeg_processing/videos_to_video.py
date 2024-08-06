import os
import json
from moviepy.editor import concatenate_videoclips, concatenate_audioclips, VideoFileClip, AudioClip, ImageSequenceClip
from natsort import natsorted

output_fps = 30
frame_gap = 10
video_dir = '../media/input_videos/'
output_file = '../media/output_video/videos_mushup_1.mp4'
times_file = '../media/output_videos/times.json'

# get list of video files
video_files = natsorted([f for f in os.listdir(video_dir) if f.endswith('.MOV')])  # assuming .MOV files

video_clips = []
audio_clips = []
times = []
total_frames = 0

# create a silent audio clip for the gaps
silence = AudioClip(lambda t: [0, 0], duration=frame_gap / output_fps)

for i, filename in enumerate(video_files):
    video_clip = VideoFileClip(os.path.join(video_dir, filename))

    # calculate start and end times
    start_time = total_frames / output_fps
    end_time = start_time + video_clip.duration

    # append times
    times.append([start_time, end_time])

    # append current video and audio clip
    video_clips.append(video_clip)
    audio_clips.append(video_clip.audio)

    # prepare next frame gap if it's not the last clip
    if i != len(video_files) - 1:
        next_filename = video_files[i + 1]
        next_clip = VideoFileClip(os.path.join(video_dir, next_filename))
        next_frame = next_clip.get_frame(0)
        next_frame_clip = ImageSequenceClip([next_frame] * frame_gap, fps=output_fps)

        video_clips.append(next_frame_clip)
        audio_clips.append(silence)  # add silence audio for the gap

    total_frames += video_clip.duration * output_fps + frame_gap  # add frame_gap for the next clip

# stitch the video and audio clips together
final_video = concatenate_videoclips(video_clips)
final_audio = concatenate_audioclips(audio_clips)

final_clip = final_video.set_audio(final_audio)

# write the result to a file
final_clip.write_videofile(output_file, codec='libx264', audio_codec='aac', fps=output_fps)

# save start and end times to a JSON file
with open(times_file, 'w') as f:
    json.dump(times, f)
