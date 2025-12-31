"""
Setup configuration for Codex compression framework.
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read the README file
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name="codex-compression",
    version="1.0.0",
    author="MUSHIKARATI",
    author_email="",
    description="A symbolic compression engine framework based on category theory and entropy minimization",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/MUSHIKARATI/CODEX",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: System :: Archiving :: Compression",
        "Topic :: Scientific/Engineering :: Mathematics",
    ],
    python_requires=">=3.8",
    install_requires=[
        # No external dependencies - uses only Python standard library
    ],
    extras_require={
        'dev': [
            'pytest>=7.0',
            'pytest-cov>=3.0',
            'black>=22.0',
            'flake8>=4.0',
            'mypy>=0.950',
        ],
    },
    entry_points={
        'console_scripts': [
            'codex=codex.cli:main',
        ],
    },
    package_data={
        'codex': ['py.typed'],
    },
    include_package_data=True,
    zip_safe=False,
    keywords=[
        'compression',
        'symbolic compression',
        'category theory',
        'entropy',
        'data compression',
        'lossless compression',
        'mathematical compression',
    ],
    project_urls={
        'Bug Reports': 'https://github.com/MUSHIKARATI/CODEX/issues',
        'Source': 'https://github.com/MUSHIKARATI/CODEX',
        'Documentation': 'https://github.com/MUSHIKARATI/CODEX/blob/main/DEVELOPER_GUIDE.md',
    },
)
