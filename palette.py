import modern_colorthief

def rgb2hex (color_tuple):
    # Source - https://stackoverflow.com/a/63569129
    # Posted by MestreLion
    # Retrieved 2026-05-22, License - CC BY-SA 4.0

    return "#" + "".join(f"{i:02X}" for i in color_tuple)
    

# path to any image
path = "foo.png"

tup: tuple = modern_colorthief.get_color(path)
print("dominant:", rgb2hex(tup))

pal: list[tuple] = modern_colorthief.get_palette(path)
print("palette:", [ rgb2hex(tup) for tup in pal ])
