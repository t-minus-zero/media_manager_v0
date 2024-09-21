from fasthtml.common import *



def pageContainer(content):
    return Div(
        Div(
            content,
            Class="w-screen h-full flex itesm-center justify-center max-w-96",
        ),
            Class="w-full h-full overflow-y-auto flex items-center justify-center"
        )

def profile(img_url):
    return Div(
        Img(src=img_url, Class="w-full h-full rounded-full"),
        Class = "flex items-center justify-center",
    )

def icon_button(img_url):
    return Div(
        Img(src=img_url, Class="button text-lg text-zinc-500 font-bold"),
        Class = "w-full h-full flex items-center justify-center p-1 rounded-lg bg-zinc-100 hover:bg-zinc-200",
    )


def statStack(stat, value):
    return Div(
        Div(
            P(stat, Class="text-xs text-zinc-300"),
            P(value, Class="text-lg text-zinc-500 font-bold leading-3"),
            Class="flex flex-col items-start justify-center",
        ),
        Class="flex flex-col items-center justify-center",
    )