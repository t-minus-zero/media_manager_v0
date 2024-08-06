from fasthtml.fastapp import *
from fasthtml.common import *
from src.navigation import navigation
from src.file_viewer import file_viewer
from src.functions.folder_operations import create_new_folder
from src.modules.ffmpeg_processing.heic_to_jpg import convert_heic_to_jpg
from os.path import dirname, join

app, rt = fast_app(
    pico=False,
    hdrs=(
        Link(rel='stylesheet', href='https://fonts.googleapis.com/css?family=Roboto:400,700&display=swap', type='text/css'),
        Script(src="https://cdn.tailwindcss.com")
    )
)

def common_layout(content, current_path):
    navigation_menu = navigation(current_path)
    return Div(
        navigation_menu,
        content,
        Class="flex flex-col justify-between h-screen"
    )


@rt('/')
def get():
    current_path = "storage/projects"  # Default path to projects folder
    file_viewer_component = file_viewer(current_path)
    navigation_menu = navigation(current_path)
    return common_layout(file_viewer_component, current_path)

@rt('/files')
def get(path: str = ""):
    file_viewer_component = file_viewer(path)
    return common_layout(file_viewer_component, path)

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
    
serve()
