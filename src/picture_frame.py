"""
Main Picture Frame Application
"""

import time
import random
import logging
from pathlib import Path
from typing import List

from .display_controller import DisplayController
from .image_processor import ImageProcessor
from .utils import load_config, get_image_files, setup_logging


class PictureFrame:
    """Main picture frame application"""
    
    def __init__(self, config_path: Path):
        """
        Initialize picture frame
        
        Args:
            config_path: Path to configuration file
        """
        # Load configuration
        self.config = load_config(config_path)
        frame_config = self.config.get('frame', {})
        display_config = self.config.get('display', {})
        
        # Setup logging
        log_config = self.config.get('logging', {})
        log_file = Path(log_config.get('file', 'picture_frame.log'))
        log_level = log_config.get('level', 'INFO')
        setup_logging(log_file, log_level)
        
        self.logger = logging.getLogger(__name__)
        self.logger.info("Initializing Picture Frame")
        
        # Initialize components
        self.display = DisplayController(
            width=display_config.get('width', 250),
            height=display_config.get('height', 122)
        )
        
        self.processor = ImageProcessor(
            width=display_config.get('width', 250),
            height=display_config.get('height', 122),
            contrast=display_config.get('image_processing', {}).get('contrast_enhancement', 1.2)
        )
        
        # Frame settings
        self.photo_dir = Path(frame_config.get('photo_directory', '/home/pi/pictures'))
        self.refresh_interval = frame_config.get('refresh_interval', 300)
        self.random_order = frame_config.get('random_order', True)
        self.full_clear_interval = display_config.get('power_management', {}).get('full_clear_interval', 10)
        self.sleep_enabled = display_config.get('power_management', {}).get('sleep_between_updates', True)
        
        # State
        self.image_list: List[Path] = []
        self.current_index = 0
        self.refresh_count = 0
        
    def initialize(self) -> bool:
        """
        Initialize hardware and load images
        
        Returns:
            True if successful
        """
        # Initialize display
        if not self.display.initialize():
            self.logger.error("Failed to initialize display")
            return False
        
        # Load images
        self.load_images()
        
        if not self.image_list:
            self.logger.error(f"No images found in {self.photo_dir}")
            return False
        
        # Show startup message
        self.show_startup_message()
        
        return True
    
    def load_images(self) -> None:
        """Load image file list"""
        extensions = self.config.get('frame', {}).get('supported_formats', ['.jpg', '.jpeg', '.png'])
        self.image_list = get_image_files(self.photo_dir, extensions)
        
        if self.random_order:
            random.shuffle(self.image_list)
        
        self.logger.info(f"Loaded {len(self.image_list)} images")
    
    def show_startup_message(self) -> None:
        """Display startup message"""
        msg = f"Picture Frame\n{len(self.image_list)} images loaded"
        startup_img = self.processor.create_text_image(msg)
        self.display.display_image(startup_img)
        time.sleep(2)
    
    def next_image(self) -> bool:
        """
        Display next image
        
        Returns:
            True if successful
        """
        if not self.image_list:
            self.logger.warning("No images available")
            return False
        
        # Get current image
        image_path = self.image_list[self.current_index]
        self.logger.info(
            f"Displaying: {image_path.name} "
            f"({self.current_index + 1}/{len(self.image_list)})"
        )
        
        # Process image
        processed_image = self.processor.process_image(image_path)
        if not processed_image:
            self.logger.error(f"Failed to process {image_path}")
            return False
        
        # Determine if full refresh needed
        self.refresh_count += 1
        full_refresh = (self.refresh_count % self.full_clear_interval == 0)
        
        # Display
        self.display.display_image(processed_image, full_refresh)
        
        # Sleep display if enabled
        if self.sleep_enabled:
            self.display.sleep()
        
        # Move to next image
        self.current_index = (self.current_index + 1) % len(self.image_list)
        
        # Reshuffle if cycle complete and random mode
        if self.current_index == 0 and self.random_order:
            random.shuffle(self.image_list)
            self.logger.info("Reshuffled images")
        
        return True
    
    def run(self) -> None:
        """Main execution loop"""
        self.logger.info("Starting picture frame loop")
        
        try:
            while True:
                # Reload images every cycle
                if self.current_index == 0:
                    old_count = len(self.image_list)
                    self.load_images()
                    if len(self.image_list) != old_count:
                        self.logger.info(
                            f"Image count changed: {old_count} → {len(self.image_list)}"
                        )
                
                # Display next image
                self.next_image()
                
                # Sleep until next refresh
                self.logger.info(f"Sleeping for {self.refresh_interval}s")
                time.sleep(self.refresh_interval)
                
        except KeyboardInterrupt:
            self.logger.info("Stopped by user")
        except Exception as e:
            self.logger.error(f"Unexpected error: {e}", exc_info=True)
        finally:
            self.cleanup()
    
    def cleanup(self) -> None:
        """Clean shutdown"""
        self.logger.info("Cleaning up")
        self.display.cleanup()


def main():
    """Entry point"""
    import sys
    
    # Get config path from command line or use default
    if len(sys.argv) > 1:
        config_path = Path(sys.argv[1])
    else:
        config_path = Path(__file__).parent.parent / "config" / "frame_config.yaml"
    
    if not config_path.exists():
        print(f"Error: Config file not found: {config_path}")
        sys.exit(1)
    
    # Create and run picture frame
    frame = PictureFrame(config_path)
    if frame.initialize():
        frame.run()
    else:
        print("Failed to initialize picture frame")
        sys.exit(1)


if __name__ == '__main__':
    main()