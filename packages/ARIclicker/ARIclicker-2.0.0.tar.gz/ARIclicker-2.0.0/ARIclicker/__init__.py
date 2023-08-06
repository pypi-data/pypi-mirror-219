import time
import threading
from pynput.mouse import Button, Controller
from pynput.keyboard import Listener, KeyCode
import pynput
import random

class ClickMouse(threading.Thread):
    def __init__(self, delay_min, delay_max, button):
        super(ClickMouse, self).__init__()
        self.delay_min = delay_min
        self.delay_max = delay_max
        self.button = button
        self.running = False
        self.program_running = True

    def start_clicking(self):
        self.running = True

    def stop_clicking(self):
        self.running = False

    def exit(self):
        self.stop_clicking()
        self.program_running = False

    def run(self):
        mouse=Controller()
        while self.program_running:
            while self.running:
                mouse.click(self.button)
                time.sleep(random.uniform(self.delay_min, self.delay_max))


def autoclick(start_stop_key_character, end_key_character, button,delay_min, delay_max ):
    if button == "left":
        button = Button.left
    if button == "right":
        button = Button.right
    start_stop_key = KeyCode(char=start_stop_key_character)
    stop_key = KeyCode(char=end_key_character)
    mouse = pynput.mouse.Controller()
    click_thread = ClickMouse(delay_min, delay_max, button)
    click_thread.start()

    def on_press(key):
        if key == start_stop_key:
            if click_thread.running:
                click_thread.stop_clicking()
            else:
                click_thread.start_clicking()
        elif key == stop_key:
            click_thread.exit()
            listener.stop()

    with Listener(on_press=on_press) as listener:
        listener.join()
        start_listening_click = True

