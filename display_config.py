# display_config.py

DISPLAY_SETTINGS = {
    "waveshare_epd_2in13": {
        "driver": "waveshare_epd",
        "class": "EPD_2in13",   # Class name for the specific display
        "width": 250,
        "height": 122,
        "pins": {"cs": 8, "dc": 25, "rst": 17, "busy": 24},
    },
    "luma_oled_128x64": {
        "driver": "luma.oled",
        "class": "ssd1306",
        "width": 128,
        "height": 64,
        "interface": "i2c",
        "address": 0x3C,
    },
    "luma_lcd_480x320": {
        "driver": "luma.lcd",
        "class": "ili9486",  # Class name for ILI9486 display
        "width": 480,
        "height": 320,
        "pins": {
            "dc": 18,   # Data/Command pin
            "reset": 25  # Reset pin
        },
        "interface": "spi",
    },
    "gamepi_15_lcd": {
        "driver": "luma.lcd",
        "class": "st7789",
        "width": 240,
        "height": 240,
        "pins": {"dc": 25, "reset": 27},
        "interface": "spi",
        "backlight": 24,
        "cs": 8,
        "sck": 11,
        "mosi": 10
    },
    "waveshare_3.5_clone": {
        "driver": "luma.lcd",
        "class": "ili9486",  # Driver for ST7735, adjusted for the display
        "width": 320,        # Width resolution (example for ILI9486)
        "height": 480,       # Height resolution
        "rotate": 1,
        "bgr": False,
        "inverse": False,
        "horizontal_flip": True,
        "pins": {
            "dc": 24,        # Data/Command -> gpio_DC pin
            "reset": 25,     # Reset -> gpio_RST pin
            "cs": 0,        # Chip Select -> gpio_CS pin
            "spi_port": 0
        },
        "bus_speed_hz": 16000000,
        "interface": "spi",  # SPI communication
    },
}
