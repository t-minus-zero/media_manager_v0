import os
from .utilities import run_command, async_sleep
from .logger import log

class ADBOps:
    def __init__(self, adb_config, device_config):
        # Load device-specific configuration
        self.adb_path = adb_config.get('adb_path', 'adb')
        self.local_folder = adb_config.get('local_folder', './images')
        self.device_camera_folder = device_config.get('device_camera_folder', '/sdcard/DCIM/Camera/')
        self.device_id = device_config['device_id']

    async def run_adb_command(self, command):
        """Run an ADB command for the specific device."""
        command = [self.adb_path, "-s", self.device_id] + command
        try:
            return run_command(command)
        except Exception as e:
            log.log_error("ADBOps.run_adb_command", f"Exception occurred while running ADB command <{command}>: {str(e)}", e)
            return

    async def push_image(self, image_path):
        """Push image to the device and refresh the media scanner."""
        try:
            device_image_path = os.path.join(self.device_camera_folder, os.path.basename(image_path))
            log.log_info("ADBOps.push_image", f"Pushing image {image_path} to {self.device_camera_folder} on the device.")
            command = ["push", image_path, self.device_camera_folder]
            await self.run_adb_command(command)
            await self.refresh_media_scanner(device_image_path)
        except Exception as e:
            log.log_error("ADBOps.push_image", f"Error pushing image: {str(e)}", e)

    async def refresh_media_scanner(self, device_image_path):
        """Force the media scanner to refresh after the image is pushed."""
        try:
            log.log_info("ADBOps.refresh_media_scanner", f"Forcing media scanner to refresh for {device_image_path}.")
            command = ["shell", "am", "broadcast", "-a", "android.intent.action.MEDIA_SCANNER_SCAN_FILE", "-d", f"file://{device_image_path}"]
            await self.run_adb_command(command)
        except Exception as e:
            log.log_error("ADBOps.refresh_media_scanner", f"Error refreshing media scanner: {str(e)}", e)

    async def pull_latest_image(self, saving_folder, saving_file_name):
        """Pull the latest image from the device and save it with a given file name, preserving the original extension."""
        try:
            log.log_info("ADBOps.pull_latest_image", "Pulling the latest image from the device's Camera folder.")
            command = ["shell", "ls", "-t", self.device_camera_folder]
            result = await self.run_adb_command(command)

            if result:
                files = result.splitlines()
                if files:
                    latest_image = files[0]
                    # Extract the extension from the latest image
                    _, extension = os.path.splitext(latest_image)
                    
                    # Construct the full path using the provided file name and the original extension
                    local_image_path = os.path.join(saving_folder, saving_file_name + extension)
                    
                    log.log_info("ADBOps.pull_latest_image", f"Pulling {latest_image} from device to {local_image_path}")
                    
                    # Pull the latest image from the device and save it with the new name
                    command = ["pull", os.path.join(self.device_camera_folder, latest_image), local_image_path]
                    await self.run_adb_command(command)
                    
                    # Return the path to the saved image
                    return local_image_path
                else:
                    log.log_warning("ADBOps.pull_latest_image", "No files found in the Camera folder.")
                    return None
            else:
                log.log_error("ADBOps.pull_latest_image", "Error retrieving the file list from the device.")
                return None
        except Exception as e:
            log.log_error("ADBOps.pull_latest_image", f"Error pulling latest image: {str(e)}", e)
            return None

    async def delete_latest_two_images(self):
        """Delete the latest two images from the device's Camera folder."""
        try:
            log.log_info("ADBOps.delete_latest_two_images", "Deleting the latest two images from the device's Camera folder.")
            command = ["shell", "ls", "-t", self.device_camera_folder]
            result = await self.run_adb_command(command)

            if result:
                files = result.splitlines()
                if len(files) >= 2:
                    latest_two_files = files[:2]
                    for file in latest_two_files:
                        log.log_info("ADBOps.delete_latest_two_images", f"Deleting {file}")
                        command = ["shell", "rm", os.path.join(self.device_camera_folder, file)]
                        await self.run_adb_command(command)
                else:
                    log.log_warning("ADBOps.delete_latest_two_images", "Not enough files to delete (less than two).")
            else:
                log.log_error("ADBOps.delete_latest_two_images", "Error retrieving the file list from the device.")
        except Exception as e:
            log.log_error("ADBOps.delete_latest_two_images", f"Error deleting images: {str(e)}", e)

    async def wait_for_processing(self, seconds=10):
        """Async sleep to wait for a given number of seconds."""
        log.log_info("ADBOps.wait_for_processing", f"Waiting for {seconds} seconds...")
        await async_sleep(seconds)

    async def cleanup(self):
        """Clean up any ongoing processes."""
        log.log_info("ADBOps.cleanup", "Cleaning up ADBOps processes...")
        for process in self.processes:
            if process and not process.returncode:
                try:
                    process.terminate()
                    await process.wait()
                    log.log_success("ADBOps.cleanup", "Terminated process successfully.")
                except Exception as e:
                    log.log_info(f"Error terminating process: {str(e)}", e)
        self.processes.clear()