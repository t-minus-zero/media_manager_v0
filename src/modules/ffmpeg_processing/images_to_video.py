import os
from pathlib import Path
import imageio.v3 as imageio  # Use imageio.v2.imread to avoid the deprecation warning
import numpy as np
from skimage.transform import resize
from image_processing import get_image_files
from video_processing import create_video
from video_processing import create_video_with_opencv
from video_processing import create_video_with_moviepy

def resize_image(image, target_width):
    height, width, _ = image.shape
    aspect_ratio = float(height) / float(width)
    target_height = int(target_width * aspect_ratio)
    resized_image = resize(image, (target_height, target_width), mode='constant', preserve_range=True).astype(np.uint8)
    return resized_image

def main():
    # Define the input and output folder paths
    app_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    input_folder = os.path.join(app_path, 'media', 'input_images') #r"C:\Users\gurpr\Documents\Coding\Projects\images_to_video_and_back\v0.1\media\input_images"
    output_folder = os.path.join(app_path, 'media', 'output_video') # r"C:\Users\gurpr\Documents\Coding\Projects\images_to_video_and_back\v0.1\media\output_video"

    input_folder = r"/Users/marcus/Documents/Coding/Projects/ImagesToVideoScreenshots/media/output_images"
    output_folder = r"/Users/marcus/Documents/Coding/Projects/ImagesToVideoScreenshots/media/output_video"
    output_file = os.path.join(output_folder, "output_video.mp4")

    print(input_folder)

    # Calculate the new video dimensions
    # Selfies(3088,1736) BackCamera(3840,2160) *(3024, 4032)-(4032,3024)-(2316, 3088)
    img_height = 3024
    img_width = 4032

    # Get the image files from the input folder
    image_files = get_image_files(input_folder, img_height, img_width) 
    print('Number of selected images: ')
    print (len(image_files))

    # Calculate the new video dimensions
    video_height = img_height
    video_width = img_width

    # Calculate the maximum number of images for the 3-minute video
    fps = 30
    max_frames_per_image = 8
    total_frames = fps * 178 * 10   # 30 fps * 120 seconds = 5400 frames (675 pics)
    max_images = total_frames // max_frames_per_image
    print('Maximum images that can be selected: ')
    print(max_images)

    # Limit the number of images to the maximum calculated number
    image_files = image_files[:max_images]

    # Prepare the images for the video
    print('Preparing images for video ...')
    images = []
    for image_file in image_files:
        image = imageio.imread(image_file)
        #resized_image = resize_image(image, video_width)
        #padded_image = np.pad(resized_image, ((0, video_height - resized_image.shape[0]), (0, 0), (0, 0)), mode='constant')
        images.append(image) # replace image with padded_image if you want some spacing at the bottom

    # Create the video from the prepared images
    print('Creating video ...')
    create_video_with_moviepy(image_files, output_file, video_width, video_height, fps, max_frames_per_image)

if __name__ == "__main__":
    main()
