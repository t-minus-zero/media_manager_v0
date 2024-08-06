import imageio

def create_video(images, output_file, width, height, fps, max_frames):
    """
    Creates a video from the given images and saves it in the specified output file.

    :param images: A list of NumPy arrays representing the images
    :param output_file: The path to the output video file
    :param width: The width of the video
    :param height: The height of the video
    :param fps: The frame rate of the video
    :param max_frames: The maximum number of frames per image
    :return: None
    """
    # Create a video writer object
    with imageio.get_writer(output_file, mode='I', fps=fps, codec='libx264', quality=9) as video_writer:
        for image in images:
            # Add the image to the video for max_frames times
            for _ in range(max_frames):
                video_writer.append_data(image)

import cv2

def create_video_with_opencv(images, output_file, width, height, fps, max_frames):
    """
    Creates a video from the given images using OpenCV and saves it in the specified output file.

    :param images: A list of NumPy arrays representing the images
    :param output_file: The path to the output video file
    :param width: The width of the video
    :param height: The height of the video
    :param fps: The frame rate of the video
    :param max_frames: The maximum number of frames per image
    :return: None
    """
    # Define the codec and create VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    video_writer = cv2.VideoWriter(output_file, fourcc, fps, (width, height))

    for image in images:
        # Ensure the image is in the correct format (uint8)
        if image.dtype != 'uint8':
            image = image.astype('uint8')
        
        # Add the image to the video for max_frames times
        for _ in range(max_frames):
            video_writer.write(image)
    
    # Release the video writer object
    video_writer.release()

# Example usage
# images = [np.zeros((480, 640, 3), dtype=np.uint8) for _ in range(10)]  # Dummy images
# create_video_with_opencv(images, 'output.avi', 640, 480, 30, 5)


from moviepy.editor import ImageSequenceClip
import numpy as np
from image_processing import convert_to_srgb

def create_video_with_moviepy(image_paths, output_file, video_width, video_height, fps, max_frames):
    normalized_images = []
    for image_path in image_paths:
        image = convert_to_srgb(image_path)
        image_array = np.array(image)
        
        # Ensure image is in uint8 format with values between 0 and 255
        if image_array.dtype != 'uint8':
            image_array = image_array.astype('uint8')
        
        normalized_images.extend([image_array] * max_frames)
    
    clip = ImageSequenceClip(normalized_images, fps=fps)
    clip.write_videofile(output_file, codec='libx264', fps=fps, preset='medium', bitrate='8000k', audio_codec='aac')

# Example usage
# image_paths = ['path_to_image1.jpg', 'path_to_image2.jpg', ...]
# create_video_with_moviepy(image_paths, 'output.mp4', 30, 5)