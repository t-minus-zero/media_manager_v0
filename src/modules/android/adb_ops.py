import os
import subprocess
import time
import asyncio

# Custom exception for ADB errors
class ADBImageManagerError(Exception):
    """Custom exception class for ADBImageManager errors."""
    def __init__(self, message, command=None, stderr=None):
        super().__init__(message)
        self.command = command
        self.stderr = stderr

class ADBImageManager:
    def __init__(self, adb_path="adb", device_camera_folder="/sdcard/DCIM/Camera/", local_folder=""):
        self.adb_path = adb_path
        self.device_camera_folder = device_camera_folder
        self.local_folder = local_folder

    async def run_adb_command(self, command):
        """Run an ADB command synchronously but wrap it in an async-compatible method."""
        try:
            result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            if result.returncode == 0:
                return result.stdout.strip()
            else:
                error_message = f"ADB command failed: {' '.join(command)}"
                raise ADBImageManagerError(error_message, command=command, stderr=result.stderr)
        except Exception as e:
            raise ADBImageManagerError(f"Exception occurred while running ADB command: {str(e)}", command=command)

    async def push_image(self, image_path):
        """Push image to the device and refresh the media scanner."""
        try:
            device_image_path = os.path.join(self.device_camera_folder, os.path.basename(image_path))
            print(f"Pushing image {image_path} to {self.device_camera_folder} on the device.")
            command = [self.adb_path, "push", image_path, self.device_camera_folder]
            await self.run_adb_command(command)
            await self.refresh_media_scanner(device_image_path)
        except ADBImageManagerError as e:
            print(f"Error pushing image: {str(e)}, Command: {e.command}, Stderr: {e.stderr}")

    async def refresh_media_scanner(self, device_image_path):
        """Force the media scanner to refresh after the image is pushed."""
        try:
            print(f"Forcing media scanner to refresh for {device_image_path}.")
            command = [self.adb_path, "shell", "am", "broadcast", "-a", "android.intent.action.MEDIA_SCANNER_SCAN_FILE", "-d", f"file://{device_image_path}"]
            await self.run_adb_command(command)
        except ADBImageManagerError as e:
            print(f"Error refreshing media scanner: {str(e)}, Command: {e.command}, Stderr: {e.stderr}")

    async def pull_latest_image(self, saving_folder, saving_file_name):
        """Pull the latest image from the device and save it with a given file name, preserving the original extension."""
        try:
            print("Pulling the latest image from the device's Camera folder.")
            command = [self.adb_path, "shell", "ls", "-t", self.device_camera_folder]
            result = await self.run_adb_command(command)

            if result:
                files = result.splitlines()
                if files:
                    latest_image = files[0]
                    # Extract the extension from the latest image
                    _, extension = os.path.splitext(latest_image)
                    
                    # Construct the full path using the provided file name and the original extension
                    local_image_path = os.path.join(saving_folder, saving_file_name + extension)
                    
                    print(f"Pulling {latest_image} from device to {local_image_path}")
                    
                    # Pull the latest image from the device and save it with the new name
                    command = [self.adb_path, "pull", os.path.join(self.device_camera_folder, latest_image), local_image_path]
                    await self.run_adb_command(command)
                    
                    # Return the path to the saved image
                    return local_image_path
                else:
                    print("No files found in the Camera folder.")
                    return None
            else:
                print("Error retrieving the file list from the device.")
                return None
        except ADBImageManagerError as e:
            print(f"Error pulling latest image: {str(e)}, Command: {e.command}, Stderr: {e.stderr}")
            return None


    async def delete_latest_two_images(self):
        """Delete the latest two images from the device's Camera folder."""
        try:
            print("Deleting the latest two images from the device's Camera folder.")
            command = [self.adb_path, "shell", "ls", "-t", self.device_camera_folder]
            result = await self.run_adb_command(command)

            if result:
                files = result.splitlines()
                if len(files) >= 2:
                    latest_two_files = files[:2]
                    for file in latest_two_files:
                        print(f"Deleting {file}")
                        command = [self.adb_path, "shell", "rm", os.path.join(self.device_camera_folder, file)]
                        await self.run_adb_command(command)
                else:
                    print("Not enough files to delete (less than two).")
            else:
                print("Error retrieving the file list from the device.")
        except ADBImageManagerError as e:
            print(f"Error deleting images: {str(e)}, Command: {e.command}, Stderr: {e.stderr}")

    async def wait_for_processing(self, seconds=10):
        """Async sleep to wait for a given number of seconds."""
        print(f"Waiting for {seconds} seconds...")
        await asyncio.sleep(seconds)