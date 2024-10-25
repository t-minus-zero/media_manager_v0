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