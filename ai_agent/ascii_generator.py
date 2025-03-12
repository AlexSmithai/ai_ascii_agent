import ascii_magic

def generate_ascii_art(text):
    art = ascii_magic.from_image_file("app/static/images/sample.png", mode=ascii_magic.MODES.ASCII)
    return art.to_ascii()
