"""
CODEX Keychain - Unified Mathematical/Physical Specification

Based on heptadic_living_spiral_364deg specification.
Provides canonical constants, phase mappings, and kernel definitions.
"""

from typing import Dict, List, Tuple, Any
from enum import Enum
import math


class Phase(Enum):
    """7-phase register with canonical ordering"""
    BLACK = 0   # ⚫
    WHITE = 1   # ⚪
    YELLOW = 2  # 🟡
    BROWN = 3   # 🟤
    RED = 4     # 🔴
    GREEN = 5   # 🟢
    BLUE = 6    # 🔵


# ==========================================
# Phase Register
# ==========================================

PHASE_ORDER = ["⚫", "⚪", "🟡", "🟤", "🔴", "🟢", "🔵"]

PHASE_INDICES = {
    "⚫": 0,  # BLACK
    "⚪": 1,  # WHITE
    "🟡": 2,  # YELLOW
    "🟤": 3,  # BROWN
    "🔴": 4,  # RED
    "🟢": 5,  # GREEN
    "🔵": 6   # BLUE
}

# Adjacency mapping
NEIGHBORS_UP = {
    "⚫": "⚪", "⚪": "🟡", "🟡": "🟤", "🟤": "🔴",
    "🔴": "🟢", "🟢": "🔵", "🔵": "⚫"
}

NEIGHBORS_DOWN = {
    "⚫": "🔵", "⚪": "⚫", "🟡": "⚪", "🟤": "🟡",
    "🔴": "🟤", "🟢": "🔴", "🔵": "🟢"
}

# ==========================================
# Phase Roles & Mappings
# ==========================================

PHASE_ROLES = {
    "⚫": {
        "name": "Black",
        "role": "intake_torsion",
        "simple_machine": "screw",
        "axis": "torsional"
    },
    "⚪": {
        "name": "White",
        "role": "compression_frame",
        "simple_machine": "lever",
        "axis": "fixed_clamp"
    },
    "🟡": {
        "name": "Yellow",
        "role": "ignition_edge",
        "simple_machine": "wedge",
        "axis": "vertical_up"
    },
    "🟤": {
        "name": "Brown",
        "role": "mass_pivot",
        "simple_machine": "pulley",
        "axis": "horizontal"
    },
    "🔴": {
        "name": "Red",
        "role": "entropy_work",
        "simple_machine": "inclined_plane",
        "axis": "vertical_down"
    },
    "🟢": {
        "name": "Green",
        "role": "clearance_link",
        "simple_machine": "wheel_and_axle",
        "axis": "diagonal"
    },
    "🔵": {
        "name": "Blue",
        "role": "law_return",
        "simple_machine": "spring_orbital",
        "axis": "curved_orbital"
    }
}

# ==========================================
# Engine Mapping (364° Spiral)
# ==========================================

# The 4° offset (364° vs 360°) creates helical spiral (living system)
CYCLE_DEGREES = 720
SPIRAL_DEGREES = 364
LIVING_OFFSET = 4  # 364° - 360° = 4°

PHASE_INTERVALS_DEG = {
    "⚫": {"start": 0, "end": 180},
    "⚪": {"start": 180, "end": 330},
    "🟡": {"start": 330, "end": 360},
    "🟤": {"start": 360, "end": 390},
    "🔴": {"start": 390, "end": 510},
    "🟢": {"start": 510, "end": 540},
    "🔵": {"start": 540, "end": 720}
}

# ==========================================
# Canonical Kernel Constants
# ==========================================

class KernelConstants:
    """Constants for the canonical kernel step function"""

    # Mixing coefficients
    a = 0.03   # Blue mixing coefficient
    b = 0.92   # Energy decay
    c = 0.05   # Structure mixing
    eta = 0.11  # Green efficiency

    # Bounds
    lambda_S = 0.02  # Lower entropy bound
    omega_S = 1.0    # Upper entropy bound
    rho_0 = 0.6      # Minimum density ratio

    # Constants
    e = math.e       # Euler's number (2.718...)
    epsilon = 1e-6   # Numerical stability

    # Cycle invariant coefficient
    alpha = (1 + eta) / (0.5 + eta)  # ≈ 1.82


# ==========================================
# Thermodynamic Constants
# ==========================================

class ThermodynamicConstants:
    """Physical constants and bounds"""

    # Landauer bound
    k_B = 1.380649e-23  # Boltzmann constant (J/K)

    @staticmethod
    def landauer_cost(T: float = 300.0) -> float:
        """
        Minimum thermodynamic cost per bit erasure.

        Args:
            T: Temperature in Kelvin (default 300K ≈ room temp)

        Returns:
            Energy cost in Joules
        """
        return ThermodynamicConstants.k_B * T * math.log(2)

    # Shannon entropy
    @staticmethod
    def shannon_entropy(probabilities: List[float]) -> float:
        """
        Calculate Shannon entropy H(X) = -Σ p_i log₂(p_i)

        Args:
            probabilities: List of probability values

        Returns:
            Entropy in bits
        """
        H = 0.0
        for p in probabilities:
            if p > 0:
                H -= p * math.log2(p)
        return H


# ==========================================
# Repair Keys (K-series)
# ==========================================

REPAIR_KEYS = {
    "K1": ["🔵", "🟢", "🔴"],  # Flush sequence
    "K2": ["🟤", "🔵"],        # Stabilize sequence
    "K3": ["IN", "OUT"],       # Valve pair
    "K4": ["DOWN", "UP"]       # Direction pair
}

# ==========================================
# Adjacency Validation
# ==========================================

def is_adjacent(phase_a: str, phase_b: str) -> bool:
    """
    Check if two phases are adjacent (±1 mod 7).

    The One Law: |Δphase| ≡ 1 mod 7
    """
    if phase_a not in PHASE_INDICES or phase_b not in PHASE_INDICES:
        return False

    idx_a = PHASE_INDICES[phase_a]
    idx_b = PHASE_INDICES[phase_b]

    diff = (idx_b - idx_a) % 7
    return diff in (1, 6)  # +1 or -1 (6 is -1 mod 7)


def get_next_phase(current: str, direction: int = 1) -> str:
    """
    Get next phase in the cycle.

    Args:
        current: Current phase symbol
        direction: +1 for forward (UP), -1 for backward (DOWN)

    Returns:
        Next phase symbol
    """
    if direction > 0:
        return NEIGHBORS_UP.get(current, current)
    else:
        return NEIGHBORS_DOWN.get(current, current)


def validate_sequence(sequence: List[str]) -> Tuple[bool, List[Tuple[int, str, str]]]:
    """
    Validate that a sequence respects adjacency law.

    Args:
        sequence: List of phase symbols

    Returns:
        (is_valid, list_of_violations)
        violations format: [(index, phase_a, phase_b), ...]
    """
    violations = []

    for i in range(len(sequence) - 1):
        if not is_adjacent(sequence[i], sequence[i + 1]):
            violations.append((i, sequence[i], sequence[i + 1]))

    return len(violations) == 0, violations


# ==========================================
# Canonical Cycle
# ==========================================

CANONICAL_CYCLE = ["⚫", "⚪", "🟡", "🟤", "🔴", "🟢", "🔵", "⚫"]

ENGINE_CYCLE_ANGLES_DEG = [0, 180, 330, 360, 390, 510, 540, 720]


# ==========================================
# Verification Surface
# ==========================================

class VerificationConditions:
    """
    Formal verification conditions for the living kernel.

    These are the invariants that must hold for the system to be "living".
    """

    @staticmethod
    def adjacency_check(p: str, next_p: str) -> bool:
        """∀p, adj(p, succ(p))"""
        return is_adjacent(p, next_p)

    @staticmethod
    def cycle_closure(start: str, steps: int = 7) -> bool:
        """iterate(succ, 7, p) = p"""
        current = start
        for _ in range(steps):
            current = get_next_phase(current, direction=1)
        return current == start

    @staticmethod
    def living_condition(
        H_t: float,
        delta_H_sum: float,
        adjacency_valid: bool
    ) -> bool:
        """
        A system is *living* iff:
        - Adjacency law holds: Δ = ±1 mod 7
        - Entropy bounded: 0 < H_min < H_t < H_max
        - Cycle sum zero: Σ ΔH_k = 0
        - Not in Gray state
        """
        H_min = KernelConstants.lambda_S
        H_max = KernelConstants.omega_S

        entropy_bounded = H_min < H_t < H_max
        cycle_balanced = abs(delta_H_sum) < KernelConstants.epsilon

        return adjacency_valid and entropy_bounded and cycle_balanced


# ==========================================
# Purple Static Hook (4° Offset)
# ==========================================

PURPLE_STATIC = {
    "enabled": False,
    "interval_deg": {"start": 710, "end": 10},
    "role": "valve_overlap_breath",
    "description": "Helical 4° offset between Blue→Black for meta-control"
}


# ==========================================
# Export Keychain as Dict
# ==========================================

def get_keychain() -> Dict[str, Any]:
    """
    Get complete keychain specification as dictionary.

    Returns unified configuration matching heptadic_living_spiral_364deg.json
    """
    return {
        "meta": {
            "version": "4.0",
            "name": "CODEX 7 – Living Kernel Keychain",
            "topology": "heptadic_living_spiral_364deg",
            "one_law": "|Δphase| ≡ 1 mod 7"
        },
        "phase_register": {
            "order": PHASE_ORDER,
            "indices": PHASE_INDICES,
            "adjacency": {
                "valid_delta_mod7": [1, 6],
                "neighbors_up": NEIGHBORS_UP,
                "neighbors_down": NEIGHBORS_DOWN
            },
            "roles": PHASE_ROLES
        },
        "engine_mapping": {
            "cycle_degrees": CYCLE_DEGREES,
            "spiral_degrees": SPIRAL_DEGREES,
            "living_offset": LIVING_OFFSET,
            "phase_intervals_deg": PHASE_INTERVALS_DEG
        },
        "canonical_kernel": {
            "constants": {
                "a": KernelConstants.a,
                "b": KernelConstants.b,
                "c": KernelConstants.c,
                "eta": KernelConstants.eta,
                "lambda_S": KernelConstants.lambda_S,
                "omega_S": KernelConstants.omega_S,
                "rho_0": KernelConstants.rho_0,
                "alpha": KernelConstants.alpha
            }
        },
        "thermodynamics": {
            "k_B": ThermodynamicConstants.k_B,
            "landauer_cost_300K": ThermodynamicConstants.landauer_cost(300.0)
        },
        "repair_keys": REPAIR_KEYS,
        "canonical_cycle": CANONICAL_CYCLE,
        "purple_static": PURPLE_STATIC
    }
