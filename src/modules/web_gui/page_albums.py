from fasthtml.fastapp import *
from fasthtml.common import *
from src.modules.web_gui.item import Item

class PageAlbums:

    @staticmethod
    def initial_page(state_manager):

        return Div(
            P(state_manager.current_persona_data['alias'], Id="profile-indicator", Class="text-zinc-100 text-md font-semibold"),
            Item.grid(),
            Class="w-full flex flex-col items-center justify-start gap-2 p-2",
            Id="main_page",
            hx_swap_oob="true"
        )
    

    
