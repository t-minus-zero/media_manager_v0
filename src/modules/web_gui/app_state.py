from src.modules.local_ops.json_ops import JSONFileManager
from src.modules.local_ops.os_ops import OSFileManager
import logging

class AppState:
    def __init__(self, storage_path):
        self.script_name = 'app_State.py'
        self.storage_path = storage_path

        self.kitt = None
        self.k_status = False
        
        self.open_screens = [] # list of open screens (pages)
        self.current_page = None # current screen (page)
        self.open_views = [] # list of open views
        
        self.personas_data = [] # list of persona objects
        self.current_persona_data= [] # persona object

        self.albums_data = [] # list of album objects
        self.current_album_data = [] # album object
        self.current_album_index = 0 # index of current album in albums_data

        self.selection_mode = False # boolean
        self.selected_items = [] # list of item objects

        self.current_item = None # item object
        self.previous_item = None # item object

        self.queue_payloads = []

    
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