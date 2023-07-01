import os
import tkinter

import screeninfo

import sys
from core.data import Converter, ProblemImage, test_api_key
from core.gui import CustomGUI
from core.util import *

if os.name != 'nt':
    sys.exit('This program only works on Windows')

from tkinter import filedialog

selected_folder = ''

def open_folder():
    folder_path = filedialog.askdirectory()
    global selected_folder
    selected_folder = folder_path
    if selected_folder == '':
        sys.exit('No folder selected')

    gui.root.destroy()


def exit_on_close():
    sys.exit('bye :)')


def convert_images():
    global selected_folder
    try:
        os.mkdir(selected_folder + "/small")
    except FileExistsError:
        pass

    for file in os.listdir(selected_folder):
        if file.endswith(".jpg") or file.endswith(".png"):
            downscale_image(selected_folder + "/" + file, selected_folder + "/small/small_" + file, 700)

    selected_folder = selected_folder + "/small/"
    gui.root.destroy()

def create_error_window(error_message):
    gui = CustomGUI(400, 100)
    gui.root.protocol("WM_DELETE_WINDOW", exit_on_close)
    gui.add_text(error_message, 0, 0).pack()
    gui.root.mainloop()

def reload_images(description=None, api_key=None):
    global converter
    images = []
    for image in os.listdir(selected_folder):
        if image.endswith('.jpg') or image.endswith('.png'):
            try:
                images.append(ProblemImage(os.path.join(selected_folder, image), ''))
            except:
                create_error_window(error_message='Error with image ' + image)

    converter = Converter(images, api_key)

    # if there are no images in the folders
    if len(images) == 0:
        create_error_window(error_message='No images in the folder')
        return

    if description is not None:
        description.delete(0, tkinter.END)

def show_api_request():
    global converter
    gui = CustomGUI(400, 100)
    gui.root.protocol("WM_DELETE_WINDOW", exit_on_close)
    gui.add_text("Enter the api key that was given to you", 0, 0).pack()
    gui.add_text("Write skip to skip and not use the feature", 0, 0).pack()
    api_key_input = gui.add_input(100, 0, 1000, 100)
    api_key_input.pack()
    gui.add_button('Submit', lambda: get_api_key(gui, api_key_input), 0, 0, 100, 50).pack()

    gui.start()


def get_api_key(gui, api_key_input):
    global api_key
    api_key = api_key_input.get()
    gui.root.destroy()


def api_key_correct():
    global api_key
    if api_key == "skip":
        return True
    try:
        return test_api_key(api_key)
    except:
        return False


converter = Converter([])
if __name__ == '__main__':
    api_key = None

    try:
        api_key = open('API_KEY', 'r').read().strip()
        if api_key is None:
            show_api_request()
    except FileNotFoundError:
        show_api_request()

    while not api_key_correct():
        show_api_request()

    # the open folder gui
    gui = CustomGUI(400, 400)
    gui.root.protocol("WM_DELETE_WINDOW", exit_on_close)
    gui.add_button('Open folder', lambda: open_folder(), 0, 0, 100, 50).pack(anchor=tkinter.CENTER, expand=True,
                                                                             fill=tkinter.BOTH)
    gui.start()

    # get monitor dimensions
    monitor_info = screeninfo.get_monitors()[0]
    monitor_width = monitor_info.width
    monitor_height = monitor_info.height

    reload_images(api_key=api_key)

    gui = CustomGUI(400, 100)
    gui.root.protocol("WM_DELETE_WINDOW", exit_on_close)
    gui.add_text("Would you like to convert the images to smaller ones in this folder", 0, 0).pack(
        anchor=tkinter.CENTER, fill=tkinter.BOTH)
    gui.add_text("and put them in a folder called 'small'?", 0, 0).pack(anchor=tkinter.CENTER, fill=tkinter.BOTH)

    gui.add_button('Yes', lambda: convert_images(), 0, 0, 100, 50).pack(side=tkinter.LEFT, expand=True,
                                                                        fill=tkinter.BOTH)
    gui.add_button('No', lambda: gui.root.destroy(), 0, 0, 100, 50).pack(side=tkinter.RIGHT, expand=True,
                                                                         fill=tkinter.BOTH)
    gui.start()

    reload_images(api_key=api_key)

    # gui and all its elements
    gui = CustomGUI(int(monitor_width / 2), int(monitor_height / 2))

    display_image = gui.add_image(converter.images[0].image_path, 100, 100, converter)
    display_image.pack(anchor=tkinter.CENTER, expand=True, fill=tkinter.BOTH)

    description = gui.add_input(100, 0, 1000, 100)
    description.bind("<Return>", lambda event: gui.update_image(display_image, description, ">", converter.images, converter))

    gui.add_button('<', lambda: gui.update_image(display_image, description, "<", converter.images, converter), 0, 0,
                   100, 50)
    gui.add_button('>', lambda: gui.update_image(display_image, description, ">", converter.images, converter), 0, 50,
                   100, 50)

    gui.add_button('<<', lambda: gui.update_image(display_image, description, "<<", converter.images, converter), 0,
                   100, 100, 50)
    gui.add_button('>>', lambda: gui.update_image(display_image, description, ">>", converter.images, converter), 0,
                   150, 100, 50)

    gui.add_button('Save', lambda: converter.save_doc(selected_folder, gui), 0, 200, 100, 50)
    gui.add_button('Preview', lambda: converter.convert_and_open(gui), 0, 250, 100, 50)

    gui.add_button('Restart', lambda: reload_images(description, api_key), 0, 300, 100, 50)

    if api_key != "skip":
        gui.add_button('Full', lambda: converter.convert_and_make_executive_summary(gui), 0, 500, 100, 50)

    gui.start()
