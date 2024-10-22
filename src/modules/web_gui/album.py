from fasthtml.fastapp import *
from fasthtml.common import *
from src.modules.web_gui.icon_view import IconView
from src.modules.metadata_ops.album_ops import AlbumManager

class Album:

    @staticmethod
    def card(album_data):
        previews_url = AlbumManager.get_album_previews(album_data)
        previews = [
            Img(src=preview_url, Class="w-full h-full object-cover")  # Updated to use 'object-cover' to cover grid spaces
            for preview_url in previews_url
        ]
        print(previews_url)

        album_id = album_data['info']['album_id'] if album_data else "Nan"
        items_number = album_data['info']['total_items'] if album_data else "Nan"
        versions = album_data['info']['total_versions'] if album_data else "Nan"

        return Div(
            Div(
                *previews,
                Class="w-full h-full relative cursor-pointer grid grid-cols-2 grid-rows-2 gap-0",
                Id= f"{album_id}",
                hx_post="/open_album",
                hx_target="#main_page",
                hx_trigger="click",
                hx_vals={"album_id": f"{album_id}"}
            ),
            Div(
                P("Id: " + album_id, Class="text-zinc-100 text-xs"),
                P("Items: " + f"{items_number}", Class="text-zinc-100 text-xs"),
                P("Versions: " + f"{versions}", Class="text-zinc-100 text-xs"),
                Class="absolute bottom-1 w-full px-2 flex flex-row justify-between gap-2 text-zinc-300 text-xs"
            ),
            Class="relative w-full max-w-[400px] min-w-[200px] aspect-square flex flex-col items-center justify-center border border-zinc-800 hover:bg-zinc-800"
        )
    
    @staticmethod
    def grid(State):


        album_cards = [Album.card(album_data) for album_data in State.albums_data]

        return Div(
            *album_cards,
            Class="w-full grid gap-0 grid-cols-[repeat(auto-fit,minmax(200px,1fr))]",
            id="albums_grid",
        )
    
