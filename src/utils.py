"""
Utility Functions
"""

import logging
import yaml
from pathlib import Path
from typing import List, Dict, Any


def load_config(config_path: Path) -> Dict[str, Any]:
    """
    Load YAML configuration file
    
    Args:
        config_path: Path to config file
        
    Returns:
        Configuration dictionary
    """
    try:
        with open(config_path, 'r') as f:
            return yaml.safe_load(f)
    except Exception as e:
        logging.error(f"Failed to load config {config_path}: {e}")
        return {}


def get_image_files(directory: Path, extensions: List[str]) -> List[Path]:
    """
    Get list of image files from directory
    
    Args:
        directory: Directory to search
        extensions: List of file extensions to include (e.g., ['.jpg', '.png'])
        
    Returns:
        List of image file paths
    """
    if not directory.exists():
        logging.warning(f"Directory does not exist: {directory}")
        return []
    
    files = []
    for ext in extensions:
        files.extend(directory.glob(f"*{ext}"))
        files.extend(directory.glob(f"*{ext.upper()}"))
    
    return sorted(files)


def setup_logging(log_file: Path, level: str = "INFO") -> None:
    """
    Configure logging
    
    Args:
        log_file: Path to log file
        level: Logging level
    """
    numeric_level = getattr(logging, level.upper(), logging.INFO)
    
    logging.basicConfig(
        level=numeric_level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()
        ]
    )