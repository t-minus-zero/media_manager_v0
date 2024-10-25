import datetime
import logging
from src.modules.local_ops.os_ops import OSFileManager
from src.modules.local_ops.json_ops import JSONFileManager
from src.modules.utility_ops.utility_ops import UtilityOps
import uuid

album_json = 'album'

class AlbumManager:

    @staticmethod
    def create_info():
        now = datetime.datetime.now()
        album_id = f"ID-{uuid.uuid4().hex[:6]}"  # 'ID' + last 2 digits of year + month + day + hour + minutes + seconds
        return {
            "version": 1,
            "album_id": album_id
        }

    @staticmethod
    def create_edit():
        return {}

    @staticmethod
    def create_version(item_id, version_number):
        item_version_id = f"{item_id}_V{version_number}"
        return {
            "item_version_id": item_version_id,
            "version_number": version_number,
            "name": item_version_id,
            "url": None,  # relative to storage
            "file_type": None,
            "extension": None,
            "status": 'edit', # edit, ready
            "group": None,
            "edits": [AlbumManager.create_edit()]  # Includes one empty edit object
        }

    @staticmethod
    def create_item(album_id, item_number):
        item_id = f"{album_id}_I{item_number}"
        versions = [AlbumManager.create_version(item_id, 1)]  # Create one version per item initially
        return {
            "item_id": item_id,
            "versions": versions,
            "flag": 'maybe', # unusable, maybe, best
        }

    @staticmethod
    def create_new_album_data():
        info = AlbumManager.create_info()
        return {
            "info": info,
            "items": []
        }

    @staticmethod
    def load_album(album_path):
        """Load the album data from the album_path (directory) or create a new album if it doesn't exist."""
        # Check if the album path exists
        if not OSFileManager.check_if_xdirectory_exists(album_path):
            logging.error(f"ERROR: The path {album_path} does not exist. FROM [album_ops.py]")
            return None

        # Check if the album.json file exists
        album_json_path = OSFileManager.find_path_of_xfile_in_xdirectory(f"{album_json}.json", album_path)
        
        if album_json_path:
            # Load the existing album data
            try:
                album_data = JSONFileManager.load_json_as_dataobj_from_xpath(album_json_path)
                album_data['info']['url'] = album_path
                logging.info(f"SUCCESS: Album data loaded from '{album_json_path}'. FROM [album_ops.py]")
            except Exception as e:
                logging.error(f"ERROR: An error occurred while loading the album data: {e}. FROM [album_ops.py]")
                return None
        else:
            # Create new album if it doesn't exist
            logging.info(f"Initializing '{album_json}' file in {album_path}. FROM [album_ops.py]")
            album_data = AlbumManager.initialize_album(album_path)

            # Save the newly created album data
            try:
                JSONFileManager.save_xdataobj_as_xname_json_at_xpath(album_data, 'album', album_path)
                logging.info(f"SUCCESS: New album data saved as '{album_json}' in {album_path}. FROM [album_ops.py]")
                album_data['info']['url'] = album_path
            except Exception as e:
                logging.error(f"ERROR: An error occurred while saving the new album data: {e}. FROM [album_ops.py]")
                return None

        return album_data

    @staticmethod
    def initialize_album(album_path):
        """Initialize a new album by gathering files from the album path and processing them."""
        file_paths_list = OSFileManager.fetch_list_of_files_in_xpath(album_path)

        if not file_paths_list:
            logging.error(f"ERROR: No files found in {album_path}. FROM [album_ops.py]")
            return None

        new_album_data = AlbumManager.create_new_album_data()

        for file_path in file_paths_list:
            file_name = OSFileManager.get_name_from_xpath(file_path)
            file_type, extension = UtilityOps.get_file_type_and_extension(file_name)

            # Skip non-image and non-video files
            if file_type != 'image' and file_type != 'video':
                continue

            # Create a new item and update its information
            new_item = AlbumManager.create_item(new_album_data['info']['album_id'], len(new_album_data['items']) + 1)
            new_file_name = new_item['versions'][0]['item_version_id']
            new_file_path = OSFileManager.rename_path(file_path, new_file_name, extension)

            # Update item version details
            new_item['versions'][0]['name'] = new_file_name
            new_item['versions'][0]['url'] = new_file_path
            new_item['versions'][0]['file_type'] = file_type
            new_item['versions'][0]['extension'] = extension

            new_album_data['items'].append(new_item)

        new_album_data['info']['total_items'] = len(new_album_data['items'])
        new_album_data['info']['total_versions'] = new_album_data['info']['total_items']
        
        return new_album_data

    @staticmethod
    def save_album(album_data, album_path):
        """Save the current album data."""
        try:
            JSONFileManager.save_xdataobj_as_xname_json_at_xpath(album_data, album_json, album_path)
            logging.info(f"SUCCESS: Album data saved successfully. FROM [album_ops.py]")
        except Exception as e:
            logging.error(f"ERROR: Failed to save album data: {e}. FROM [album_ops.py]")

    @staticmethod
    def update_album(current_album, album_path):
        """Placeholder for updating the album with new items."""
        # Logic for updating album items, like checking for new media files and renaming
        return current_album
    
    @staticmethod
    def update_item(current_item, current_album, album_path):
        """Placeholder for updating the item with new versions."""
        album_json_path = OSFileManager.find_path_of_xfile_in_xdirectory(album_json, album_path)
        for index, item in enumerate(current_album['items']):
            if item['item_id'] == current_item['item_id']:
                current_album['items'][index] = current_item
                break
        JSONFileManager.save_xdataobj_as_xname_json_at_xpath(current_album, 'album', album_path)

        return current_album
    
    @staticmethod
    def get_album_previews(album_data):
        """Get the preview images for the album."""
        preview_images = []
        
        # Check if album_data is None or doesn't have 'items'
        if not album_data or 'items' not in album_data or not album_data['items']:
            return preview_images
        
        # Determine the positions to select the items
        items_number = len(album_data['items'])
        
        indices = [
            0,  # First item
            abs(items_number // 3),  # Item at position ABS(ItemsNumber / 3)
            abs(items_number - items_number // 3),  # Item at position ABS(ItemsNumber - ItemsNumber / 3)
            items_number - 1  # Last item
        ]
        
        # Ensure unique indices and keep them within the range
        indices = sorted(set(min(items_number - 1, max(0, idx)) for idx in indices))
        
        # Select the preview images based on the calculated indices
        for idx in indices:
            item = album_data['items'][idx]
            if item['versions']:
                latest_version = item['versions'][-1]
                preview_images.append(latest_version['url'])
        
        return preview_images
