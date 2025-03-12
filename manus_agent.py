from art import text2art

class ManusAgent:
    """ AI Agent that generates ASCII Art """

    def __init__(self, name="Manus", font="block", verbose=True):
        self.name = name
        self.font = font
        self.verbose = verbose

    def get_ascii_art(self, text):
        """ Generates ASCII text """
        return text2art(text, font=self.font)
