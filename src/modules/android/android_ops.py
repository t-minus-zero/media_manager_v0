from appium import webdriver
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.common.actions.action_builder import ActionBuilder
import asyncio
import time
import traceback
from appium.options.android import UiAutomator2Options

# Class to perform operations on an Android device using Appium
class AndroidOps:
    def __init__(self, driver_url="http://localhost:4723", desired_capabilities={}):
        self.driver_url = driver_url
        self.options = UiAutomator2Options()
        if desired_capabilities == {}:
            # Set the desired capabilities for the physical device
            self.options.platform_name = "Android"
            self.options.platform_version = "14"  # Optional
            self.options.device_name = "R5CT227HXLW"  # Use the device serial number from 'adb devices'
            self.options.automation_name = "UiAutomator2"
            self.options.auto_grant_permissions = True

        # Initialize the Appium driver
        self.initialize_driver()

    # Function to initialize or reinitialize the driver
    def initialize_driver(self):
        print("Initializing Appium driver...")
        self.driver = webdriver.Remote(self.driver_url, options=self.options)

    # Function to check if the driver session is active
    def check_driver_session(self):
        try:
            # If the session is still alive, this should succeed
            self.driver.session_id
        except Exception as e:
            print("Session is not active. Reinitializing the driver...")
            self.initialize_driver()

    # Utility function to log errors
    def log_error(self, step_description, error):
        print(f"Error at step: {step_description}")
        print(f"Reason: {str(error)}")
        print(traceback.format_exc())

    # Function to find an element by XPath and click
    def find_and_click(self, xpath, step_description, timeout=10):
        self.check_driver_session()  # Ensure the session is active
        try:
            element = self.driver.find_element(AppiumBy.XPATH, xpath)
            element.click()
            print(f"Success: {step_description}")
        except Exception as e:
            self.log_error(step_description, e)

    # Function to find an element and return its bounds
    def get_bounds(self, xpath, step_description, timeout=10):
        self.check_driver_session()  # Ensure the session is active
        try:
            element = self.driver.find_element(AppiumBy.XPATH, xpath)
            bounds = element.rect  # Returns dict: {'x': int, 'y': int, 'width': int, 'height': int}
            print(f"Bounds of element in step {step_description}: {bounds}")
            return bounds
        except Exception as e:
            self.log_error(step_description, e)
            return None

    # Function to perform a tap at specified coordinates using W3C Actions
    def tap(self, x, y, step_description):
        self.check_driver_session()  # Ensure the session is active
        try:
            # Create an action sequence directly without initializing the finger pointer
            action = ActionBuilder(self.driver)
            action.pointer_action.move_to_location(x, y)
            action.pointer_action.pointer_down()
            action.pointer_action.pointer_up()
            action.perform()

            print(f"Tapped on screen at ({x}, {y})")
        except Exception as e:
            self.log_error(step_description, e)

    # Function to swipe on an element by a percentage of its width using W3C Actions
    def swipe_by_percentage(self, xpath, start_percent, end_percent, step_description, timeout=10):
        self.check_driver_session()  # Ensure the session is active
        try:
            bounds = self.get_bounds(xpath, step_description)
            if bounds:
                x_start = bounds['x'] + int(bounds['width'] * start_percent)
                x_end = bounds['x'] + int(bounds['width'] * end_percent)
                y = bounds['y'] + int(bounds['height'] / 2)  # Swipe at the middle of the element height

                # Create an action sequence directly without initializing the finger pointer
                action = ActionBuilder(self.driver)
                action.pointer_action.move_to_location(x_start, y)
                action.pointer_action.pointer_down()
                action.pointer_action.move_to_location(x_end, y)
                action.pointer_action.pointer_up()
                action.perform()

                print(f"Swipe performed from {start_percent*100}% to {end_percent*100}% on {step_description}")
        except Exception as e:
            self.log_error(step_description, e)

    # Function to swipe across the screen using coordinates with W3C Actions
    def swipe_on_screen(self, start_x, start_y, end_x, end_y, step_description):
        self.check_driver_session()  # Ensure the session is active
        try:
            # Create an action sequence directly without initializing the finger pointer
            action = ActionBuilder(self.driver)
            action.pointer_action.move_to_location(start_x, start_y)
            action.pointer_action.pointer_down()
            action.pointer_action.move_to_location(end_x, end_y)
            action.pointer_action.pointer_up()
            action.perform()

            print(f"Swiped on screen from ({start_x},{start_y}) to ({end_x},{end_y})")
        except Exception as e:
            self.log_error(step_description, e)

    # Function to scroll horizontally until an element becomes visible and click on it
    async def scroll_until_visible(self, scrollable_xpath, target_xpath, max_swipes=5, step_description="Scroll horizontally"):
        self.check_driver_session()  # Ensure the session is active
        try:
            # Scrollable element (HorizontalScrollView or RecyclerView)
            scrollable_element = self.driver.find_element(AppiumBy.XPATH, scrollable_xpath)
            bounds = scrollable_element.rect
            start_x = bounds['x'] + bounds['width'] * 0.9  # Start from right side
            end_x = bounds['x'] + bounds['width'] * 0.1    # Scroll to the left

            for i in range(max_swipes):
                try:
                    # Check if the target element is visible
                    target_element = self.driver.find_element(AppiumBy.XPATH, target_xpath)
                    # If found, click on the target element
                    target_element.click()
                    print(f"Success: {step_description} - Element is now visible and clicked")
                    return True  # Element is found and clicked
                except:
                    # Element is not yet visible, perform a swipe
                    self.swipe_on_screen(start_x, bounds['y'], end_x, bounds['y'], f"Swipe {i+1} on {step_description}")
                    await asyncio.sleep(1)  # Small delay after each swipe
            raise Exception(f"{step_description} - Element not found after {max_swipes} swipes")
        except Exception as e:
            self.log_error(step_description, e)
            return False

    # Execute steps with horizontal scrolling included
    async def execute_steps(self, instructions):
        # List to store the status of each instruction
        instruction_status = []

        for instruction in instructions:
            try:
                if instruction['type'] == "tap":
                    self.tap(instruction['x'], instruction['y'], instruction['description'])
                    instruction_status.append(f"[SUCCESS] {instruction['description']}")
                elif instruction['type'] == "click_xpath":
                    self.find_and_click(instruction['xpath'], instruction['description'])
                    instruction_status.append(f"[SUCCESS] {instruction['description']}")
                elif instruction['type'] == "swipe_slider":
                    self.swipe_by_percentage(instruction['xpath'], instruction['start_percent'], instruction['end_percent'], instruction['description'])
                    instruction_status.append(f"[SUCCESS] {instruction['description']}")
                elif instruction['type'] == "swipe_element":
                    bounds = self.get_bounds(instruction['start_xpath'], instruction['description'])
                    if bounds:
                        start_x = bounds['x'] + bounds['width'] * 3  # Start at the right edge of the element
                        end_x = bounds['x']  # End at the left edge of the element
                        self.swipe_on_screen(start_x, bounds['y'], end_x, bounds['y'], instruction['description'])
                        instruction_status.append(f"[SUCCESS] {instruction['description']}")
                    else:
                        instruction_status.append(f"[FAILED] {instruction['description']} - Element not found")
                elif instruction['type'] == "scroll_until_visible":
                    result = await self.scroll_until_visible(instruction['scrollable_xpath'], instruction['target_xpath'], instruction.get('max_swipes', 5), instruction['description'])
                    if result:
                        instruction_status.append(f"[SUCCESS] {instruction['description']}")
                    else:
                        instruction_status.append(f"[FAILED] {instruction['description']} - Element not found")

                # Add a non-blocking sleep if required
                if 'wait' in instruction:
                    await asyncio.sleep(instruction['wait'])

            except Exception as e:
                # Log the error and add failure status to the list
                self.log_error(f"Executing step: {instruction['description']}", e)
                instruction_status.append(f"[FAILED] {instruction['description']}")

        # Print all the statuses at the end of the function
        print("\nExecution Summary:")
        for status in instruction_status:
            print(status)
