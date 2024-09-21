import os
import logging

class OSFileManager:
    
    def __init__(self):
        pass

    @staticmethod
    def fetch_list_of_files_in_xpath(directory_path):
        if os.path.isdir(directory_path):
            list_of_items = os.listdir(directory_path)
            list_of_files = [os.path.join(directory_path, item) for item in list_of_items if os.path.isfile(os.path.join(directory_path, item))]
        else:
            list_of_files = []
        
        return list_of_files  # Returns a list of full file paths in the directory

    @staticmethod
    def fetch_list_of_directories_in_xpath(directory_path):
        if os.path.isdir(directory_path):
            list_of_items = os.listdir(directory_path)
            list_of_directories = [os.path.join(directory_path, item) for item in list_of_items if os.path.isdir(os.path.join(directory_path, item))]
        else:
            list_of_directories = []
        return list_of_directories

    @staticmethod
    def find_path_of_xfile_in_xdirectory(file_name, directory_path):
        if os.path.isdir(directory_path):
            for root, dirs, files in os.walk(directory_path):
                if file_name in files:
                    return os.path.join(root, file_name) # returns the path of the file
        return None

    @staticmethod
    def find_path_of_xdirectory_in_xdirectory(directory_name, directory_path):
        if os.path.isdir(directory_path):
            for root, dirs, files in os.walk(directory_path):
                if directory_name in dirs:
                    return os.path.join(root, directory_name) # returns the path of the directory
        return None
    
    @staticmethod
    def check_if_xdirectory_exists(directory_path):
        if os.path.isdir(directory_path):
            return True
        return False
    
    @staticmethod
    def get_name_from_xpath(path):
        if not path:
            raise ValueError("ERROR: Invalid path: Path cannot be empty. FROM [os_ops.py]")
        name = os.path.basename(path)
        if not name:
            raise ValueError(f"ERROR: Invalid path: Unable to extract name from '{path}'. FROM [os_ops.py]")
        return name
    
    @staticmethod
    def rename_path(original_path, new_name):
        if not os.path.exists(original_path):
            logging.error(f"ERROR: The path '{original_path}' does not exist.")
            raise FileNotFoundError(f"The path '{original_path}' does not exist.")
        # Determine if the original path is a file or a directory
        if os.path.isfile(original_path):
            # For files, preserve the original extension
            file_extension = os.path.splitext(original_path)[1]  # Get the file extension
            new_name_with_extension = f"{new_name}{file_extension}"
        else:
            # For directories, just use the new name
            new_name_with_extension = new_name
        # Get the directory that contains the original file or directory
        parent_dir = os.path.dirname(original_path)
        new_path = os.path.join(parent_dir, new_name_with_extension)
        try:
            os.rename(original_path, new_path)
            logging.info(f"SUCCESS: Renamed '{original_path}' to '{new_path}'.")
            return new_path
        except Exception as e:
            logging.error(f"ERROR: Failed to rename '{original_path}'. {e}")
            raise OSError(f"Failed to rename '{original_path}': {e}")

"""

from os_ops import OSFileManager

try:
    # Example 1: Get list of files in a directory
    files = OSFileManager.fetch_list_of_files_in_xpath('/path/to/directory')
    print("Files:", files)

    # Example 2: Get list of directories in a directory
    directories = OSFileManager.fetch_list_of_directories_in_xpath('/path/to/directory')
    print("Directories:", directories)

    # Example 3: Find a specific file in the directory and its subdirectories
    file_path = OSFileManager.find_path_of_xfile_in_xdirectory('file_name.txt', '/path/to/directory')
    if file_path:
        print(f"File found at: {file_path}")
    else:
        print("File not found")

    # Example 4: Find a specific directory in the directory and its subdirectories
    dir_path = OSFileManager.find_path_of_xdirectory_in_xdirectory('target_directory', '/path/to/directory')
    if dir_path:
        print(f"Directory found at: {dir_path}")
    else:
        print("Directory not found")

except Exception as e:
    print(f"An error occurred: {e}")

"""