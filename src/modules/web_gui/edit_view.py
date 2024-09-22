from fasthtml.fastapp import *
from fasthtml.common import *

class GUIEditView:

    @staticmethod
    def edit_view_swapper(item):
        image_url = item['versions'][-1]['url']
        return Div(
                    Div(
                        Img(
                            src=image_url, 
                            Class="h-full rounded-md", 
                            alt="Preview"
                        ), 
                        Class="flex h-full w-full items-center justify-center"
                    ),
                    Class= "h-full w-full p-2 flex items-center justify-center",
                    #hx_swap_oob="true"
                ),

