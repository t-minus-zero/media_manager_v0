from fasthtml.fastapp import *
from fasthtml.common import *
from src.modules.local_ops.json_ops import JSONFileManager
from src.modules.local_ops.os_ops import OSFileManager
import logging

class PageProfile:

    @staticmethod
    def persona_card(alias, thumbnail, path):
        return Div(
            Div(
                Img(
                    src=thumbnail, 
                    Class="h-12 w-12 object-contain object-center rounded-full", 
                    alt=f"{alias} Profile Picture",
                ),
                P(
                    alias, 
                    Class="text-zinc-100 text-md font-semibold"
                ),
                Class="w-full h-full flex flex-row items-center justify-start gap-2 cursor-pointer",
                hx_post="/change_persona",
                hx_target="#profile-indicator",
                hx_trigger="click",
                hx_vals={'alias': alias}
            ),
            Class="w-full h-12 max-w-[400px] mx-auto p-2 bg-zinc-900/50 rounded-full border border-zinc-700/50"
        )

    @staticmethod
    def initial_page(state_manager):
        personas_data = state_manager.personas_data
        cards = [PageProfile.persona_card(persona['alias'], persona['thumbnail'], persona['path']) for persona in personas_data]

        return Div(
            P("Profile page for " + state_manager.current_persona_data['alias'], Id="profile-indicator", hx_swap_oob="true"),
            *cards,
            Class="w-full h-full flex flex-col items-center justify-start gap-2 p-2",
            Id="main_page",
            hx_swap_oob="true"
        )
    


