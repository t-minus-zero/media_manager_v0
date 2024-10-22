from fasthtml.fastapp import *
from fasthtml.common import *
from src.modules.web_gui.structure import Structure
from src.modules.web_gui.navigation import Navigation
from src.modules.web_gui.persona import Persona
from src.modules.web_gui.album import Album
from src.modules.web_gui.item import Item
from src.modules.web_gui.edit import Edit

class Behaviours:

    

    @staticmethod
    def initialize_app( State ):

        initial_page = Div(
            Persona.persona_info(State),
            Class="w-full h-full flex flex-col items-center justify-start",
            Id="main_page",
            hx_swap_oob="true"
        )

        navigation_bar = Structure.floating_navigation_bar(Navigation.navigation_bar(State))
        
        screens = [
            Structure.floating_screen("main_screen", [navigation_bar, initial_page])
        ]
        web_app = Structure.app_container(screens)
        return web_app
    
    @staticmethod
    def open_queue():
        queue_screen = Structure.floating_screen("queue_screen", [Div("Queue", Class="text-2xl text-zinc-500", Id="queue_page")])
        queue_button = Navigation.queue_button(True)
        return queue_screen, queue_button
    
    @staticmethod
    def close_queue():
        return Navigation.queue_button(False)
    
    @staticmethod
    def toggle_persona_switcher(State, sheet_id, is_open):
        sheet_content = Persona.persona_switcher(State, sheet_id)
        bottom_sheet = Structure.bottom_sheet(sheet_id, sheet_content, sheet_open=is_open)
        return bottom_sheet
    
    @staticmethod
    def toggle_persona(State):
        main_page = Persona.persona_info(State)
        updated_nav_button = Navigation.persona_options(True)
        updated_albums_button = Navigation.albums_button(False)
        return updated_nav_button, main_page, updated_albums_button
    
    @staticmethod
    def toggle_albums(State):
        main_page  = Album.grid(State)
        updated_nav_button = Navigation.albums_button(True)
        updated_persona_button = Navigation.persona_options(False)
        top_bar = Structure.grid_3_columns(
            [Navigation.persona_alias_button(alias=State.current_persona_data['alias'], active=True)],
            "",
            ""
            )
        top_navigation = Structure.sticky_top_navigation_bar(top_bar)
        return top_navigation, updated_nav_button, main_page, updated_persona_button, 


    @staticmethod
    def open_album(State):
        main_page = Item.grid(State)
        title = P(State.current_album_data['info']['album_id'], Class="text-md text-zinc-500 font-semibold")
        top_bar = Structure.grid_3_columns(
            [Navigation.back_to_albums_button(), title], 
            "",
            ""
            )
        top_navigation = Structure.sticky_top_navigation_bar(top_bar)
        return top_navigation, main_page

    @staticmethod
    def open_item_in_edit_1(State):
        current_item_card = Item.card(State.current_item, State)
        previous_item_card = None
        if State.previous_item:
            previous_item_card = Item.card(State.previous_item, State)
            previous_item_card.attrs['hx-swap-oob'] = 'true'
        current_item_card.attrs['hx-swap-oob'] = 'true'
        return current_item_card, previous_item_card
    
    @staticmethod
    def open_item_in_edit(State):
        current_item_card = Item.card(State.current_item, State)
        previous_item_card = None
        if State.previous_item:
            previous_item_card = Item.card(State.previous_item, State)
            previous_item_card.attrs['hx-swap-oob'] = 'true'
        current_item_card.attrs['hx-swap-oob'] = 'true'

        edit_view = Edit.view(State)
        if "edit" not in State.open_screens:
            edit_screen =  Structure.floating_screen("edit_screen", [edit_view])
            State.open_screens.append("edit")
            print("added edit screen to open screens")
            return edit_screen, current_item_card
        else:
            edit_view.attrs['hx-swap-oob'] = 'true'

        return current_item_card, previous_item_card, edit_view
            
    @staticmethod
    def key_pressed(key, State):
        # Step 1: Get the index of the current item in the album data
        current_index = None
        if State.current_item:
            for index, item in enumerate(State.current_album_data['items']):
                if item['item_id'] == State.current_item['item_id']:
                    current_index = index
                    break

        # Step 2: Handle the left or right arrow key press
        if key == "ArrowRight":
            # Update the previous item
            if State.current_item:
                State.previous_item = State.current_item

            # If we're at the last item, set index to 0
            if current_index is not None and current_index == len(State.current_album_data['items']) - 1:
                State.current_album_index = 0
            else:
                # Increment index if it's not the last item
                State.current_album_index = (current_index + 1) if current_index is not None else 0
            State.current_item = State.current_album_data['items'][State.current_album_index]
            return Behaviours.open_item_in_edit(State)

        elif key == "ArrowLeft":
            # Update the previous item
            if State.current_item:
                State.previous_item = State.current_item

            # If we're at the first item, set index to the last item
            if current_index is not None and current_index == 0:
                State.current_album_index = len(State.current_album_data['items']) - 1
            else:
                # Decrement index if it's not the first item
                State.current_album_index = (current_index - 1) if current_index is not None else len(State.current_album_data['items']) - 1
            State.current_item = State.current_album_data['items'][State.current_album_index]
            return Behaviours.open_item_in_edit(State)
        
        return Div("", id="dynamic-element", Class="w-0 h-0")