import cv2
import os
import numpy as np

def create_video_writer(output_path, dimensions, fps, codec='avc1', file_extension='.mp4'):
    """
    Creates a video writer object with the specified output path, dimensions, and frame rate.

    :param output_path: The path to the output folder where the video will be saved
    :param dimensions: A tuple of (width, height) for the video dimensions
    :param fps: The frame rate for the video
    :param codec: The codec to be used for the video (default is 'avc1' for .mp4)
    :param file_extension: The file extension for the video (default is '.mp4')
    :return: A video writer object
    """
    fourcc = cv2.VideoWriter_fourcc(*codec)
    output_file = os.path.join(output_path, f'output{file_extension}')
    video_writer = cv2.VideoWriter(output_file, fourcc, fps, dimensions)

    return video_writer

def add_images_to_video(image_files, video_writer, frames_per_image):
    """
    Adds images to the video writer object for the specified number of frames per image.

    :param image_files: A list of image file paths
    :param video_writer: A video writer object
    :param frames_per_image: The number of frames each image should appear in the video
    """
    for image_file in image_files:
        image = cv2.imread(image_file)
        for _ in range(frames_per_image):
            video_writer.write(image)


def save_video(video_writer):
    """
    Closes the video writer object to save the video file.

    :param video_writer: A video writer object
    """
    video_writer.release()
