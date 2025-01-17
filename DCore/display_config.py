# display_config.py

DISPLAY_SETTINGS = {
    # E-papers
    "waveshare_1.3_v2": {
        "driver": "waveshare_epd",
        "class": "epd2in13_V2",
        "mode": "1",
        "width": 250,
        "height": 122,
    },
    "waveshare_1.3_v3": {
        "driver": "waveshare_epd",
        "class": "epd2in13_V3",
        "mode": "1",
        "width": 250,
        "height": 122,
    },
    "waveshare_1.3_v4": {
        "driver": "waveshare_epd",
        "class": "epd2in13_V4",
        "mode": "1",
        "width": 250,
        "height": 122,
    },
    "waveshare_2.7": {
        "driver": "waveshare_epd",
        "class": "epd2in7",
        "mode": "1",
        "width": 264,
        "height": 176,
    },
    "waveshare_2.7_tri": {
        "driver": "waveshare_epd",
        "class": "epd2in7b",
        "mode": "3",
        "width": 264,
        "height": 176,
    },
    # Waveshare 2.7" with partial refresh
    # https://github.com/elad661/rpi_epd2in7
    "waveshare_2.7a": {
        "driver": "waveshare_epd",
        "class": "epd2in7a",
        "mode": "1",
        "rotate": 1,
        "width": 176,
        "height": 264,
    },
    # OLED
    "luma_oled_spi_128x64": {
        "driver": "luma.oled",
        "class": "sh1106",
        "width": 128,
        "height": 64,
        "rotate": 0,
        "mode": "1",
        "pins": {
            "dc": 24,
            "reset": 25,
            "sck": 11,
            "backlight": None,
            "cs": 8,
            "mosi": 10,
        },
        "interface": "spi",
        "spi_port": 0,
        "spi_device": 0,
        "spi_speed_hz": 8000000,
        "fps": 20,
    },
    # LCD
    "gamepi_1.3_lcd": {
        "driver": "luma.lcd",
        "class": "st7789",
        "width": 240,
        "height": 240,
        "rotate": 0,
        "mode": "RGB",
        "pins": {
            "dc": 25, 
            "reset": 27,
            "cs": 8,
            "sck": 11,
            "mosi": 10,
            "backlight": 24,
        },
        "interface": "spi",
        "spi_speed_hz": 16000000,
        "spi_port": 0,
        "spi_device": 0,
        "fps": 60,
        "invert": True,
    },
    "gamepi_1.44_lcd": {
        "driver": "luma.lcd",
        "class": "st7789",
        "width": 128,
        "height": 128,
        "mode": "RGB",
        "pins": {
            "dc": 25, 
            "reset": 27,
            "cs": 8,
            "sck": 11,
            "mosi": 10,
            "backlight": 24,
        },
        "interface": "spi",
        "spi_speed_hz": 16000000,
        "spi_port": 0,
        "spi_device": 0,
        "fps": 60,
    },
    "gamepi_1.5_lcd": {
        "driver": "luma.lcd",
        "class": "st7789",
        "width": 240,
        "height": 240,
        "rotate": 1,
        "mode": "RGB",
        "pins": {
            "dc": 25, 
            "reset": 27,
            "cs": 8,
            "sck": 11,
            "mosi": 10,
            "backlight": 24,
        },
        "interface": "spi",
        "spi_speed_hz": 16000000,
        "spi_port": 0,
        "spi_device": 0,
        "fps": 60,
        "invert": True,
    },
    "gamepi_1.54_lcd": {
        "driver": "luma.lcd",
        "class": "st7789",
        "width": 240,
        "height": 240,
        "rotate": 0,
        "mode": "RGBA",
        "bgr": False,
        "pins": {
            "dc": 22, 
            "reset": 27,
            "cs": 0,
            "sck": 11,
            "mosi": 10,
            "backlight": None,
        },
        "interface": "spi",
        "spi_speed_hz": 8000000,
        "spi_port": 0,
        "spi_device": 0,
        "fps": 60,
        "invert": True,
    },
    "gamepi_2.0_lcd": {
        "driver": "luma.lcd",
        "class": "st7789",
        "width": 320,
        "height": 240,
        "rotate": 2,
        "mode": "RGB",
        "pins": {
            "dc": 25, 
            "reset": 27,
            "cs": 8,
            "sck": 11,
            "mosi": 10,
            "backlight": 24,
        },
        "interface": "spi",
        "spi_speed_hz": 16000000,
        "spi_port": 0,
        "spi_device": 0,
        "fps": 60,
        "invert": True,
    },
    "displayhatmini": {
        "driver": "luma.lcd",
        "class": "st7789",
        "width": 320,
        "height": 240,
        "mode": "RGB",
        "pins": {
            "dc": 9, 
            "cs": 1,
            "backlight": 13,
        },
        "interface": "spi",
        "spi_speed_hz": 60000000,
        "spi_port": 0,
        "spi_device": 1,
        "fps": 60,
        "invert": True,
    },
    "waveshare_3.5_clone": {
        "driver": "luma.lcd",
        "class": "ili9486",
        "width": 320,
        "height": 480,
        "rotate": 0,
        "bgr": False,
        "invert": False,
        "inverse": True,
        "mode": "RGB",
        "pins": {
            "dc": 24,
            "reset": 25,
            "cs": 0,
        },
        "spi_speed_hz": 16000000,
        "interface": "spi",
        "spi_port": 0,
        "spi_device": 0,
        "fps": 60,
    },

    # Tests:
    

}
