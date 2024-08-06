import os
import imageio as imageio

def extract_frames(video_file, output_folder, start_frame, step):
    # Create the output folder if it does not exist
    os.makedirs(output_folder, exist_ok=True)

    # Read the video
    video_reader = imageio.get_reader(video_file)

    for i, frame in enumerate(video_reader):
        if i >= start_frame and (i - start_frame) % step == 0:
            # Crop the frame by 128 pixels from the bottom
            cropped_frame = frame[:-128, :, :]
            # Save the cropped frame as an image in the output folder
            output_file = os.path.join(output_folder, f"chained_together_2_{i:03d}.jpg")
            imageio.imwrite(output_file, cropped_frame)

def main():
    # Define the input video file and output folder paths
    app_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    input_video_file = os.path.join(app_path, 'media', 'input_video', 'phone_v.mov') #r"C:\Users\gurpr\Documents\Coding\Projects\images_to_video_and_back\v0.1\media\input_video\output_video.mp4"
    
    input_video_file = r"/Users/marcus/Documents/Coding/Projects/ImagesToVideoScreenshots/media/input_videos/video_2.MOV"
    output_folder = r"/Users/marcus/Documents/Coding/Projects/ImagesToVideoScreenshots/media/input_images"


    # Extract frames from the video
    start_frame = 5
    step = 8
    extract_frames(input_video_file, output_folder, start_frame, step)

if __name__ == "__main__":
    main()
