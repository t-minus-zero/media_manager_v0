from PIL import Image
import numpy as np

def inspect_image_properties(image_path):
    image = Image.open(image_path)
    print(f"Mode: {image.mode}")
    print(f"Format: {image.format}")
    print(f"Size: {image.size}")
    print(f"Color Profile: {image.info.get('icc_profile')}")
    image_array = np.array(image)
    print(f"Dtype: {image_array.dtype}")
    print(f"Min: {image_array.min()}, Max: {image_array.max()}")
    return image_array

# Example usage
# image_path = 'path_to_your_image.jpg'
# image_array = inspect_image_properties(image_path)

if __name__ == "__main__":
    input_image = r"/Users/marcus/Documents/Coding/Projects/ImagesToVideoScreenshots/media/output_images/IMG_8932.jpg"
    inspect_image_properties(input_image)