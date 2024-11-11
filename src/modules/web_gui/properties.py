from fasthtml.fastapp import *
from fasthtml.common import *
from src.modules.web_gui.structure import Structure
from src.modules.web_gui.icon_view import IconView

class Properties:

    @staticmethod
    def header(text):
        return Div(
            P(f"{text}", Class="text-sm font-semibold text-zinc-400"),
            Class="w-full p-2 flex items-center justify-start",
        )
    
    @staticmethod
    def footer(text):
        return Div(
            P(f"{text}", Class="text-xs text-zinc-400"),
            Class="w-full p-2 flex items-center justify-start",
        )
    
    @staticmethod
    def container(header_text, content, footer_text):

        header_content = Properties.header(header_text) if header_text else ""
        footer_content = Properties.footer(footer_text) if footer_text else ""

        return Div(
            header_content,
            Div(
                *content,
                Class="w-full flex flex-col items-start bg-zinc-800/90 backdrop-blur-md rounded-lg shadow-md text-zinc-50"
            ),
            footer_content,
            Class= "w-full flex flex-col items-start justify-start px-2"
        )
    
    @staticmethod
    def item(icon, label, sublabel, action, right):

        icon_element = IconView.get_icon_view(icon, "size-6 text-zinc-100") if icon else ""
        label_element = P(f"{label}", Class="text-xs text-zinc-100") if label else ""
        sublabel_element = P(f"{sublabel}", Class="text-xs text-zinc-400") if sublabel else ""
        right_section_content = right if right else []

        result =  Div(
            Div( # Icon Section
                    icon_element,
                    Class="h-full flex items-center justify-center pl-2"
                ),
            Div(
                Div( # Left Section
                    Div(
                        label_element,
                        sublabel_element,
                        Class="flex flex-col gap-1 items-center justify-start"
                    ),
                    Class="w-full flex items-center",
                    hx_post= action['post'] if action else "",
                    hx_target= action['target'] if action else "",
                    hx_trigger= action['trigger'] if action else "",
                    hx_vals= action['vals'] if action else ""
                ),
                Div( # Right Section
                    *right_section_content,
                    Class="flex items-center"
                ),
                Class="w-full flex items-center justify-between gap-2 border-b border-zinc-700 pr-2"
            ),
            Class="w-full flex items-center justify-start gap-2 p-1"
        )
    
        return result
    
    @staticmethod
    def text_button(label, action):
        return Button(
            f"{label}",
            Class="w-full flex items-center justify-center gap-2 text-xs text-blue-500 p-1",
            hx_post= action['post'],
            hx_target= action['target'],
            hx_trigger= action['trigger'],
            hx_vals= action['vals']
        )
    
    @staticmethod
    def media_grid(images):
        images_list = []
        for image, index in images:
            if index < 7:
                images_list.append(
                    Div(
                        Img(src=image['url'], Class="w-full h-full object-cover"),
                        Class="overflow-hidden"
                    )
                )
        return Div(
            *images_list,
            Class="grid grid-cols-4 grid-rows-2 gap-2 p-2"
        )
    
    @staticmethod
    def back_button():
        return Button(
            IconView.get_icon_view("left-chevron", "size-6 text-zinc-400"),
            P("Back", Class="text-zinc-400 text-xs"),
            Class="bg-zinc-700 text-blue-500 text-sm rounded-lg focus:outline-none"
        )
    
    @staticmethod
    def menu(left, center, right):
        back_button = Properties.back_button()
        header = P("Page Title", Class="text-zinc-100 text-sm font-semibold")
        right_menu = []  # *right_menu_actions
        Menu = Structure.sticky_top_navigation_bar(
                Div(
                    Structure.grid_3_columns(*left, *center, *right),
                    Class="w-full bg-zinc-900/90 backdrop-blur-md border-b border-zinc-700/50"
                )
            )
        return Menu

    @staticmethod
    def view(State):

        Menu = Properties.menu()
        Content = []
        
        return Div(
            Menu,
            Div(
                *Content,
                Class="w-full flex flex-col items-center justify-start gap-4 px-2"
            ),
            Class = "w-full flex flex-col items-center justify-start"
        )
