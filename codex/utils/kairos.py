"""
KAIROS Module - CODEX Adjacency Law Enforcement and Gray Detection

Implements formal adjacency validation, Gray detection, and K-series repair
for the CODEX symbolic system. Integrates with both the symbolic dynamics
engine and the CODEX token system.

Based on:
- Adjacency law: adj(a,b) ⟺ (index(b) - index(a)) mod 7 ∈ {+1,-1}
- Gray detection: symbolic (adjacency violations) + spectral (Dirichlet energy)
- K-series repair: K1=[Blue,Green,Red] flush, K2=[Brown,Blue] stabilize
"""

from enum import IntEnum
from typing import List, Tuple, Optional, Dict
from collections import Counter

try:
    import numpy as np
    HAS_NUMPY = True
except ImportError:
    HAS_NUMPY = False

from .tokens import MagickToken, codex_tokens


class KairosMode(IntEnum):
    """KAIROS operational modes"""
    PASSIVE = 0      # Monitor only
    DEFENSIVE = 1    # Detect and flag
    ACTIVE = 2       # Detect and repair
    WEAPONIZED = 3   # Hunt and eliminate


class GrayThreat:
    """Detected Gray corruption with forensic details"""

    def __init__(
        self,
        index: int,
        token_a: str,
        token_b: str,
        distance: int,
        timestamp: Optional[int] = None
    ):
        self.index = index
        self.token_a = token_a
        self.token_b = token_b
        self.distance = distance
        self.timestamp = timestamp
        self.severity = self._compute_severity()

    def _compute_severity(self) -> float:
        """Compute threat severity based on distance"""
        # Distance 2-3 = medium, distance 4+ = critical
        if self.distance <= 1:
            return 0.0
        elif self.distance == 2:
            return 0.4
        elif self.distance == 3:
            return 0.7
        else:
            return 1.0

    def __repr__(self) -> str:
        return f"GrayThreat(idx={self.index}, {self.token_a}→{self.token_b}, dist={self.distance}, severity={self.severity:.2f})"


class KairosEngine:
    """KAIROS engine for adjacency enforcement and Gray detection"""

    # Symbolic gray threshold (normalized)
    TAU_SYM = 0.05

    # Spectral gray threshold
    TAU_SPEC = 0.3

    # K-series repair sequences
    K1_FLUSH = [MagickToken.BLUE, MagickToken.GREEN, MagickToken.RED]
    K2_STABILIZE = [MagickToken.BROWN, MagickToken.BLUE]

    # Circular index mapping (0-6) for adjacency calculation
    # Order: BLACK, WHITE, YELLOW, BROWN, RED, GREEN, BLUE
    TOKEN_INDEX = {
        MagickToken.BLACK: 0,
        MagickToken.WHITE: 1,
        MagickToken.YELLOW: 2,
        MagickToken.BROWN: 3,
        MagickToken.RED: 4,
        MagickToken.GREEN: 5,
        MagickToken.BLUE: 6,
    }

    def __init__(self, mode: KairosMode = KairosMode.ACTIVE):
        self.mode = mode
        self.threat_log: List[GrayThreat] = []
        self.repair_count = 0
        self.quarantine: List[List[MagickToken]] = []

    # --- Adjacency validation ---

    @classmethod
    def adjacent(cls, a: MagickToken, b: MagickToken) -> bool:
        """Check if two tokens are adjacent (±1 mod 7)"""
        idx_a = cls.TOKEN_INDEX[a]
        idx_b = cls.TOKEN_INDEX[b]
        diff = (idx_b - idx_a) % 7
        return diff in (1, 6)  # +1 or -1 (which is 6 in mod 7)

    @classmethod
    def adjacency_distance(cls, a: MagickToken, b: MagickToken) -> int:
        """Compute shortest circular distance between tokens"""
        idx_a = cls.TOKEN_INDEX[a]
        idx_b = cls.TOKEN_INDEX[b]
        diff = abs(idx_b - idx_a) % 7
        return min(diff, 7 - diff)

    def violations(self, seq: List[MagickToken]) -> int:
        """Count adjacency violations in sequence"""
        return sum(
            1 for i in range(len(seq) - 1)
            if not self.adjacent(seq[i], seq[i + 1])
        )

    def sym_gray_score(self, seq: List[MagickToken]) -> float:
        """Compute symbolic gray score (normalized violation rate)"""
        n = max(1, len(seq) - 1)
        return self.violations(seq) / n

    def spec_gray_score(self, psi, L) -> float:
        """Compute spectral gray score using Laplacian

        Note: Requires numpy. Returns 0.0 if numpy not available.
        """
        if not HAS_NUMPY:
            return 0.0
        num = psi.T @ L @ psi
        den = max(1e-12, psi.T @ psi)
        return float(num / den)

    # --- Gray detection ---

    def detect_gray(self, seq: List[MagickToken], timestamp: Optional[int] = None) -> List[GrayThreat]:
        """Detect all Gray violations in sequence"""
        threats = []
        for i in range(len(seq) - 1):
            if not self.adjacent(seq[i], seq[i + 1]):
                dist = self.adjacency_distance(seq[i], seq[i + 1])
                threat = GrayThreat(
                    index=i,
                    token_a=seq[i].emoji,
                    token_b=seq[i + 1].emoji,
                    distance=dist,
                    timestamp=timestamp
                )
                threats.append(threat)
                self.threat_log.append(threat)

        return threats

    # --- Repair strategies ---

    def repair_greedy(self, seq: List[MagickToken], window: int = 3) -> List[MagickToken]:
        """Greedy local repair: swap to fix adjacency violations"""
        seq = seq.copy()
        L = len(seq)

        for i in range(L - 1):
            if not self.adjacent(seq[i], seq[i + 1]):
                # Try to find an adjacent token in the window
                left = max(0, i - window)
                right = min(L, i + 2 + window)
                neighborhood = seq[left:right]

                # Count votes for each token
                votes = Counter(neighborhood)

                # Find best adjacent token to seq[i]
                best_token = None
                best_score = -1

                for token in MagickToken:
                    if self.adjacent(seq[i], token):
                        score = votes.get(token, 0)
                        if score > best_score:
                            best_score = score
                            best_token = token

                if best_token:
                    seq[i + 1] = best_token
                    self.repair_count += 1

        return seq

    def repair_k1_flush(self, seq: List[MagickToken], violation_idx: int) -> List[MagickToken]:
        """Apply K1 flush sequence at violation point"""
        seq = seq.copy()
        # Insert K1 sequence after violation
        seq[violation_idx + 1:violation_idx + 1] = self.K1_FLUSH
        self.repair_count += 1
        return seq

    def repair_k2_stabilize(self, seq: List[MagickToken], violation_idx: int) -> List[MagickToken]:
        """Apply K2 stabilize sequence at violation point"""
        seq = seq.copy()
        # Insert K2 sequence after violation
        seq[violation_idx + 1:violation_idx + 1] = self.K2_STABILIZE
        self.repair_count += 1
        return seq

    def repair_sequence(
        self,
        seq: List[MagickToken],
        max_attempts: int = 3
    ) -> Tuple[List[MagickToken], bool]:
        """Full repair protocol with escalation

        Returns:
            (repaired_sequence, success)
        """
        if self.mode == KairosMode.PASSIVE:
            return seq, False

        seq = seq.copy()

        for attempt in range(max_attempts):
            threats = self.detect_gray(seq)

            if not threats:
                return seq, True

            if attempt == 0:
                # Try greedy repair
                seq = self.repair_greedy(seq)
            elif attempt == 1:
                # Escalate to K1 flush
                for threat in threats:
                    seq = self.repair_k1_flush(seq, threat.index)
            else:
                # Final escalation to K2 stabilize
                for threat in threats:
                    seq = self.repair_k2_stabilize(seq, threat.index)

        # If still failing after max_attempts, quarantine
        if self.violations(seq) > 0:
            self.quarantine.append(seq)
            return seq, False

        return seq, True

    # --- Forensics ---

    def get_threat_report(self) -> Dict:
        """Generate forensic report of detected threats"""
        if not self.threat_log:
            return {
                "total_threats": 0,
                "avg_severity": 0.0,
                "critical_count": 0,
                "repair_count": self.repair_count,
                "quarantine_count": len(self.quarantine)
            }

        severities = [t.severity for t in self.threat_log]
        critical = sum(1 for s in severities if s >= 0.7)

        return {
            "total_threats": len(self.threat_log),
            "avg_severity": sum(severities) / len(severities),
            "critical_count": critical,
            "repair_count": self.repair_count,
            "quarantine_count": len(self.quarantine),
            "recent_threats": self.threat_log[-10:]  # Last 10
        }

    def clear_log(self):
        """Clear threat log and reset counters"""
        self.threat_log.clear()
        self.repair_count = 0
        self.quarantine.clear()


# --- Convenience functions ---

def validate_sequence(seq: List[MagickToken]) -> Tuple[bool, List[GrayThreat]]:
    """Validate a sequence for adjacency compliance

    Returns:
        (is_valid, list_of_threats)
    """
    engine = KairosEngine(mode=KairosMode.PASSIVE)
    threats = engine.detect_gray(seq)
    return len(threats) == 0, threats


def repair_sequence(seq: List[MagickToken]) -> Tuple[List[MagickToken], bool]:
    """Repair a sequence to enforce adjacency law

    Returns:
        (repaired_sequence, success)
    """
    engine = KairosEngine(mode=KairosMode.ACTIVE)
    return engine.repair_sequence(seq)


def is_adjacent(a: MagickToken, b: MagickToken) -> bool:
    """Quick check if two tokens are adjacent"""
    return KairosEngine.adjacent(a, b)
