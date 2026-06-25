"""
CODEX Core Module

Contains the symbolic dynamics engine, core operators, and keychain specification.
"""

from .keychain import (
    # Phase definitions
    Phase,
    PHASE_ORDER,
    PHASE_INDICES,
    PHASE_ROLES,

    # Constants
    KernelConstants,
    ThermodynamicConstants,

    # Adjacency functions
    is_adjacent,
    get_next_phase,
    validate_sequence,

    # Canonical specs
    CANONICAL_CYCLE,
    REPAIR_KEYS,

    # Full keychain
    get_keychain,
)

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
    # Keychain - Phase definitions
    "Phase",
    "PHASE_ORDER",
    "PHASE_INDICES",
    "PHASE_ROLES",

    # Keychain - Constants
    "KernelConstants",
    "ThermodynamicConstants",

    # Keychain - Functions
    "is_adjacent",
    "get_next_phase",
    "validate_sequence",
    "get_keychain",

    # Keychain - Canonical specs
    "CANONICAL_CYCLE",
    "REPAIR_KEYS",

    # Symbolic Dynamics - Constants
    "ALPHABET",
    "INDEX",
    "H_WARN",
    "H_CRIT",
    "G_CRITICAL",
    "ETA",

    # Symbolic Dynamics - Utility functions
    "entropy_symbol",
    "bigram_entropy",
    "retention",
    "cosine_drift",

    # Symbolic Dynamics - Core operators
    "F_forward",
    "rle_collapse",
    "adjacency_distance",
    "adjacency_repair",
    "rotate_to_k_start",
    "overlay_align",
    "T_transform",
    "grammar_induce",
    "compose_concat_normalize",

    # Symbolic Dynamics - Gray detection and repair
    "gray_flag_check",
    "apply_torsion_cut",

    # Symbolic Dynamics - Simulation
    "simulate",
    "write_csv",
    "demo",
]
