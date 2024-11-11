import asyncio
import threading
from src.modules.local_ops.os_ops import OSFileManager
from src.modules.local_ops.json_ops import JSONFileManager
from src.modules.utility_ops.utility_ops import UtilityOps
from modules.android.android_ops import AndroidOps
from src.modules.android.adb_ops import ADBOps
from src.modules.android.appium_ops import Appium

class KITT:
    def __init__(self):
        self.script_name = 'kitt.py'
        self.androidOps = None
        self.adb_manager = None
        self.procedures = None
        self.is_running = False

    async def initialize(self):
        print("Starting Appium Server")
        Appium.start_server_with_cors()
        await asyncio.sleep(10)
        print("Starting Android Ops")
        self.androidOps = AndroidOps()
        print("Starting ADB Manager")
        await asyncio.sleep(10)
        self.adb_manager = ADBImageManager(
            adb_path="adb",
            device_camera_folder="/sdcard/DCIM/Camera/",
            local_folder=r"C:\Users\gurpr\Documents\Coding\Projects\FastHTML_Test\android\images_test"
        )
        self.procedures = self.load_procedures() # List of instructions as data objects

    def load_procedures(self):
        procedure_urls = [
            r'C:\Users\gurpr\Documents\Coding\Projects\FastHTML_Test\src\modules\android\procedures\soda_test_edit.json',
        ]
        procedures = []
        for procedure_url in procedure_urls:
            procedure_data = {
                "name": OSFileManager.get_just_name_from_xpath(procedure_url),
                "instructions": JSONFileManager.load_json_as_dataobj_from_xpath(procedure_url)
            }
            print(procedure_data['name'])
            procedures.append(procedure_data)

        return procedures

    async def send_data_to_device(self, url):
        await self.adb_manager.push_image(url)

    async def pull_data_from_device(self, album_url, file_name):
        await self.adb_manager.pull_latest_image(album_url, file_name)
        #new_version['file_type'], new_version['extension'] = UtilityOps.get_file_type_and_extension(new_version['url'])

    async def delete_latest_2_media(self):
        await self.adb_manager.delete_latest_two_images()

    async def log_event(self, payload, message):
        # Append a log entry to the payload log
        payload['info']['log'].append(message)
        print(message)

    async def run_payload(self, payload):
        if self.is_running:
            await self.log_event(payload, "Another payload is already running. Aborting this request.")
            return

        self.is_running = True
        # Initialize the log
        payload['info']['log'] = []
        payload['info']['job-index'] = 1
        
        try:
            # Process each job in payload
            for idx, job in enumerate(payload['jobs']):
                payload['info']['job-index'] = idx + 1
                job['status'] = 'processing'
                await self.log_event(payload, f"Processing job {idx + 1}: {job['status']}")

                # Run the processing for each job
                result = await self.process_job(job)
                
                if result:  # If no errors
                    job['status'] = 'completed'
                    await self.log_event(payload, f"Completed job {idx + 1}: {job['status']}")
                else:
                    job['status'] = 'aborted'
                    payload['info']['status'] = 'aborted'
                    await self.log_event(payload, f"Error in job {idx + 1}: {job['status']}")
                    break  # Stop further processing on error

            # Mark the payload status as complete if all jobs succeeded
            if all(job['status'] == 'completed' for job in payload['jobs']):
                payload['info']['status'] = 'completed'
            else:
                payload['info']['status'] = 'aborted'

        except Exception as e:
            # Global error handling for unexpected issues
            payload['info']['status'] = 'aborted'
            await self.log_event(payload, f"Unexpected error: {str(e)}")
        finally:
            self.is_running = False

    async def process_job(self, job):
        version_url = job['item-data']['versions'][job['version-index']]['url']
        album_url = OSFileManager.get_folder_path_from_xpath(version_url)
        version_name = OSFileManager.get_name_from_xpath(version_url)
        for edit in job['edits']:
            try:
                await self.process_edit(edit, version_url, album_url, version_name)
                return True  # Return True if job succeeds
            except Exception as e:
                await self.log_event(job, f"Error: {str(e)}")
                return False  # Return False if job fails

    async def process_edit(self, edit, version_url, album_url, version_name):
        for procedure in self.procedures:
                if procedure['name'] == edit['name']:
                    instructions = procedure['instructions']
                    await self.send_data_to_device(version_url)
                    await asyncio.sleep(5)
                    await self.androidOps.execute_steps(instructions)
                    await asyncio.sleep(5)
                    await self.pull_data_from_device(album_url , version_name)
                    await asyncio.sleep(5)
                    await self.delete_latest_2_media()
                    await asyncio.sleep(5)
                    break
                else:
                    print("Procedure "+ edit['name'] +" not found ain loaded procedures.")

    def run_payload_in_background(self, payload):
        if not self.is_running:
            threading.Thread(target=lambda: asyncio.run(self.run_payload(payload)), daemon=True).start()
        else:
            print("Another payload is already running. Aborting this request.")
