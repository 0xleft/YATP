import json

import eel
from requests import post

from core.gui import GUI
import atexit

class APIKeyHandler:

    def __init__(self):
        self.api_key = None
        eel.expose(self.submit_api_key)
        eel.expose(self.get_api_key)

    def initial_check(self):
        try:
            with open("api_key.bin", "r") as f:
                self.api_key = f.read()
            if self.api_key_correct():
                eel.hide_api_key_screen()
        except:
            pass


    def api_key_correct(self):
        eel.show_loading_screen()
        if self.api_key == "skip":
            eel.hide_ai_button()
            return True
        try:
            return self.test_api_key()
        except:
            return False

    def test_api_key(self):
        response = post("http://pageup.lt:8700/pleasegivetomeyes", data=json.dumps({
            "model": "gpt-3.5-turbo"
            , "messages": [{"role": "system", "content": "say something"}]}),
                        headers={"Authorization": f"{self.api_key}", "Content-Type": "application/json"})

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