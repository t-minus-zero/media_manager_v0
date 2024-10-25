from fasthtml.fastapp import *
from fasthtml.common import *
from src.modules.web_gui.structure import Structure
from src.modules.web_gui.navigation import Navigation
from src.modules.web_gui.persona import Persona
from src.modules.web_gui.album import Album
from src.modules.web_gui.item import Item
from src.modules.web_gui.edit import Edit
from src.modules.web_gui.queue import Queue
from src.modules.web_gui.options import Options
from src.modules.metadata_ops.album_ops import AlbumManager
from src.modules.local_ops.os_ops import OSFileManager
from src.modules.utility_ops.utility_ops import UtilityOps
import asyncio

class Behaviours:

    @staticmethod
    def initialize_app( State ):

        initial_page = Div(
            Persona.persona_info(State),
            Class="w-full h-full flex flex-col items-center justify-start",
            Id="main_page",
            hx_swap_oob="true"
        )

        navigation_bar = Structure.floating_navigation_bar(Navigation.navigation_bar(State))
        
        screens = [
            Structure.floating_screen("main_screen", [navigation_bar, initial_page])
        ]
        web_app = Structure.app_container(screens)
        return web_app
    
    @staticmethod
    def open_queue(State):
        queue_screen = Queue.view(State)
        queue_button = Navigation.queue_button(True)
        return queue_screen, queue_button
    
    @staticmethod
    def close_queue():
        return Navigation.queue_button(False)
    
    @staticmethod
    def toggle_persona_switcher(State, sheet_id, is_open):
        sheet_content = Persona.persona_switcher(State, sheet_id)
        bottom_sheet = Structure.bottom_sheet(sheet_id, sheet_content, sheet_open=is_open)
        return bottom_sheet
    
    @staticmethod
    def toggle_edit_options(State, sheet_id, is_open):
        sheet_content = Div(
            Options.automation_kiara(), 
            Class="w-full h-full flex items-center justify-center h-48 text-lg text-zinc-500 bg-zinc-700"
        )
        bottom_sheet = Structure.bottom_sheet(sheet_id, sheet_content, sheet_open=is_open)
        return bottom_sheet
    
    @staticmethod
    def toggle_persona(State):
        main_page = Persona.persona_info(State)
        updated_nav_button = Navigation.persona_options(True)
        updated_albums_button = Navigation.albums_button(False)
        return updated_nav_button, main_page, updated_albums_button
    
    @staticmethod
    def toggle_albums(State):
        main_page  = Album.grid(State)
        updated_nav_button = Navigation.albums_button(True)
        updated_persona_button = Navigation.persona_options(False)
        top_bar = Structure.grid_3_columns(
            [Navigation.persona_alias_button(alias=State.current_persona_data['alias'], active=True)],
            "",
            ""
            )
        top_navigation = Structure.sticky_top_navigation_bar(top_bar)
        return top_navigation, updated_nav_button, main_page, updated_persona_button, 

    @staticmethod
    def open_album(State):
        main_page = Item.grid(State)
        title = P(State.current_album_data['info']['album_id'], Class="text-md text-zinc-500 font-semibold")
        top_bar = Structure.grid_3_columns(
            [Navigation.back_to_albums_button(), title], 
            "",
            ""
            )
        top_navigation = Structure.sticky_top_navigation_bar(top_bar)
        return top_navigation, main_page
    
    @staticmethod
    def add_remove_selected_item(item_id, State):
        # Find the selected item
        selected_item = next((item for item in State.current_album_data['items'] if item['item_id'] == item_id), None)

        if selected_item is None:
            # If the item_id is not found, return an empty result
            return

        result = []

        if selected_item in State.selected_items:
            # Remove item if it is already selected
            State.selected_items.remove(selected_item)
        else:
            # Add item to the selected list
            State.selected_items.append(selected_item)

        # Create cards for the updated list of selected items
        for item_data in State.selected_items:
            card = Item.card(item_data, State)
            card.attrs['hx-swap-oob'] = 'true'
            result.append(card)

        # If the item was removed, we should still return its card to handle removal in the UI
        if selected_item not in State.selected_items:
            removed_card = Item.card(selected_item, State)
            removed_card.attrs['hx-swap-oob'] = 'true'
            result.append(removed_card)

        # Turn off selection mode if there are no selected items
        if not State.selected_items:
            State.selection_mode = False

        # Return each card individually, unpacking the result list
        return *result,

    @staticmethod
    def change_flag(item_id, State, flag):

        if State.current_item and State.current_item['item_id'] == item_id:
            State.current_item['flag'] = flag

        if State.current_album_data:
            album_item = next((item for item in State.current_album_data['items'] if item['item_id'] == item_id), None)
            if album_item:
                album_item['flag'] = flag

        album_item_card = Item.card(album_item, State)
        album_item_card.attrs['hx-swap-oob'] = 'true'

        if State.current_page == "albums":
            return  album_item_card

    @staticmethod
    def open_item_in_edit_1(State):
        current_item_card = Item.card(State.current_item, State)
        previous_item_card = None
        if State.previous_item:
            previous_item_card = Item.card(State.previous_item, State)
            previous_item_card.attrs['hx-swap-oob'] = 'true'
        current_item_card.attrs['hx-swap-oob'] = 'true'
        return current_item_card, previous_item_card
    
    @staticmethod
    def open_item_in_edit(State):
        current_item_card = Item.card(State.current_item, State)
        previous_item_card = None
        if State.previous_item:
            previous_item_card = Item.card(State.previous_item, State)
            previous_item_card.attrs['hx-swap-oob'] = 'true'
        current_item_card.attrs['hx-swap-oob'] = 'true'

        edit_view = Edit.view(State)
        if "edit" not in State.open_screens:
            edit_screen =  Structure.floating_screen("edit_screen", [edit_view])
            State.open_screens.append("edit")
            print("added edit screen to open screens")
            return edit_screen, current_item_card
        else:
            edit_view.attrs['hx-swap-oob'] = 'true'

        return current_item_card, previous_item_card, edit_view
            
    @staticmethod
    def key_arrow_left_right(key, State):
        # Step 1: Get the index of the current item in the album data
        current_index = None
        if State.current_item:
            for index, item in enumerate(State.current_album_data['items']):
                if item['item_id'] == State.current_item['item_id']:
                    current_index = index
                    break

        # Step 2: Handle the left or right arrow key press
        if key == "ArrowRight":
            # Update the previous item
            if State.current_item:
                State.previous_item = State.current_item

            # If we're at the last item, set index to 0
            if current_index is not None and current_index == len(State.current_album_data['items']) - 1:
                State.current_album_index = 0
            else:
                # Increment index if it's not the last item
                State.current_album_index = (current_index + 1) if current_index is not None else 0
            State.current_item = State.current_album_data['items'][State.current_album_index]
            return Behaviours.open_item_in_edit(State)

        elif key == "ArrowLeft":
            # Update the previous item
            if State.current_item:
                State.previous_item = State.current_item

            # If we're at the first item, set index to the last item
            if current_index is not None and current_index == 0:
                State.current_album_index = len(State.current_album_data['items']) - 1
            else:
                # Decrement index if it's not the first item
                State.current_album_index = (current_index - 1) if current_index is not None else len(State.current_album_data['items']) - 1
            State.current_item = State.current_album_data['items'][State.current_album_index]
            return Behaviours.open_item_in_edit(State)
        
        return Div("", id="dynamic-element", Class="w-0 h-0")
    
    @staticmethod
    async def send_to_queue(State):
        if State.selected_items:
            payload = []
            for item in State.selected_items:
                new_version =  AlbumManager.create_version(item['item_id'], len(item['versions'])+1)
                payload.append(
                    {
                        'procedures': [
                            {
                                'name': 'soda_test_edit',
                                'settings': {}
                             }
                            ],
                        'album_id': State.current_album_data['info']['album_id'],
                        'album_url': State.current_album_data['info']['url'],
                        'item_id': item['item_id'],
                        'version_url': item['versions'][-1]['url'],
                        'new_version_file_name': new_version['item_version_id']
                    }
                )

                new_version['status'] = 'queued'
                new_version_url = OSFileManager.copy_xfile_with_new_xname(item['versions'][-1]['url'], new_version['item_version_id'])
                new_version['file_type'], new_version['extension'] = UtilityOps.get_file_type_and_extension(new_version_url)
                new_version['url'] = new_version_url

                print("--------------------")
                print("new version: " + str(new_version))

                if State.current_album_data['info']['album_id'] == payload[0]['album_id']:
                    item_index = State.current_album_data['items'].index(item)
                    State.current_album_data['items'][item_index]['versions'].append(new_version)
                    State.current_item = State.current_album_data['items'][item_index]
                print("--------------------")
                print("current album data item: " + str( State.current_album_data['items'][State.current_album_data['items'].index(item)]['versions']))
                print("--------------------")


            AlbumManager.save_album(State.current_album_data, State.current_album_data['info']['url'])
            
            print("Waiting")
            await asyncio.sleep(2)

            #await State.kitt.process_payload(payload)
            State.queue_payloads.append(payload)

            button = Options.automation_kiara()

            edit_screen = Structure.floating_screen("edit_screen", [Edit.view(State)])
            edit_screen.attrs['hx-swap-oob'] = 'true'

            result = []
            for item_data in State.selected_items:
                card = Item.card(item_data, State)
                card.attrs['hx-swap-oob'] = 'true'
                result.append(card)

            State.selected_items = []

            return button, result, edit_screen
           