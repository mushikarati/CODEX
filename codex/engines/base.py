"""
Base abstract class for all compression engines.

This module defines the interface that all compression engines must implement,
ensuring consistency and enabling the registry/factory pattern.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, Tuple
from dataclasses import dataclass


@dataclass
class CompressionResult:
    """Result of a compression operation."""
    compressed_data: bytes
    original_size: int
    compressed_size: int
    compression_ratio: float
    entropy_original: Optional[float] = None
    entropy_compressed: Optional[float] = None
    metadata: Optional[Dict[str, Any]] = None

    def __str__(self) -> str:
        return (
            f"CompressionResult(\n"
            f"  Original Size: {self.original_size} bytes\n"
            f"  Compressed Size: {self.compressed_size} bytes\n"
            f"  Compression Ratio: {self.compression_ratio:.2%}\n"
            f"  Entropy (Original): {self.entropy_original:.4f if self.entropy_original else 'N/A'}\n"
            f"  Entropy (Compressed): {self.entropy_compressed:.4f if self.entropy_compressed else 'N/A'}\n"
            f")"
        )


@dataclass
class DecompressionResult:
    """Result of a decompression operation."""
    decompressed_data: bytes
    original_compressed_size: int
    decompressed_size: int
    metadata: Optional[Dict[str, Any]] = None


class CompressionEngine(ABC):
    """
    Abstract base class for all compression engines.

    All compression engines must inherit from this class and implement
    the compress() and decompress() methods.
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize the compression engine.

        Args:
            config: Optional configuration dictionary for engine-specific parameters
        """
        self.config = config or {}
        self._validate_config()

    @property
    @abstractmethod
    def name(self) -> str:
        """Return the name of the compression engine."""
        pass

    @property
    @abstractmethod
    def description(self) -> str:
        """Return a brief description of the compression engine."""
        pass

    @property
    @abstractmethod
    def version(self) -> str:
        """Return the version of the compression engine."""
        pass

    @abstractmethod
    def compress(self, data: bytes) -> CompressionResult:
        """
        Compress the input data.

        Args:
            data: Input data as bytes

        Returns:
            CompressionResult containing compressed data and metrics
        """
        pass

    @abstractmethod
    def decompress(self, compressed_data: bytes) -> DecompressionResult:
        """
        Decompress the compressed data.

        Args:
            compressed_data: Compressed data as bytes

        Returns:
            DecompressionResult containing decompressed data and metrics
        """
        pass

    def _validate_config(self) -> None:
        """
        Validate the configuration. Override in subclasses for custom validation.

        Raises:
            ValueError: If configuration is invalid
        """
        pass

    def get_info(self) -> Dict[str, Any]:
        """
        Get information about the engine.

        Returns:
            Dictionary with engine information
        """
        return {
            "name": self.name,
            "description": self.description,
            "version": self.version,
            "config": self.config
        }

    def benchmark(self, data: bytes) -> Dict[str, Any]:
        """
        Run a compression benchmark on the provided data.

        Args:
            data: Input data as bytes

        Returns:
            Dictionary with benchmark results
        """
        import time

        # Compression benchmark
        start_time = time.perf_counter()
        compress_result = self.compress(data)
        compress_time = time.perf_counter() - start_time

        # Decompression benchmark
        start_time = time.perf_counter()
        decompress_result = self.decompress(compress_result.compressed_data)
        decompress_time = time.perf_counter() - start_time

        # Verify integrity
        integrity_ok = decompress_result.decompressed_data == data

        return {
            "engine": self.name,
            "original_size": len(data),
            "compressed_size": compress_result.compressed_size,
            "compression_ratio": compress_result.compression_ratio,
            "compression_time": compress_time,
            "decompression_time": decompress_time,
            "throughput_compress_mbps": (len(data) / compress_time) / (1024 * 1024) if compress_time > 0 else 0,
            "throughput_decompress_mbps": (len(data) / decompress_time) / (1024 * 1024) if decompress_time > 0 else 0,
            "integrity_check": integrity_ok,
            "entropy_original": compress_result.entropy_original,
            "entropy_compressed": compress_result.entropy_compressed
        }
