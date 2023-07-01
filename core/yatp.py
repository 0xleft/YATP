import os
import tkinter
from tkinter import filedialog

import eel

from core.api.api_key_handler import APIKeyHandler
from core.data import Converter, make_images_smaller
from core.gui import GUI


class YATP:
    def __init__(self, width, height):
        self.selected_folder = None
        eel.expose(self.get_selected_folder)
        eel.expose(self.convert_images)
        eel.expose(self.next_image)
        eel.expose(self.previous_image)
        eel.expose(self.preview)
        eel.expose(self.save)
        eel.expose(self.full)
        eel.expose(self.open_image)
        self.converter = Converter()
        self.api_key_handler = APIKeyHandler()
        self.image_index = 0
        self.gui = GUI(width, height, 'index.html')
        self.api_key_handler.initial_check()

    def get_selected_folder(self):
        root = tkinter.Tk()
        root.attributes("-topmost", True)
        root.withdraw()
        directory_path = filedialog.askdirectory()
        if directory_path == "":
            self.get_selected_folder()

        self.selected_folder = directory_path
        print(self.selected_folder)
        eel.hide_folder_select_screen()

    def convert_images(self, convert):
        eel.show_loading_screen()
        self.converter.load_images(self.selected_folder)
        if convert:
            make_images_smaller(self.selected_folder)
            self.selected_folder += "/small"
            self.converter.load_images(self.selected_folder)
        eel.hide_loading_screen()
        eel.hide_convert_confirmation()

        eel.update_image(self.converter.get_image_src(self.image_index), self.converter.images[self.image_index].description)

    def next_image(self, description):
        eel.show_loading_screen()

        self.converter.update_description(self.image_index, description)

        if self.image_index < len(self.converter.images) - 1:
            self.image_index += 1
            eel.update_image(self.converter.get_image_src(self.image_index), self.converter.images[self.image_index].description)
        eel.hide_loading_screen()

    def previous_image(self, description):
        eel.show_loading_screen()

        self.converter.update_description(self.image_index, description)

        if self.image_index > 0:
            self.image_index -= 1
            eel.update_image(self.converter.get_image_src(self.image_index), self.converter.images[self.image_index].description)
        eel.hide_loading_screen()

    def preview(self):
        self.converter.convert()
        self.converter.open()

    def save(self):
        self.converter.save_doc(self.selected_folder)
        eel.show_notification("Saved!")

    def full(self):
        self.converter.convert_and_make_executive_summary(self.api_key_handler.get_api_key())
        self.converter.open()

    def open_image(self):
        os.startfile(self.converter.images[self.image_index].image_path)