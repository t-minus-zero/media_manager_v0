from fasthtml.common import *
import os
from src.components.folder_card import folder_card

def file_viewer(current_path):
    if not current_path or current_path == "/":
        current_path = "storage/projects"  # Default path to projects folder
    
    entries = os.listdir(current_path)
    cards = [folder_card(name, os.path.join(current_path, name), f"/files?path={os.path.join(current_path, name)}") for name in entries]

    parent_path = os.path.dirname(current_path)
    back_link = A("Back", href=f"/files?path={parent_path}", Class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded") if current_path != "storage/projects" else ""

    return Div(
        Div('Current Directory:', Class="text-xl font-bold p-4"),
        Div(back_link, id='back', Class="p-2"),
        Div(*cards, Class="flex flex-wrap justify-around", style="padding: 10px;"),
        Class="flex flex-col space-y-4"
    )
