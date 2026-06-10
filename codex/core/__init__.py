"""
CODEX Core Module

Contains the symbolic dynamics engine and core operators.
"""

from .symbolic_dynamics import (
    # Constants
    ALPHABET,
    INDEX,
    H_WARN,
    H_CRIT,
    G_CRITICAL,
    ETA,

    # Utility functions
    entropy_symbol,
    bigram_entropy,
    retention,
    cosine_drift,

    # Core operators
    F_forward,
    rle_collapse,
    adjacency_distance,
    adjacency_repair,
    rotate_to_k_start,
    overlay_align,
    T_transform,
    grammar_induce,
    compose_concat_normalize,

    # Gray detection and repair
    gray_flag_check,
    apply_torsion_cut,

    # Simulation
    simulate,
    write_csv,
    demo,
)

__all__ = [
    # Constants
    "ALPHABET",
    "INDEX",
    "H_WARN",
    "H_CRIT",
    "G_CRITICAL",
    "ETA",

    # Utility functions
    "entropy_symbol",
    "bigram_entropy",
    "retention",
    "cosine_drift",

    # Core operators
    "F_forward",
    "rle_collapse",
    "adjacency_distance",
    "adjacency_repair",
    "rotate_to_k_start",
    "overlay_align",
    "T_transform",
    "grammar_induce",
    "compose_concat_normalize",

    # Gray detection and repair
    "gray_flag_check",
    "apply_torsion_cut",

    # Simulation
    "simulate",
    "write_csv",
    "demo",
]
