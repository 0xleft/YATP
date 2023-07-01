import eel
import tkinter
import tkinter.filedialog as filedialog


class GUI:
    def __init__(self, width, height, html_file, on_close=None):
        eel.init('web')
        if on_close is None:
            eel.start(html_file, size=(width, height), port=51515)
        else:
            eel.start(html_file, size=(width, height), close_callback=on_close, port=51515)