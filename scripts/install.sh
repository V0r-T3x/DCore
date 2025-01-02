#!/bin/bash

# Exit on errors
set -e

# Define default venv path if no argument is provided
VENV_DIR="${1:-/home/pi/DCore}"

# Script folder
SCRIPT_DIR="$(dirname "$(realpath "$0")")"
# Get the parent directory of the script
PARENT_DIR="$(dirname "$SCRIPT_DIR")"
# Reference a folder inside the parent directory
REPO_DIR="${PARENT_DIR}/DCore"

PYTHON_VERSION="python3.11"
VENV_PYTHON_SITE_PACKAGES="${VENV_DIR}/lib/${PYTHON_VERSION}/site-packages/DCore"

# Step 1: Update and install system-level dependencies
echo "Updating system and installing dependencies..."
sudo apt update
sudo apt install -y python3-pip python3-spidev python3-rpi.gpio python3-numpy python3-pil git

# Step 2: Create the Python virtual environment
echo "Creating a Python virtual environment at $VENV_DIR..."
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

# Step 6: Create a systemd service file
SERVICE_FILE="/etc/systemd/system/dcore.service"

echo "Creating systemd service file..."
sudo bash -c "cat > $SERVICE_FILE" <<EOF
[Service]
Type=simple
ExecStart=/usr/bin/dcore
WorkingDirectory=${VENV_PYTHON_SITE_PACKAGES}
Environment="VIRTUAL_ENV=${VENV_DIR}"
Environment="PATH=${VENV_DIR}/bin:/usr/bin"
Restart=always
User=pi
StandardOutput=file:/var/log/dcore.log
StandardError=file:/var/log/dcore_error.log

[Install]
WantedBy=multi-user.target
EOF

echo "Creating the dcore launcher"
sudo bash -c "cat > /usr/bin/dcore" <<EOF
#!/usr/bin/env bash

# Custom pre-launch logic
if [ -f "${VENV_PYTHON_SITE_PACKAGES}/config.yaml" ]; then
    echo "Found config.yaml. Starting DCore service..."
else
    echo "Missing config.yaml! DCore may not run properly."
fi

# Execute the main Python application
/home/pi/DCore/bin/python -m DCore

# Add any cleanup or post-run tasks here, if needed
echo "DCore service has exited."
EOF

sudo chmod +x /usr/bin/dcore

# Step 7: Enable and start the service
echo "Enabling and starting the DCore service..."
sudo systemctl daemon-reload
sudo systemctl enable dcore.service
sudo systemctl start dcore.service

# Step 8: Clean up and finalize
echo "Setup and service installation completed successfully!"
