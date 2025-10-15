"""
Setup configuration for E-Paper Picture Frame
Allows installation as a Python package
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read the README file for long description
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding='utf-8')

# Read requirements from requirements.txt
requirements = []
requirements_file = this_directory / "requirements.txt"
if requirements_file.exists():
    with open(requirements_file, 'r', encoding='utf-8') as f:
        # Skip comments and empty lines
        requirements = [
            line.strip() 
            for line in f 
            if line.strip() and not line.startswith('#')
        ]

setup(
    # ============================================
    # Basic Package Information
    # ============================================
    
    name="epaper-picture-frame",
    version="1.0.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="Battery-powered e-paper digital picture frame for Raspberry Pi",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/YOUR_USERNAME/epaper-picture-frame",
    
    # ============================================
    # Package Discovery
    # ============================================
    
    # Automatically find all packages in 'src' directory
    packages=find_packages(where="."),
    
    # Include the 'src' directory in the package
    package_dir={"": "."},
    
    # ============================================
    # Dependencies
    # ============================================
    
    # Runtime dependencies (from requirements.txt)
    install_requires=requirements,
    
    # Optional dependencies for development
    extras_require={
        'dev': [
            'pytest>=7.4.0',
            'pytest-cov>=4.1.0',
            'black>=23.0.0',
            'pylint>=2.17.0',
            'mypy>=1.0.0',
        ],
        'docs': [
            'sphinx>=5.0.0',
            'sphinx-rtd-theme>=1.2.0',
        ],
    },
    
    # ============================================
    # Python Version & Compatibility
    # ============================================
    
    python_requires=">=3.9",
    
    classifiers=[
        # Development Status
        "Development Status :: 4 - Beta",
        
        # Intended Audience
        "Intended Audience :: Developers",
        "Intended Audience :: End Users/Desktop",
        
        # License
        "License :: OSI Approved :: MIT License",
        
        # Python Versions
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        
        # Operating System
        "Operating System :: POSIX :: Linux",
        
        # Topics
        "Topic :: Multimedia :: Graphics :: Presentation",
        "Topic :: System :: Hardware",
    ],
    
    # ============================================
    # Entry Points (Command Line Scripts)
    # ============================================
    
    entry_points={
        'console_scripts': [
            # Creates 'picture-frame' command that runs the application
            'picture-frame=src.picture_frame:main',
        ],
    },
    
    # ============================================
    # Additional Files
    # ============================================
    
    # Include non-Python files in the package
    include_package_data=True,
    
    # Specify which additional files to include
    package_data={
        '': [
            'config/*.yaml',
            'scripts/*.sh',
            'scripts/systemd/*.service',
        ],
    },
    
    # ============================================
    # Project URLs
    # ============================================
    
    project_urls={
        "Bug Reports": "https://github.com/vasmedia713/epaper-picture-frame/issues",
        "Source": "https://github.com/vasmedia713/epaper-picture-frame",
        "Documentation": "https://github.com//vasmedia713/epaper-picture-frame/tree/main/docs",
    },
    
    # ============================================
    # Keywords (for searching on PyPI)
    # ============================================
    
    keywords=[
        'raspberry-pi',
        'e-paper',
        'picture-frame',
        'digital-frame',
        'epaper',
        'waveshare',
        'iot',
        'embedded',
    ],
)