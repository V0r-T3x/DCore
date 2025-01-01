import yaml
#from display_config import DISPLAY_SETTINGS
from .display_config import DISPLAY_SETTINGS
from importlib import import_module
from PIL import Image  # Import Pillow for image manipulation


class DisplayManager:
    def __init__(self, config_file):
        self.config = self.load_config(config_file)
        self.screens = self.init_screens()

    def load_config(self, config_file):
        """Load the display configuration from a YAML file."""
        with open(config_file, 'r') as file:
            return yaml.safe_load(file)

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
            return spi(port=pins.get("spi_port", 0), device=pins.get("cs", 0),
                       gpio_DC=pins["dc"], gpio_RST=pins.get("reset"),
                       bus_speed_hz=settings.get("bus_speed_hz", 8000000))
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

        if settings.get("horizontal_flip", False):
            image = image.transpose(Image.FLIP_LEFT_RIGHT)

        if display.__class__.__name__.startswith("EPD"):
            image = image.convert("1")

        if hasattr(display, "display"):
            display.display(image)
        elif hasattr(display, "show"):
            display.show(image)
        else:
            print("Warning: Display method not supported for this screen.")


if __name__ == "__main__":
    from PIL import ImageDraw
    import os
    import time
    CONFIG = os.path.join(os.path.dirname(__file__), 'config.yaml')
    display_manager = DisplayManager(CONFIG)
    img = Image.new("RGB", (320, 480), "white")
    draw = ImageDraw.Draw(img)
    draw.text((100, 100), "Hello, Screen1!", fill="black")
    display_manager.show_image(img, "screen1")

    # Create another image for screen2
#    img2 = Image.new("RGB", (128, 64), "white")
#    draw2 = ImageDraw.Draw(img2)
#    draw2.text((10, 20), "Hello, Screen2!", fill="black")

    # Show the image on screen2
#    display_manager.show_image(img2, "screen2")

    print("Images displayed successfully.")
    time.sleep(10)
    print("Clearing displays...")
