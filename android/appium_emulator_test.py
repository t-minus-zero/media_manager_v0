from appium import webdriver
from appium.options.android import UiAutomator2Options
import time

# Create an instance of UiAutomator2Options
options = UiAutomator2Options()

# Set the desired capabilities
options.platform_name = "Android"
options.platform_version = "13.0"  # Replace with your emulator's Android version
options.device_name = "emulator-5554"  # Use 'adb devices' to find your device name
options.app = r"C:\Users\gurpr\Documents\Coding\Projects\FastHTML_Test\android\SODA8OG.apk"  # Path to your APK
options.automation_name = "UiAutomator2"
options.auto_grant_permissions = True

# Initialize the driver (Start the Appium session)
driver = webdriver.Remote("http://localhost:4723", options=options)

# Wait for the app to launch
time.sleep(10)

# Print a success message
print("App has been launched successfully!")

# Quit the driver (End the Appium session)
driver.quit()
