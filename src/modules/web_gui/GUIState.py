from src.modules.local_ops.json_ops import JSONFileManager
from src.modules.local_ops.os_ops import OSFileManager
import logging

class StateManager:
    def __init__(self, storage_path):
        self.storage_path = storage_path
        self.album_paths_list = None
        self.replacer = None
        self.current_album = None
        self.previous_item = None
        self.current_item = None
        self.selected_items = []
        self.script_name = 'GUIState.py'

    def set_album_paths_list(self, album_paths_list):
        self.album_paths_list = album_paths_list

    def set_current_album(self, current_album):
        self.current_album = current_album
    
    def set_previous_item(self, item):
        self.previous_item = item
    
    def set_current_item(self, current_item):
        #if self.current_item['item_id'] != current_item['item_id']:
        #    self.set_previous_item(self, current_item)
        self.previous_item = self.current_item 
        self.current_item = current_item

    def add_to_selected_items(self, item):
        self.selected_items.append(item)
    
    def empty_selected_items(self):
        self.selected_items = []