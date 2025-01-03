# display_config.py

DISPLAY_SETTINGS = {
    "waveshare_epd_2in13": {
        "driver": "waveshare_epd",
        "class": "EPD_2in13",
        "width": 250,
        "height": 122,
        "pins": {
            "cs": 8, 
            "dc": 25, 
            "reset": 17, 
            "busy": 24
        },
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
        "class": "ili9486",
        "width": 480,
        "height": 320,
        "pins": {
            "dc": 18,
            "reset": 25,
        },
        "interface": "spi",
    },
    "gamepi_1.5_lcd": {
        "driver": "luma.lcd",
        "class": "st7789",
        "width": 240,
        "height": 240,
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
    "displayhatmini": {
        "driver": "luma.lcd",
        "class": "st7789",
        "width": 320,
        "height": 240,
        "rotate": 0,
        "bgr": False,
        "invert": True,
        "horizontal_flip": False,
        "pins": {
            "dc": 9, 
            "cs": 1,
            "backlight": 13,
        },
        "interface": "spi",
        "spi_speed_hz": 60000000,
        "spi_port": 0,
        "spi_device": 0,
        "fps": 60,
        "mode": "RGBA",
    },
    "waveshare_3.5_clone": {
        "driver": "luma.lcd",
        "class": "ili9486",
        "width": 320,
        "height": 480,
        "rotate": 1,
        "bgr": False,
        "invert": False,
        "horizontal_flip": True,
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
        "mode": "RGB",
    },
}
