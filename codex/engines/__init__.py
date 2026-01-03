"""
Compression engines package.

Contains all compression engine implementations.
"""

from .base import CompressionEngine, CompressionResult, DecompressionResult
from .codex_engine import CodexEngine
from .gzip_engine import GzipEngine
from .black_lzw_screw import BlackLZWScrewEngine

# Auto-register engines
from ..registry import register_engine

register_engine(CodexEngine)
register_engine(GzipEngine)
register_engine(BlackLZWScrewEngine)

__all__ = [
    'CompressionEngine',
    'CompressionResult',
    'DecompressionResult',
    'CodexEngine',
    'GzipEngine',
    'BlackLZWScrewEngine',
]
