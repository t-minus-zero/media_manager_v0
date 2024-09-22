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
from src.modules.metadata_ops.persona_ops import PersonaManager
from src.modules.metadata_ops.album_ops import AlbumManager
from src.modules.web_gui.file_card import GUICards
from src.modules.web_gui.GUIState import StateManager
from src.modules.web_gui.edit_view import GUIEditView
from src.modules.telegram_bot.telegram_test import send_images_from_urls

app, rt = fast_app(
    pico=False,
    hdrs=(
        Link(rel='stylesheet', href='https://fonts.googleapis.com/css?family=Roboto:400,700&display=swap', type='text/css'),
        Script(src="https://cdn.tailwindcss.com")
    )
)

# Constants
path_to_storage = "storage/" # storage is in the root directory

# Initializations
logging.basicConfig(level=logging.INFO)
persona_manager = PersonaManager(path_to_storage)
state_manager = StateManager(path_to_storage)

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
            Class="h-full w-full flex items-center justify-center bg-zinc-50",
            id='dashboard'
        ),
        Class="w-screen h-screen flex flex-row overflow-hidden"
    )

@rt('/view-files')
def post(path: str):
    album_data = AlbumManager.load_album(path) 
    state_manager.set_current_album(album_data)
    result = [GUICards.file_card(item) for item in album_data['items']]
    return Div(*result, Class="w-full h-full flex flex-wrap justify-center")

@rt('/add-selection')
def post(item_id: str):
    print(item_id)
    album_data = state_manager.current_album
    matching_item = next((item for item in album_data['items'] if item['item_id'] == item_id), None)
    state_manager.add_to_selected_items(matching_item)
    print(state_manager.selected_items[0]['item_id'])
    return Div(f"Key pressed: {item_id}", Id="response")


@rt('/view-edit')
def post(item_id: str):
    album_data = state_manager.current_album
    matching_item = next((item for item in album_data['items'] if item['item_id'] == item_id), None)
    state_manager.set_current_item(matching_item)
    edit_view_swapper = GUIEditView.edit_view_swapper(matching_item)
    card_swapper = GUICards.file_card_active(matching_item)
    previous_card_swapper = GUICards.file_card_previous(state_manager.previous_item)
    return  edit_view_swapper, card_swapper, previous_card_swapper

@app.post('/send-for-edit-test')
async def post():
    selected_items = state_manager.selected_items
    print(selected_items)
    urls = [item['versions'][-1]['url'] for item in selected_items]
    # Call the asynchronous function and await it
    await send_images_from_urls(urls)
    return {"status": "Images sent successfully"}

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
    

