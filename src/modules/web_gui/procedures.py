from fasthtml.fastapp import *
from fasthtml.common import *
from src.modules.web_gui.icon_view import IconView
from src.modules.web_gui.structure import Structure

class Procedure:

    @staticmethod
    def card(procedure):
        instructions_number = len(procedure['steps'])

        edit_name = procedure['info']['name']
        value = "edit value"

        left_col = [
            Div(
                    P(procedure['info']['name'] , Class="text-zinc-100 text-sm font-semibold"),
                    P(f"{instructions_number} Instructions", Class="h-full text-zinc-100 text-xs"),
                    Class="flex flex-col gap-1 items-start justify-center"
                ),
            ]
        center_col = []
        right_col = [
                    Button(
                        "Test", 
                        Class="text-zinc-100 text-xs bg-zinc-700 rounded-md flex items-center justify-center p-2",
                        hx_post="/run-procedure",
                        hx_target="#queue_page",
                        hx_trigger="click",
                        hx_vals={"procedure_name": procedure['info']['name']}
                    ),
                    Button(
                        "Add to queue", 
                        Class="text-zinc-100 text-xs bg-zinc-700 rounded-md flex items-center justify-center p-2",
                        hx_post="/add-edit",
                        hx_target="#queue_page",
                        hx_trigger="click",
                        hx_vals={'target': 'current' , 'edit_name': edit_name, 'edit_value': "value"}
                    )
            ]

        return Div(
            Structure.grid_3_columns(left_col, center_col, right_col),
            Class="flex flex-row gap-2 items-start justify-center w-full overflow-hidden rounded-md p-2",
        )
    
    @staticmethod
    def send_to_queue_button():
        return Button(
            "Send to queue", 
            Class="text-zinc-100 text-xs bg-zinc-700 rounded-md flex items-center justify-center p-2",
            hx_post="/send-to-queue",
            hx_target="#queue_page",
            hx_trigger="click",
        )

    @staticmethod
    def group(title):
        return Div(
            Div(
                P(title, Class="text-zinc-100 text-sm font-semibold"),
                IconView.get_icon_view("left-chevron", "size-6 text-zinc-100"),
                Class="w-full bg-zinc-800 rounded-md p-2 flex flex-row items-center justify-between gap-2",
            ),
            Class="w-full flex flex-col items-center justify-start",
            hx_post="/update-procedures",
            hx_target="#procedures_view",
            hx_trigger="click",
            hx_vals={"app_name": title}
        )
    
    @staticmethod
    def menu(current_page):
        left_col = [Div(
            IconView.get_icon_view("left-chevron", "size-6 text-zinc-100"), 
            Class="flex flex-row items-center justify-center",
            hx_post="/update-procedures",
            hx_target="#procedures_view",
            hx_trigger="click",
            hx_vals={"app_name": "procedures"}
        )]
        center_col = [Div(P(f"{current_page}", Class="text-zinc-100 text-lg font-semibold"), Class="flex flex-row items-center justify-center")]
        right_col = [Div(IconView.get_icon_view("x", "size-6 text-zinc-100"), Class="flex flex-row items-center justify-center")]
        menu = Structure.grid_3_columns(left_col, center_col, right_col)
        return Structure.sticky_top_navigation_bar(menu)
        

    @staticmethod
    def view(State, app_name):

        page_content = []
        if app_name == "procedures":
            unique_apps = {procedure['info']['app'] for procedure in State.procedures}
            page_content = [Procedure.group(app) for app in unique_apps]
        else:
            page_content = [Procedure.card(procedure) for procedure in State.procedures if procedure['info']['app'] == app_name]
        
        menu = Procedure.menu(app_name)  
    
        return Div(
            menu,
            Div(
                *page_content,
                Class = "w-full h-full flex flex-col items-center justify-start gap-2 overflow-y-scroll overflow-x-hidden"
                ),
            Class="relative w-full max-w-96 flex flex-col items-center justify-start gap-2 overflow-hidden",
            Id="procedures_view"
        )
    