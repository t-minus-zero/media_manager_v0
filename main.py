from fasthtml.fastapp import *
from fasthtml.common import *
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

# Global state
personas = [] #get_personas(path_to_storage) # load_personas()

# Dashboard state
prev_album = None # {'path':''} # path to the previous album and it's metadata
album = None # {'path':''} # path to the current album and it's metadata
file = None # {versionId: '', 'path':'', 'metadata':''} # path to the current file and it's metadata
prev_selections = None
selections = None #[{versionId: '', 'path':'', 'metadata':''}] # list of selected files and their metadata


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
    #files = os.listdir(path)
    #result = [file_card(file, os.path.join(path, file)) for file in files]
    album_data = AlbumManager.load_album(path)
    result = [file_card(item['versions'][0]['name'], item['versions'][0]['url']) for item in album_data['items']]
    return Div(
                *result,
                Class="w-full flex flex-wrap justify-center",
                #hx_swap_oob="true"
            )

@rt('/view-edit')
def post(path: str, name:str):
    return  Div(
                Div(Img(src=path, Class="h-full rounded-md", alt="Preview"), Class="flex h-full w-full items-center justify-center"),
                Class= "h-full w-full p-2 flex items-center justify-center",
            ), Div(
            Div(Img(src=path, Class="h-full rounded-md hover:scale-150 transition-all ease-in-out duration-150", alt="Preview"), Class="h-4/5 p-1"),
            Div(P(name, Class="text-xs text-zinc-300"), Class="flex flex-col items-center justify-center h-1/5"),
            Id = name,
            Class= "h-48 w-36 p-2 flex flex-col items-center justify-center rounded-lg bg-zinc-300 hover:bg-zinc-100 cursor-pointer",
            hx_post="/view-edit",
            hx_trigger="click",
            hx_vals={"path": path, "name" : name},
            hx_target="#view-edit",
            hx_swap="innerHTML",
            hx_swap_oob="true"
        )

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
    

