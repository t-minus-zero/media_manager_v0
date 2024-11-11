from src.modules.local_ops.json_ops import JSONFileManager
from src.modules.local_ops.os_ops import OSFileManager
import logging
import os

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
        self.selected_items = [] # list of item objects { 'item-data' : item_data, 'version-index' : 3 }

        self.current_item = { 'item-data' : None, 'version-index' : 0 } # item object
        self.previous_item = { 'item-data' : None, 'version-index' : 0 } # item object

        self.current_payload = None 
        self.queue_payloads = JSONFileManager.load_json_as_dataobj_from_xpath(os.path.join(self.storage_path, 'queues', 'queued.json'))
        self.queue_aborted = JSONFileManager.load_json_as_dataobj_from_xpath(os.path.join(self.storage_path, 'queues', 'aborted.json'))
        self.queue_completed = JSONFileManager.load_json_as_dataobj_from_xpath(os.path.join(self.storage_path, 'queues', 'completed.json'))

        self.procedures = [] # list of procedure objects

    
    def set_current_item(self, item_data, version_index=0):
        if self.previous_item['item-data'] is None or self.previous_item['item-data']['item_id'] != self.current_item['item-data']['item_id']:
            self.previous_item['item-data'] = self.current_item['item-data']
            self.previous_item['version-index'] = self.current_item['version-index']
        #print("Previous item: " + str(self.previous_item['item-data']['item_id']))
        version_index = len(item_data['versions'])-1 if version_index == -1 else version_index
        self.current_item['item-data'] = item_data
        self.current_item['version-index'] = version_index
        #print("Current item: " + str(self.current_item['item-data']['item_id']))

    def add_to_selected_items(self, item_data, version_index=-1):
        item = { 'item-data' : item_data, 'version-index' : version_index }
        self.selected_items.append(item)
        print("All items selected: " + str([(item['item-data']['item_id'], item['version-index']) for item in self.selected_items]))

    def remove_from_selected_items(self, item_data, version_index=-1):
        if not self.selected_items:
            print("ERROR: Cannot remove item from Selected items list as the list is empty.")
            return

        item_id = item_data.get('item_id')

        if version_index == -1:
            # Remove all items with the same item_id
            self.selected_items = [item for item in self.selected_items if item.get('item-data', {}).get('item_id') != item_id]
        else:
            # Remove items with matching item_id and version_index
            self.selected_items = [
                item for item in self.selected_items
                if item.get('item-data', {}).get('item_id') != item_id or item.get('version-index') != version_index
            ]
        print("All items selected: " + str([(item['item-data']['item_id'], item['version-index']) for item in self.selected_items]))

    def empty_selected_items(self):
        num_selected_items = len(self.selected_items)
        self.selected_items = []
        print(f"Emptied Selected Items list. Removed {num_selected_items} items.")

    def find_first_index_by_item_id_in_selected(self, item_id):
        for index, item in enumerate(self.selected_items):
            if item.get('item-data', {}).get('item_id') == item_id:
                return index
        return -1  # Return -1 if no matching item_id is found
    
    def find_index_of_item_in_album_items(self, item_id):
        for index, item in enumerate(self.current_album_data['items']):
            if item.get('item_id') == item_id:
                return index
        return -1  # Return -1 if no matching item_id is found

    def update_current_persona(self, alias):
        #who? persona-alias, what? setting-name, how? new-setting-value
        self.current_persona_data = next((persona for persona in self.personas_data if persona['alias'] == alias), None)
        print("updated current persona to: " + self.current_persona_data['alias'])