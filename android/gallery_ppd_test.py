import os
import subprocess
import time
import asyncio

# ADBImageManager class with async compatibility
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
                print(f"Error running command: {result.stderr}")
                return None
        except Exception as e:
            print(f"Exception occurred: {str(e)}")
            return None

    async def push_image(self, image_path):
        """Push image to the device and refresh the media scanner."""
        device_image_path = os.path.join(self.device_camera_folder, os.path.basename(image_path))
        print(f"Pushing image {image_path} to {self.device_camera_folder} on the device.")
        command = [self.adb_path, "push", image_path, self.device_camera_folder]
        await self.run_adb_command(command)
        await self.refresh_media_scanner(device_image_path)

    async def refresh_media_scanner(self, device_image_path):
        """Force the media scanner to refresh after the image is pushed."""
        print(f"Forcing media scanner to refresh for {device_image_path}.")
        command = [self.adb_path, "shell", "am", "broadcast", "-a", "android.intent.action.MEDIA_SCANNER_SCAN_FILE", "-d", f"file://{device_image_path}"]
        await self.run_adb_command(command)

    async def pull_latest_image(self):
        """Pull the latest image from the device."""
        print("Pulling the latest image from the device's Camera folder.")
        command = [self.adb_path, "shell", "ls", "-t", self.device_camera_folder]
        result = await self.run_adb_command(command)

        if result:
            files = result.splitlines()
            if files:
                latest_image = files[0]
                local_image_path = os.path.join(self.local_folder, latest_image)
                print(f"Pulling {latest_image} from device to {local_image_path}")
                command = [self.adb_path, "pull", os.path.join(self.device_camera_folder, latest_image), self.local_folder]
                await self.run_adb_command(command)
            else:
                print("No files found in the Camera folder.")
        else:
            print("Error retrieving the file list from the device.")

    async def delete_latest_two_images(self):
        """Delete the latest two images from the device's Camera folder."""
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

    async def wait_for_processing(self, seconds=10):
        """Async sleep to wait for a given number of seconds."""
        print(f"Waiting for {seconds} seconds...")
        await asyncio.sleep(seconds)
