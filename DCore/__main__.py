# Microservice idea:
# https://github.com/OnurYilmazGit/-Paper-Module-RaspberryPi-Services-Fork-

from DCore.display_config import DISPLAY_SETTINGS
import yaml
from importlib import import_module
from PIL import Image
from threading import Thread
import time
import RPi.GPIO as GPIO
import DCore.log as Log
import sys

class DisplayManager:
    def __init__(self, config_file):
        self.default_pins = {
            "reset": 17,
            "dc": 25,
            "cs": 8,
            "busy": 24,
            "pwr": 18,
            "mosi": 10,
            "sck": 11,
            "backlight": None,
        }
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
        for input_name, input_config in self.config["frame_inputs"].items():
            inputs[input_name] = input_config["path"]
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

    def set_backlight(self, pin=24, enable=True):
        GPIO.setup(pin, GPIO.OUT)
        GPIO.output(pin, GPIO.LOW)
        time.sleep(0.1)
        if enable:
            GPIO.output(pin, GPIO.HIGH)


    def init_display(self, settings):
        """Initialize a single display based on the provided settings."""
        driver_module = settings["driver"]
        driver_class = settings["class"]
        pins = self.default_pins
        pins = settings.get("pins", {})
        width = settings["width"]
        height = settings["height"]
        rotate = settings.get("rotate", 0)
        framebuffer = settings.get("framebuffer", None)
        h_offset = settings.get("h_offset", 0)
        v_offset = settings.get("v_offset", 0)
        bgr = settings.get("bgr", False)
        inverse = settings.get("inverse", False)
        invert = settings.get("invert", False)
        if driver_module == "waveshare_epd":
            epd_module = import_module(f"waveshare_epd.{driver_class}")
            epd = epd_module.EPD()
            if hasattr(epd, 'FULL_UPDATE'):
                epd.init(epd.FULL_UPDATE)
                epd.Clear(0xff)
                epd.init(epd.PART_UPDATE)
                print(dir(epd))
                print(type(epd))
            else:
                epd.init()
                if hasattr(epd, "smart_update"):
                    print("Smart update")
                    sys.stdout.flush()
                    image = Image.new('1', (epd.width, epd.height), 255)
                    epd.smart_update(image)
                if hasattr(epd, "Clear"):
                    epd.Clear(0xff)
            sys.stdout.flush()
            return epd
        elif driver_module.startswith("luma."):
            luma_device = import_module(f"{driver_module}.device")
            serial_interface = self.init_serial_interface(settings)
            display = getattr(luma_device, driver_class)(serial_interface=serial_interface, 
                width=width, height=height, rotate=rotate, 
                framebuffer=framebuffer, h_offset=h_offset, v_offset=v_offset,
                bgr=bgr, inverse=inverse, invert=invert)
            
            if pins.get("backlight", 24):
                self.set_backlight(pins.get("backlight", 24))
            
            #if settings.get("bgr", False):
            #    display.command(0x36, 0x40)  # Set the BGR mode
            if settings.get("invert", False):
                display.command(0x21)  # Enable invert color
            else:
                display.command(0x20)  # Disable invert color
            return display

    def init_serial_interface(self, settings):
        """Initialize SPI or I2C serial interface based on display settings."""
        print(f"Settings: {settings}")
        interface = settings["interface"]
        port = settings.get("port", 0)
        if interface == "i2c":
            from luma.core.interface.serial import i2c
            return i2c(address=settings.get("address", 0x3C))
        elif interface == "spi":
            from luma.core.interface.serial import spi
            pins = settings.get("pins", {})
            port = settings.get("spiport", 0)
            dc = pins.get("dc", 25)
            device = settings.get("spi_device", 0)
            rst = pins.get("reset", 27)
            speed = settings.get("spi_speed_hz", 8000000)
            Log.log_event(f"Using SPI interface with pins: port={port}, dc={dc}, device={device}, rst={rst}, speed={speed}")
            return spi(port=port, device=device, gpio_DC=dc, gpio_RST=rst, spi_speed_hz=speed)
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
            display.Clear(0xff)
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
        width = settings.get("width", image.width)
        height = settings.get("height", image.height)
        target_mode = settings.get("mode", "RGB")
        epd = display.__class__.__name__.startswith("EPD")
        if settings.get("inverse", False):
            image = image.transpose(Image.FLIP_LEFT_RIGHT)
        if epd:
            rotate = settings.get("rotate", 0)
            if rotate == 1:
                image = image.rotate(90, expand=True)
            elif rotate == 2:
                image = image.rotate(180, expand=True)
            elif rotate == 3:
                image = image.rotate(270, expand=True)
            resized_image = image.resize((width, height)).convert(target_mode)
            print(resized_image)
            if hasattr(display, "getbuffer"):
                buffer = display.getbuffer(resized_image)
                display.Clear(0xff)
                resized_image = buffer
            #if hasattr(display, "_get_frame_buffer"):
            #    buffer = display._get_frame_buffer(resized_image)
            #    resized_image = buffer
            else:
                print("Warning: Display getbuffer method not supported for this screen.")
                #return
        else:
            resized_image = image.resize((width, height)).convert(target_mode)
        if hasattr(display, "display"):
            display.display(resized_image)
            #if hasattr(display, "PART_UPDATE"):
            #    device.PART_UPDATE
        elif hasattr(display, "show"):
            display.show(resized_image)
        #elif hasattr(display, "smart_update"):
        #    print("Smart update")
        #    display.smart_update(resized_image)
        #    sys.stdout.flush()
        #elif hasattr(display, "display_frame"):
        #    print("Display frame")
        #    display.display_frame(resized_image)
        elif hasattr(display, "display_partial_frame"):
            print("Display partial frame")
            loc = 25
            display.display_partial_frame(resized_image, 0, 0, display.height, display.width, fast=True)
        else:
            print("Warning: Display method not supported for this screen.")

    def run_display_cycle(self):
        """Main loop to manage inputs and screens."""
        last_frames = {screen: None for screen in self.screens}
        while True:
            for screen_name, screen_config in self.config["screens"].items():
                settings = DISPLAY_SETTINGS.get(screen_config['name'], {})
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
                fps = DISPLAY_SETTINGS.get(screen_config['name'], {}).get("fps", 30)
                try:
                    current_image = Image.open(source_path).convert(settings.get("mode", "RGB"))
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
    while True:
        continue
