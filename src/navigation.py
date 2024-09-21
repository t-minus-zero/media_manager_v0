from fasthtml.common import Div, A, Img
from src.components.ui_design_system import icon_button, profile

def iconButton(button_text, button_icon):

    return Div(
        Div(
            Div(
                Img(src=button_icon, Class="w-full h-full"), 
                Class="button w-6 h-6"
                ),
            A(button_text),
            Class="flex flex-row items-center justify-center gap-x-2 w-full",
        ),
        Class="flex bg-zinc-100 p-2 rounded-lg hover:bg-zinc-200",
    )

def navigation(current_path):
    
    buttonIcon = "https://cdn-icons-png.flaticon.com/512/2549/2549900.png"

    return Div(
        Div(
            A(iconButton("", buttonIcon), href="/"),
            A(iconButton("Kiara", buttonIcon), href="/upload-file"),
            Div("/", Class="text-xl p-1 text-zinc-300"),
            A("Create Folder", hx_get=f"/create-folder?path={current_path}", hx_target= "#folder-action-response", hx_swap="innerHTML",  Class="button hover:font-medium"),
            A("Merge", href="/upload-file", Class="button hover:font-medium"),
            A("HEIC to JPG", hx_get=f"/convert-heic-to-jpg?path={current_path}", hx_target= "#folder-action-response", hx_swap="innerHTML",  Class="button hover:font-medium"),
            A("Open", hx_get=f"/convert-heic-to-jpg?path={current_path}", hx_target= "#folder-action-response", hx_swap="innerHTML",  Class="button hover:font-medium"),
            A("Refresh", href="/", Class="button hover:font-medium"),
            Class="flex justify-around p-2 rounded-lg bg-zinc-100",
        ),
        Div(id="folder-action-response", Class="mt-2 hidden"),
        Class="fixed flex items-center justify-center z-10 bottom-4 w-full ",
    )


def screensToggle(persona):
    def togglerJS(view):
        return f"""
                    var x = document.getElementById('view-{view}');
                    if (x.style.display === 'none' || x.style.display === '') {{
                        x.style.display = 'block';
                    }} else {{
                        x.style.display = 'none';
                    }}
                """

    return Div(
        A(icon_button("https://cdn-icons-png.flaticon.com/32/10054/10054600.png"),Class="w-8 h-8", href=f"/"),
        A(profile(persona['picture']), Class="w-6 h-6 min-w-6 min-h-6", href="/"),
        Div("",Class="w-full border-solid border-b-2 border-zinc-200 w-8 h-2"),
        Div(icon_button("https://cdn-icons-png.flaticon.com/32/10054/10054237.png"), 
            Class="w-8 h-8",
            onclick = togglerJS("gallery")
        ),
        Div(icon_button("https://cdn-icons-png.flaticon.com/32/10054/10054249.png"),
            Class="w-8 h-8",
            onclick = togglerJS("edit")
            ),
        Div(icon_button("https://cdn-icons-png.flaticon.com/32/9307/9307921.png",),
            Class="w-8 h-8",
            onclick = togglerJS("schedule")
            ),
        Div(icon_button("https://cdn-icons-png.flaticon.com/32/10317/10317509.png"),
            Class="w-8 h-8",
            onclick = togglerJS("accounts")
            ),
        Class="flex flex-col items-center justify-center w-full gap-2" 
    )
