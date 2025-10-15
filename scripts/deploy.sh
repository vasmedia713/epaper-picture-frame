#!/bin/bash
# Deployment script - runs from your development machine
# Syncs code to Raspberry Pi and installs it

# Configuration
PI_HOST="${1:-pi@picture-frame.local}"
PROJECT_DIR="/home/pi/epaper-picture-frame"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo "=========================================="
echo "Deploying to: $PI_HOST"
echo "=========================================="
echo ""

# Check if Pi is reachable
echo "Checking connection to Pi..."
if ! ping -c 1 -W 2 $(echo $PI_HOST | cut -d'@' -f2) > /dev/null 2>&1; then
    echo -e "${RED}ERROR: Cannot reach $PI_HOST${NC}"
    echo "Make sure your Pi is powered on and connected to the network"
    exit 1
fi
echo -e "${GREEN}✓ Connection OK${NC}"
echo ""

# Sync project files
echo "Syncing files..."
rsync -av --delete \
    --exclude '.git' \
    --exclude '__pycache__' \
    --exclude '*.pyc' \
    --exclude '*.pyo' \
    --exclude '.pytest_cache' \
    --exclude 'pictures/' \
    --exclude '.env' \
    --exclude 'test_output/' \
    --exclude '.vscode' \
    --exclude '.idea' \
    --exclude 'venv/' \
    --exclude '*.log' \
    --progress \
    ./ "$PI_HOST:$PROJECT_DIR/"

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ Files synced successfully${NC}"
else
    echo -e "${RED}ERROR: File sync failed${NC}"
    exit 1
fi
echo ""

# Make scripts executable
echo "Setting permissions..."
ssh "$PI_HOST" "chmod +x $PROJECT_DIR/scripts/*.sh"
echo -e "${GREEN}✓ Permissions set${NC}"
echo ""

# Run installation script
echo "Running installation on Pi..."
ssh "$PI_HOST" "cd $PROJECT_DIR && bash scripts/install.sh"

if [ $? -eq 0 ]; then
    echo ""
    echo -e "${GREEN}✓ Installation complete${NC}"
else
    echo ""
    echo -e "${RED}ERROR: Installation failed${NC}"
    exit 1
fi
echo ""

# Restart service if it exists
echo "Checking for existing service..."
if ssh "$PI_HOST" "systemctl is-enabled picture-frame.service > /dev/null 2>&1"; then
    echo "Restarting picture-frame service..."
    ssh "$PI_HOST" "sudo systemctl restart picture-frame.service"
    echo -e "${GREEN}✓ Service restarted${NC}"
    echo ""
    echo "Checking service status..."
    ssh "$PI_HOST" "sudo systemctl status picture-frame.service --no-pager"
else
    echo -e "${YELLOW}Service not installed yet${NC}"
    echo "Start manually with: ssh $PI_HOST 'sudo systemctl start picture-frame'"
fi

echo ""
echo "=========================================="
echo "Deployment Complete!"
echo "=========================================="
echo ""
echo "Useful commands:"
echo "  View logs:   ssh $PI_HOST 'journalctl -u picture-frame -f'"
echo "  Stop frame:  ssh $PI_HOST 'sudo systemctl stop picture-frame'"
echo "  Start frame: ssh $PI_HOST 'sudo systemctl start picture-frame'"
echo "  SSH to Pi:   ssh $PI_HOST"
echo ""