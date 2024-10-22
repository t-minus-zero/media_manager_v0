from fasthtml.fastapp import *
from fasthtml.common import *
from src.modules.web_gui.structure import Structure


class Persona:

    @staticmethod
    def card(alias, thumbnail, path, sheet_id):
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
                hx_target="#main_page",
                hx_trigger="click",
                hx_vals={'alias': alias},
                onclick=f"closeBottomSheet('{sheet_id}')"
            ),
            Class="w-full h-12 max-w-[400px] mx-auto p-2 bg-zinc-900/50 rounded-full border border-zinc-700/50"
        )
    
    @staticmethod
    def persona_switcher(State, sheet_id):
        cards = [Persona.card(persona['alias'], persona['thumbnail'], persona['path'], sheet_id) for persona in State.personas_data]
        return Div(
            *cards,
            Class="w-full h-32 bg-zinc-800 flex flex-col items-center justify-center gap-2 p-2",
            Id="persona_switcher"
        )
    
    @staticmethod
    def persona_info(State):
        return Div(
            P(
                State.current_persona_data['alias'], 
                Class="text-zinc-100 text-lg font-semibold"
            ),
            P(
                State.current_persona_data['alias'], 
                Class="text-zinc-100 text-xs"
            ),
            Class="w-full h-16 flex flex-col items-start justify-center gap-1 p-2",
            Id="persona_info"
        )
