from appium import webdriver
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver import ActionChains
from selenium.webdriver.common.actions.pointer_input import PointerInput
from selenium.webdriver.common.actions.interaction import Interaction
from appium.options.android import UiAutomator2Options

options = UiAutomator2Options()
options.platform_name = "Android"
options.platform_version = "14"  # Optional
options.device_name = "R5CT227HXLW"  # Use the device serial number from 'adb devices'
options.automation_name = "UiAutomator2"
options.auto_grant_permissions = True
driver = webdriver.Remote("http://localhost:4723", options=options)

# Initialize the actions
actions = ActionChains(driver)

# Define the touch action to tap at a specific position (X, Y)
actions.w3c_actions.pointer_action.move_to_location(x=120, y=1950)
actions.w3c_actions.pointer_action.pointer_down()
actions.w3c_actions.pointer_action.pause(0.1)  # Optional: A small pause to simulate realistic tap duration
actions.w3c_actions.pointer_action.pointer_up()

# Perform the action
actions.perform()
