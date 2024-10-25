from fasthtml.fastapp import *
from fasthtml.common import *
from typing import Any
from datetime import datetime
from src.navigation import navigation, screensToggle
from src.file_viewer import file_viewer
from src.modules.ffmpeg_processing.heic_to_jpg import convert_heic_to_jpg
from os.path import dirname, join
from src.functions.os_operations import  get_personas, create_new_folder, load_json_from_directory
from src.components.ui_design_system import pageContainer, icon_button, profile
from src.components.persona_card import persona_card
from src.components.file_card import file_card
import os
import logging
import asyncio
from src.modules.metadata_ops.persona_ops import PersonaManager
from src.modules.metadata_ops.album_ops import AlbumManager
from src.modules.web_gui.file_card import GUICards
from src.modules.web_gui.app_state import AppState
from src.modules.web_gui.edit_view import GUIEditView
from src.modules.telegram_bot.telegram_test import send_images_from_urls
from src.modules.android.appium_ops import Appium
from src.modules.android.android_ops import AndroidOps
from src.modules.local_ops.json_ops import JSONFileManager
from src.modules.android.adb_ops import ADBImageManager
from src.modules.local_ops.os_ops import OSFileManager
from src.modules.utility_ops.utility_ops import UtilityOps
from src.modules.web_gui.behaviours import Behaviours
from src.modules.web_gui.options import Options
from src.modules.automation.kitt import KITT

from fastapi.responses import FileResponse

app = FastHTML(
    pico=False,
    exts = 'ws',
    ws_hdr = True,
    hdrs=(
        Link(rel='stylesheet', href='https://fonts.googleapis.com/css?family=Roboto:400,700&display=swap', type='text/css'),
        Link(rel='stylesheet', href='/src/modules/web_gui/style.css', type='text/css'),
        Script(src="https://cdn.tailwindcss.com")
    )
)

rt = app.route

# Constants
path_to_storage = "storage/" # storage is in the root directory

# Initializations
logging.basicConfig(level=logging.INFO)
persona_manager = PersonaManager(path_to_storage)
State = AppState(path_to_storage)

@app.get("/storage/{file_path:path}")
async def serve_static(file_path: str):
    # IDK how this works but it fixes the issue with files not loading in the gui
    full_path = os.path.join("storage", file_path)
    if os.path.exists(full_path):
        return FileResponse(full_path)
    else:
        return {"error": "File not found"}
    

async def on_connect(send):
    await asyncio.sleep(2)  # 2-second delay before initial message
    print("Connection established, sending initial message")
    await send(Script("alert('WebSocket connected on client');")),
    while True:
        current_time = datetime.now().strftime("%M:%S")
        print(f"Sending current time: {current_time}")
        await send(P(f"Current time: {current_time}", Class="text-zinc-100 text-xs", Id="queue_status"),)
        await asyncio.sleep(10)  # Send every 3 seconds

@rt('/')
def get():
    return Div(
        Div(id="notifications"),  # Placeholder for WebSocket messages
        Script("console.log('WebSocket connected on client');"),
        hx_ext='ws', ws_connect='/ws'
    )

@app.ws('/ws', conn=on_connect)
async def ws(msg: str, send):
    #should be using this to make the websockets work but it does not do IDK why
    await send(Script("alert('WebSocket reply');")),


@rt('/app')
def get():
    State.personas_data = persona_manager.load_personas_data()
    State.current_persona_data = State.personas_data[0]
    print(State.personas_data)
    return Behaviours.initialize_app(State)

@rt('/change_persona')
def post(alias: str):
    State.update_current_persona(alias)
    album_paths = persona_manager.get_list_of_persona_album_paths(State.current_persona_data['path'])
    State.albums_data = [AlbumManager.load_album(album_path) for album_path in album_paths]
    result = Behaviours.toggle_persona(State) if State.current_page == 'persona' else Behaviours.toggle_albums(State)
    return result

@rt('/toggle_persona_switcher')
def post(sheet_id: str):
    return Behaviours.toggle_persona_switcher(State, sheet_id, is_open=True)

@rt('/toggle_queue')
def post(page: str):
    if 'queue' in State.open_screens:
        State.open_screens.remove('queue')
        return Behaviours.close_queue()
    State.open_screens.append('queue')
    return Behaviours.open_queue(State)

@rt('/close_edit')
def post(page: str):
    State.open_screens.remove('edit')
    return None

@rt('/toggle_albums')
def post(page: str):
    State.current_page = page
    return Behaviours.toggle_albums(State)

@rt('/toggle_profile')
def post(page: str):
    State.current_page = page
    return Behaviours.toggle_persona(State)

@rt('/open_album')
def post(album_id: str):
    State.current_album_data = next((album for album in State.albums_data if album['info']['album_id'] == album_id), None)
    return Behaviours.open_album(State)

@rt ('/open-item-in-edit')
def post(item_id: str):
    selected_item = next((item for item in State.current_album_data['items'] if item['item_id'] == item_id), None)
    if State.current_item and State.current_item['item_id'] != selected_item['item_id']:
        State.previous_item = State.current_item
    State.current_item = selected_item
    return Behaviours.open_item_in_edit(State)

@rt('/toggle_edit_options')
def post(sheet_id: str):
    return Behaviours.toggle_edit_options(State, sheet_id, is_open=True)

@rt('/key-arrow-left-right')
def post(key: str):
    return Behaviours.key_arrow_left_right(key, State)

@rt('/change-flag')
def post(item_id: str, flag: str):
    return Behaviours.change_flag(item_id, State, flag)

@rt('/add_remove_selected_item')
def post(item_id: str):
    return Behaviours.add_remove_selected_item(item_id, State)

@rt('/key-pressed')
def post(key: str):
    print(key)

    if key in ['v', 'b', 'n', 'm']:
        if State.current_item:
            flag = {"v": "unflagged", "b": "yes", "n": "no", "m": "maybe"}.get(key, "unflagged")
            item_id = State.current_item['item_id']
            return Behaviours.change_flag(item_id, State, flag)
        
    if key in ['s']:
        if State.current_item:
            State.selection_mode = True
            item_id = State.current_item['item_id']
            return Behaviours.add_remove_selected_item(item_id, State)

    return Div("key pressed: " + key, Id="response")


# Routes for testing - some need to be deleted

@app.post('/send-for-edit-test')
async def post():
    selected_items = State.selected_items
    print(selected_items)
    urls = [item['versions'][-1]['url'] for item in selected_items]
    # Call the asynchronous function and await it
    await send_images_from_urls(urls)
    return {"status": "Images sent successfully"}

@rt('/initialize-kitt')
async def post():
    print("Initializing KITT")
    State.kitt = KITT()
    await State.kitt.initialize()
    State.k_status = True
    print("KITT Initialized")
    return P("KITT is alive", Class="text-zinc-100 text-xs", Id="adb_status")

@rt('/start_automation')
async def post(edit: str):
    print("Starting Automation")
    button, result, edit_screen = await Behaviours.send_to_queue(State)
    return button, *result, edit_screen

serve()


@rt('/create-folder')
def get(path: str):
    result = create_new_folder(path)
    return result

@rt('/convert-heic-to-jpg')
def get(path: str):
    try:
        output_path = join(dirname(path), "processing")
        convert_heic_to_jpg(path, output_path)
        return {'success': True, 'message': 'Folder created successfully', 'path': path}
    except Exception as e:
        return {'success': False, 'message': str(e)}
    

