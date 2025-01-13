#!/usr/bin/env bash

# Default venv folder
DEFAULT_VENV="/home/pi/DCore"

# Parse the argument or use the default
VENV_FOLDER=${1:-$DEFAULT_VENV}

# Service name
SERVICE_NAME="DCore.service"

echo "Starting uninstallation..."

# Stop and disable the service
if systemctl is-active --quiet $SERVICE_NAME; then
    echo "Stopping $SERVICE_NAME..."
    sudo systemctl stop $SERVICE_NAME
fi

if systemctl is-enabled --quiet $SERVICE_NAME; then
    echo "Disabling $SERVICE_NAME..."
    sudo systemctl disable $SERVICE_NAME
fi

# Remove the service file
if [ -f "/etc/systemd/system/$SERVICE_NAME" ]; then
    echo "Removing service file..."
    sudo rm -f "/etc/systemd/system/$SERVICE_NAME"
else
    echo "Service file not found."
fi

# Reload systemd daemon
echo "Reloading systemd daemon..."
sudo systemctl daemon-reload

# Remove the virtual environment folder
if [ -d "$VENV_FOLDER" ]; then
    echo "Removing virtual environment folder: $VENV_FOLDER..."
    rm -rf "$VENV_FOLDER"
else
    echo "Virtual environment folder not found: $VENV_FOLDER"
fi

# Optional: Remove launcher script
LAUNCHER="/usr/bin/dcore-launcher"
if [ -f "$LAUNCHER" ]; then
    echo "Removing launcher script: $LAUNCHER..."
    sudo rm -f "$LAUNCHER"
else
    echo "Launcher script not found: $LAUNCHER"
fi

echo "Uninstallation completed."
