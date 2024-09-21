from fasthtml.common import *
import os

def album_card(name, path, file_count):
    icon = "https://cdn-icons-png.flaticon.com/512/716/716784.png"
    print(path)
    return Div(
        Div(
            Div(Img(src=icon, Class="h-8", alt="Preview"), Class="h-full"),
            Div(P(name, Class="text-sm font-medium"), P(f"Files: {file_count}", Class="text-xs"), Class="flex flex-col items-left justify-center h-full pl-2"),
            Class= "w-full p-2 flex flex-row items-center justify-center rounded-lg hover:bg-zinc-100 cursor-pointer bg-zinc-0",
            hx_post="/view-files",
            hx_trigger="click",
            hx_vals={"path": f"{path}"},
            hx_target="#view-files",
            hx_swap="innerHTML",
        ),
    )

def file_viewer(album_paths_list):
    entries = album_paths_list

    def get_folder_info(folder_path):
        """Returns the folder name and the number of files inside the folder minus one."""
        files = os.listdir(folder_path)
        return len(files)
    cards = [
        album_card(
            "album_name", 
            album_path,
            get_folder_info(album_path)
        ) 
        for album_path in album_paths_list
    ]

    return Div(
        Div(
            Div(*cards, Id="view-albums", Class="flex flex-col gap-1 p-2 min-w-36 w-36 h-full border-zinc-200 border-r-1 overflow-y-scroll"),
            Div( 
                Id="view-files" , 
                Class="flex h-full w-full shrink overflow-y-scroll"
            ),
            Class="flex flex-row h-full w-full overflow-hidden"
        ),
        Class="flex flex-col w-full h-full"
    )