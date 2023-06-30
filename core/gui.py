import os
import tkinter as tk
from PIL import ImageTk, Image
from ppgl.ppgl import GUI


# gui class that is reusable meaning it easy
class CustomGUI(GUI):
    def __init__(self, width, height):
        super().__init__(width, height)
        self.image_id = 0

    def update_image(self, display_image, description, direction, image_list, converter):
        converter.update_description(self.image_id, description.get())

        if converter.images[self.image_id].waiting_for_answer:
            print("waiting for answer")
            return

        if direction == "<":
            self.image_id -= 1
        elif direction == ">":
            self.image_id += 1
        elif direction == "<<":
            self.image_id = 0
        elif direction == ">>":
            self.image_id = len(image_list) - 1
        else:
            pass

        if self.image_id < 0:
            self.image_id = 0
            return

        if self.image_id >= len(image_list):
            self.image_id = len(image_list) - 1
            return

        image_path = image_list[self.image_id].image_path

        image = ImageTk.PhotoImage(Image.open(image_path))
        display_image.config(image=image)
        display_image.image = image

        description.delete(0, tk.END)
        description.insert(0, image_list[self.image_id].description)

        self.root.update()
