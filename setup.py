"""
PILOTFORGEAI - AI-Powered Film & TV Production Budget Intelligence
Setup configuration for pip installation
"""

from setuptools import setup, find_packages
import os

# Read README for long description
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# Read requirements
with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="pilotforgeai",
    version="0.6.0",
    author="Hannah Neal",
    author_email="hneal055@example.com",
    description="AI-Powered Film & TV Production Budget Intelligence System",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/hneal055/EnhancedBudgetPro",
    project_urls={
        "Bug Tracker": "https://github.com/hneal055/EnhancedBudgetPro/issues",
        "Documentation": "https://github.com/hneal055/EnhancedBudgetPro/wiki",
        "Source Code": "https://github.com/hneal055/EnhancedBudgetPro",
    },
    packages=find_packages(exclude=["tests", "tests.*", "samples", "output*"]),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: End Users/Desktop",
        "Topic :: Multimedia :: Video",
        "Topic :: Office/Business :: Financial",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.11",
    install_requires=requirements,
    extras_require={
        "gpu": ["torch>=2.0.0"],
        "dev": [
            "pytest>=9.0.0",
            "pytest-cov>=7.0.0",
            "pytest-xdist>=3.8.0",
            "black>=24.0.0",
            "flake8>=7.0.0",
        ],
        "web": [
            "flask>=3.0.0",
            "werkzeug>=3.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "pilotforge=src.cli:main",
            "pilotforge-web=web_app:main",
        ],
    },
    include_package_data=True,
    package_data={
        "src": ["*.txt", "*.md"],
        "samples": ["*.fdx", "*.fountain", "*.json"],
    },
    keywords=[
        "screenplay", "script", "budget", "film", "tv", "production",
        "ai", "nlp", "sentiment", "analysis", "visualization"
    ],
    zip_safe=False,
)
