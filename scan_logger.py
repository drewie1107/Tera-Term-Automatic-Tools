import pyautogui
import time
import csv
import keyboard

threshold = 0.05

pyautogui.PAUSE = 0.3

last_pressed_key = None

def on_key_event(event):
    if event.event_type == keyboard.KEY_DOWN:
        if event.name.isdigit():
            if last_pressed_key is None:
                print(f"Key {event.name} was pressed. First assignation.")
                tic = time.time()
                last_pressed_key = event.name
            else:
                toc = time.time()
                if toc-tic>threshold:
                    tic = time.time

            




keyboard.hook(on_key_event)

# Keep the script running
keyboard.wait('esc')  # Press 'esc' to exit
