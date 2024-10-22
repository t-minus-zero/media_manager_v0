from fasthtml.fastapp import *
from fasthtml.common import *
from typing import Any
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
from src.modules.android.android_ops import AndroidOps
from src.modules.local_ops.json_ops import JSONFileManager
from src.modules.android.adb_ops import ADBImageManager
from src.modules.local_ops.os_ops import OSFileManager
from src.modules.utility_ops.utility_ops import UtilityOps
from src.modules.web_gui.behaviours import Behaviours
from src.modules.web_gui.navigation import Navigation

app, rt = fast_app(
    pico=False,
    hdrs=(
        Link(rel='stylesheet', href='https://fonts.googleapis.com/css?family=Roboto:400,700&display=swap', type='text/css'),
        Link(rel='stylesheet', href='/src/modules/web_gui/style.css', type='text/css'),
        Script(src="https://cdn.tailwindcss.com"),
    )
)

# Constants
path_to_storage = "storage/" # storage is in the root directory

# Initializations
logging.basicConfig(level=logging.INFO)
persona_manager = PersonaManager(path_to_storage)
State = AppState(path_to_storage)
#android_ops = AndroidOps()
#adb_manager = ADBImageManager(
#        adb_path="adb",
#        device_camera_folder="/sdcard/DCIM/Camera/",
#        local_folder=r"C:\Users\gurpr\Documents\Coding\Projects\FastHTML_Test\android\images_test"
#    )

key_event_js = """
document.addEventListener('keydown', function(event) {
    const key = event.key; // Get the key pressed

    // Set the key value dynamically in the hx-vals attribute
    document.getElementById('dynamic-element').setAttribute('hx-vals', JSON.stringify({ key: key }));

    // Trigger the custom HTMX event
    htmx.trigger(document.getElementById('dynamic-element'), 'customTrigger');
});
"""

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
    return Behaviours.open_queue()

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

@rt('/key-pressed')
def post(key: str):
    print(key)
    return Behaviours.key_pressed(key, State)
    


@rt('/update-nav-tab')
def get(page: str):
    right_page = ""
    print("page: " + page)
    if page in State.open_tabs:
        State.open_tabs.remove(page)
        right_page = Div(P("aaaaa"), Class="transition-all w-[0] h-full bg-zinc-700 items-center justify-center", Id="right_page", hx_swap_oob="true")
        print("removed" + page + "from open tabs" + str(State.open_tabs)) 
    else: 
        State.open_tabs.append(page)
        right_page = Div(P("aaaaa"), Class="transition-all flex w-full h-full bg-zinc-700 items-center justify-center", Id="right_page", hx_swap_oob="true")
        print("added" + page + "to open tabs" + str(State.open_tabs))
    return Navigation.navigation_bar(State), right_page

@rt('/')
def get():
    personas = persona_manager.load_personas_data()
    cards = [persona_card(persona['alias'], persona['thumbnail'], persona['path'] ) for persona in personas]
    return Div(
        pageContainer(Div(*cards, Class="flex flex-col w-full h-full gap-2 items-center justify-center p-2")),
        Class = "w-screen h-screen"
        )

@rt('/dashboard')
def get(path: str):
    persona = persona_manager.fetch_persona_data(path)
    return Div(
        Div(
            screensToggle(persona),
            Div(icon_button("https://cdn-icons-png.flaticon.com/32/10054/10054237.png"), 
                Class="w-8 h-8",
            ),
            Class="h-full flex flex-col items-center justify-between w-12 bg-zinc-100 p-2" 
        ),
        #Main editing area
        Div(
            Div(file_viewer(persona_manager.get_list_of_persona_album_paths(path)), Id="view-gallery", Class="h-full w-full flex items-center justify-center", Style="display: none"),
            Div('edit', Id="view-edit", Class="h-full w-full flex items-center justify-center overflow-hidden", Style="display: none"),
            Div('schedule', Id="view-schedule", Class="h-full w-full flex items-center justify-center", Style="display: none"),
            Div('accounts', Id="view-accounts", Class="h-full w-full flex items-center justify-center", Style="display: none"),
            Div('Dynamic Element', Id="dynamic-element", hx_post="/key-pressed", hx_trigger="customTrigger", hx_swap="innerHTML", Style="display: none"),
            Script(key_event_js),
            Class="h-full w-full flex items-center justify-center bg-zinc-50",
            id='dashboard'
        ),
        Class="w-screen h-screen flex flex-row overflow-hidden"
    )

@rt('/view-files')
def post(path: str):
    album_data = AlbumManager.load_album(path)
    State.set_current_album_path(path)
    State.set_current_album(album_data)
    State.current_album_path
    result = [GUICards.file_card(item) for item in album_data['items']]
    return Div(*result, Class="w-full h-full flex flex-wrap justify-center")

@rt('/add-selection')
def post(item_id: str):
    print(item_id)
    album_data = State.current_album
    matching_item = next((item for item in album_data['items'] if item['item_id'] == item_id), None)
    State.add_to_selected_items(matching_item)
    print(State.selected_items[0]['item_id'])
    return Div(f"Key pressed: {item_id}", Id="response")


@rt('/view-edit')
def post(item_id: str):
    album_data = State.current_album
    matching_item = next((item for item in album_data['items'] if item['item_id'] == item_id), None)
    State.set_current_item(matching_item)
    edit_view_swapper = GUIEditView.edit_view_swapper(matching_item)
    card_swapper = GUICards.file_card_active(matching_item)
    previous_card_swapper = GUICards.file_card_previous(State.previous_item)
    return  edit_view_swapper, card_swapper, previous_card_swapper

@app.post('/send-for-edit-test')
async def post():
    selected_items = State.selected_items
    print(selected_items)
    urls = [item['versions'][-1]['url'] for item in selected_items]
    # Call the asynchronous function and await it
    await send_images_from_urls(urls)
    return {"status": "Images sent successfully"}

@app.post('/soda-edit')
async def post():
    current_item = State.current_item
    url = current_item['versions'][-1]['url']
    og_name = OSFileManager.get_name_from_xpath(url)
    print(og_name)
    new_version = AlbumManager.create_version(current_item['item_id'], len(current_item['versions'])+1)
    await adb_manager.push_image(url)
    instructions_json = r'C:\Users\gurpr\Documents\Coding\Projects\FastHTML_Test\src\modules\android\instructions\soda_test_edit.json'
    instructions = JSONFileManager.load_json_as_dataobj_from_xpath(instructions_json)
    await android_ops.execute_steps(instructions)
    print(State.current_album_path)
    new_version['url'] = await adb_manager.pull_latest_image(State.current_album_path, new_version['item_version_id'])
    new_version['file_type'], new_version['extension'] = UtilityOps.get_file_type_and_extension(new_version['url'])
    State.current_item['versions'].append(new_version)
    State.current_album
    State.set_current_album(AlbumManager.update_item(State.current_item, State.current_album, State.current_album_path))
    await adb_manager.delete_latest_two_images()
    album_data = State.current_album
    matching_item = next((item for item in album_data['items'] if item['item_id'] == current_item['item_id']), None)
    State.set_current_item(matching_item)
    card_swapper = GUICards.file_card_active(matching_item)
    return card_swapper

@rt('/design-system')
def get():
    #album_data = AlbumManager.load_album(path) 
    #result = [GUICards.file_card(item) for item in album_data['items']]
    #return Div(*result, Class="w-full h-full flex flex-wrap justify-center")
    return Div()



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
    

