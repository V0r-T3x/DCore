from .display_config import DISPLAY_SETTINGS
import yaml
from importlib import import_module
from PIL import Image
from threading import Thread
import time

class DisplayManager:
    def __init__(self, config_file):
        self.config = self.load_config(config_file)
        self.screens = self.init_screens()
        self.inputs = self.init_inputs()

    def load_config(self, config_file):
        """Load the display configuration from a YAML file."""
        with open(config_file, 'r') as file:
            return yaml.safe_load(file)

    def init_inputs(self):
        """Initialize input sources for frames."""
        inputs = {}
        for input_name, input_config in self.config["frame_inputs"].items():  # Changed "inputs" to "frame_inputs"
            inputs[input_name] = input_config["path"]  # Assuming "path" is the key for the source
        return inputs

    def init_screens(self):
        """Initialize multiple displays based on the configuration."""
        screens = {}
        for screen_name, screen_config in self.config["screens"].items():
            display_name = screen_config["name"]
            settings = DISPLAY_SETTINGS.get(display_name)
            if not settings:
                raise ValueError(f"Unsupported display: {display_name}")
            screens[screen_name] = self.init_display(settings)
        return screens

    def init_display(self, settings):
        """Initialize a single display based on the provided settings."""
        driver_module = settings["driver"]
        driver_class = settings["class"]
        if driver_module == "waveshare_epd":
            epd_module = import_module(f"waveshare_epd.{driver_class}")
            return epd_module.EPD()
        elif driver_module.startswith("luma."):
            luma_device = import_module(f"{driver_module}.device")
            serial = self.init_serial_interface(settings)
            display = getattr(luma_device, driver_class)(serial)
            if settings.get("bgr", False):
                display.command(0x36, 0x40)  # Set the BGR mode
            if settings.get("inverse", False):
                display.command(0x21)  # Enable inverse color
            else:
                display.command(0x20)  # Disable inverse color
            return display

    def init_serial_interface(self, settings):
        """Initialize SPI or I2C serial interface based on display settings."""
        interface = settings["interface"]
        if interface == "i2c":
            from luma.core.interface.serial import i2c
            return i2c(address=settings.get("address", 0x3C))
        elif interface == "spi":
            from luma.core.interface.serial import spi
            pins = settings["pins"]
            return spi(port=settings.get("spi_port", 0), device=pins.get("cs", 0),
                       gpio_DC=pins["dc"], gpio_RST=pins.get("reset"),
                       spi_speed_hz=settings.get("spi_speed_hz", 8000000))
        else:
            raise ValueError(f"Unsupported interface: {interface}")

    def clear(self, screen_name=None):
        """Clear one or all displays."""
        if screen_name:
            display = self.screens.get(screen_name)
            if display:
                self._clear_display(display)
            else:
                print(f"Screen '{screen_name}' not found.")
        else:
            for display in self.screens.values():
                self._clear_display(display)

    def _clear_display(self, display):
        """Helper to clear a specific display."""
        if hasattr(display, "Clear"):  # For Waveshare EPD
            display.Clear()
        elif hasattr(display, "clear"):  # For Luma OLED/LCD
            display.clear()
        else:
            print("Warning: Clear method not supported for this display.")

    def show_image(self, image, screen_name):
        """Display an image on the specified screen."""
        display = self.screens.get(screen_name)
        if not display:
            print(f"Screen '{screen_name}' not found.")
            return
        display_name = self.config["screens"][screen_name]["name"]
        settings = DISPLAY_SETTINGS.get(display_name, {})
        target_width = settings.get("width", image.width)
        target_height = settings.get("height", image.height)
        try:
            resized_image = image.resize((target_width, target_height), Image.Resampling.LANCZOS)
        except AttributeError:
            resized_image = image.resize((target_width, target_height), Image.LANCZOS)
        if settings.get("horizontal_flip", False):
            resized_image = resized_image.transpose(Image.FLIP_LEFT_RIGHT)
        if display.__class__.__name__.startswith("EPD"):
            resized_image = resized_image.convert("1")
        if hasattr(display, "display"):
            display.display(resized_image)
        elif hasattr(display, "show"):
            display.show(resized_image)
        else:
            print("Warning: Display method not supported for this screen.")

    def run_display_cycle(self):
        """Main loop to manage inputs and screens."""
        last_frames = {screen: None for screen in self.screens}
        while True:
            for screen_name, screen_config in self.config["screens"].items():
                # Get the input associated with this screen
                input_name = screen_config.get("default_input")
                if not input_name:
                    print(f"No default_input defined for screen '{screen_name}'")
                    continue
                frame_input = self.config["frame_inputs"].get(input_name)
                if not frame_input:
                    print(f"Input '{input_name}' not found in frame_inputs for screen '{screen_name}'")
                    continue
                source_path = frame_input["path"]
                display_name = screen_config["name"]
                fps = DISPLAY_SETTINGS.get(display_name, {}).get("fps", 30)
                try:
                    # Load the image from the source path
                    current_image = Image.open(source_path).convert("RGB")
                except (FileNotFoundError, IOError, Image.UnidentifiedImageError, SyntaxError) as e:
                    current_image = last_frames.get(screen_name)
                if current_image:
                    self.show_image(current_image, screen_name)
                    last_frames[screen_name] = current_image
                time.sleep(1 / fps)

if __name__ == "__main__":
    import os
    CONFIG = os.path.join(os.path.dirname(__file__), 'config.yaml')
    display_manager = DisplayManager(CONFIG)
    main_loop = Thread(target=display_manager.run_display_cycle, daemon=True)
    main_loop.start()
    input("Press Enter to stop...\n")
    print("Exiting.")
