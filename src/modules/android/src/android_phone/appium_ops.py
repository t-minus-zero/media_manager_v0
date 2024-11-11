import subprocess
import psutil
import requests
from .utilities import async_sleep, run_command
from .logger import log

class AppiumOps:
    @staticmethod
    def kill_existing_appium():
        """Kill any existing Appium server processes."""
        for proc in psutil.process_iter(['pid', 'name']):
            try:
                if proc.info['name'] == 'node.exe' and 'appium' in proc.cmdline():
                    log.log_info("AppiumOps.kill_existing_appium", f"Killing existing Appium process with PID: {proc.info['pid']}")
                    proc.kill()
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                continue

    @staticmethod
    async def start_server_with_cors(appium_config, port):
        """Start the Appium server with CORS enabled and verify it is running."""
        try:
            AppiumOps.kill_existing_appium()

            command = [appium_config['appium_path'], "--allow-cors", "-p", str(port)]
            log.log_info("AppiumOps.start_server_with_cors", f"Starting Appium server with command: {' '.join(command)}")

            process = subprocess.Popen(
                command,
                creationflags=subprocess.CREATE_NEW_CONSOLE,
                text=True
            )
            log.log_info("AppiumOps.start_server_with_cors", f"Appium server started with CORS enabled on port {port}.")
            log.log_info("AppiumOps.start_server_with_cors", f"Waiting for Appium server on port {port} to be ready...")

            # Wait for the Appium server to be ready
            url = f"http://localhost:{port}/status"
            for _ in range(appium_config.get('max_startup_wait_seconds', 10)):
                try:
                    response = requests.get(url)
                    if response.status_code == 200:
                        log.log_success("AppiumOps.start_server_with_cors", f"Appium server on port {port} is fully operational.")
                        return process
                except requests.ConnectionError:
                    pass  # Server not ready yet
                await async_sleep(1)  # Retry every second

            log.log_error("AppiumOps.start_server_with_cors", f"Failed to detect Appium server startup on {url}.", None)
            return None

        except Exception as e:
            log.log_error("AppiumOps.start_server_with_cors", f"Failed to start Appium server: {e}", e)
            return None

    @staticmethod
    def stop_server(process):
        """Stop the Appium server by terminating the process."""
        if process and process.poll() is None:  # Check if process is running
            log.log_info("AppiumOps.stop_server", "Stopping the Appium server.")
            process.terminate()
            process.wait()
            log.log_info("AppiumOps.stop_server", "Appium server stopped successfully.")

    @staticmethod
    async def restart_server(appium_config, port):
        """Restart the Appium server."""
        AppiumOps.kill_existing_appium()  # Ensure no lingering processes
        return await AppiumOps.start_server_with_cors(appium_config, port)
    
    @staticmethod
    async def is_session_active(driver):
        """Check if the Appium session is still active."""
        try:
            driver_status = driver.session_id  # Access session ID to validate if it's active
            if driver_status is not None:
                log.log_info("AppiumOps.is_session_active", "Appium session is active.")
                return True
            else:
                log.log_info("AppiumOps.is_session_active", "Appium session is inactive.")
                return False
        except Exception:
            log.log_info("AppiumOps.is_session_active", "Appium session is inactive or terminated.")
            return False