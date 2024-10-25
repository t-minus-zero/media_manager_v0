from fasthtml.fastapp import *
from fasthtml.common import *
from src.modules.web_gui.structure import Structure

class Queue:

    @staticmethod
    def start_adb( ):

        return Button(
            P("Initialize KITT", Class="text-zinc-100 text-md font-semibold "),
            Class="border border-zinc-100 px-2 rounded-md text-zinc-500 hover:text-zinc-100 rounded-full flex items-center justify-center cursor-pointer",
            Id="start_adb_button",
            hx_post="/initialize-kitt",
            hx_target="#adb_status",
            hx_trigger="click",
            hx_vals={"edit": "automation_kiara"}
        )
    

    @staticmethod
    def payload_item(payload_item):
        procedures = [procedure['name'] for procedure in payload_item['procedures']]
        procedures_str = ', '.join(map(str, procedures))
        return Div(
                P(procedures_str, Class="text-zinc-100 text-xs"),
                P(payload_item['album_id'], Class="text-zinc-100 text-xs"),
                P(payload_item['album_url'], Class="text-zinc-100 text-xs"),
                P(payload_item['item_id'], Class="text-zinc-100 text-xs"),
                P(payload_item['version_url'], Class="text-zinc-100 text-xs"),
                P(payload_item['new_version_file_name'], Class="text-zinc-100 text-xs"),
            Class="w-full flex flex-col items-center justify-start p-2 border-b border-zinc-700/50",
        )
    
    @staticmethod
    def card(payload):

        pyload_items = [Queue.payload_item(payload_item) for payload_item in payload]
            
        return Div(
            *pyload_items,
            Class="w-full flex flex-col items-center justify-start p-2",
        )

    
    @staticmethod
    def view( State ):
        cards = [Queue.card(payload) for payload in State.queue_payloads]
        queue_screen = Structure.floating_screen("queue_screen", [
            Div(
                Div(
                    Div(
                        Queue.start_adb(), 
                        P("KITT sleeping", Class="text-zinc-100 text-xs", Id="adb_status"),
                        P("Updating this", Class="text-zinc-100 text-xs", Id="queue_status"),
                        Class="w-full h-12 flex flex-row items-center justify-between px-2 bg-zinc-900/90 border-b border-zinc-700 backdrop-blur-md"
                    ),
                    Class="w-full top-0 sticky z-30 overflow-hidden"
                ),
                *cards,
                Class="relative w-full h-full flex flex-col items-center justify-start overflow-y-scroll overflow-x-hidden", 
                Id="queue_page",         
            )])
        return queue_screen