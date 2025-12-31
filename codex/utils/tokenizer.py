"""
Tokenization utilities for symbolic compression engines.

Provides tokenization logic for converting between UTF-8 text
and symbolic token representations.
"""

from typing import List, Dict, Tuple
import re


class SymbolicTokenizer:
    """
    Base tokenizer for symbolic compression.

    Converts text/data into symbolic tokens for compression engines
    that operate on symbolic grammars rather than raw bytes.
    """

    def __init__(self, token_map: Dict[str, str]):
        """
        Initialize tokenizer with a token mapping.

        Args:
            token_map: Dictionary mapping patterns to tokens
        """
        self.token_map = token_map
        self.reverse_map = {v: k for k, v in token_map.items()}

    def tokenize(self, text: str) -> List[str]:
        """
        Convert text into tokens.

        Args:
            text: Input text

        Returns:
            List of tokens
        """
        tokens = []
        i = 0
        while i < len(text):
            matched = False
            # Try to match longest pattern first
            for pattern in sorted(self.token_map.keys(), key=len, reverse=True):
                if text[i:i+len(pattern)] == pattern:
                    tokens.append(self.token_map[pattern])
                    i += len(pattern)
                    matched = True
                    break
            if not matched:
                # Single character fallback
                tokens.append(text[i])
                i += 1
        return tokens

    def detokenize(self, tokens: List[str]) -> str:
        """
        Convert tokens back to text.

        Args:
            tokens: List of tokens

        Returns:
            Reconstructed text
        """
        result = []
        for token in tokens:
            if token in self.reverse_map:
                result.append(self.reverse_map[token])
            else:
                result.append(token)
        return ''.join(result)


class CodexTokenizer(SymbolicTokenizer):
    """
    Codex-specific tokenizer using 7-token grammar.

    Based on the Codex compression specification with fixed token alphabet.
    """

    # Codex 7-token alphabet + 3 meta tokens
    DEFAULT_TOKENS = {
        # Core operators (from category theory morphisms)
        '∘': 'COMPOSE',      # Function composition
        '⊗': 'TENSOR',       # Tensor product
        '→': 'MORPH',        # Morphism/arrow
        '∫': 'INTEGRATE',    # Integration operator
        '∂': 'PARTIAL',      # Partial derivative
        '∇': 'GRADIENT',     # Gradient/del operator
        '⊕': 'DIRECTSUM',    # Direct sum

        # Meta tokens
        '⟨': 'LANGLE',       # Left angle bracket
        '⟩': 'RANGLE',       # Right angle bracket
        '≡': 'EQUIV',        # Equivalence
    }

    def __init__(self, custom_tokens: Dict[str, str] = None):
        """
        Initialize Codex tokenizer.

        Args:
            custom_tokens: Optional additional token mappings
        """
        tokens = self.DEFAULT_TOKENS.copy()
        if custom_tokens:
            tokens.update(custom_tokens)
        super().__init__(tokens)

    def encode_numeric(self, text: str) -> List[str]:
        """
        Encode numeric patterns symbolically.

        Converts mathematical expressions to symbolic token sequences.

        Args:
            text: Input mathematical text

        Returns:
            Token sequence
        """
        # Replace common mathematical patterns
        replacements = [
            (r'd/dx', '∂'),
            (r'compose', '∘'),
            (r'integral', '∫'),
            (r'->', '→'),
        ]

        processed = text
        for pattern, token in replacements:
            processed = processed.replace(pattern, token)

        return self.tokenize(processed)


def create_lzw_tokenizer():
    """
    Create a tokenizer for LZW-based compression.

    Returns:
        SymbolicTokenizer configured for LZW operations
    """
    # Placeholder for future Black_LZW_Screw engine
    lzw_tokens = {
        'DICT_ADD': 'D+',
        'DICT_REF': 'D@',
        'LITERAL': 'L',
    }
    return SymbolicTokenizer(lzw_tokens)
