"""
Codex: A Symbolic Compression Engine Framework

A modular framework for implementing and comparing compression engines
based on symbolic reasoning, category theory, and entropy minimization.

Author: MUSHIKARATI
License: MIT
"""

__version__ = "1.0.0"
__author__ = "MUSHIKARATI"

from .engines import (
    CompressionEngine,
    CompressionResult,
    DecompressionResult,
    CodexEngine
)

from .registry import (
    EngineRegistry,
    register_engine,
    get_engine,
    list_engines
)

__all__ = [
    'CompressionEngine',
    'CompressionResult',
    'DecompressionResult',
    'CodexEngine',
    'EngineRegistry',
    'register_engine',
    'get_engine',
    'list_engines',
]
