from fasthtml.fastapp import *
from fasthtml.common import *

class GUICards:

    @staticmethod
    def flag_indicator(flag):
        if flag == "unusable" : flag = "N"
        elif flag == "maybe" : flag = "M"
        elif flag == "best" : flag = "B"
        else: flag = None
        if flag is not None:
            return Div(
                Div( flag,
                    Class="text-xs font-semibold text-white rounded-full"
                    ),
                Class="w-6 h-6 flex items-center justify-center rounded-full cursor-pointer bg-zinc-300"
            )
        else: return None

    def status_indicator(status):
        if status == "edit" : status = "E"
        elif status == "ready" : status = "R"
        else: status = None
        if status is not None:
            return Div(
                Div( status,
                    Class="text-xs font-semibold text-white rounded-full"
                    ),
                Class="w-6 h-6 flex items-center justify-center rounded-full cursor-pointer bg-zinc-300"
            )
        else: return None
    
    @staticmethod
    def selection_indicator(selection_number, item_id=None):
        if selection_number is not None:
            return Div(
                Input(
                    type="checkbox",
                    hx_post="/add-selection",
                    hx_trigger="click",
                    hx_vals={"item_id": f"{item_id}"},
                    Class=(
                        "h-6 w-6 rounded-full border-2 border-white transition-colors "
                        "checked:bg-lightblue-500 checked:border-lightblue-500 "
                        "cursor-pointer opacity-0 checked:opacity-100 group-hover:opacity-100"
                    ),
                    id=f"checkbox_{selection_number}",  # Give it an ID to ensure uniqueness
                    name=f"checkbox_{selection_number}",  # Unique name for form submissions
                ),
                Div(
                    selection_number,
                    Class="text-xs font-semibold text-blue-500 rounded-full p-1"
                ),
                Class="flex items-center justify-center space-x-2"
            )
        else:
            return None

    
    
    # bg-[radial-gradient(circle,_transparent_97%,_black_100%)]

    @staticmethod
    def file_card(item):
        """Generates a file card for the latest version of an item."""
        # Access the latest version using the negative index
        latest_version = item['versions'][-1]
        image_url = latest_version['url']
        item_version_id = latest_version['item_version_id']
        
        # Return the Div structure as described
        return Div(
            Div(
                Img(
                    src=image_url, 
                    Class="h-full w-full object-contain object-center rounded-md", 
                    alt="Preview"
                ), 
                Class="relative h-36 p-1 rounded-md",
                hx_post="/view-edit",
                hx_trigger="click",
                hx_target="#view-edit",
                hx_swap="innerHTML",
                hx_vals={"item_id": f"{item['item_id']}"},
            ),
            Div(
                    Div(GUICards.flag_indicator(item['flag']), GUICards.status_indicator(latest_version['status']), Class="flex flex-row gap-1"),
                    Div(GUICards.selection_indicator("1", item['item_id']), Class="flex flex-row"),
                    Class="transition-all duration-100 flex flex-row justify-between w-full"
                ),
            Id=item_version_id,
            Class="relative group h-48 w-36 p-2 flex flex-col items-center justify-between rounded-lg bg-zinc-0 hover:bg-zinc-100",
        )
    
    @staticmethod
    def file_card_active(item):
        """Generates a file card for the latest version of an item."""
        # Access the latest version using the negative index
        latest_version = item['versions'][-1]
        image_url = latest_version['url']
        item_version_id = latest_version['item_version_id']
        
        # Return the Div structure as described
        return Div(
            Div(
                Img(
                    src=image_url, 
                    Class="h-full w-full object-contain object-center rounded-md", 
                    alt="Preview"
                ), 
                hx_post="/view-edit",
                hx_trigger="click",
                hx_target="#view-edit",
                hx_swap="innerHTML",
                hx_vals={"item_id": f"{item['item_id']}"},
                Class="relative h-36 p-1 rounded-md",
            ),
            Div(
                    Div(GUICards.flag_indicator(item['flag']), GUICards.status_indicator(latest_version['status']), Class="flex flex-row gap-1"),
                    Div(GUICards.selection_indicator("1"), Class="flex flex-row"),
                    Class="transition-all duration-1 flex flex-row justify-between w-full"
                ),
            Id=item_version_id,
            hx_swap_oob="true",
            Class="relative group h-48 w-36 p-2 flex flex-col items-center justify-between rounded-lg bg-zinc-200 hover:bg-zinc-100",
        )
    
    @staticmethod
    def file_card_previous(item):
        """Generates a file card for the latest version of an item."""
        # Access the latest version using the negative index
        latest_version = item['versions'][-1]
        image_url = latest_version['url']
        item_version_id = latest_version['item_version_id']
        
        # Return the Div structure as described
        return Div(
            Div(
                Img(
                    src=image_url, 
                    Class="h-full w-full object-contain object-center rounded-md", 
                    alt="Preview"
                ), 
                hx_post="/view-edit",
                hx_trigger="click",
                hx_target="#view-edit",
                hx_swap="innerHTML",
                hx_vals={"item_id": f"{item['item_id']}"},
                Class="relative h-36 p-1 rounded-md",
            ),
            Div(
                    Div(GUICards.flag_indicator(item['flag']), GUICards.status_indicator(latest_version['status']), Class="flex flex-row gap-1"),
                    Div(GUICards.selection_indicator("1"), Class="flex flex-row"),
                    Class="transition-all duration-1 flex flex-row justify-between w-full"
                ),
            Id=item_version_id,
            hx_swap_oob="true",
            Class="relative group h-48 w-36 p-2 flex flex-col items-center justify-between rounded-lg bg-zinc-0 hover:bg-zinc-100",
        )