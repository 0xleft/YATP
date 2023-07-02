import eel
import tkinter
import tkinter.filedialog as filedialog


class GUI:
    def __init__(self, width, height, html_file):
        eel.init('web')
        eel.start(html_file, size=(width, height), port=51515)
