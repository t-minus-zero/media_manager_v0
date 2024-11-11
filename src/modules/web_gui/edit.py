from fasthtml.fastapp import *
from fasthtml.common import *
from src.modules.web_gui.item import Item
from src.modules.web_gui.icon_view import IconView
from time import time

class Edit:

    @staticmethod
    def options():

        options_icon = IconView.get_icon_view("dots-vertical", "size-6 text-zinc-100")

        return Button(
            options_icon,
            Class="w-8 h-8 text-zinc-500 hover:text-zinc-100 rounded-full flex items-center justify-center cursor-pointer",
            Id="edit_options_button",
            hx_post="/toggle_edit_options",
            hx_target="#edit_screen_bottom_sheet",
            hx_swap="outerHTML",
            hx_trigger="click",
            hx_vals={"sheet_id": "edit_screen_bottom_sheet"}
        )
    
    def close_button():
        target = "#edit_screen"
        return Button(
            IconView.get_icon_view("x", "size-6 text-zinc-100"),
            Class="w-8 h-8 flex items-center justify-center",
            Id="close-edit-button",
            hx_post="/close_edit",
            hx_target= target,
            hx_swap= "delete",
            hx_trigger="click",
            hx_vals={"page": "edit"}
        )


    @staticmethod
    def menu(State):
        
        versions_count = len(State.current_item['item-data']['versions'])
        current_version = State.current_item['item-data']['versions'][State.current_item['version-index']]['version_number']
        flag_icon = Item.card_flag(State.current_item['item-data']['item_id'], State)

        return Div(
            Edit.close_button(),
            Div(
                f"{current_version}/{versions_count}", 
                Class="text-white text-xs w-6 h-6 border border-zinc-100 rounded-md flex items-center justify-center font-semibold text-md",
                Id = "version-index"
            ),
            flag_icon,
            Edit.options(), 
            Class = "flex flex-col items-center justify-center gap-2",
        )
    

    @staticmethod
    def preview(item_data, version):
        
        img_class = "w-full h-full object-contain"
        if item_data['versions'][version]['status'] == "queued":
            img_class = "w-full h-full object-contain opacity-66"
        img_url = item_data['versions'][version]['url'].replace("\\", "/")
        img_url += f"?v={int(time())}" # Add a timestamp to the image URL to prevent caching andforcing reload
        print("Image URL of version:", img_url)
        if not img_url:
            img_url = "https://via.placeholder.com/150" 
        return Div(
                Img(src=img_url , Class=img_class),
                Class="w-full h-full relative",
                Id = "edit_preview"
            )


    @staticmethod
    def view(State):

        item_data = State.current_item['item-data']
        menu = [Edit.menu(State)]

        return Div(
            Edit.preview(State.current_item['item-data'] , State.current_item['version-index']),
            Div(
                *menu,
                Class= "absolute right-2 z-30"
            ),
            Class="relative w-full h-full flex flex-col items-center justify-center overflow-hidden",
            Id="edit_view"
        )
    

    @staticmethod
    def info(State):
        item_data = State.current_item['item-data']
        version = State.current_item['version-index']
        
        current_edits = []
        for edit in item_data['versions'][version]['edits']:
            current_edits.append(
                Div(
                    Div(
                        P(f"{edit['name']}", Class="text-zinc-100 text-xs"),
                        P(f"{edit['status']}", Class="text-zinc-100 text-xs"),
                        Class="w-full flex flex-row items-center justify-between gap-2 p-2"
                    ),
                    Class="w-full flex flex-col items-center justify-start gap-2"
                )
            )

        return Div(
            *current_edits,
            Class="w-full flex flex-col items-center justify-start gap-2",
            Id="edit_info"
        )