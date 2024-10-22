from appium import webdriver
from appium.options.android import UiAutomator2Options
import time

# Create an instance of UiAutomator2Options
options = UiAutomator2Options()

# Set the desired capabilities for the physical device
options.platform_name = "Android"
options.platform_version = "14"  # Optional: Use 'adb shell getprop ro.build.version.release' to get the version.
options.device_name = "R5CT227HXLW"  # Use the device serial number from 'adb devices'
options.app = r"C:\Users\gurpr\Documents\Coding\Projects\FastHTML_Test\android\SODAv8.apk"  # Path to your APK
options.automation_name = "UiAutomator2"
options.auto_grant_permissions = True

# Initialize the driver (Start the Appium session)
driver = webdriver.Remote("http://localhost:4723", options=options)

# Wait for the app to launch
time.sleep(10)

# Print a success message
print("App has been launched successfully on the physical device!")

# Quit the driver (End the Appium session)
driver.quit()
