import os
from src.modules.local_ops.json_ops import JSONFileManager
from src.modules.local_ops.os_ops import OSFileManager
from src.modules.android.src.android_phone.utilities import log_error, logger

class ConfigOps:
    
    @staticmethod
    def fetch_test_storage_folder_path():
        try:
            test_storage_folder = OSFileManager.find_path_of_xdirectory_in_xdirectory('test_storage', 'storage')
            if not os.path.exists(test_storage_folder):
                raise FileNotFoundError(f"Test storage folder not found: {test_storage_folder}")
            return test_storage_folder
        except Exception as e:
            log_error("Fetching test storage folder path", e)
            raise

    @staticmethod
    def fetch_android_config():
        try:
            config_file_path = OSFileManager.find_path_of_xfile_in_xdirectory('android_config.json', 'storage/config')
            if not config_file_path:
                raise FileNotFoundError("Android config file path not found.")
            config_file = JSONFileManager.load_json_as_dataobj_from_xpath(config_file_path)
            if not config_file:
                raise ValueError("Failed to load android config file.")
            return config_file
        except Exception as e:
            log_error("Fetching android config", e)
            raise

    @staticmethod
    def fetch_procedures():
        try:
            procedures_folder = OSFileManager.find_path_of_xdirectory_in_xdirectory('procedures', 'storage')
            if not procedures_folder:
                raise FileNotFoundError("Procedures folder not found.")
            
            procedures = []
            procedure_paths = OSFileManager.fetch_list_of_files_in_xpath(procedures_folder)
            if not procedure_paths:
                raise FileNotFoundError("No procedure files found in procedures folder.")
            
            for procedure_path in procedure_paths:
                procedure_data = JSONFileManager.load_json_as_dataobj_from_xpath(procedure_path)
                if procedure_data:
                    procedures.append(procedure_data)
                else:
                    logger.warning(f"Failed to load procedure data from: {procedure_path}")
            
            return procedures
        except Exception as e:
            log_error("Fetching procedures", e)
            raise

