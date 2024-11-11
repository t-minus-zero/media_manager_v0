from fasthtml.fastapp import *
from fasthtml.common import *
from src.modules.web_gui.item import Item
from src.modules.web_gui.icon_view import IconView

class Options:

    @staticmethod
    def automation_kiara():
        return Button(
            IconView.get_icon_view("out-arrow", "size-6 text-zinc-100"),
            Class="w-8 h-8 text-zinc-500 hover:text-zinc-100 rounded-full flex items-center justify-center cursor-pointer",
            Id="automation_button",
            hx_post="/start_automation",
            hx_trigger="click",
            hx_vals={"edit": "soda_test_edit"}
        )
    
    @staticmethod
    def add_edit_button():
        edit_name = "soda_test_edit"
        value = "edit value"
        return Button(
            P("Add Edit", Class="text-xs border border-zinc-100 rounded-md px-2 py-1"),
            Class="w-8 h-8 text-zinc-500 hover:text-zinc-100 rounded-full flex items-center justify-center cursor-pointer",
            Id="add-edit-button",
            hx_post="/add-edit",
            hx_target="#edit_view",
            hx_trigger="click",
            hx_vals={'target': 'current' , 'edit_name': edit_name, 'edit_value': value}
        )
    
    @staticmethod
    def send_to_queue_button():
        return Button(
            P("Send to Queue", Class="text-xs border border-zinc-100 rounded-md px-2 py-1"),
            Class="w-8 h-8 text-zinc-500 hover:text-zinc-100 rounded-full flex items-center justify-center cursor-pointer",
            Id="send-to-queue-button",
            hx_post="/send-to-queue",
            hx_trigger="click"
        )
    
    