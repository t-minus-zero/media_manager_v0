import mimetypes
import logging

class UtilityOps:
    
    def __init__(self):
        self.script_name = "utility_ops.py"

    @staticmethod
    def get_file_type_and_extension(file_name):
        # Check if the file_name contains an extension
        if '.' not in file_name or file_name.startswith('.'):
            logging.error(f"ERROR: The file '{file_name}' does not have a valid extension.")
            raise ValueError(f"Invalid file name: '{file_name}' does not contain a valid extension.")
        # Extract the extension without using os
        extension = file_name.split('.')[-1].lower()
        # Guess MIME type based on file extension
        mime_type, _ = mimetypes.guess_type(file_name)
        # Validate the MIME type
        if not mime_type:
            logging.error(f"ERROR: Unable to determine the MIME type for '{file_name}'. FROM [utility_ops.py]")
            raise ValueError(f"Could not determine MIME type for file: '{file_name}'")
        # Determine the file type based on MIME type
        if mime_type.startswith('image'):
            file_type = 'image'
        elif mime_type.startswith('video'):
            file_type = 'video'
        elif mime_type.startswith('audio'):
            file_type = 'audio'
        elif mime_type.startswith('application'):
            file_type = 'document'
        else:
            file_type = 'other'
        logging.info(f"SUCCESS: File '{file_name}' is identified as '{file_type}' with extension '.{extension}'.")
        return file_type, extension
