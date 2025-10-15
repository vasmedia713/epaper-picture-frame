# E-Paper Picture Frame

> Battery-powered digital picture frame for Raspberry Pi Zero 2 W

A low-power, e-paper based picture frame that displays your favorite photos with a unique paper-like aesthetic. Perfect for desk or wall mounting with multi-day battery life.

## 📸 Features

- **Low Power**: 2-3 days on a single charge
- **Paper-like Display**: E-ink technology for easy viewing
- **Auto-Rotate**: Cycles through photos every 5 minutes
- **Wireless**: Upload photos via WiFi
- **Portable**: Completely wireless with battery power

## 🔧 Hardware Requirements

| Component | Model | Notes |
|-----------|-------|-------|
| Computer | Raspberry Pi Zero 2 W | Must be Zero 2 (not original Zero) |
| Display | Waveshare 2.13" e-paper HAT | 250x122 resolution |
| Battery | PiSugar 1200mAh | 3.7V Li-ion, 4.44Whr |
| Storage | microSD Card | 8GB minimum, 16GB recommended |

**Total Cost:** ~$50-60 USD

## 🚀 Quick Start

### For Users (Just Want It Working)
```bash
# On your Raspberry Pi
git clone https://github.com/vasmedia713/paper-picture-frame.git
cd epaper-picture-frame
bash scripts/install.sh

# Add your photos
scp /path/to/photos/*.jpg pi@picture-frame.local:/home/pi/pictures/

# Start the frame
sudo systemctl start picture-frame
```

### For Developers

See [Development Guide](docs/development.md) for detailed setup instructions.

## 📚 Documentation

- **[Hardware Setup](docs/hardware_setup.md)** - Assembly and wiring
- **[Deployment Guide](docs/deployment.md)** - Installation on Pi
- **[Development Guide](docs/development.md)** - Contributing and testing
- **[Troubleshooting](docs/troubleshooting.md)** - Common issues

## 📁 Project Structure
```
epaper-picture-frame/
├── src/                    # Source code
│   ├── picture_frame.py    # Main application
│   ├── display_controller.py
│   └── image_processor.py
├── config/                 # Configuration files
├── scripts/                # Installation/deployment scripts
├── tests/                  # Unit tests
└── docs/                   # Documentation
```

## 🔄 Usage

The picture frame automatically starts on boot. To control it:
```bash
# View status
sudo systemctl status picture-frame

# Stop
sudo systemctl stop picture-frame

# View logs
journalctl -u picture-frame -f

# Add more photos (they're detected automatically)
scp newphoto.jpg pi@picture-frame.local:/home/pi/pictures/
```

## ⚙️ Configuration

Edit `config/frame_config.yaml` to customize:

- Refresh interval (default: 5 minutes)
- Random vs sequential order
- Image processing settings
- Power management options

## 🤝 Contributing

Contributions welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Waveshare for e-paper display libraries
- PiSugar for battery management
- The Raspberry Pi community

## 📧 Contact



Project Link: [https://github.com/vasmedia713/epaper-picture-frame](https://github.com/YOUR_USERNAME/epaper-picture-frame)

---

**⭐ Star this repo if you find it useful!**