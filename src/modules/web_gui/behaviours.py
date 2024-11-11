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
from src.modules.web_gui.procedures import Procedure
from src.modules.metadata_ops.payload_ops import PayloadOps
from src.modules.metadata_ops.album_ops import AlbumManager
from src.modules.utility_ops.utility_ops import UtilityOps
from src.modules.local_ops.json_ops import JSONFileManager
from src.modules.local_ops.os_ops import OSFileManager
from src.modules.web_gui.properties import Properties
from src.modules.web_gui.icon_view import IconView
import requests
import asyncio
import httpx
import os

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
        selected_item_version = State.current_item['version-index']

        if selected_item is None:
            # If the item_id is not found, return an empty result
            return

        result = []

        if any(selected_item['item_id'] == item['item-data'].get('item_id') for item in State.selected_items):
            # Remove item if it is already selected
            State.remove_from_selected_items(selected_item, selected_item_version)
            print("Removed item from selected items: " + selected_item['item_id'] + " with version index: " + str(selected_item_version))
        else:
            # Add item to the selected list
            State.add_to_selected_items(selected_item, selected_item_version)
            print("Added item to selected items: " + selected_item['item_id'] + " with version index: " + str(selected_item_version))

        # Create cards for the updated list of selected items
        for item in State.selected_items:
            card = Item.card(item['item-data'], State)
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

        if State.current_item['item-data'] and State.current_item['item-data']['item_id'] == item_id:
            State.current_item['item-data']['flag'] = flag

        if State.current_album_data:
            album_item = next((item for item in State.current_album_data['items'] if item['item_id'] == item_id), None)
            if album_item:
                album_item['flag'] = flag

        album_item_card = Item.card(album_item, State)
        album_item_card.attrs['hx-swap-oob'] = 'true'

        if State.current_page == "albums":
            return  album_item_card

    @staticmethod
    def open_item_in_edit(State):
        current_item_card = Item.card(State.current_item['item-data'], State)
        previous_item_card = None
        if State.previous_item['item-data']:
            print("This is the previous item: " + str(State.previous_item['item-data']['item_id']))
            previous_item_card = Item.card(State.previous_item['item-data'], State)
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
        current_index = State.find_index_of_item_in_album_items(State.current_item['item-data']['item_id'])

        # Step 2: Handle the left or right arrow key press
        if key in ("ArrowRight", "ArrowLeft"):
            num_items = len(State.current_album_data['items'])

            # Determine the new index based on the key press without using modulo
            if key == "ArrowRight":
                if current_index == num_items - 1:
                    State.current_album_index = 0  # Wrap around to the first item
                else:
                    State.current_album_index = current_index + 1  # Move to the next item
            elif key == "ArrowLeft":
                if current_index == 0:
                    State.current_album_index = num_items - 1  # Wrap around to the last item
                else:
                    State.current_album_index = current_index - 1  # Move to the previous item

            current_album_index = State.current_album_index

            # Update the current item
            new_item = State.current_album_data['items'][current_album_index]
            State.set_current_item(new_item,  version_index=0)

            print("Previous item: " + str(State.previous_item['item-data']['item_id']))
            print("Current item: " + str(State.current_item['item-data']['item_id']))
            # Open the item in edit mode
            return Behaviours.open_item_in_edit(State)

        # Return an empty Div if no valid key is pressed
        return Div("", id="dynamic-element", Class="w-0 h-0")

    @staticmethod
    def key_arrow_up_down(key, State):

        print("Current version index: " + str(State.current_item['version-index']))

        if key == "ArrowUp":
            if State.current_item['version-index'] > 0:
                State.current_item['version-index'] -= 1
        elif key == "ArrowDown":
            if State.current_item['version-index'] < len(State.current_item['item-data']['versions']) - 1:
                State.current_item['version-index'] += 1

        edit_preview = Edit.preview(State.current_item['item-data'], State.current_item['version-index'])
        edit_view = Edit.view(State)
        print("Updated edit preview with version index: " + str(State.current_item['version-index']))

        return edit_view

    @staticmethod
    def toggle_edit_options(State, sheet_id, is_open):
        edit_options_screen = Behaviours.edits_list(State)
        edit_options_screen
        bottom_sheet = Structure.bottom_sheet(sheet_id, edit_options_screen, sheet_open=is_open)
        return bottom_sheet
    
    @staticmethod
    def load_procedures(State):
        procedures_path = OSFileManager.find_path_of_xdirectory_in_xdirectory("procedures", "storage")
        procedure_paths = OSFileManager.fetch_list_of_files_in_xpath(procedures_path)
        procedures_list = []
        for filepath in procedure_paths:
            procedure = JSONFileManager.load_json_as_dataobj_from_xpath(filepath)
            procedures_list.append(procedure)
        return procedures_list
    
    @staticmethod
    def edits_list(State):
        left_col = []
        center_col = [P("Edits List", Class="text-lg text-zinc-500 font-semibold")]
        right_col = [Button(
            IconView.get_icon_view("x", "size-6 text-zinc-100"), 
            Class="h-8 w-8 flex items-center justify-center", 
            onclick=f"closeBottomSheet('edit_screen_bottom_sheet')")]

        top_menu = Structure.grid_3_columns(left_col, center_col, right_col)

        version_edits = State.current_item['item-data']['versions'][State.current_item['version-index']]['edits']

        completed_edits = [Properties.item(None, edit['name'], None, None, None) for edit in version_edits if edit['status'] == 'completed']
        pending_edits = [] 
        for edit in version_edits:
            if edit['status'] == 'pending':
                action = {
                    'post': '/edit-details',
                    'target': '#edit-options-screen',
                    'trigger': 'click',
                    'vals': {'edit_name': edit['name']}
                }
                right = [Div(
                    IconView.get_icon_view("right-chevron", "size-6 text-zinc-100"), 
                    Class="flex items-center justify-center"
                    )]
                edit_item = Properties.item(None, edit['name'], None, action, right)
                pending_edits.append(edit_item)
        
        add_edits = {
            'post': '/procedures-list',
            'target': '#edit-options-screen',
            'trigger': 'click',
            'vals': {}
        }
        pending_edits.append(Properties.text_button("Add Edit", add_edits))

        send_to_queue = {
            'post': '/send-to-queue',
            'target': '#edit_screen',
            'trigger': 'click',
            'vals': {'target': 'current'}
        }
        send_all_to_queue = {
            'post': '/send-to-queue',
            'target': '#edit_screen',
            'trigger': 'click',
            'vals': {'target': 'selected'}
        }

        content = [ 
            Structure.sticky_top_navigation_bar(top_menu),
            Properties.container("Completed", completed_edits, None), 
            Properties.container("Pending", pending_edits, None),
            Properties.container(None, [Properties.text_button("Send Current to Queue", send_to_queue)] , None),
            Properties.container(None, [Properties.text_button("Send All Selected to Queue", send_all_to_queue)] , None)
            ]
        
        return Div(
            *content, 
            Class="w-full h-full flex flex-col gap-2 items-start justify-start min-h-48 text-lg text-zinc-500 bg-zinc-700",
            Id="edit-options-screen"
        )

    @staticmethod
    def edit_details(State, edit_name):

        left_col = [Button(
            IconView.get_icon_view("left-chevron", "size-6 text-zinc-100"), 
            Class="h-8 w-8 flex items-center justify-center",
            hx_post="/edits-list",
            hx_target="#edit-options-screen",
            hx_trigger="click",
        )]
        center_col = [P(edit_name, Class="text-lg text-zinc-500 font-semibold")]
        right_col = [Button(IconView.get_icon_view("x", "size-6 text-zinc-100"), Class="h-8 w-8 flex items-center justify-center", onclick=f"closeBottomSheet('edit_screen_bottom_sheet')")]
        top_menu = Structure.grid_3_columns(left_col, center_col, right_col)

        edit = next((edit for edit in State.current_item['item-data']['versions'][State.current_item['version-index']]['edits'] if edit['name'] == edit_name), None)
        
        info_container = []
        info_items = []

        if edit:
            right_name = [P(edit['name'], Class="text-zinc-400 text-xs")]
            info_items.append(Properties.item(None, "Name:", None, None, right_name))
            right_value = [P(edit['value'], Class="text-zinc-400 text-xs")]
            info_items.append(Properties.item(None, "Value:", None, None, right_value))
            right_status = [P(edit['status'], Class="text-zinc-400 text-xs")]
            info_items.append(Properties.item(None, "Status:", None, None, right_status))
            if edit['status'] == 'pending':
                remove_edit = {
                    'post': '/remove-edit',
                    'target': '#edit-options-screen',
                    'trigger': 'click',
                    'vals': {'edit_name': edit['name']}
                }
                info_items.append(Properties.text_button("Remove", remove_edit))
            info_container.append(Properties.container( edit['name'] , info_items, None))   

        
        return Div(
            Structure.sticky_top_navigation_bar(top_menu),
            *info_container,
            Class="w-full h-full flex flex-col gap-2 items-center justify-start min-h-48 text-lg text-zinc-500 bg-zinc-700",
            Id="edit-options-screen"
        )

    @staticmethod
    def procedures_list(State):

        left_col = [Button(
            IconView.get_icon_view("left-chevron", "size-6 text-zinc-100"), 
            Class="h-8 w-8 flex items-center justify-center",
            hx_post="/edits-list",
            hx_target="#edit-options-screen",
            hx_trigger="click",
        )]
        center_col = [P("Procedures List", Class="text-lg text-zinc-500 font-semibold")]
        right_col = [Button(IconView.get_icon_view("x", "size-6 text-zinc-100"), Class="h-8 w-8 flex items-center justify-center", onclick=f"closeBottomSheet('edit_screen_bottom_sheet')")]
        top_menu = Structure.grid_3_columns(left_col, center_col, right_col)


        procedures_container = []
        procedures_items = []

        for procedure in State.procedures:
            action = {
                'post': '/procedure-details',
                'target': '#edit-options-screen',
                'trigger': 'click',
                'vals': {'procedure_name': procedure['info']['name']}
            }
            right = [Div(
                IconView.get_icon_view("right-chevron", "size-6 text-zinc-100"), 
                Class="flex items-center justify-center"
                )]
            procedures_items.append(Properties.item(None, procedure['info']['name'], None, action, right))
            procedures_container.append(Properties.container("Procedures", procedures_items, None))

        return Div(
            Structure.sticky_top_navigation_bar(top_menu),
            *procedures_container,
            Class="w-full h-full flex flex-col gap-2 items-center justify-start min-h-48 text-lg text-zinc-500 bg-zinc-700",
            Id="edit-options-screen"
        )
        
    @staticmethod
    def procedure_details(State, procedure_name):
        
        left_col = [Button(
            IconView.get_icon_view("left-chevron", "size-6 text-zinc-100"), 
            Class="h-8 w-8 flex items-center justify-center",
            hx_post="/procedures-list",
            hx_target="#edit-options-screen",
            hx_trigger="click",
        )]
        center_col = [P(procedure_name, Class="text-lg text-zinc-500 font-semibold")]
        right_col = [Button(IconView.get_icon_view("x", "size-6 text-zinc-100"), Class="h-8 w-8 flex items-center justify-center", onclick=f"closeBottomSheet('edit_screen_bottom_sheet')")]
        top_menu = Structure.grid_3_columns(left_col, center_col, right_col)

        procedure = next((procedure for procedure in State.procedures if procedure['info']['name'] == procedure_name), None)
        
        info_container = []
        info_items = []

        if procedure:
            right_name = [P(procedure['info']['name'], Class="text-zinc-400 text-xs")]
            info_items.append(Properties.item(None, "Name:", None, None, right_name))
            right_value = [P(f"{len(procedure['steps'])}", Class="text-zinc-400 text-xs")]
            info_items.append(Properties.item(None, "Steps:", None, None, right_value))
            add_to_current = {
                'post': '/add-edit',
                'target': '#edit-options-screen',
                'trigger': 'click',
                'vals': {'edit_name': procedure['info']['name'], 'edit_value': "value", 'target': "current",}
            }
            info_items.append(Properties.text_button("Add to Current", add_to_current))
            add_to_all = {
                'post': '/add-edit',
                'target': '#edit-options-screen',
                'trigger': 'click',
                'vals': {'edit_name': procedure['info']['name'], 'edit_value': "value", 'target': "selected",}
            }
            info_items.append(Properties.text_button("Add to All Selected", add_to_all))
            info_container.append(Properties.container( procedure['info']['name'] , info_items, None))

        return Div(
            Structure.sticky_top_navigation_bar(top_menu),
            *info_container,
            Class="w-full h-full flex flex-col gap-2 items-center justify-start min-h-48 text-lg text-zinc-500 bg-zinc-700",
            Id="edit-options-screen"
        )

    @staticmethod
    def add_edit_to_current(State, edit_name, edit_value):
        if State.current_item:
            State.current_item['item-data']['versions'][State.current_item['version-index']]['edits'].append({
                'name': f"{edit_name}",
                'value': f"{edit_value}",
                'status': 'pending'
            })
            print("Added this edit to current item: " + edit_name + " : " + edit_value)
            return Queue.view(State)
        return Queue.view(State)
    
    @staticmethod
    def send_to_queue(State, target):
        # Determine items to process based on target
        items = [State.current_item] if target == 'current' else State.selected_items
        State.selected_items = []
        item_cards = []
        jobs = []

        print("Starting send_to_queue with target:", target)
        print("Items to process:", items)
        
        for item in items:
            # Get original version URL
            og_version_url = item['item-data']['versions'][item['version-index']]['url']
            duplicate_version_index = len(item['item-data']['versions'])  # Calculate new version index
            print("Original version URL:", og_version_url)
            print("New duplicate version index:", duplicate_version_index)

            # Create a duplicate version
            duplicate_version = AlbumManager.create_version(item['item-data']['item_id'], duplicate_version_index + 1)
            duplicate_version['status'] = 'queued'
            duplicate_version['edits'] = item['item-data']['versions'][item['version-index']]['edits']
            print("Duplicate version created:", duplicate_version)
            
            # Copy file with a new name for duplicate
            duplicate_version_url = OSFileManager.copy_xfile_with_new_xname(og_version_url, duplicate_version['item_version_id'])
            if duplicate_version_url:
                duplicate_version['file_type'], duplicate_version['extension'] = UtilityOps.get_file_type_and_extension(duplicate_version_url)
                duplicate_version['url'] = duplicate_version_url
                print("Duplicate version file URL assigned:", duplicate_version_url)
            else:
                print("Error: Failed to create or locate duplicate version file.")
                continue  # Skip processing if copy fails
            
            # Find the index of the current item within the album's items based on item_id
            item_index_in_album = next((i for i, album_item in enumerate(State.current_album_data['items']) if album_item['item_id'] == item['item-data']['item_id']), None)
            if item_index_in_album is None:
                print(f"Error: Item with ID {item['item-data']['item_id']} not found in album.")
                continue  # Skip processing if item is not found in the album

            print("Item index in album data:", item_index_in_album)

            # Remove pending edits from the current version's edits before updating
            current_version_edits = item['item-data']['versions'][item['version-index']]['edits']
            item['item-data']['versions'][item['version-index']]['edits'] = [
                edit for edit in current_version_edits if edit['status'] != 'pending'
            ]
            print("Pending edits removed from current version's edits.")

            # Add duplicate version to the album's item versions list
            State.current_album_data['items'][item_index_in_album]['versions'].append(duplicate_version)
            print("Duplicate version appended to album at item index:", item_index_in_album)
            
            # Create job for the duplicate version
            updated_item_data = item['item-data']
            State.procedures = Behaviours.load_procedures(State)
            job = PayloadOps.create_job(updated_item_data, duplicate_version_index, State.procedures)
            
            if job:
                jobs.append(job)
                print("Job created and added to jobs list:", job)
            
            # Create an item card for the UI update
            item_card = Item.card(item['item-data'], State)
            item_card.attrs['hx-swap-oob'] = 'true'
            item_cards.append(item_card)
            print("Item card created for item:", item_card)

        # Create payload from jobs
        payload = PayloadOps.create_payload(jobs)
        State.queue_payloads.append(payload)
        print("Payload created with ID:", payload['info']['payload-id'])

        # Save the payload to the queued.json file
        path_to_queues = OSFileManager.find_path_of_xdirectory_in_xdirectory("queues", State.storage_path)
        print("------- >>>>>>> Path to queues:", path_to_queues)
        JSONFileManager.save_xdataobj_as_xname_json_at_xpath(State.queue_payloads, "queued", path_to_queues)
        
        # Update current item to reflect duplicate version
        State.current_item['item-data'] = State.current_album_data['items'][item_index_in_album]
        State.current_item['version-index'] = duplicate_version_index
        print("Updated current item data and version index:", State.current_item)

        # Save album with the new version in the album data
        AlbumManager.save_album(State.current_album_data, State.current_album_data['info']['url'])
        print("Album saved with updated data.")

        # Return edit screen and item cards
        edit_screen = Structure.floating_screen("edit_screen", [Edit.view(State)])
        print("Edit screen and item cards returned.")
        
        return edit_screen, item_cards

    @staticmethod
    def update_queue(State):
        if State.current_payload is not None:
            status = State.current_payload['info']['status']
            path_to_queues = OSFileManager.find_path_of_xdirectory_in_xdirectory("queues", State.storage_path)
            if status == 'completed':
                State.queue_completed.append(State.current_payload)
                # Update the album data with the new version and its edits, save the album data and update state and GUI if affected
                JSONFileManager.save_xdataobj_as_xname_json_at_xpath(State.queue_completed, "completed", path_to_queues)
                State.current_payload = None
                return True
            elif status == 'aborted':
                State.queue_aborted.append(State.current_payload)
                JSONFileManager.save_xdataobj_as_xname_json_at_xpath(State.queue_aborted, "aborted", path_to_queues)
                State.current_payload = None
                return True
            elif status == 'processing':
                # Keep the current payload as-is, return the current queue screen and the processing queue card
                return False
            elif status == 'queued':
                State.current_payload['info']['status'] = 'processing'
                return False
        return True
            
    @staticmethod
    def start_payload(State):
        if len(State.queue_payloads) > 0 :
            State.current_payload = State.queue_payloads.pop(0)
            State.current_payload['info']['status'] = 'processing'

            # Use asyncio to start the non-blocking request
            asyncio.create_task(Behaviours.send_payload_to_android_server(State))

            path_to_queues = OSFileManager.find_path_of_xdirectory_in_xdirectory("queues", State.storage_path)
            JSONFileManager.save_xdataobj_as_xname_json_at_xpath(State.queue_payloads, "queued", path_to_queues)
            print("Started payload: " + State.current_payload['info']['payload-id'])
        else:
            State.current_payload = None
            print("Queue is empty.")


    @staticmethod
    async def send_payload_to_android_server(State):
        url = "http://127.0.0.1:8000/process-payload"
        data = {"payload": State.current_payload}

        timeout = httpx.Timeout(120.0)

        async with httpx.AsyncClient(timeout=timeout) as client:
            try:
                response = await client.post(url, json=data)
                response.raise_for_status()
                # Process the server's response with a callback function
                print(">>>>>>> RECEIVED RESPONSE <<<<<<<")
                Behaviours.process_response(State, response.json())
                print(">>>>>>> PROCESSED RESPONSE <<<<<<<")
            except httpx.RequestError as e:
                print("Error communicating with the server:", e)


    @staticmethod
    def process_response(State, response_data):
        if 'result' not in response_data:
            print("NO RESULT IN SERVER RESPONSE")
            return
        
        payload = response_data['result']
        State.current_payload = payload  # Updates State with the new payload from server

        # Iterate over each job in the response payload
        for job in payload['jobs']:
            # Extract relevant details from job
            item_id = job['item-data']['item_id']
            version_index = job['version-index']
            job_version = job['item-data']['versions'][version_index]
            job_edits = job['edits']

            # Locate the matching media item in the album data by item_id
            media_item = next((item for item in State.current_album_data['items'] if item['item_id'] == item_id), None)

            if media_item is None:
                print(f"Media item with ID {item_id} not found in album data.")
                continue

            # Access the version to update in the media item's versions
            media_version = media_item['versions'][version_index]

            # Check if the file extensions of the URLs are different
            media_extension = os.path.splitext(media_version['url'])[1]
            job_extension = os.path.splitext(job_version['url'])[1]

            if media_extension != job_extension:
                # Delete the old image if extensions differ
                old_image_path = media_version['url']  # Use the URL/path of the old image
                print("Deleting old image at path:", old_image_path)
                OSFileManager.delete_xfile(old_image_path)

            # Update the version data in the media item with the new version from job
            media_item['versions'][version_index] = job_version

            # Process edits: remove incomplete edits from the existing media version
            media_item['versions'][version_index]['edits'] = [
                edit for edit in media_item['versions'][version_index].get('edits', []) if edit.get('status') == 'completed'
            ]

            # Add new edits from the job, excluding the 'procedure' field
            processed_edits = []
            for edit in job_edits:
                edit_copy = edit.copy()  # Make a copy to avoid modifying the original job edit
                edit_copy.pop('procedure', None)  # Remove 'procedure' if it exists
                processed_edits.append(edit_copy)
            
            # Append these processed edits to the media version's edits
            media_item['versions'][version_index]['edits'].extend(processed_edits)

            # Set the media version's status to "completed"
            media_item['versions'][version_index]['status'] = "completed"

            # Update the file type and extension based on the updated URL
            updated_url = media_item['versions'][version_index]['url']
            file_type, extension = UtilityOps.get_file_type_and_extension(updated_url)
            media_item['versions'][version_index]['file_type'] = file_type
            media_item['versions'][version_index]['extension'] = extension

        # Save the updated album data
        AlbumManager.save_album(State.current_album_data, State.current_album_data['info']['url'])
        return


            
        

          

    #------------------- Debugging -------------------

    @staticmethod
    def view_state(State):
        return Div(
            P("Persona Data: " + str(State.current_persona_data)),
            P("Queue Payloads: " + str(State.queue_payloads)),
            P("Queue Aborted: " + str(State.queue_aborted)),
            P("Queue Completed: " + str(State.queue_completed)),
            P("Current Page: " + str(State.current_page)),
            P("Current Album: " + str(State.current_album_data)),
            P("Current Item: " + str(State.current_item)),
            P("Procedures: " + str(State.procedures)),
            P("Selection Mode: " + str(State.selection_mode)),
            P("Selected Items: " + str(State.selected_items)),
            P("Kitt Status: " + str(State.kitt)),
            P("K Status: " + str(State.k_status)),
            Id="state",
            Class="w-full h-full bg-zinc-900 flex flex-col items-start justify-start gap-4 p-4 text-zinc-300 text-xs"
        )




