"""
Display Controller for Waveshare 2.13" E-Paper HAT Rev 2.1
Handles low-level display operations
"""

import logging
from typing import Optional
from PIL import Image

try:
    from waveshare_epd import epd2in13_V2
    DISPLAY_AVAILABLE = True
except ImportError:
    DISPLAY_AVAILABLE = False
    logging.warning("Display library not available - running in simulation mode")


class DisplayController:
    """Controls the e-paper display hardware"""
    
    def __init__(self, width: int = 250, height: int = 122):
        """
        Initialize display controller for Rev 2.1
        
        Args:
            width: Display width in pixels (250 for 2.13")
            height: Display height in pixels (122 for 2.13")
        """
        self.width = width
        self.height = height
        self.epd = None
        self.refresh_count = 0
        self.logger = logging.getLogger(__name__)
        
    def initialize(self) -> bool:
        """
        Initialize the e-paper display
        
        Returns:
            True if successful, False otherwise
        """
        if not DISPLAY_AVAILABLE:
            self.logger.warning("Display hardware not available")
            return False
        
        try:
            self.epd = epd2in13_V2.EPD()
            # Rev 2.1 uses init(0) for full update
            self.epd.init(0)
            self.epd.Clear(0xFF)
            self.logger.info(f"Display initialized: {self.width}x{self.height}")
            return True
        except Exception as e:
            self.logger.error(f"Display initialization failed: {e}")
            return False
    
    def display_image(self, image: Image.Image, full_refresh: bool = False) -> bool:
        """
        Display image on e-paper
        
        Args:
            image: PIL Image object (should be 1-bit black/white)
            full_refresh: Force full display refresh
            
        Returns:
            True if successful
        """
        if not DISPLAY_AVAILABLE or self.epd is None:
            # Simulation mode - save to file
            import os
            os.makedirs("test_output", exist_ok=True)
            image.save(f"test_output/frame_{self.refresh_count:04d}.png")
            self.logger.info(f"Simulated display (saved to file)")
            self.refresh_count += 1
            return True
        
        try:
            if full_refresh:
                self.logger.info("Performing full refresh")
                self.epd.init(0)
                self.epd.Clear(0xFF)
            
            self.epd.display(self.epd.getbuffer(image))
            self.refresh_count += 1
            self.logger.info(f"Image displayed (refresh #{self.refresh_count})")
            return True
            
        except Exception as e:
            self.logger.error(f"Display error: {e}")
            return False
    
    def sleep(self) -> None:
        """Put display into low-power sleep mode"""
        if DISPLAY_AVAILABLE and self.epd:
            try:
                self.epd.sleep()
                self.logger.debug("Display in sleep mode")
            except Exception as e:
                self.logger.error(f"Sleep mode error: {e}")
    
    def clear(self) -> None:
        """Clear display to white"""
        if DISPLAY_AVAILABLE and self.epd:
            try:
                self.epd.init(0)
                self.epd.Clear(0xFF)
                self.logger.info("Display cleared")
            except Exception as e:
                self.logger.error(f"Clear error: {e}")
    
    def cleanup(self) -> None:
        """Clean shutdown of display"""
        self.logger.info("Display cleanup")
        self.clear()
        self.sleep()