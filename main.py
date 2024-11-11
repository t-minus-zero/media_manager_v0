from fasthtml.fastapp import *
from fasthtml.common import *
from fastapi.responses import FileResponse, Response
from datetime import datetime
from src.modules.ffmpeg_processing.heic_to_jpg import convert_heic_to_jpg
from os.path import dirname, join
import os
import logging
import asyncio
import requests
from src.modules.metadata_ops.persona_ops import PersonaManager
from src.modules.metadata_ops.album_ops import AlbumManager
from src.modules.web_gui.app_state import AppState
from src.modules.telegram_bot.telegram_test import send_images_from_urls
from src.modules.web_gui.behaviours import Behaviours
from src.modules.automation.kitt import KITT
from src.modules.web_gui.queue import Queue
from starlette.websockets import WebSocketDisconnect


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
        # Set cache control headers to prevent caching
        headers = {
            "Cache-Control": "no-store, must-revalidate", 
            "Pragma": "no-cache",
            "Expires": "0"
        }
        return FileResponse(full_path, headers=headers)
    else:
        return Response(content="File not found", status_code=404)
    

async def on_connect(send):
    await asyncio.sleep(2)  # 2-second delay before initial message
    print("Connection established, sending initial message")
    while True:
        print("Checking for queue updates")
        updated = Behaviours.update_queue(State)
        if updated: #check if the android server is running
            Behaviours.start_payload(State)
        
        if 'queue' in State.open_screens:
            print("Sending updated queue page")
            updated_queue_page = Queue.view(State)
            try:
                await send(updated_queue_page)
            except Exception:
                print("WebSocket disconnected.")
                break  # Exit loop if disconnected
        
        await asyncio.sleep(15)  # Adjust delay as needed


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
    State.set_current_item(selected_item)
    return Behaviours.open_item_in_edit(State)

@rt('/toggle_edit_tabs')
def post(tab: str):
    return Behaviours.toggle_edit_tabs(State, tab)

@rt('/key-arrow-left-right')
def post(key: str):
    return Behaviours.key_arrow_left_right(key, State)

@rt('/key-arrow-up-down')
def post(key: str):
    return Behaviours.key_arrow_up_down(key, State)

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
            item_id = State.current_item['item-data']['item_id']
            return Behaviours.change_flag(item_id, State, flag)
        
    if key in ['s']:
        if State.current_item:
            State.selection_mode = True
            item_id = State.current_item['item-data']['item_id']
            return Behaviours.add_remove_selected_item(item_id, State)

    return Div("key pressed: " + key, Id="response")


#------------------- Edit Options Routes -------------------

@rt('/toggle_edit_options')
def post(sheet_id: str):
    State.procedures = Behaviours.load_procedures(State)
    return Behaviours.toggle_edit_options(State, sheet_id, is_open=True)

@rt('/edits-list')
def post():
    return Behaviours.edits_list(State)

@rt('/edit-details')
def post(edit_name: str):
    return Behaviours.edit_details(State, edit_name)

@rt('/procedures-list')
def post():
    State.procedures = Behaviours.load_procedures(State)
    return Behaviours.procedures_list(State)

@rt('/procedure-details')
def post(procedure_name: str):
    return Behaviours.procedure_details(State, procedure_name)

@rt('/add-edit')
def post(edit_name: str, edit_value: str, target: str):
    if target == 'current':
        Behaviours.add_edit_to_current(State, edit_name, edit_value)
        return Behaviours.procedures_list(State)
    elif target == 'selected':
        item_id = State.selected_items[0]['item_id']
        version_index = State.selected_items[0]['version_index']
    else:
        return P("Invalid target", Id="response")

@rt('/send-to-queue')
def post(target: str):
    edit_screen, item_cards = Behaviours.send_to_queue(State, target)
    return edit_screen, *item_cards,


#------------------- Routes for testing - Some need to be deleted -------------------

@app.post('/test-procedures') # This is to test procedures with android server
async def get():
    return Div()

@app.post('/send-for-edit-test') # This is a telegram test route
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

@rt('/run-procedure')
def post(procedure_name: str):
    procedure = next((p for p in State.procedures if p['info']['name'] == procedure_name), None)
    url = "http://127.0.0.1:8000/process-image"
    payload = {
        "image_path": "image_path",
        "data_object": procedure
    }
    # Send the request to the FastAPI server
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()  # Raise an exception if the request was unsuccessful
        print("Server response:", response.json())
    except requests.exceptions.RequestException as e:
        print("Error communicating with the server:", e)
        return Behaviours.update_procedures_view(State, app_name='procedures')

#------------------- Debugging routes -------------------
@rt('/state')
def get():
    return Behaviours.view_state(State)

serve()

@rt('/convert-heic-to-jpg')
def get(path: str):
    try:
        output_path = join(dirname(path), "processing")
        convert_heic_to_jpg(path, output_path)
        return {'success': True, 'message': 'Folder created successfully', 'path': path}
    except Exception as e:
        return {'success': False, 'message': str(e)}
    

