from fasthtml.fastapp import *
from fasthtml.common import *
from src.modules.web_gui.item import Item
from src.modules.web_gui.icon_view import IconView

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
        
        versions_count = len(State.current_item['versions'])
        flag_icon = Item.card_flag(State.current_item['item_id'], State)

        return Div(
            Edit.close_button(),
            Div(
                f"{versions_count}", 
                Class="text-white text-xs w-6 h-6 border border-zinc-100 rounded-md flex items-center justify-center font-semibold text-md"
            ),
            flag_icon,
            Edit.options(), 
            Class = "flex flex-col items-center justify-center gap-2",
        )
    

    @staticmethod
    def view(State):

        item_data = State.current_item
        menu = [Edit.menu(State)]

        return Div(
            Div(
                Img(src=item_data['versions'][-1]['url'] , Class="w-full h-full object-contain"),
                Class="w-full h-full relative"
            ),
            Div(
                *menu,
                Class= "absolute right-2 z-30"
            ),
            Class="relative w-full h-full flex flex-col items-center justify-center overflow-hidden",
            Id="edit_view"
        )