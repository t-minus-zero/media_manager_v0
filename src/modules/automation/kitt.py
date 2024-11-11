import asyncio
import threading
from src.modules.metadata_ops.config_ops import ConfigOps
from src.modules.android.src.android_phone.phone_ops import PhoneOps
from src.modules.local_ops.os_ops import OSFileManager

class KITT:
    def __init__(self):
        self.script_name = 'kitt.py'
        self.is_running = False
        self.procedures = []
        self.test_storage_folder = ConfigOps.fetch_test_storage_folder_path()

    async def initialize(self):
        android_config = ConfigOps.fetch_android_config()
        self.phone = PhoneOps(android_config)
        await self.phone.async_initialize() 
        self.procedures = self.load_procedures() # List of instructions as data objects

    async def log_event(self, payload, message):
        # Append a log entry to the payload log
        payload['info']['log'].append(message)
        print(message)

    async def run_payload(self, payload):
        if self.is_running:
            print("Another payload is already running. Aborting this request.")
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
                if procedure['info']['name'] == edit['name']:
                    await self.phone.perform_procedure(procedure)
                else:
                    print("Procedure "+ edit['name'] +" not found in loaded procedures.")

    def run_payload_in_background(self, payload):
        if not self.is_running:
            threading.Thread(target=lambda: asyncio.run(self.run_payload(payload)), daemon=True).start()
        else:
            print("Another payload is already running. Aborting this request.")
