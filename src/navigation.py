from fasthtml.common import Div, A


def navigation(current_path):
    
    return Div(
        Div(
            A("Create Folder", hx_get=f"/create-folder?path={current_path}", hx_target= "#folder-action-response", hx_swap="innerHTML",  Class="button hover:font-medium"),
            A("Merge", href="/upload-file", Class="button hover:font-medium"),
            A("HEIC to JPG", hx_get=f"/convert-heic-to-jpg?path={current_path}", hx_target= "#folder-action-response", hx_swap="innerHTML",  Class="button hover:font-medium"),
            A("Refresh", href="/", Class="button hover:font-medium"),
            Class="w-80 flex justify-around p-2 rounded-lg bg-zinc-100",
        ),
        Div(id="folder-action-response", Class="mt-2 hidden"),
        Class="fixed flex items-center justify-center z-10 bottom-4 w-full ",
    )