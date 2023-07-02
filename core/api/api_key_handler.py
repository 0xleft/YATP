import json

import eel
from requests import post

from core.api import request_handler
from core.gui import GUI
import atexit


class APIKeyHandler:

    def __init__(self):
        self.api_key = None
        eel.expose(self.submit_api_key)
        eel.expose(self.get_api_key)
        eel.expose(self.initial_check)

    def initial_check(self):
        eel.show_loading_screen()
        try:
            with open("api_key.bin", "r") as f:
                self.api_key = f.read()
            if self.api_key_correct():
                eel.hide_api_key_screen()
        except:
            pass
        eel.hide_loading_screen()

    def api_key_correct(self):
        print("checking api key")
        eel.show_loading_screen()
        if self.api_key == "skip":
            eel.hide_ai_button()
            eel.hide_loading_screen()
            return True
        try:
            if self.test_api_key():
                eel.hide_loading_screen()
                return True
        except:
            pass
        eel.hide_loading_screen()
        return False

    def test_api_key(self):
        response = request_handler.model_complete_request_prompt(self.api_key, "test", input_prompt="say something")

        print(response.text)
        if 'error' in response.text:
            return False
        self.save_api_key()
        return True

    def save_api_key(self):
        with open("api_key.bin", "w") as f:
            f.write(self.api_key)

    def submit_api_key(self, api_key):
        self.api_key = api_key
        if self.api_key_correct():
            eel.hide_api_key_screen()
        else:
            eel.show_notification('ERROR', 'Invalid API key')
        eel.hide_loading_screen()

    def get_api_key(self):
        return self.api_key
