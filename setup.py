"""
Setup script for Tempo - Personal Activity Tracker
"""
from setuptools import setup, find_packages
from pathlib import Path

# Read the README file
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name="tempo-tracker",
    version="0.2.0",
    author="AnrokX",
    author_email="",
    description="A lightweight, privacy-focused activity tracker for personal productivity",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/AnrokX/tempo",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: End Users/Desktop",
        "Topic :: Office/Business :: Scheduling",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: POSIX :: Linux",
    ],
    python_requires=">=3.8",
    install_requires=[
        "click>=8.1.0",
        "pyyaml>=6.0",
        "python-dotenv>=1.0.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "pytest-mock>=3.10.0",
            "pytest-xdist>=3.0.0",
            "pytest-watch>=4.2.0",
            "freezegun>=1.2.0",
            "factory-boy>=3.2.0",
            "psutil>=5.8.0",
        ],
        "windows": [
            "pywin32>=300; sys_platform == 'win32'",
        ],
        "linux": [
            "python-xlib>=0.31; sys_platform == 'linux'",
        ],
    },
    entry_points={
        "console_scripts": [
            "tempo=src.cli:cli",
        ],
    },
    project_urls={
        "Bug Reports": "https://github.com/AnrokX/tempo/issues",
        "Source": "https://github.com/AnrokX/tempo",
    },
)