from src.modules.local_ops.json_ops import JSONFileManager
from src.modules.local_ops.os_ops import OSFileManager
import logging

class StateManager:
    def __init__(self, storage_path):
        self.script_name = 'GUIState.py'
        self.storage_path = storage_path
        self.open_tabs = []
        self.album_paths_list = None
        self.replacer = None
        self.current_album = None
        self.current_album_path = None
        self.previous_item = None
        self.current_item = None
        self.selected_items = []
        self.personas_data = []
        self.current_persona_data= []

    def set_album_paths_list(self, album_paths_list):
        self.album_paths_list = album_paths_list

    def set_current_album(self, current_album):
        self.current_album = current_album

    def set_current_album_path(self, current_album_path):
        self.current_album_path = current_album_path
    
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

    def update_current_persona(self, alias):
        self.current_persona_data = next((persona for persona in self.personas_data if persona['alias'] == alias), None)
        print("updated current persona to: " + self.current_persona_data['alias'])