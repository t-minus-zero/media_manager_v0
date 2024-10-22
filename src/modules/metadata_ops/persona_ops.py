from src.modules.local_ops.json_ops import JSONFileManager
from src.modules.local_ops.os_ops import OSFileManager
import logging

class PersonaManager:
    def __init__(self, storage_path):
        self.script_name = 'persona_ops.py'
        self.storage_path = storage_path
        self.album = None
        self.replacer = None
        self.persona_dir = 'persona'
        self.profile_dir = 'profile'
        self.albums_dir = 'albums'
        self.persona_json = 'persona.json'
        self.accounts_json = 'accounts.json'
        self.schedule_json = 'schedule.json'
        self.stats_json = 'stats.json'
        self.thumbnail = 'thumbnail.jpg'
        self.default_thumbnail_path = 'default_thumbnail.jpg'

    def set_album(self, album):
        self.album = album

    def set_replacer(self, replacer):
        self.replacer = replacer

    def load_personas_data(self):
        """
        Load data for all personas.
        """
        personas_data = []

        personas_path = self.get_personas_path()
        if not personas_path:
            return personas_data

        persona_paths = self.get_list_of_persona_paths(personas_path)
        if not persona_paths:
            return personas_data

        for persona_path in persona_paths:
            profile_path = self.get_persona_profile_path(persona_path)
            if not profile_path:
                continue  # Skip this persona if no profile is found
            
            persona_data = self.fetch_persona_data(profile_path)
            if not persona_data:
                continue  # Skip if persona data can't be loaded

            persona_thumbnail = self.fetch_persona_thumbnail(profile_path)
            persona_data['thumbnail'] = persona_thumbnail
            persona_data['profile_path'] = profile_path
            persona_data['path'] = persona_path
            personas_data.append(persona_data)

        return personas_data

    def get_personas_path(self):
        """
        Get the path to the personas directory.
        """
        logging.info(f"LOADING: Looking for '{self.persona_dir}' directory. FROM [{self.script_name}]")
        personas_path = OSFileManager.find_path_of_xdirectory_in_xdirectory(self.persona_dir, self.storage_path)
        if not personas_path:
            logging.error(f"ERROR: Can't find the '{self.persona_dir}' directory in the storage path. FROM [{self.script_name}]")
            return None
        logging.info(f"SUCCESS: Directory '{self.persona_dir}' found. [{self.script_name}]")
        return personas_path

    def get_list_of_persona_paths(self, personas_path):
        """
        Get a list of paths to each persona directory.
        """
        personas_paths_list = OSFileManager.fetch_list_of_directories_in_xpath(personas_path)
        if not personas_paths_list:
            logging.error(f"ERROR: No personas found in the '{self.persona_dir}' directory. FROM [{self.script_name}]")
            return None
        logging.info(f"SUCCESS: Found {len(personas_paths_list)} personas. FROM [{self.script_name}]")
        return personas_paths_list
    
    def get_list_of_persona_album_paths(self, persona_path):
        """
        Fetch the list of albums for a persona.
        """
        albums = []
        albums_path = OSFileManager.find_path_of_xdirectory_in_xdirectory(self.albums_dir, persona_path)
        if not albums_path:
            logging.error(f"ERROR: No {self.albums_dir} directory found in the {self.persona_dir} directory. FROM [{self.script_name}]")
            return albums
        album_paths_list = OSFileManager.fetch_list_of_directories_in_xpath(albums_path)
        if not album_paths_list:
            logging.error(f"ERROR: No albums found in the {self.albums_dir} directory. FROM [{self.script_name}]")
            return albums
        return album_paths_list

    def get_persona_profile_path(self, persona_path):
        """
        Get the path to the profile directory of a specific persona.
        """
        profile_path = OSFileManager.find_path_of_xdirectory_in_xdirectory(self.profile_dir, persona_path)
        if not profile_path:
            logging.error(f"ERROR: {self.profile_dir} not found in {persona_path}. FROM [{self.script_name}]")
            return None
        logging.info(f"SUCCESS: Found {self.profile_dir} in {persona_path}. FROM [{self.script_name}]")
        return profile_path

    def fetch_persona_data(self, persona_profile_path):
        """
        Fetch data from the persona.json file in the profile directory.
        """
        persona_json_path = OSFileManager.find_path_of_xfile_in_xdirectory(self.persona_json, persona_profile_path)
        if not persona_json_path:
            logging.error(f"ERROR: {self.persona_json} not found in the persona directory. FROM [{self.script_name}]")
            return None
        persona_data = JSONFileManager.load_json_as_dataobj_from_xpath(persona_json_path)
        return persona_data

    def fetch_persona_thumbnail(self, persona_profile_path):
        """
        Fetch the path to the persona's thumbnail.
        """
        thumbnail_path = OSFileManager.find_path_of_xfile_in_xdirectory(self.thumbnail, persona_profile_path)
        if not thumbnail_path:
            logging.warning(f"ERROR: Thumbnail not found in the persona directory. Defaulting to '{self.default_thumbnail_path}'. FROM [{self.script_name}]")
            return self.default_thumbnail_path
        logging.info(f"SUCCESS: Thumbnail found at '{thumbnail_path}'. FROM [{self.script_name}]")
        return thumbnail_path
