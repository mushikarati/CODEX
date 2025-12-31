"""
Entropy calculation utilities for compression engines.

Provides symbolic and statistical entropy measures for analyzing
compression efficiency and information content.
"""

import math
from collections import Counter
from typing import Union, List


def calculate_shannon_entropy(data: Union[bytes, str]) -> float:
    """
    Calculate Shannon entropy of the data.

    Shannon entropy measures the average information content in bits per symbol.
    H(X) = -Σ p(x) * log2(p(x))

    Args:
        data: Input data as bytes or string

    Returns:
        Entropy value in bits per byte/character
    """
    if not data:
        return 0.0

    # Count frequency of each byte/character
    counter = Counter(data)
    length = len(data)

    # Calculate entropy
    entropy = 0.0
    for count in counter.values():
        probability = count / length
        if probability > 0:
            entropy -= probability * math.log2(probability)

    return entropy


def calculate_symbolic_entropy(tokens: List[str]) -> float:
    """
    Calculate symbolic entropy based on token frequency.

    Used for symbolic compression engines that work with token grammars
    rather than raw bytes.

    Args:
        tokens: List of symbolic tokens

    Returns:
        Symbolic entropy value
    """
    if not tokens:
        return 0.0

    counter = Counter(tokens)
    length = len(tokens)

    entropy = 0.0
    for count in counter.values():
        probability = count / length
        if probability > 0:
            entropy -= probability * math.log2(probability)

    return entropy


def calculate_compression_gain(original_entropy: float, compressed_entropy: float,
                               original_size: int, compressed_size: int) -> dict:
    """
    Calculate various compression metrics.

    Args:
        original_entropy: Entropy of original data
        compressed_entropy: Entropy of compressed data
        original_size: Size of original data in bytes
        compressed_size: Size of compressed data in bytes

    Returns:
        Dictionary with compression metrics
    """
    entropy_reduction = original_entropy - compressed_entropy
    compression_ratio = compressed_size / original_size if original_size > 0 else 1.0
    space_saving = 1.0 - compression_ratio

    return {
        "entropy_reduction": entropy_reduction,
        "entropy_reduction_percent": (entropy_reduction / original_entropy * 100) if original_entropy > 0 else 0,
        "compression_ratio": compression_ratio,
        "space_saving": space_saving,
        "space_saving_percent": space_saving * 100,
        "bits_saved": original_size * 8 - compressed_size * 8
    }


def estimate_kolmogorov_complexity(data: bytes, compressor_size: int = 216) -> float:
    """
    Estimate Kolmogorov complexity using compression.

    K(x) ≈ |compressed(x)| + |compressor|

    Args:
        data: Input data
        compressor_size: Size of the compression model in bytes (default: 216 for Codex)

    Returns:
        Estimated Kolmogorov complexity in bytes
    """
    # This is a rough approximation
    # Real K-complexity is uncomputable, but we can approximate via compression
    import zlib
    compressed = zlib.compress(data)
    return len(compressed) + compressor_size


def calculate_mdl_score(data_bits: int, model_bits: int) -> float:
    """
    Calculate Minimum Description Length (MDL) score.

    MDL = L_model + L_data|model

    Args:
        data_bits: Bits required to encode data given the model
        model_bits: Bits required to describe the model

    Returns:
        Total MDL score in bits
    """
    return model_bits + data_bits
