"""
Compression engines package.

Contains all compression engine implementations.
"""

from .base import CompressionEngine, CompressionResult, DecompressionResult
from .codex_engine import CodexEngine

# Auto-register engines
from ..registry import register_engine

register_engine(CodexEngine)

__all__ = [
    'CompressionEngine',
    'CompressionResult',
    'DecompressionResult',
    'CodexEngine',
]
