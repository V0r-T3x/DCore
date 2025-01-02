#!/bin/bash

# Exit on errors
set -e

# Define paths
# Script folder
SCRIPT_DIR="$(dirname "$(realpath "$0")")"
# Get the parent directory of the script
PARENT_DIR="$(dirname "$SCRIPT_DIR")"
# Reference a folder inside the parent directory
REPO_DIR="${PARENT_DIR}/DCore"
#REPO_DIR="$(pwd)"
VENV_DIR="/home/pi/DCore"
PYTHON_VERSION="python3.11"
VENV_PYTHON_SITE_PACKAGES="${VENV_DIR}/lib/${PYTHON_VERSION}/site-packages/DCore"

# Step 1: Update and install system-level dependencies
echo "Updating system and installing dependencies..."
sudo apt update
sudo apt install -y python3-pip python3-spidev python3-rpi.gpio python3-numpy python3-pil git

# Step 2: Create the Python virtual environment
echo "Creating a Python virtual environment..."
python3 create_venv.py "$VENV_DIR"

# Step 3: Activate the Python virtual environment
echo "Activating the Python virtual environment..."
source "$VENV_DIR/bin/activate"

# Step 4: Copy necessary files to the virtual environment
echo "Copying DCore files to the virtual environment..."
mkdir -p "$VENV_PYTHON_SITE_PACKAGES"
rsync -av --exclude 'scripts' --exclude 'LICENSE' --exclude 'README.md' \
    --exclude '.git' --exclude '.gitattributes' --exclude 'install.sh' --exclude 'setup.sh' \
    "${REPO_DIR}/" "$VENV_PYTHON_SITE_PACKAGES"

# Step 5: Run the setup script
echo "Running the setup script..."
chmod +x setup.sh
./setup.sh

# Step 6: Clean up and finalize
echo "Setup completed successfully!"
