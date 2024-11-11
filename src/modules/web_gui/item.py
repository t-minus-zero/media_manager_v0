from fasthtml.fastapp import *
from fasthtml.common import *
from src.modules.web_gui.icon_view import IconView

class Item:

    def checkbox(checkbox_data, item_id):

        version_numbers = [version['version_number'] for version in checkbox_data['versions']]
        version_numbers_str = ','.join(map(str, version_numbers))

        checkbox_classes = "w-6 h-6 items-center justify-center rounded-full bg-zinc-500/0 border border-zinc-100 group-hover:flex"
        if checkbox_data['is_selected'] == True:
            checkbox_classes = "w-6 h-6 items-center justify-center rounded-full bg-blue-500/100 border-0 border-zinc-100 group-hover:flex"
        
        if not checkbox_data['selection_mode'] and not checkbox_data['is_current'] and not checkbox_data['is_selected']:
            checkbox_classes += " hidden"
        
        return Div(
                Button(
                    P(f"{checkbox_data['index']}", Class="text-zinc-100 text-xs"), 
                    Class = checkbox_classes,
                    hx_post="/add_remove_selected_item",
                    hx_trigger="click",
                    hx_vals={"item_id": item_id}
                ),
                Button(
                    Div(
                        version_numbers_str,
                         Class="border-2 border-zinc-200 text-zinc-200 rounded-md px-1 min-w-6 h-6 flex items-center justify-center text-xs font-semibold"
                        ),
                    Class="flex flex-row gap-1 items-center"
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

    def card_flag(item_id, flag):

        flag_icon = IconView.get_icon_view("flag-outline", "size-4 text-zinc-100")

        if flag == "maybe":
            flag_icon = IconView.get_icon_view("flag-solid", "size-4 text-yellow-500")
        elif flag == "no":
            flag_icon = IconView.get_icon_view("flag-solid", "size-4 text-red-500")
        elif flag == "yes":
            flag_icon = IconView.get_icon_view("flag-solid", "size-4 text-green-500")
        
        return Button(
            flag_icon,
            Class="w-4 h-4 flex items-center justify-center",
            id=f"flag_{item_id}",
            hx_post="/change-flag",
            hx_trigger="click",
            hx_vals={"item_id": item_id, "flag": "no"}
        )

    def card(item_data, State):

        checkbox_data = {
            "selection_mode" : State.selection_mode,
            "is_selected" : False,
            "is_current" : False,
            "versions" : [item_data['versions'][-1]] if item_data else [],
            "index" : "",
        }

        is_focus = False 
        target = "none"	
        if State.current_item['item-data'] and item_data:
            if item_data['item_id'] == State.current_item['item-data']['item_id']:
                checkbox_data['is_current'] = True
                is_focus = True 
            target = f"#item_{item_data['item_id']}"

        if any(item_data['item_id'] == item['item-data'].get('item_id') for item in State.selected_items):
            checkbox_data['is_selected'] = True
            checkbox_data['index'] = State.find_first_index_by_item_id_in_selected(item_data['item_id']) + 1
        
        swap_oob = "true" if is_focus else "false"

        card_classes = "group relative w-full max-w-[400px] min-w-[200px] aspect-square flex flex-col items-center justify-center border border-zinc-800 hover:bg-zinc-800"
        if is_focus: 
            card_classes += " border border-blue-500"

        image_classes = "w-full h-full object-contain" if item_data['versions'][-1]['status'] == "queued" else "w-full h-full object-contain"
        
        image_src = item_data['versions'][-1]['url'].replace('\\', '/') if item_data['versions'][-1]['url'] else "https://via.placeholder.com/150"

        return Div(
                Div(
                    Img(src= image_src , alt="Image 1", Class=image_classes),
                    Class="w-[90%] h-[80%] mx-auto relative cursor-pointer",
                    hx_post="/open-item-in-edit",
                    hx_trigger="click",
                    hx_target= "#screen-container",
                    hx_swap = "beforeend",
                    hx_vals={"item_id": item_data['item_id']}
                ),
                Div(
                    Item.checkbox(checkbox_data, item_id=item_data['item_id']),
                    Class="absolute top-1 left-1"
                ),
                Div(
                    Item.card_icons(), 
                    Item.card_flag(item_id=item_data['item_id'], flag = item_data['flag']),
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