import asyncio
import subprocess
import requests
from .appium_ops import AppiumOps
from .adb_ops import ADBOps
from .android_ops import AndroidOps
from .logger import log

class PhoneOps:
    def __init__(self, android_config):
        # Load device configuration
        self.device_config = android_config['device']
        self.device_name = self.device_config['device_name']
        self.adb_config = android_config['adb']
        self.appium_config = android_config['appium']

        # Initialize state
        self.current_app = None
        self.is_busy = False
        self.ready = False
        self.apps = android_config['apps']
        self.android_ops = None  # Set AndroidOps to None initially

    async def async_initialize(self):
        """Asynchronous initialization of the device."""
        if not self.is_device_connected(self.device_config['device_id']):
            log.log_error('PhoneOps.async_initialize', f"Device '{self.device_name}' with ID '{self.device_config['device_id']}' is not connected.")
            return

        self.adb_manager = ADBOps(self.adb_config, self.device_config)
        self.appium_process = await AppiumOps.start_server_with_cors(self.appium_config, self.device_config['port'])

        await self.is_appium_server_running(self.device_config['port'])
        self.ready = True
        log.log_success('PhoneOps.async_initialize', f"PhoneOps for device '{self.device_name}' initialized successfully.")

    def is_device_connected(self, device_id):
        result = subprocess.run(["adb", "devices"], stdout=subprocess.PIPE, text=True)
        connected_devices = result.stdout.splitlines()
        return any(device_id in line and "device" in line for line in connected_devices)
    
    async def is_appium_server_running(self, port):
        max_retries = 3
        retries = 0
        while retries < max_retries:
            try:
                response = requests.get(f"http://localhost:{port}/status")
                if response.status_code == 200:
                    log.log_success('PhoneOps.is_appium_server_running', f"Appium server on port {port} is ready.")
                    return True
            except requests.ConnectionError:
                pass
            log.log_info('PhoneOps.is_appium_server_running', f"Waiting for Appium server on port {port} to be ready...")
            retries += 1
            await asyncio.sleep(2)
        
        log.log_error('PhoneOps.is_appium_server_running', f"Appium server on port {port} is not responding after max retries.")
        return False

    # --- Main procedure execution --- #

    async def perform_procedure(self, procedure, url):
        if self.is_busy:
            log.log_warning('PhoneOps.perform_procedure', f"Phone '{self.device_name}' is currently busy.")
            return

        log.log_info('PhoneOps.perform_procedure', f"Starting procedure '{procedure['info']['name']}' on phone '{self.device_name}'...")
        self.is_busy = True

        app_name = procedure['info'].get('app')
        if not app_name:
            log.log_error("PhoneOps.perform_procedure", "No app specified in the procedure.")
            self.is_busy = False
            return

        try:
            # Initialize the driver for the app, then execute the procedure steps
            await self.initialize_android_driver_for_app(app_name)
            await asyncio.sleep(9)  # Optional delay if needed
            await self._execute_procedure(procedure)
            log.log_success("PhoneOps.perform_procedure", f"Procedure '{procedure['info']['name']}' completed on '{self.device_name}'.")

        except Exception as e:
            log.log_error('PhoneOps.perform_procedure', f"Error during procedure execution: {e}")

        finally:
            # Stop the driver session after procedure completion
            if self.android_ops:
                self.android_ops.stop_session()
                self.android_ops = None
            self.is_busy = False

    async def _execute_procedure(self, procedure):
        if self.android_ops is None:
            log.log_error("PhoneOps._execute_procedure", "AndroidOps is not initialized. Cannot execute procedure.")
            return

        try:
            await self.android_ops.execute_steps(procedure['steps'])
            log.log_success('PhoneOps._execute_procedure', f"Procedure '{procedure['info']['name']}' completed successfully for phone '{self.device_name}'.")
        except Exception as e:
            log.log_error('PhoneOps._execute_procedure', f"Failed to execute procedure '{procedure['info']['name']}' on phone '{self.device_name}'", str(e))

    # --- Initialize driver for specific app --- #

    async def initialize_android_driver_for_app(self, app_name):
        """Initialize Android driver specifically for the app."""
        app_info = next((app for app in self.apps if app['name'].lower() == app_name.lower()), None)
        
        if app_info is None:
            log.log_error("PhoneOps.initialize_android_driver_for_app", f"App '{app_name}' not found in device configuration for '{self.device_name}'")
            return

        package_name = app_info['package_name']
        activity_name = app_info['activity_name']
        
        log.log_info("PhoneOps.initialize_android_driver_for_app", f"Initializing Android driver for app '{app_name}' with package '{package_name}' and activity '{activity_name}'.")
        
        try:
            await asyncio.sleep(1)  # Optional delay if needed
            # Create a new AndroidOps instance for the current app
            self.android_ops = AndroidOps(self.device_config)
            self.android_ops.initialize_driver(package_name, activity_name)
            self.current_app = app_name
            log.log_success("PhoneOps.initialize_android_driver_for_app", f"Driver initialized for app '{app_name}' on '{self.device_name}'.")
        except Exception as e:
            log.log_error("PhoneOps.initialize_android_driver_for_app", f"Failed to initialize driver for app '{app_name}' on '{self.device_name}'", str(e))


    # --- Data transfer operations --- #

    async def send_data_to_device(self, data_url):
        try:
            await self.adb_manager.push_image(data_url)
            self.is_busy = True
            log.log_info('PhoneOps.send_data_to_device', f"Sending data to phone '{self.device_name}'...") 
        except Exception as e:
            log.log_error('PhoneOps.send_data_to_device', f"Failed to send data to phone '{self.device_name}'", e)
        finally:
            self.is_busy = False
    
    async def pull_data_from_device(self, album_url, file_name):
        local_image_path = None
        try:
            local_image_path =  await self.adb_manager.pull_latest_image(album_url, file_name)
            self.is_busy = True
            log.log_info('PhoneOps.pull_data_from_device', f"Pulling data from phone '{self.device_name}'...")
            return local_image_path
        except Exception as e:
            log.log_error('PhoneOps.pull_data_from_device', f"Failed to pull data from phone '{self.device_name}'", e)
        finally:
            self.is_busy = False
            return local_image_path

    async def delete_latest_two_images(self):
        try:
            await self.adb_manager.delete_latest_two_images()
            self.is_busy = True
            log.log_info('PhoneOps.delete_latest_two_images', f"Deleting latest two images from phone '{self.device_name}'...")
        except Exception as e:
            log.log_error('PhoneOps.delete_latest_two_images', f"Failed to delete latest two images from phone '{self.device_name}'", e)
        finally:
            self.is_busy = False

    def get_battery_level(self):
        try:
            command = ["adb", "shell", "dumpsys", "battery"]
            result = subprocess.run(command, stdout=subprocess.PIPE, text=True).stdout
            for line in result.splitlines():
                if "level" in line:
                    return int(line.split(':')[-1].strip())
        except Exception as e:
            log.log_error('PhoneOps.get_battery_level', f"Failed to get battery level for phone '{self.device_name}'", e)
        return None

