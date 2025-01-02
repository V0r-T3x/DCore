from PIL import Image
from .__main__ import DisplayManager
import time
import threading
import sys
import os

CONFIG_FILE = os.path.join(os.path.dirname(__file__), 'config.yaml')

exit_flag = False

def listen_for_input():
    """Thread function to listen for user input."""
    global exit_flag
    input("Press Enter to exit...\n")
    exit_flag = True

def main():
    global exit_flag
    input_thread = threading.Thread(target=listen_for_input, daemon=True)
    input_thread.start()

    print(CONFIG_FILE)
    display_manager = DisplayManager(CONFIG_FILE)
    print(display_manager)

    display_manager.clear()
    print("Display cleared.")

    image_path = "/var/tmp/pwnagotchi/pwnagotchi.png"
    last_image = None 

    try:
        while not exit_flag:
            try:
                current_image = Image.open(image_path).rotate(270, expand=True)
                current_image = current_image.resize((320, 480)).convert("RGB")
                last_image = current_image
            except (FileNotFoundError, IOError, Image.UnidentifiedImageError, SyntaxError) as e:
                if last_image:
                    current_image = last_image
                else:
                    print(f"No valid image found, skipping this cycle.")
                    continue 

            display_manager.show_image(current_image, "screen1")
            time.sleep(0.2)

    except KeyboardInterrupt:
        print("Exiting...")

    print("Cleaning up...")

if __name__ == "__main__":
    main()
