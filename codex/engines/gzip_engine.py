"""
Standard Gzip Compression Engine (Baseline)

Simple wrapper around Python's gzip module for baseline comparison.
This demonstrates that Codex→gzip outperforms plain gzip.
"""

import gzip
from typing import Dict, Any, Optional

from .base import CompressionEngine, CompressionResult, DecompressionResult
from ..utils.entropy import calculate_shannon_entropy


class GzipEngine(CompressionEngine):
    """
    Plain gzip compression engine (baseline).

    Used for comparison to show that symbolic preprocessing
    (Codex) provides gains over statistical compression alone.
    """

    VERSION = "1.0.0"

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize Gzip engine.

        Config options:
            - compression_level: 0-9, default 9 (max compression)
        """
        super().__init__(config)
        self.compression_level = self.config.get('compression_level', 9)

    @property
    def name(self) -> str:
        return "Gzip"

    @property
    def description(self) -> str:
        return "Standard gzip compression (baseline for comparison)"

    @property
    def version(self) -> str:
        return self.VERSION

    def compress(self, data: bytes) -> CompressionResult:
        """
        Compress data using gzip.

        Args:
            data: Input data as bytes

        Returns:
            CompressionResult with compressed data and metrics
        """
        original_size = len(data)
        entropy_original = calculate_shannon_entropy(data)

        # Compress with gzip
        compressed_data = gzip.compress(data, compresslevel=self.compression_level)

        compressed_size = len(compressed_data)
        compression_ratio = compressed_size / original_size if original_size > 0 else 1.0
        entropy_compressed = calculate_shannon_entropy(compressed_data)

        return CompressionResult(
            compressed_data=compressed_data,
            original_size=original_size,
            compressed_size=compressed_size,
            compression_ratio=compression_ratio,
            entropy_original=entropy_original,
            entropy_compressed=entropy_compressed,
            metadata={
                'compression_level': self.compression_level,
                'algorithm': 'gzip'
            }
        )

    def decompress(self, compressed_data: bytes) -> DecompressionResult:
        """
        Decompress gzip-compressed data.

        Args:
            compressed_data: Gzip-compressed data

        Returns:
            DecompressionResult with original data
        """
        decompressed_data = gzip.decompress(compressed_data)

        return DecompressionResult(
            decompressed_data=decompressed_data,
            original_compressed_size=len(compressed_data),
            decompressed_size=len(decompressed_data),
            metadata={'algorithm': 'gzip'}
        )
