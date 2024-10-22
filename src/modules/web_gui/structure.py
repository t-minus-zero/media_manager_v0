from fasthtml.fastapp import *
from fasthtml.common import *

class Structure:

    def close_bottom_sheet():
        close_bottom_sheet = """
                function closeBottomSheet(sheetId) {
                    var sheetElement = document.getElementById(sheetId);
                    if (sheetElement) {
                    sheetElement.classList.remove('translate-y-0');
                    sheetElement.classList.add('translate-y-full');
                    }
                }
        """
        return close_bottom_sheet
    
    key_event_js = """
        document.addEventListener('keydown', function(event) {
            const key = event.key; // Get the key pressed

            // Set the key value dynamically in the hx-vals attribute
            document.getElementById('dynamic-element').setAttribute('hx-vals', JSON.stringify({ key: key }));

            // Trigger the custom HTMX event
            htmx.trigger(document.getElementById('dynamic-element'), 'customTrigger');
        });
        """

    def app_container(screens):

        app_container_classes= "w-screen h-screen bg-zinc-900 relative overflow-hidden flex flex-row"
        screen_container_classes= "transition-all relative h-full w-full flex flex-row items-center justify-center"

        return Div(
                Div(
                    *screens,
                    Class= screen_container_classes,
                    Id="screen-container",
                ),
                Div('Dynamic Element', Id="dynamic-element", hx_post="/key-pressed", hx_trigger="customTrigger", hx_swap="innerHTML", Class="w-0 h-0", Style="display: none"),
                Script(Structure.close_bottom_sheet()),
                Script(Structure.key_event_js),
                Class= app_container_classes,
                Id="app-container"
        )
    
    def floating_screen(screen_id, screen_content):

        floating_screen_classes =  "w-full h-full bg-zinc-900 absolute lg:relative z-30"
        content_container_classes = "relative w-full h-full flex flex-col items-center justify-start overflow-hidden"
        content_wrapper_classes = "relative w-full h-full flex flex-col items-center justify-start overflow-y-scroll overflow-x-hidden"

        return Div(
            Div( 
                Div(
                    *screen_content,
                    Class= content_wrapper_classes,
                    ),
                Structure.bottom_sheet(screen_id+"_bottom_sheet", P("Bottom Sheet Content"), sheet_open=False ),
                Class= content_container_classes
            ),
            Class= floating_screen_classes,
            Id= screen_id
        )

    def bottom_sheet(sheet_id, *sheet_content, sheet_open):

        bottom_sheet_classes = "w-full max-h-[80%] bottom-0 transition-all fixed z-30 grid max-w-96"
        bottom_sheet_classes += " translate-y-0" if sheet_open else " translate-y-full"
    
        return Div(
            Div(
                    Button(
                        "Done",
                        Class="w-full h-12 bg-zinc-700 text-blue-500",
                        onclick=f"closeBottomSheet('{sheet_id}')"
                    ),
                    *sheet_content,
                    Class = "w-full h-full flex flex-col items-start justify-center overflow-y-scroll overflow-x-hidden relative"
            ),
            Class= bottom_sheet_classes,
            Id= sheet_id
        )


    def grid_3_columns(left_col, center_col, right_col):
        return Div(
            Div(
                *left_col,
                Class="h-full flex flex-row items-center justify-start flex-grow gap-2"
            ),
            Div(
                *center_col,
                Class="h-full flex items-center justify-center flex-grow gap-2"
            ),
            Div(
                *right_col,
                Class="h-full flex flex-row items-center justify-end flex-grow gap-2"
            ),
            Class="w-full h-full flex flex-row p-2 items-start justify-center bg-zinc-900/90 backdrop-blur-md z-20 border-b border-zinc-700/50"
        )

    def sticky_top_navigation_bar(navigation_content):
         
         return Div(
            navigation_content,
            Class="sticky top-0 z-20 w-full"
         )

    def floating_navigation_bar(navigation_content):
         
        return Div(
            navigation_content,
            Class="fixed bottom-2 z-20"
        )