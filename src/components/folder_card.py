from fasthtml.common import *
import os
import mimetypes

def folder_card(name, path, link):
    # Determine the type of the item (folder, file type)
    if os.path.isdir(path):
        icon = "https://cdn-icons-png.flaticon.com/512/716/716784.png"  # Placeholder folder icon
        type_display = "Folder"
    else:
        mimetype, _ = mimetypes.guess_type(path)
        if mimetype and ('image' in mimetype or 'video' in mimetype):
            icon = path  # Shows the image or video as a preview
            type_display = "Preview"
        else:
            icon = "https://cdn-icons-png.flaticon.com/512/337/337946.png"  # Placeholder file icon
            type_display = "File"

    # Setup card dimensions and styles
    card_style = "width: 200px; height: 300px; border: 1px solid gray; display: inline-block; margin: 10px; position: relative; cursor: pointer;"
    img_style = "width: 100%; height: 75%; object-fit: cover;" if type_display == "Preview" else "width: 60px; height: 60px; position: absolute; top: 10px; left: calc(50% - 30px);"
    text_style = "position: absolute; bottom: 10px; width: 100%; text-align: center;"

    return A(
        Div(
            Img(src=icon, style=img_style, alt=type_display),
            P(name, style=text_style),
            style=card_style + " overflow: hidden; background: white; border-radius: 8px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);"
        ),
        href=link
    )
