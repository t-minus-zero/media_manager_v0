from fasthtml.fastapp import *
from fasthtml.common import *
from src.modules.web_gui.icon_view import IconView
from src.modules.metadata_ops.album_ops import AlbumManager

class Edit:

    @staticmethod
    def view(State):

        item_data = State.current_item

        return Div(
            Div(
                Img(src=item_data['versions'][-1]['url'] , Class="w-full h-96 object-cover"),
                Class="w-full h-96 relative"
            ),
            Class="relative w-full h-full flex flex-col items-center justify-center overflow-hidden",
            Id="edit_view"
        )