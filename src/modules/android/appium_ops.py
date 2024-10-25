### use this in termianl to kill all already running processes: taskkill /F /IM node.exe /T


import subprocess
import time
import psutil

class Appium:
    @staticmethod
    def kill_existing_appium():
        """
        Kills any existing Appium processes.
        """
        for proc in psutil.process_iter(['pid', 'name']):
            try:
                if proc.info['name'] == 'node.exe' and 'appium' in proc.cmdline():
                    print(f"Killing existing Appium process with PID: {proc.info['pid']}")
                    proc.kill()
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                continue

    @staticmethod
    def start_server_with_cors():
        """
        Starts the Appium server with CORS enabled.
        """
        try:
            # Kill existing Appium processes to avoid conflicts
            Appium.kill_existing_appium()

            # Run the Appium server with CORS enabled as a subprocess
            process = subprocess.Popen(
                [r"C:\Program Files\nodejs\appium.cmd", "--allow-cors"],
                creationflags=subprocess.CREATE_NEW_CONSOLE  # Opens a new console window
            )
            print("Appium server started with CORS enabled.")

            # Wait for the server to be ready
            for _ in range(10):  # Wait for up to 10 seconds
                output = process.stdout.readline().decode()
                if "Appium REST http interface listener started" in output:
                    print("Appium server is fully operational.")
                    return process
                time.sleep(1)

            # If we did not see the expected output, print any error messages
            stderr_output = process.stderr.read().decode()
            print(f"Failed to detect Appium server startup message. Error: {stderr_output}")
            return None
        except Exception as e:
            print(f"Failed to start Appium server: {e}")
            return None

# Example usage
if __name__ == "__main__":
    appium_process = Appium.start_server_with_cors()
    if appium_process:
        print("Appium server is running...")
        try:
            while True:
                time.sleep(1)  # Keep the script running to keep the Appium server alive
        except KeyboardInterrupt:
            print("Shutting down Appium server...")
            appium_process.terminate()
            appium_process.wait()
    else:
        print("Failed to start Appium server.")
