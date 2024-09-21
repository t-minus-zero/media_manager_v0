from fasthtml.common import *
from src.components.ui_design_system import profile, statStack

def persona_card(alias, img_url, persona_path):
    return Div(
        A(
            Div(
                Div(profile(img_url), Class="w-12 h-12 min-w-12 min-h-12"),
                P(alias, Class="w-full text-sm font-bold"),
                Div(
                    P("$XX.xxx", Class="text-lg text-zinc-300 font-bold text-zinc-700"),
                    Class="w-full flex flex-row items-center justify-end mr-2"
                ),
                Class="w-full flex flex-row items-center justify-center gap-2"
            ),
            Class="flex flex-col items-center justify-center gap-1 bg-zinc-50 hover:bg-zinc-100 rounded-full p-2",
            href=f"/dashboard/?path={persona_path}"
        ),
        Class="w-full flex flex-col space-y-4 overflow-hidden cursor-pointer"
    )