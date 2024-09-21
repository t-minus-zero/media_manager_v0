import json
import os

class JSONFileManager:
    def __init__(self):
        pass

    @staticmethod
    def load_json_as_dataobj_from_xpath(path):
        if os.path.exists(path) and path.endswith('.json'):
            with open(path, 'r') as file:
                data_obj = json.load(file)
            return data_obj
        else:
            raise FileNotFoundError(f"No valid JSON file found at {path}")

    @staticmethod
    def save_xdataobj_as_xname_json_at_xpath(data_obj, name, path):
        if not os.path.isdir(path):
            raise NotADirectoryError(f"The directory {path} does not exist.")
        
        full_path = os.path.join(path, f"{name}.json")
        with open(full_path, 'w') as file:
            json.dump(data_obj, file, indent=4)


"""
# Example usage of the JSONFileManager class

from json_ops import JSONFileManager

try:
    data = JSONFileManager.load_json_as_dataobj_from_xpath('path_to_file.json')
except Exception as e:
    print(f"An unexpected error occurred: {e}")

"""
