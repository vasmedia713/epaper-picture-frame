#!/bin/bash
# Installation script for Raspberry Pi
# This script sets up everything needed for the picture frame

set -e  # Exit on any error

echo "=========================================="
echo "E-Paper Picture Frame Installation"
echo "=========================================="
echo ""

# Check if running on Raspberry Pi
if [ ! -f /proc/device-tree/model ]; then
    echo "WARNING: This doesn't appear to be a Raspberry Pi"
    read -p "Continue anyway? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Update system
echo "Step 1/7: Updating system..."
sudo apt update
sudo apt upgrade -y

# Install system dependencies
echo ""
echo "Step 2/7: Installing system dependencies..."
sudo apt install -y \
    python3-pip \
    python3-pil \
    python3-numpy \
    python3-yaml \
    git \
    vim \
    tmux

# Install Python packages
echo ""
echo "Step 3/7: Installing Python packages..."
if [ -f requirements.txt ]; then
    sudo pip3 install -r requirements.txt --break-system-packages
else
    echo "ERROR: requirements.txt not found!"
    exit 1
fi

# Enable SPI (required for e-paper display)
echo ""
echo "Step 4/7: Enabling SPI interface..."
sudo raspi-config nonint do_spi 0

# Create necessary directories
echo ""
echo "Step 5/7: Creating directories..."
mkdir -p /home/pi/pictures
mkdir -p /home/pi/logs
mkdir -p /home/pi/.picture_frame_cache

# Set correct permissions
chmod 755 /home/pi/pictures
chmod 755 /home/pi/logs

# Configure power management
echo ""
echo "Step 6/7: Configuring power management..."
if ! grep -q "gpu_mem=16" /boot/firmware/config.txt; then
    echo "gpu_mem=16" | sudo tee -a /boot/firmware/config.txt
    echo "GPU memory reduced to 16MB (display not needed)"
fi

# Install systemd service
echo ""
echo "Step 7/7: Installing systemd service..."
if [ -f scripts/systemd/picture-frame.service ]; then
    sudo cp scripts/systemd/picture-frame.service /etc/systemd/system/
    sudo systemctl daemon-reload
    sudo systemctl enable picture-frame.service
    echo "Service installed and enabled for auto-start"
else
    echo "WARNING: Service file not found at scripts/systemd/picture-frame.service"
    echo "You'll need to start the frame manually"
fi

echo ""
echo "=========================================="
echo "Installation Complete!"
echo "=========================================="
echo ""
echo "Next steps:"
echo "1. Add photos to /home/pi/pictures"
echo "   Example: scp photo.jpg pi@picture-frame.local:/home/pi/pictures/"
echo ""
echo "2. Start the picture frame:"
echo "   sudo systemctl start picture-frame"
echo ""
echo "3. Check status:"
echo "   sudo systemctl status picture-frame"
echo ""
echo "4. View logs:"
echo "   journalctl -u picture-frame -f"
echo ""
echo "5. A reboot is recommended to apply all changes:"
echo "   sudo reboot"
echo ""