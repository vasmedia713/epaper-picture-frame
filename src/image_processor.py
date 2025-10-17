"""
Image Processing for E-Paper Display
Handles image loading, resizing, and optimization for e-paper
"""

import logging
from pathlib import Path
from typing import Optional
from PIL import Image, ImageDraw, ImageFont, ImageEnhance, ImageOps


class ImageProcessor:
    """Process images for e-paper display"""
    
    def __init__(self, width: int, height: int, contrast: float = 1.2):
        """
        Initialize image processor
        
        Args:
            width: Target display width
            height: Target display height
            contrast: Contrast enhancement factor (1.0 = no change)
        """
        self.width = width
        self.height = height
        self.contrast = contrast
        self.logger = logging.getLogger(__name__)
        
    def process_image(
        self,
        image_path: Path,
        add_border: bool = True,
        border_width: int = 1
    ) -> Optional[Image.Image]:
        """
        Process image for e-paper display
        
        Args:
            image_path: Path to source image
            add_border: Add border around image
            border_width: Border width in pixels
            
        Returns:
            Processed PIL Image or None on error
        """
        try:
            # Load image
            img = Image.open(image_path)
            
            # Auto-rotate based on EXIF
            img = ImageOps.exif_transpose(img)
            
            # Convert to RGB
            img = img.convert('RGB')
            
            # Resize maintaining aspect ratio
            img = self._resize_maintain_aspect(img)
            
            # Enhance contrast for better e-paper appearance
            if self.contrast != 1.0:
                enhancer = ImageEnhance.Contrast(img)
                img = enhancer.enhance(self.contrast)
            
            # Convert to grayscale
            img = img.convert('L')
            
            # Apply Floyd-Steinberg dithering
            img = img.convert('1', dither=Image.Dither.FLOYDSTEINBERG)
            
            # Create final canvas
            final_img = self._create_canvas(img)
            
            # Add border if requested
            if add_border:
                self._add_border(final_img, border_width)
            
            self.logger.debug(f"Processed image: {image_path.name}")
            return final_img
            
        except Exception as e:
            self.logger.error(f"Error processing {image_path}: {e}")
            return None
    
    def _resize_maintain_aspect(self, img: Image.Image) -> Image.Image:
        """Resize image maintaining aspect ratio"""
        img_ratio = img.width / img.height
        display_ratio = self.width / self.height
        
        if img_ratio > display_ratio:
            # Image is wider - fit to width
            new_width = self.width
            new_height = int(self.width / img_ratio)
        else:
            # Image is taller - fit to height
            new_height = self.height
            new_width = int(self.height * img_ratio)
        
        return img.resize((new_width, new_height), Image.Resampling.LANCZOS)
    
    def _create_canvas(self, img: Image.Image) -> Image.Image:
        """Create canvas and center image"""
        canvas = Image.new('1', (self.width, self.height), 255)
        
        # Calculate centering offset
        x_offset = (self.width - img.width) // 2
        y_offset = (self.height - img.height) // 2
        
        canvas.paste(img, (x_offset, y_offset))
        return canvas
    
    def _add_border(self, img: Image.Image, width: int) -> None:
        """Add border to image (modifies in place)"""
        draw = ImageDraw.Draw(img)
        draw.rectangle(
            [0, 0, self.width - 1, self.height - 1],
            outline=0,
            width=width
        )
    
    def create_text_image(self, text: str, font_size: int = 16) -> Image.Image:
        """
        Create simple text image
        
        Args:
            text: Text to display
            font_size: Font size
            
        Returns:
            PIL Image with text
        """
        img = Image.new('1', (self.width, self.height), 255)
        draw = ImageDraw.Draw(img)
        
        try:
            font = ImageFont.truetype(
                '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',
                font_size
            )
        except:
            font = ImageFont.load_default()
        
        # Get text size and center it
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        
        position = (
            (self.width - text_width) // 2,
            (self.height - text_height) // 2
        )
        
        draw.text(position, text, font=font, fill=0)
        return img
