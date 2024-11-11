from appium import webdriver
from appium.options.android import UiAutomator2Options
import asyncio
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.actions.action_builder import ActionBuilder
from appium.webdriver.common.appiumby import AppiumBy
from .utilities import async_sleep
from .logger import log
import requests

class AndroidOps:
    def __init__(self, device_config):
        # Store device configuration and set up driver URL
        self.device_config = device_config
        self.driver_url = f"http://localhost:{device_config['port']}"
        self.device_id = device_config['device_id']
        self.options = UiAutomator2Options()
        self.options.platform_name = device_config['platform_name']
        self.options.platform_version = device_config['platform_version']
        self.options.device_name = device_config['device_id']
        self.options.automation_name = device_config['automation_name']
        self.options.auto_grant_permissions = device_config.get('auto_grant_permissions', True)
        
        # Initialize driver to None initially
        self.driver = None

    def initialize_driver(self, package_name, activity_name):
        """Initialize a new Appium driver session with app-specific options."""
        log.log_info("AndroidOps.initialize_driver", f"Initializing driver for {package_name}/{activity_name} on device {self.device_id}...")
        
        # Ensure Appium server is accessible
        if not self._is_appium_server_running():
            log.log_error("AndroidOps.initialize_driver", "Appium server is not available. Cannot initialize driver.")
            return
        
        # Set app-specific options for package and activity
        self.options.app_package = package_name
        self.options.app_activity = activity_name
        self.options.no_reset = True  # Prevents clearing app data
        self.options.full_reset = False  # Ensures the app is not reinstalled
        
        try:
            # Initialize the driver with the specific app's package and activity
            self.driver = webdriver.Remote(self.driver_url, options=self.options)
            log.log_success("AndroidOps.initialize_driver", f"Driver initialized for app {package_name}/{activity_name}.")
        except Exception as e:
            log.log_error("AndroidOps.initialize_driver", f"Failed to initialize driver: {str(e)}")

    def stop_session(self):
        """Stop the current Appium driver session, closing the app without resetting data."""
        if self.driver:
            try:
                log.log_info("AndroidOps.stop_session", "Terminating the app while preserving data...")
                
                # Attempt to terminate the app session using package name from options
                if self.options.app_package:
                    self.driver.terminate_app(self.options.app_package)
                    log.log_info("AndroidOps.stop_session", f"App {self.options.app_package} terminated successfully.")
                
                # Clean up the driver session to release resources
                log.log_info("AndroidOps.stop_session", "Stopping Appium driver session...")
                self.driver.quit()
                self.driver = None
                log.log_info("AndroidOps.stop_session", "Appium driver session fully stopped.")
            except Exception as e:
                log.log_warning("AndroidOps.stop_session", "Failed to stop Appium driver session.", str(e))
        else:
            log.log_info("AndroidOps.stop_session", "No active Appium session to stop.")


    def reconnect_driver(self, package_name, activity_name):
        """Reconnect the driver by stopping and restarting the session for a specific app."""
        self.stop_session()
        self.initialize_driver(package_name, activity_name)

    def check_driver_session(self):
        """Check if the Appium driver session is active, and if not, log an error."""
        if not self.driver or not self.driver.session_id:
            log.log_warning("AndroidOps.check_driver_session", "Driver session is inactive or missing.")

    def _is_appium_server_running(self):
        """Check if the Appium server is accessible."""
        try:
            response = requests.get(f"{self.driver_url}/status")
            return response.status_code == 200
        except requests.ConnectionError:
            return False

    #------------------- Methods for Android Operations -------------------#

    # Function to find an element with a wait and click
    def find_and_click(self, xpath, step_description, timeout=10):
        self.check_driver_session()  # Ensure the session is active
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.element_to_be_clickable((AppiumBy.XPATH, xpath))
            )
            element.click()
            log.log_success("AndroidOps.find_and_click", step_description)
        except Exception as e:
            log.log_error("AndroidOps.find_and_click", step_description, str(e))

    # Function to perform a tap at specified coordinates using W3C Actions
    async def tap(self, x, y, step_description):
        self.check_driver_session()  # Ensure the session is active
        try:
            action = ActionBuilder(self.driver)
            action.pointer_action.move_to_location(x, y)
            action.pointer_action.pointer_down()
            action.pointer_action.pointer_up()
            action.perform()

            log.log_info("AndroidOps.tap", f"Tapped on screen at ({x}, {y})")
        except Exception as e:
            log.log_error("AndroidOps.tap", step_description, str(e))

    # Function to swipe by percentage using W3C Actions
    async def swipe_by_percentage(self, xpath, start_percent, end_percent, step_description, timeout=10):
        self.check_driver_session()  # Ensure the session is active
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((AppiumBy.XPATH, xpath))
            )
            bounds = element.rect
            x_start = bounds['x'] + int(bounds['width'] * start_percent)
            x_end = bounds['x'] + int(bounds['width'] * end_percent)
            y = bounds['y'] + int(bounds['height'] / 2)

            action = ActionBuilder(self.driver)
            action.pointer_action.move_to_location(x_start, y)
            action.pointer_action.pointer_down()
            action.pointer_action.move_to_location(x_end, y)
            action.pointer_action.pointer_up()
            action.perform()

            log.log_info("AndroidOps.swipe_by_percentage", f"Swipe performed from {start_percent * 100}% to {end_percent * 100}% on {step_description}")
        except Exception as e:
            log.log_error("AndroidOps.swipe_by_percentage", step_description, str(e))

    # Function to scroll until an element is visible and click it
    async def scroll_until_visible(self, scrollable_xpath, target_xpath, step_description, max_swipes=5, timeout=10):
        self.check_driver_session()  # Ensure the session is active
        try:
            scrollable_element = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((AppiumBy.XPATH, scrollable_xpath))
            )
            bounds = scrollable_element.rect
            start_x = bounds['x'] + bounds['width'] * 0.9
            end_x = bounds['x'] + bounds['width'] * 0.1
            y = bounds['y'] + bounds['height'] / 2

            for i in range(max_swipes):
                try:
                    target_element = self.driver.find_element(AppiumBy.XPATH, target_xpath)
                    target_element.click()
                    log.log_success("AndroidOps.scroll_until_visible", f"{step_description} - Element is now visible and clicked")
                    return True
                except Exception:
                    action = ActionBuilder(self.driver)
                    action.pointer_action.move_to_location(start_x, y)
                    action.pointer_action.pointer_down()
                    action.pointer_action.move_to_location(end_x, y)
                    action.pointer_action.pointer_up()
                    action.perform()
                    await async_sleep(1)

            raise Exception(f"{step_description} - Element not found after {max_swipes} swipes")
        except Exception as e:
            log.log_error("AndroidOps.scroll_until_visible", step_description, str(e))
            return False

    # Function to execute steps from JSON instructions
    async def execute_steps(self, instructions):
        instruction_status = []

        for instruction in instructions:
            try:
                if instruction['type'] == "tap":
                    await self.tap(instruction['x'], instruction['y'], instruction['description'])
                    instruction_status.append(f"[SUCCESS] {instruction['description']}")
                elif instruction['type'] == "click-xpath":
                    self.find_and_click(instruction['xpath'], instruction['description'], instruction.get('timeout', 10))
                    instruction_status.append(f"[SUCCESS] {instruction['description']}")
                elif instruction['type'] == "swipe-slider":
                    await self.swipe_by_percentage(
                        instruction['xpath'], instruction['start-percent'], instruction['end-percent'], instruction['description'], instruction.get('timeout', 10)
                    )
                    instruction_status.append(f"[SUCCESS] {instruction['description']}")
                elif instruction['type'] == "scroll-until-visible":
                    result = await self.scroll_until_visible(
                        instruction['scrollable_xpath'], instruction['target-xpath'], instruction['description'], instruction.get('max_swipes', 5), instruction.get('timeout', 10)
                    )
                    if result:
                        instruction_status.append(f"[SUCCESS] {instruction['description']}")
                    else:
                        instruction_status.append(f"[FAILED] {instruction['description']} - Element not found")

                if 'wait' in instruction:
                    await asyncio.sleep(instruction['wait'])

            except Exception as e:
                log.log_error(f"Executing step: {instruction['description']}", str(e))
                instruction_status.append(f"[FAILED] {instruction['description']}")

        log.log_info("AndroidOps.execute_steps", "Execution Summary:")
        for status in instruction_status:
            log.log_info("AndroidOps.execute_steps", status)
