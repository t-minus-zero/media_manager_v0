import os
import subprocess

def convert_heic_to_jpg(input_folder, output_folder):
    # Ensure the output directory exists
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Iterate through all files in the input directory
    for filename in os.listdir(input_folder):
        if filename.lower().endswith('.heic'):
            heic_path = os.path.join(input_folder, filename)
            jpg_filename = os.path.splitext(filename)[0] + '.jpg'
            jpg_path = os.path.join(output_folder, jpg_filename)
            
            # Convert HEIC to JPG using ImageMagick
            try:
                subprocess.run(['magick', 'convert', heic_path, jpg_path], check=True)
                print(f"Converted {heic_path} to {jpg_path}")
            except subprocess.CalledProcessError as e:
                print(f"Failed to convert {heic_path}: {e}")

def main():
    # Define the input and output folder paths
    input_folder = r"/Users/marcus/Documents/Coding/Projects/ImagesToVideoScreenshots/media/input_images"
    output_folder = r"/Users/marcus/Documents/Coding/Projects/ImagesToVideoScreenshots/media/output_images"

    convert_heic_to_jpg(input_folder, output_folder)

if __name__ == "__main__":
    main()