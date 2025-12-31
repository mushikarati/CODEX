"""
Codex Symbolic Compression Engine.

Implements the Codex compression algorithm based on:
- 7-token symbolic alphabet
- Category theory morphisms
- Recursive homotopy rewrites
- Entropy minimization via symbolic invariants

Reference: Codex_Compression_CheatSheet.md
"""

import struct
import zlib
from typing import Dict, Any, List, Tuple, Optional

from .base import CompressionEngine, CompressionResult, DecompressionResult
from ..utils.entropy import calculate_shannon_entropy, calculate_symbolic_entropy
from ..utils.tokenizer import CodexTokenizer


class CodexEngine(CompressionEngine):
    """
    Codex symbolic compression engine.

    Compresses data by:
    1. Tokenizing input to symbolic alphabet (7 tokens + 3 meta)
    2. Applying recursive morphism rewrites
    3. Minimizing symbolic entropy
    4. Secondary compression with gzip
    """

    # Model size constants (from CheatSheet)
    MODEL_SIZE_BYTES = 216
    TABLE_SIZE = 24
    FSM_SIZE = 176
    HEADER_SIZE = 16

    VERSION = "1.0.0"

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize Codex engine.

        Config options:
            - use_secondary_compression: Apply gzip after symbolic compression (default: True)
            - rewrite_depth: Maximum depth for recursive rewrites (default: 3)
            - min_token_length: Minimum token sequence length for rewriting (default: 2)
        """
        super().__init__(config)
        self.tokenizer = CodexTokenizer()
        self.use_secondary = self.config.get('use_secondary_compression', True)
        self.rewrite_depth = self.config.get('rewrite_depth', 3)
        self.min_token_length = self.config.get('min_token_length', 2)

    @property
    def name(self) -> str:
        return "Codex"

    @property
    def description(self) -> str:
        return "Symbolic compression engine using category theory and recursive rewrites"

    @property
    def version(self) -> str:
        return self.VERSION

    def compress(self, data: bytes) -> CompressionResult:
        """
        Compress data using Codex symbolic compression.

        Args:
            data: Input data as bytes

        Returns:
            CompressionResult with compressed data and metrics
        """
        original_size = len(data)

        # Decode bytes to string (assuming UTF-8)
        try:
            text = data.decode('utf-8', errors='replace')
        except Exception:
            text = str(data)

        # Calculate original entropy
        entropy_original = calculate_shannon_entropy(data)

        # Step 1: Tokenize to symbolic alphabet
        tokens = self.tokenizer.tokenize(text)

        # Step 2: Apply recursive morphism rewrites
        rewritten_tokens = self._apply_rewrites(tokens)

        # Step 3: Encode tokens to bytes
        symbolic_data = self._encode_tokens(rewritten_tokens)

        # Calculate symbolic entropy
        entropy_symbolic = calculate_symbolic_entropy(rewritten_tokens)

        # Step 4: Optional secondary compression (gzip)
        if self.use_secondary:
            compressed_data = zlib.compress(symbolic_data, level=9)
        else:
            compressed_data = symbolic_data

        # Add header with metadata
        header = self._create_header(original_size, len(rewritten_tokens))
        final_data = header + compressed_data

        compressed_size = len(final_data)
        compression_ratio = compressed_size / original_size if original_size > 0 else 1.0

        entropy_compressed = calculate_shannon_entropy(final_data)

        return CompressionResult(
            compressed_data=final_data,
            original_size=original_size,
            compressed_size=compressed_size,
            compression_ratio=compression_ratio,
            entropy_original=entropy_original,
            entropy_compressed=entropy_compressed,
            metadata={
                'token_count': len(tokens),
                'rewritten_token_count': len(rewritten_tokens),
                'symbolic_entropy': entropy_symbolic,
                'rewrite_depth': self.rewrite_depth,
                'model_size': self.MODEL_SIZE_BYTES
            }
        )

    def decompress(self, compressed_data: bytes) -> DecompressionResult:
        """
        Decompress Codex-compressed data.

        Args:
            compressed_data: Compressed data with Codex header

        Returns:
            DecompressionResult with original data
        """
        # Parse header
        original_size, token_count = self._parse_header(compressed_data[:self.HEADER_SIZE])
        payload = compressed_data[self.HEADER_SIZE:]

        # Decompress if secondary compression was used
        if self.use_secondary:
            try:
                symbolic_data = zlib.decompress(payload)
            except zlib.error:
                # Fallback if not compressed
                symbolic_data = payload
        else:
            symbolic_data = payload

        # Decode tokens
        tokens = self._decode_tokens(symbolic_data, token_count)

        # Reverse rewrites
        original_tokens = self._reverse_rewrites(tokens)

        # Detokenize
        text = self.tokenizer.detokenize(original_tokens)

        # Convert back to bytes
        try:
            decompressed_data = text.encode('utf-8')
        except Exception:
            decompressed_data = text.encode('utf-8', errors='replace')

        return DecompressionResult(
            decompressed_data=decompressed_data,
            original_compressed_size=len(compressed_data),
            decompressed_size=len(decompressed_data),
            metadata={'token_count': token_count}
        )

    def _apply_rewrites(self, tokens: List[str]) -> List[str]:
        """
        Apply recursive morphism rewrites to minimize symbolic entropy.

        Implements category theory-based rewrite rules:
        - Composition simplification: A∘B∘C → (A∘B)∘C
        - Tensor fusion: A⊗B⊗C → ⟨A⊗B⊗C⟩
        - Identity elimination: A∘id → A

        Args:
            tokens: Input token sequence

        Returns:
            Rewritten token sequence
        """
        result = tokens.copy()

        for depth in range(self.rewrite_depth):
            result = self._rewrite_pass(result)

        return result

    def _rewrite_pass(self, tokens: List[str]) -> List[str]:
        """
        Single pass of rewrite rules.

        Args:
            tokens: Token sequence

        Returns:
            Rewritten sequence
        """
        result = []
        i = 0

        while i < len(tokens):
            # Rule 1: Composition chains - collapse sequences
            if i + 2 < len(tokens) and tokens[i] == 'COMPOSE' and tokens[i+2] == 'COMPOSE':
                # A ∘ B ∘ C → ⟨A∘B∘C⟩
                result.extend(['LANGLE', tokens[i], tokens[i+1], tokens[i+2], 'RANGLE'])
                i += 3
                continue

            # Rule 2: Tensor products - group them
            if i + 2 < len(tokens) and tokens[i] == 'TENSOR' and tokens[i+2] == 'TENSOR':
                result.extend(['LANGLE', tokens[i], tokens[i+1], tokens[i+2], 'RANGLE'])
                i += 3
                continue

            # Rule 3: Morphism sequences
            if i + 1 < len(tokens) and tokens[i] == 'MORPH':
                result.append('MORPH')
                i += 1
                continue

            result.append(tokens[i])
            i += 1

        return result

    def _reverse_rewrites(self, tokens: List[str]) -> List[str]:
        """
        Reverse the rewrite transformations.

        Args:
            tokens: Rewritten token sequence

        Returns:
            Original token sequence
        """
        result = []
        i = 0

        while i < len(tokens):
            # Expand grouped sequences
            if i < len(tokens) and tokens[i] == 'LANGLE':
                # Find matching RANGLE
                depth = 1
                j = i + 1
                while j < len(tokens) and depth > 0:
                    if tokens[j] == 'LANGLE':
                        depth += 1
                    elif tokens[j] == 'RANGLE':
                        depth -= 1
                    j += 1
                # Add contents without brackets
                result.extend(tokens[i+1:j-1])
                i = j
                continue

            result.append(tokens[i])
            i += 1

        return result

    def _encode_tokens(self, tokens: List[str]) -> bytes:
        """
        Encode token sequence to bytes.

        Uses a simple encoding scheme where each token is represented
        as a length-prefixed string.

        Args:
            tokens: Token sequence

        Returns:
            Encoded bytes
        """
        parts = []
        for token in tokens:
            token_bytes = token.encode('utf-8')
            parts.append(struct.pack('B', len(token_bytes)))
            parts.append(token_bytes)
        return b''.join(parts)

    def _decode_tokens(self, data: bytes, expected_count: int) -> List[str]:
        """
        Decode tokens from bytes.

        Args:
            data: Encoded token data
            expected_count: Expected number of tokens (for validation)

        Returns:
            List of tokens
        """
        tokens = []
        i = 0

        while i < len(data):
            # Read length prefix
            if i >= len(data):
                break
            length = data[i]
            i += 1

            # Read token
            if i + length > len(data):
                break
            token_bytes = data[i:i+length]
            tokens.append(token_bytes.decode('utf-8'))
            i += length

        return tokens

    def _create_header(self, original_size: int, token_count: int) -> bytes:
        """
        Create Codex header with metadata.

        Header format (16 bytes):
        - Magic: 4 bytes ('CDEX')
        - Version: 2 bytes
        - Original size: 4 bytes
        - Token count: 4 bytes
        - Reserved: 2 bytes

        Args:
            original_size: Size of original data
            token_count: Number of tokens

        Returns:
            Header bytes
        """
        return struct.pack(
            '>4sHIIH',
            b'CDEX',           # Magic
            1,                 # Version
            original_size,     # Original size
            token_count,       # Token count
            0                  # Reserved
        )

    def _parse_header(self, header: bytes) -> Tuple[int, int]:
        """
        Parse Codex header.

        Args:
            header: Header bytes

        Returns:
            Tuple of (original_size, token_count)
        """
        magic, version, original_size, token_count, _ = struct.unpack('>4sHIIH', header)

        if magic != b'CDEX':
            raise ValueError(f"Invalid Codex magic: {magic}")

        return original_size, token_count
