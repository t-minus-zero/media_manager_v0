import asyncio
from src.modules.local_ops.os_ops import OSFileManager
from src.modules.local_ops.json_ops import JSONFileManager
from src.modules.utility_ops.utility_ops import UtilityOps
from src.modules.android.android_ops import AndroidOps
from src.modules.android.adb_ops import ADBImageManager
from src.modules.android.appium_ops import Appium

class KITT:
    def __init__(self):
        self.script_name = 'kitt.py'
        self.androidOps = None
        self.adb_manager = None
        self.procedures = None

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

    async def process_payload(self, payload):

        og_name = OSFileManager.get_name_from_xpath(payload[0]['version_url'])
        print(og_name)


        for payload_procedure in payload[0]['procedures']:
            for procedure in self.procedures:
                if procedure['name'] == payload_procedure['name']:
                    print("Procedure "+ payload_procedure['name'] +" found - starting execution")
                    instructions = procedure['instructions']
                    await self.send_data_to_device(payload[0]['version_url'])
                    await asyncio.sleep(5)
                    await self.androidOps.execute_steps(instructions)
                    await asyncio.sleep(5)
                    await self.pull_data_from_device(payload[0]['album_url'] , payload[0]['new_version_file_name'])
                    await asyncio.sleep(5)
                    await self.delete_latest_2_media()
                    await asyncio.sleep(5)
                    break
                else:
                    print("Procedure "+ payload_procedure['name'] +" not found")

    async def send_data_to_device(self, url):
        await self.adb_manager.push_image(url)

 
    async def pull_data_from_device(self, album_url, file_name):
        await self.adb_manager.pull_latest_image(album_url, file_name)
        #new_version['file_type'], new_version['extension'] = UtilityOps.get_file_type_and_extension(new_version['url'])

    async def delete_latest_2_media(self):
        await self.adb_manager.delete_latest_two_images()
