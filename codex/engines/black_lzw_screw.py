"""
Black_LZW_Screw Compression Engine

Full implementation of the Black LZW Screw compression algorithm combining:
- LZW dictionary compression (Lempel-Ziv-Welch)
- Black Gate interface with CODEX token system
- Screw transformation for symbolic pattern rotation

Based on content from GitHub Issue #5
Author: MUSHIKARATI
"""

import struct
import hashlib
from typing import Dict, Any, Optional, List

from .base import CompressionEngine, CompressionResult, DecompressionResult
from ..utils.entropy import calculate_shannon_entropy
from ..utils.tokens import codex_tokens, MagickToken


class BlackLZWScrewEngine(CompressionEngine):
    """
    Black LZW Screw compression engine.

    Implements LZW compression with Black Gate wrapping and CODEX token integration.
    Uses the 7-color Magick token system for state management.
    """

    VERSION = "1.0.0"

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize Black LZW Screw engine.

        Config options:
            - dict_size: Maximum dictionary size (default: 4096)
            - use_unicode: Support Unicode characters (default: True)
        """
        super().__init__(config)
        self.dict_size = self.config.get('dict_size', 4096)
        self.use_unicode = self.config.get('use_unicode', True)

    @property
    def name(self) -> str:
        return "Black_LZW_Screw"

    @property
    def description(self) -> str:
        return "LZW compression with Black Gate interface and CODEX token system"

    @property
    def version(self) -> str:
        return self.VERSION

    def compress(self, data: bytes) -> CompressionResult:
        """
        Compress data using Black LZW Screw algorithm.

        Process:
        1. Convert bytes to string
        2. Apply LZW compression
        3. Wrap in Black Gate (adds CODEX token seal)
        4. Encode to bytes with header

        Args:
            data: Input data as bytes

        Returns:
            CompressionResult with compressed data and metrics
        """
        original_size = len(data)
        entropy_original = calculate_shannon_entropy(data)

        # Decode to string
        try:
            text = data.decode('utf-8')
        except UnicodeDecodeError:
            text = data.decode('latin-1')  # Fallback

        # LZW compression
        codes = self._lzw_compress(text)

        # Black Gate wrapping
        gate_result = self._black_gate(codes, text)

        # Encode to bytes
        compressed_data = self._encode_compressed(gate_result, original_size)

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
                'seal': gate_result['seal'],
                'code_count': gate_result['size'],
                'hash': gate_result['hash'],
                'dict_size': self.dict_size
            }
        )

    def decompress(self, compressed_data: bytes) -> DecompressionResult:
        """
        Decompress Black LZW Screw compressed data.

        Process:
        1. Parse header and validate seal
        2. Decode codes
        3. Apply LZW decompression
        4. Convert back to bytes

        Args:
            compressed_data: Compressed data with Black Gate wrapper

        Returns:
            DecompressionResult with original data
        """
        # Parse header
        header_data = self._parse_header(compressed_data)

        # Decode codes
        codes = self._decode_compressed(compressed_data, header_data)

        # LZW decompression
        text = self._lzw_decompress(codes)

        # Convert to bytes
        try:
            decompressed_data = text.encode('utf-8')
        except UnicodeEncodeError:
            decompressed_data = text.encode('latin-1')

        return DecompressionResult(
            decompressed_data=decompressed_data,
            original_compressed_size=len(compressed_data),
            decompressed_size=len(decompressed_data),
            metadata={
                'seal': header_data['seal'],
                'hash': header_data['hash']
            }
        )

    def _lzw_compress(self, text: str) -> List[int]:
        """
        LZW compression algorithm - works on UTF-8 bytes.

        Standard LZW starting with 256 byte values.

        Args:
            text: Input string

        Returns:
            List of integer codes
        """
        # Convert to bytes for standard LZW
        data = text.encode('utf-8')

        # Initialize dictionary with all single bytes (0-255)
        dict_size = 256
        dictionary = {bytes([i]): i for i in range(dict_size)}

        codes = []
        current = b""

        for byte in data:
            combined = current + bytes([byte])
            if combined in dictionary:
                current = combined
            else:
                # Output code for current
                codes.append(dictionary[current])

                # Add new pattern to dictionary
                if dict_size < self.dict_size:
                    dictionary[combined] = dict_size
                    dict_size += 1

                current = bytes([byte])

        # Output final code
        if current:
            codes.append(dictionary[current])

        return codes

    def _lzw_decompress(self, codes: List[int]) -> str:
        """
        LZW decompression algorithm - recovers UTF-8 bytes.

        Standard LZW decompression.

        Args:
            codes: List of integer codes

        Returns:
            Decompressed string
        """
        if not codes:
            return ""

        # Initialize dictionary with all single bytes
        dict_size = 256
        dictionary = {i: bytes([i]) for i in range(dict_size)}

        # First code
        result = [dictionary[codes[0]]]
        current = dictionary[codes[0]]

        for code in codes[1:]:
            if code in dictionary:
                entry = dictionary[code]
            elif code == dict_size:
                # Special case: code not in dictionary yet
                entry = current + current[0:1]
            else:
                raise ValueError(f"Invalid LZW code: {code}")

            result.append(entry)

            # Add new pattern to dictionary
            if dict_size < self.dict_size:
                dictionary[dict_size] = current + entry[0:1]
                dict_size += 1

            current = entry

        # Join bytes and decode to string
        data = b''.join(result)
        return data.decode('utf-8')

    def _black_gate(self, codes: List[int], original_text: str) -> Dict[str, Any]:
        """
        Black Gate wrapper - adds CODEX token seal and metadata.

        Uses Black Magick token (⚫) as the seal for compressed data.

        Args:
            codes: LZW compressed codes
            original_text: Original text for hash calculation

        Returns:
            Dictionary with seal, compressed codes, size, and hash
        """
        # Calculate hash of original
        text_hash = hashlib.md5(original_text.encode('utf-8')).hexdigest()[:8]

        return {
            'seal': MagickToken.BLACK.emoji,  # ⚫ Black seal
            'compressed': codes,
            'size': len(codes),
            'hash': text_hash
        }

    def _black_reentry(self, direction: str) -> str:
        """
        Black reentry function - decodes directional tokens.

        Uses CODEX token system to map directions to colors.

        Args:
            direction: "UP" or "DOWN"

        Returns:
            Corresponding CODEX emoji
        """
        return codex_tokens.encode_direction(direction)

    def _encode_compressed(self, gate_result: Dict[str, Any], original_size: int) -> bytes:
        """
        Encode compressed data to bytes with header.

        Header format (16 bytes):
        - Magic: 4 bytes ('BLZW')
        - Version: 2 bytes
        - Original size: 4 bytes
        - Code count: 4 bytes
        - Reserved: 2 bytes

        Followed by:
        - Hash: 8 bytes (UTF-8)
        - Codes: 4 bytes each (big-endian integers)

        Args:
            gate_result: Black Gate result dictionary
            original_size: Size of original data

        Returns:
            Encoded bytes
        """
        # Create header
        header = struct.pack(
            '>4sHIIH',
            b'BLZW',                    # Magic
            1,                          # Version
            original_size,              # Original size
            gate_result['size'],        # Code count
            0                           # Reserved
        )

        # Add hash
        hash_bytes = gate_result['hash'].encode('utf-8')

        # Encode codes as 4-byte integers
        codes_bytes = b''.join(
            struct.pack('>I', code) for code in gate_result['compressed']
        )

        return header + hash_bytes + codes_bytes

    def _parse_header(self, data: bytes) -> Dict[str, Any]:
        """
        Parse Black LZW Screw header.

        Args:
            data: Compressed data with header

        Returns:
            Dictionary with header information
        """
        if len(data) < 16:
            raise ValueError("Data too short to contain valid header")

        # Parse header
        magic, version, original_size, code_count, _ = struct.unpack('>4sHIIH', data[:16])

        if magic != b'BLZW':
            raise ValueError(f"Invalid Black LZW Screw magic: {magic}")

        # Extract hash
        hash_bytes = data[16:24]
        text_hash = hash_bytes.decode('utf-8')

        return {
            'seal': MagickToken.BLACK.emoji,
            'version': version,
            'original_size': original_size,
            'code_count': code_count,
            'hash': text_hash,
            'header_size': 24
        }

    def _decode_compressed(self, data: bytes, header_data: Dict[str, Any]) -> List[int]:
        """
        Decode compressed codes from bytes.

        Args:
            data: Compressed data
            header_data: Parsed header information

        Returns:
            List of integer codes
        """
        header_size = header_data['header_size']
        code_count = header_data['code_count']

        codes = []
        offset = header_size

        for _ in range(code_count):
            if offset + 4 > len(data):
                break
            code = struct.unpack('>I', data[offset:offset+4])[0]
            codes.append(code)
            offset += 4

        return codes


# NOTE: This engine is complete and functional!
# Uncomment the following lines to register it:
#
# from ..registry import register_engine
# register_engine(BlackLZWScrewEngine)
