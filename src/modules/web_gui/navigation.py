from fasthtml.fastapp import *
from fasthtml.common import *
from src.modules.web_gui.icon_view import IconView

class Navigation:

    def icon_button(icon_name: str, icon_classes: str, button_classes="w-8 h-8 text-zinc-500 hover:text-zinc-100"):
        return Div(
            IconView.get_icon_view(icon_name, icon_classes),
            Class= button_classes + " rounded-full flex items-center flex hover:text-zinc-100 items-center justify-center cursor-pointer"
        )

    def persona_button(active=False):
        classes = "w-8 h-8 text-blue-500" if active else "w-8 h-8 text-zinc-500"
        return Div(
            Navigation.icon_button("profile-solid", "size-4", classes),
            Id="persona_button",
            hx_post="/toggle_profile",
            hx_target="#main_page",
            hx_trigger="click",
            hx_vals={"page": "persona"},
            hx_swap_oob="true"
        )

    def albums_button(active=False):
        classes = "w-8 h-8 text-blue-500" if active else "w-8 h-8 text-zinc-500"
        return Div(
            Navigation.icon_button("albums-solid", "size-4", classes),
            Id="albums_button",
            hx_post="/toggle_albums",
            hx_target="#main_page",
            hx_trigger="click",
            hx_vals={"page": "albums"},
            hx_swap_oob="true"
        )

    def queue_button(active=False):
        classes = "w-8 h-8 text-blue-500" if active else "w-8 h-8 text-zinc-500"
        swap = "delete" if active else "beforeend"
        target = "#queue_screen" if active else "#screen-container"
        return Div(
            Navigation.icon_button("bolt-solid", "size-4", classes),
            Id="queue_button",
            hx_post="/toggle_queue",
            hx_target= target,
            hx_swap= swap,
            hx_trigger="click",
            hx_vals={"page": "queue"},
            hx_swap_oob="true"
        )
    
    def schedule_button(active=False):
        classes = "w-8 h-8 text-blue-500" if active else "w-8 h-8 text-zinc-500"
        swap = "delete" if active else "beforeend"
        target = "#schedule_screen" if active else "#screen-container"
        return Div(
            Navigation.icon_button("calendar-solid", "size-4", classes),
            Id="schedule_button",
            hx_post="/toggle_schedule",
            hx_target= target,
            hx_swap= swap,
            hx_trigger="click",
            hx_vals={"page": "schedule"},
            hx_swap_oob="true"
        )
    
    def switch_button(sheet_id):
        target = "#" + sheet_id
        return Div(
            Navigation.icon_button("arrows-horizontal", "size-4", "w-8 h-8 text-zinc-500"),
            Id="switch_button",
            hx_post="/toggle_persona_switcher",
            hx_target= target,
            hx_swap="outerHTML",
            hx_trigger="click",
            hx_vals={"sheet_id": sheet_id},
            hx_swap_oob="true"
        )
    
    def persona_alias_button(alias, active=False):

        return Button(
            Div(
                P(alias, Class="text-zinc-100 text-md font-semibold"),
                Navigation.icon_button("vertical-chevrons", "size-4", "w-8 h-8 text-zinc-100"),
                Class="w-full flex flex-row items-center justify-start gap-2"
             ),
            Id="alias_button",
            hx_post="/toggle_persona_switcher",
            hx_target= "#main_screen_bottom_sheet",
            hx_swap="outerHTML",
            hx_trigger="click",
            hx_vals={"sheet_id": "main_screen_bottom_sheet"},
            Class=""
        )
    
    def persona_options(active=False):
        classes = "flex flex-row items-center justify-center overflow-hidden border-r border-zinc-700/50 h-6 transition-all"
        classes += " w-full" if active else " w-0"
        return Div(
            Navigation.persona_button(active),
            Div(
                Navigation.switch_button("main_screen_bottom_sheet"),
                Navigation.schedule_button(False),
                Class= classes,
                Id="persona_options",
                hx_swap_oob="true"
                ),
            Class="flex flex-row items-center justify-start"
        )

    def pages_tab(State):
        nav_buttons = []
        if 'profile' in State.open_screens:
            nav_buttons.append(Navigation.persona_options(True))
        else: nav_buttons.append(Navigation.persona_options(False))
            
        if 'albums' in State.open_screens:
            nav_buttons.append(Navigation.albums_button(True))
        else: nav_buttons.append(Navigation.albums_button(False))

        if 'queue' in State.open_screens:
            nav_buttons.append(Navigation.queue_button(True))
        else: nav_buttons.append(Navigation.queue_button(False))
        
        return Div(
            *nav_buttons,
            Class="flex flex-row items-center justify-start border border-zinc-700/50 bg-zinc-800/90 backdrop-blur-md rounded-full",
            Id="nav-tab",
            hx_swap_oob="true"
        )

    def filter_button():
        return Div(
            Navigation.icon_button("filter-solid", "size-4"),
            Class="flex flex-row items-center justify-start border border-zinc-700/50 bg-zinc-800/90 backdrop-blur-md rounded-full"
        )

    def back_to_albums_button():
        return Button(
            Navigation.icon_button("left-chevron", "size-4", "w-8 h-8 text-zinc-100"),
            Class="relative flex flex-row items-center justify-center",
            Id="back_to_albums_button",
            hx_post="/toggle_albums",
            hx_target="#main_page",
            hx_trigger="click",
            hx_vals={"page": "albums"}
        )

    def selection_tab():
        return Button(
            P("152", Class="text-blue-500 text-sm pl-2 font-semibold"),
            Navigation.icon_button("vertical-chevrons", "size-4"),
            Class="flex flex-row items-center justify-start border border-zinc-700/50 bg-zinc-800/90 backdrop-blur-md rounded-full"
        )
    
    def navigation_bar(State):
        return Div(
            Navigation.pages_tab(State),
            Class="w-full flex items-center justify-around text-zinc-100 max-w-64",
            Id="bottom-nav"
        )
    