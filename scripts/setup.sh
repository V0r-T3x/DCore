#!/usr/bin/env bash

# Exit on errors
set -e

# Step 1: Install system-level dependencies
echo "Updating system and installing dependencies..."
sudo apt update
sudo apt install -y python3-pip python3-spidev python3-rpi.gpio python3-numpy python3-pil git

# Step 2: Install Python packages in the active virtual environment
echo "Installing Python libraries in the current virtual environment..."
pip install --upgrade pip
echo "Installing luma.core from custom repository..."
pip install git+https://github.com/V0r-T3x/luma.core.git
pip install spidev RPi.GPIO pillow luma.oled luma.lcd pyyaml gpiozero lgpio

# Step 3: Clone Waveshare e-Paper repository
if [ ! -d "e-Paper" ]; then
    echo "Cloning Waveshare e-Paper repository..."
    git clone https://github.com/V0r-T3x/e-Paper.git
fi

# Step 4: Create and run custom setup.py script
echo "Creating custom setup.py script for Waveshare e-Paper..."
cat <<EOF > e-Paper/RaspberryPi_JetsonNano/python/setup.py
from setuptools import setup

# Custom hardcoded dependencies for Raspberry Pi
dependencies = ['Pillow', 'RPi.GPIO', 'spidev']

setup(
    name='waveshare-epd',
    description='Waveshare e-Paper Display',
    author='Waveshare',
    package_dir={'': 'lib'},
    packages=['waveshare_epd'],
    install_requires=dependencies,
)
EOF

echo "Installing Waveshare e-Paper library..."
cd e-Paper/RaspberryPi_JetsonNano/python/
# python3 setup.py install
pip install .

# Step 6: Return to project root and remove e-Paper folder
cd ../../../
if [ -d "e-Paper" ]; then
    echo "Removing the e-Paper folder..."
    rm -rf e-Paper
else
    echo "e-Paper folder already removed or does not exist."
fi
echo "Setup completed successfully!"
