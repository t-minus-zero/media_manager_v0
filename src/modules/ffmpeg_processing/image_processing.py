import glob
import os
from PIL import Image, ImageCms

def get_image_files_old(input_folder, size_v, size_h):
    """
    Retrieves all image files from the input folder and sorts them in the desired order.

    :param input_folder: The path to the input folder containing the images
    :return: A sorted list of image file paths
    """
    # Get all image files in the input folder
    image_files = glob.glob(os.path.join(input_folder, '*.JPG')) + glob.glob(os.path.join(input_folder, '*.jpeg')) + glob.glob(os.path.join(input_folder, '*.png'))

    # Sort the image files
    image_files.sort()

    return image_files

def get_image_files(input_folder, size_v, size_h):
    """
    Retrieves all image files from the input folder and sorts them in the desired order.

    :param input_folder: The path to the input folder containing the images
    :param size_v: The required height of the images in pixels
    :param size_h: The required width of the images in pixels
    :return: A sorted list of image file paths
    """
    # Get all image files in the input folder
    image_files = glob.glob(os.path.join(input_folder, '*.jpg')) + glob.glob(os.path.join(input_folder, '*.jpeg')) + glob.glob(os.path.join(input_folder, '*.png'))

    # Filter the image files based on the specified dimensions
    selected_files = []
    for file in image_files:
        img = Image.open(file)
        #print(f"Image: {file}, Size: {img.size}")  # Print the size of each image
        if img.size == (size_h, size_v):
            selected_files.append(file)
            #print(f"Selected: {file}")  # Print when an image is selected

    # Sort the selected image files
    selected_files.sort()

    return selected_files

from io import BytesIO
import numpy as np

def convert_to_srgb(image_path):
    try:
        image = Image.open(image_path)
        if 'icc_profile' in image.info:
            icc_profile = image.info['icc_profile']
            input_profile = ImageCms.ImageCmsProfile(BytesIO(icc_profile))
            srgb_profile = ImageCms.createProfile('sRGB')
            image = ImageCms.profileToProfile(image, input_profile, srgb_profile)
        return image
    except Exception as e:
        print(f"Error converting {image_path} to sRGB: {e}")
        return Image.open(image_path)  # Return the original image if conversion fails

# Example usage
# image = convert_to_srgb('path_to_your_image.jpg')
# image.show()

