# README.txt

## Overview
This project provides a comprehensive solution for managing and automating multiple Android devices using Python. It uses a combination of `ADB`, `Appium`, and custom scripts to perform automated procedures on Android devices. The system is composed of the following main components:

- **ADB Operations (`adb_ops.py`)**: Manages ADB-related commands and file operations.
- **Appium Operations (`appium_ops.py`)**: Manages the starting and stopping of the Appium server.
- **Android Operations (`android_ops.py`)**: Manages UI-related tasks on the Android devices.
- **Phone Operations (`phone_ops.py`)**: Coordinates the initialization of devices and execution of automation procedures.
- **Terminal Testing (`TerminalTesting.py`)**: Allows interaction with `PhoneOps` through terminal commands.

## File Descriptions

### 1. `android_config.json`
This is the main configuration file for the project. It includes the following sections:
- **Appium Configuration**: Details such as the path to the Appium executable and settings like CORS and startup wait time.
- **ADB Configuration**: Includes the ADB executable path and local folder for images.
- **Devices List**: Details for each device, including device name, ID, port, platform details, and available apps.

### 2. `adb_ops.py`
Manages ADB-related tasks for each device.
- **`ADBOps` Class**:
  - `__init__(adb_config, device_config)`: Initializes the class with ADB paths and device-specific configurations.
  - `run_adb_command(command)`: Runs ADB commands for a specific device.
  - `push_image(image_path)`: Pushes an image to the device and refreshes the media scanner.
  - `refresh_media_scanner(device_image_path)`: Forces a media scanner refresh.
  - `pull_latest_image(saving_folder, saving_file_name)`: Pulls the latest image from the device's camera folder.
  - `delete_latest_two_images()`: Deletes the latest two images from the device's camera folder.
  - `wait_for_processing(seconds)`: Waits asynchronously for a given number of seconds.

**Note**: The `adb_config` is now loaded from the `android_config.json` file to centralize configurations.

### 3. `appium_ops.py`
Manages the Appium server for each device.
- **`Appium` Class**:
  - `kill_existing_appium()`: Kills any existing Appium processes to avoid conflicts.
  - `start_server_with_cors(appium_config, port)`: Starts the Appium server with CORS enabled on a specific port.
  - Uses retry logic to wait for the Appium server to be ready.

**Note**: The Appium server runs on different ports for each device to allow simultaneous control of multiple devices.

### 4. `android_ops.py`
Handles Android-specific UI actions using Appium and WebDriver.
- **`AndroidOps` Class**:
  - `__init__(device_config)`: Initializes the driver using device configurations.
  - `initialize_driver()`: Initializes or reinitializes the Appium driver.
  - `check_driver_session()`: Checks if the current driver session is active and reinitializes if needed.
  - `find_and_click(xpath, step_description, timeout)`: Finds an element by XPath and clicks on it.
  - `tap(x, y, step_description)`: Taps on specific coordinates.
  - `swipe_by_percentage(xpath, start_percent, end_percent, step_description, timeout)`: Swipes on an element based on percentages.
  - `scroll_until_visible(scrollable_xpath, target_xpath, step_description, max_swipes, timeout)`: Scrolls until a target element is visible.
  - `execute_steps(instructions)`: Executes a set of UI instructions from JSON.

**Note**: Many methods in `AndroidOps` are asynchronous to support concurrent actions.

### 5. `phone_ops.py`
Coordinates phone initialization, Appium server management, and procedure execution.
- **`PhoneOps` Class**:
  - `__init__()`: Initializes paths and loads configuration data.
  - `async_initialize()`: Asynchronously initializes the devices, including starting Appium servers and setting up Android operations.
  - `is_device_connected(device_id)`: Checks if a device is currently connected.
  - `load_procedures(folder_path)`: Loads all procedure files from the specified folder.
  - `perform_procedure(phone_name, app_name, procedure_name)`: Asynchronously performs a procedure on a device.
  - `get_phone_status(phone_name)`: Retrieves the current status of a specific phone.
  - `is_appium_server_running(port)`: Checks if an Appium server is running on a given port.

**Important Notes**:
- The `async_initialize()` method must be awaited to ensure all devices are initialized correctly before interacting with them.
- Procedures are defined in JSON files in the `procedures` folder, which contain the steps for each operation.

### 6. `TerminalTesting.py`
This script allows interaction with `PhoneOps` via terminal commands.
- **Commands Available**:
  - `<phone_name> run <procedure_name>`: Runs a specific procedure on the given phone.
  - `<phone_name> send <file_url>`: Sends a file to the specified phone.
  - `<phone_name> savelatest test-storage`: Saves the latest file from the device to the `test_storage` folder.

**Usage**:
To run a procedure on a phone named "S22":
```sh
python TerminalTesting.py
Enter command: S22 run procedure slim_face_procedure
```
To send a file to the phone "S22":
```sh
python TerminalTesting.py
Enter command: S22 send file C:\path\to\file.jpg
```
To save the latest file to test storage:
```sh
python TerminalTesting.py
Enter command: S22 savelatest test-storage
```

**Note**:
- Make sure to properly await `async_initialize()` before issuing any commands in `TerminalTesting.py`.
- The interactive command prompt allows users to enter commands in real time.

## Procedures Folder
The `procedures` folder contains JSON files that define automation steps for each procedure. Each JSON file should have the structure:
```json
{
  "steps": [
    {
      "type": "tap",
      "x": 100,
      "y": 200,
      "description": "Tap on the button"
    },
    ...
  ]
}
```
Procedures are executed on the device using the `perform_procedure()` method in `PhoneOps`.

## Running the Scripts
1. **Initialization**:
   - Run `TerminalTesting.py` to interact with the devices via terminal commands.
   - The `PhoneOps` class will manage the initialization, ensuring that Appium servers are started and devices are ready.

2. **Dependencies**:
   - Install the necessary Python packages with:
   ```sh
   pip install -r requirements.txt
   ```
   - Make sure `Appium` and `ADB` are installed and added to your system's `PATH`.

## Important Notes
- **Appium Server Ports**: Each device is assigned a unique Appium server port for independent control. Make sure no other services are using these ports.
- **Asynchronous Operations**: Many operations are asynchronous to support multiple devices concurrently. Ensure that the proper `await` keyword is used.
- **Error Handling**: Custom error classes (`ADBOpsError`) are used for better traceability. Use these to understand issues when they occur.

