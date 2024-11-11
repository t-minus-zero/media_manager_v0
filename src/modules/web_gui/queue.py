from fasthtml.fastapp import *
from fasthtml.common import *
from src.modules.web_gui.structure import Structure
from datetime import datetime

class Queue:

    @staticmethod
    def start_adb( ):

        return Button(
            P("Initialize KITT", Class="text-zinc-100 text-md font-semibold "),
        )
    

    @staticmethod
    def payload_item(payload_item):
        return Div(
            P(f"Pyload Id: {payload_item['info']['payload-id']}", Class="text-zinc-100 text-xs"),
            P(f"Status: {payload_item['info']['status']}", Class="text-zinc-100 text-xs"),
            P(f"Current job: {payload_item['info']['job-index']}", Class="text-zinc-100 text-xs"),
            P(f"Number of jobs: {payload_item['info']['job-count']}", Class="text-zinc-100 text-xs"),
            Class="w-full flex flex-col items-center justify-start p-2 border-b border-zinc-800",
        )
    
    @staticmethod
    def card(payload):

        pyload_item = Queue.payload_item(payload)
            
        return Div(
            pyload_item,
            Class="w-full flex flex-col items-center justify-start p-2",
        )

    
    @staticmethod
    def view( State ):
        cards = [Queue.card(payload) for payload in State.queue_payloads]
        current_time = datetime.now().strftime("%M:%S")
        queue_screen = Structure.floating_screen("queue_screen", [
            Div(
                Div(
                    Div(
                        P("KITT sleeping", Class="text-zinc-100 text-xs", Id="adb_status"),
                        P(current_time, Class="text-zinc-100 text-xs", Id="queue_status"),
                        Class="w-full h-12 flex flex-row items-center justify-between px-2 bg-zinc-900/90 border-b border-zinc-700 backdrop-blur-md"
                    ),
                    Class="w-full top-0 sticky z-30 overflow-hidden"
                ),
                *cards,
                Class="relative w-full h-full flex flex-col items-center justify-start overflow-y-scroll overflow-x-hidden", 
                Id="queue_page",         
            )])
        return queue_screen