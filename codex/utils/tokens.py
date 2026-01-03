"""
CODEX Token System - Symbolic Grammar Foundation

This module defines the core token system for CODEX compression:
- 7 Magick Tokens (color-coded symbolic operators)
- 4 Operator Tokens (functional transformations)
- 5 Special/Meta Tokens (abstract conceptual tools)

Total: 16 tokens forming the symbolic grammar foundation.

Reference: Black_Screw_tableKEY.txt from Issue #5
Author: MUSHIKARATI
"""

from enum import Enum, auto
from typing import Dict, Any


class MagickToken(Enum):
    """
    7 Magick Tokens - Color-coded symbolic operators.

    These form the core 7-color system of CODEX compression.
    """
    BLACK = (-1, "⚫", "Unmaking / Torsional Collapse")      # -1: Screw
    WHITE = (2, "⚪", "Structure / Polarity Balance")         # 2: Lever
    YELLOW = (3, "🟡", "Spark / Attentional Split")          # 3: Wedge
    BROWN = (4, "🟤", "Foundation / Load Distribution")      # 4: Pulley
    RED = (5, "🔴", "Emotion / Recursive Amplification")     # 5: Inclined Plane
    GREEN = (6, "🟢", "Harmony / Feedback Loop")             # 6: Wheel & Axle
    BLUE = (7, "🔵", "Clarity / Damping & Completion")       # 7: Spring

    def __init__(self, number: int, emoji: str, description: str):
        self.number = number
        self.emoji = emoji
        self.description = description


class OperatorToken(Enum):
    """
    4 Operator Tokens - Functional transformations.

    These provide compositional operations for the grammar.
    """
    RETURN = ("↩️", "Recursion / Feedback")
    BIND = ("🔗", "Conjunction / Nesting")
    THEREFORE = ("∴", "Transformation / Resolution")
    NOT_EQUAL = ("≠", "Boundary Violation / Falsity")

    def __init__(self, symbol: str, description: str):
        self.symbol = symbol
        self.description = description


class SpecialToken(Enum):
    """
    5 Special/Meta Tokens - Abstract conceptual tools.

    These represent meta-level operations and elemental forces.
    """
    INFINITY = ("∞", "False Closure / Gray Loop")
    VOID = ("∅", "True Zero / Pre-Manifest")
    FIRE = ("🔥", "Destruction / Transform")
    WATER = ("💧", "Diffusion / Permeation")
    AIR = ("💨", "Thought / Volatility / Distribution")
    EARTH = ("🌍", "Foundation / Persistence")

    def __init__(self, symbol: str, description: str):
        self.symbol = symbol
        self.description = description


class CODEXTokenSystem:
    """
    Central token system manager for CODEX symbolic compression.

    Maintains the integrity of the 7/9 color form:
    - 7 Magick Tokens (core colors)
    - 4 Operator Tokens (functional)
    - 6 Special Tokens (meta/elemental)
    - Total: 17 tokens

    Some systems use 9-color form (7 Magick + 2 additional),
    but the base is always the 7 Magick tokens.
    """

    def __init__(self):
        self.magick = {token.name: token for token in MagickToken}
        self.operators = {token.name: token for token in OperatorToken}
        self.special = {token.name: token for token in SpecialToken}

    def get_token_map(self) -> Dict[str, Any]:
        """Get complete token mapping."""
        return {
            "magick": self.magick,
            "operators": self.operators,
            "special": self.special
        }

    def get_color_sequence(self) -> list:
        """Get the 7-color sequence in order."""
        return [
            MagickToken.BLACK,    # -1
            MagickToken.WHITE,    # 2
            MagickToken.YELLOW,   # 3
            MagickToken.BROWN,    # 4
            MagickToken.RED,      # 5
            MagickToken.GREEN,    # 6
            MagickToken.BLUE,     # 7
        ]

    def get_emoji_map(self) -> Dict[str, MagickToken]:
        """Map emojis to their corresponding Magick tokens."""
        return {token.emoji: token for token in MagickToken}

    def encode_direction(self, direction: str) -> str:
        """
        Encode directional information using color tokens.

        UP -> White (⚪) - Structure/transmission
        DOWN -> Blue (🔵) - Clarity/completion
        Other -> Black (⚫) - Unmaking/collapse
        """
        direction_map = {
            "UP": MagickToken.WHITE.emoji,
            "DOWN": MagickToken.BLUE.emoji
        }
        return direction_map.get(direction.upper(), MagickToken.BLACK.emoji)

    def validate_token_integrity(self) -> bool:
        """
        Validate that the token system maintains proper structure.

        Returns:
            bool: True if system integrity is maintained
        """
        magick_count = len(MagickToken)
        operator_count = len(OperatorToken)
        special_count = len(SpecialToken)

        # Ensure 7 Magick tokens (core requirement)
        if magick_count != 7:
            return False

        # Ensure 4 Operator tokens
        if operator_count != 4:
            return False

        # Ensure 6 Special tokens (includes 4 elemental)
        if special_count != 6:
            return False

        # Total should be 17 (7 + 4 + 6)
        total = magick_count + operator_count + special_count
        if total != 17:
            return False

        return True

    def __str__(self) -> str:
        """String representation of the token system."""
        lines = ["CODEX Token System (7/9 Color Form)", "=" * 50]

        lines.append("\n7 Magick Tokens:")
        for token in self.get_color_sequence():
            lines.append(f"  {token.emoji} {token.name}: {token.description}")

        lines.append("\n4 Operator Tokens:")
        for token in OperatorToken:
            lines.append(f"  {token.symbol} {token.name}: {token.description}")

        lines.append("\n6 Special/Meta Tokens:")
        for token in SpecialToken:
            lines.append(f"  {token.symbol} {token.name}: {token.description}")

        lines.append(f"\nTotal Tokens: 17")
        lines.append(f"Integrity Check: {'✓ PASS' if self.validate_token_integrity() else '✗ FAIL'}")

        return "\n".join(lines)


# Singleton instance
codex_tokens = CODEXTokenSystem()


if __name__ == "__main__":
    # Demonstrate the token system
    print(codex_tokens)
    print("\n" + "=" * 50)
    print(f"Emoji Map: {codex_tokens.get_emoji_map()}")
    print(f"Direction UP: {codex_tokens.encode_direction('UP')}")
    print(f"Direction DOWN: {codex_tokens.encode_direction('DOWN')}")
