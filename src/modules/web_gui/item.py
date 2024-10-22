from fasthtml.fastapp import *
from fasthtml.common import *
from src.modules.web_gui.icon_view import IconView


class Item:

    def checkbox(checkbox_data):

        version_numbers = [version['version_number'] for version in checkbox_data['versions']]
        version_numbers_str = ','.join(map(str, version_numbers))

        checkbox_classes = "w-6 h-6 items-center justify-center rounded-full bg-zinc-500/0 border border-zinc-100"
        if checkbox_data['is_selected'] == True:
            checkbox_classes = "w-6 h-6 items-center justify-center rounded-full bg-blue-500/100 border-0 border-zinc-100"
        
        if checkbox_data['selection_mode'] == False:
            checkbox_classes += " hidden"
        
        return Div(
                Button(
                    P(f"{checkbox_data['index']}", Class="text-zinc-100 text-xs"), 
                    Class = checkbox_classes
                ),
                Button(
                    Div(
                        version_numbers_str,
                         Class="border-2 border-zinc-200 text-zinc-200 rounded-md px-1 min-w-6 h-6 flex items-center justify-center text-xs font-semibold"
                        ),
                    Class="flex flex-row gap-1 group items-center"
                ),
                Button(
                    IconView.get_icon_view("vertical-chevrons", "size-4"),
                    Class="relative w-4 h-6 flex items-center justify-center text-zinc-100"
                ),
            Class="relative flex flex-row items-center gap-1 p-1 backdrop-blur-md rounded-md"
        )

    def card_icons():
        tags_icons = []
        #if tag in tag list add to list this:
        tags_icons.append( Li( Button( IconView.get_icon_view("image-solid", "size-4 text-zinc-500") , Class="w-4 h-4 flex items-center justify-center"), Class="" ))
        
        return Ul(
            *tags_icons,
            Class="w-4 h-4 flex items-center justify-center"
        )

    def card_flag(flag):

        if flag == "none":
            flag = IconView.get_icon_view("flag-solid", "size-4 text-zinc-300")
        elif flag == "maybe":
            flag = IconView.get_icon_view("flag-solid", "size-4 text-yellow-500")
        elif flag == "no":
            flag = IconView.get_icon_view("flag-solid", "size-4 text-red-500")
        elif flag == "yes":
            flag = IconView.get_icon_view("flag-solid", "size-4 text-green-500")
        
        return Button(
            flag,
            Class="w-4 h-4 flex items-center justify-center"
        )

    def card(item_data, State):

        checkbox_data = {
            "selection_mode" : State.selection_mode,
            "is_selected" : False,
            "versions" : [item_data['versions'][-1]] if item_data else [],
            "index" : "",
        }

        for item in State.selected_items:

            if item['item_id'] == item_data['item_id']:
                checkbox_data['is_selected'] = False
                checkbox_data['versions'].append(item['version'])

        is_focus = False 
        if State.current_item:
            if State.current_item['item_id'] == item_data['item_id']:
                is_focus = True 
        swap_oob = "true" if is_focus else "false"

        card_classes = "relative w-full max-w-[400px] min-w-[200px] aspect-square flex flex-col items-center justify-center border border-zinc-800 hover:bg-zinc-800"
        if is_focus: 
            card_classes += " border border-blue-500"

        target = f"#item_{item_data['item_id']}"

        return Div(
                Div(
                    Img(src= item_data['versions'][-1]['url'] , alt="Image 1", Class="w-full h-full object-contain"),
                    Class="w-[90%] h-[80%] mx-auto relative cursor-pointer",
                    hx_post="/open-item-in-edit",
                    hx_trigger="click",
                    hx_target= "#screen-container",
                    hx_swap = "beforeend",
                    hx_vals={"item_id": item_data['item_id']}
                ),
                Div(
                    Item.checkbox(checkbox_data),
                    Class="absolute top-1 left-1"
                ),
                Div(
                    Item.card_icons(), Item.card_flag(flag = item_data['flag']),
                    Class="absolute bottom-1 w-full px-2  flex flex-row justify-between gap-2 text-zinc-300 text-xs"
                ),
            id=f"item_{item_data['item_id']}",
            Class= card_classes
        )


    def grid(State):

        item_cards = [Item.card(item_data, State) for item_data in State.current_album_data['items']]

        return Div(
            *item_cards,
            Class="w-full grid gap-0 grid-cols-[repeat(auto-fit,minmax(200px,1fr))]",
            id="items_grid",
        )