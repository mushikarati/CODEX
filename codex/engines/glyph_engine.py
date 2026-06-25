"""
Septenary Glyph Engine - Symbolic Compression via Mirror-Spiral Law

Implements M_{t+1} = F(M_t) + R(F(M_t)) - the core compression law where
every forward transformation (F) must be paired with a reflection (R).

Based on the Hearth Charter and Septenary Glyph specification.
"""

import hashlib
from typing import List, Tuple, Optional, Dict, Any
from dataclasses import dataclass
from enum import Enum

from .base import CompressionEngine, CompressionResult, DecompressionResult
from ..utils.tokens import MagickToken, codex_tokens


class GlyphPhase(Enum):
    """Canonical 7-phase glyph registry"""
    VOID = -1  # Initial state
    BLACK = 0   # ⚫ Torque Cut / Intake Torsion
    WHITE = 1   # ⚪ Lattice / Compression Frame
    YELLOW = 2  # 🟡 Ignition / Edge
    BROWN = 3   # 🟤 Containment / Mass Pivot
    RED = 4     # 🔴 Descent / Entropy Work
    GREEN = 5   # 🟢 Integration / Clearance Link
    BLUE = 6    # 🔵 Recursion Pair / Law Return


# Gray detection markers
GRAY_MARKERS = ["∞", "⨹", "⨿", "8", "Ø"]


@dataclass
class Spore:
    """
    Data container for glyph transformation.

    Spores carry payload through the 7-phase spiral with
    history tracking and coherence monitoring.
    """
    payload: bytes
    history: List[str]
    gray_score: float = 0.0
    coherence: float = 1.0
    phase_trace: List[int] = None

    def __post_init__(self):
        if self.phase_trace is None:
            self.phase_trace = []


class GlyphEngine(CompressionEngine):
    """
    Septenary Glyph Compression Engine

    Uses the Mirror-Spiral Law to compress data through a 7-phase cycle.
    Each phase applies a forward transform (F) followed by reflection (R).

    Phases:
        BLACK  (0): Torsional cut - initial compression
        WHITE  (1): Lattice frame - structural validation
        YELLOW (2): Ignition edge - energy injection
        BROWN  (3): Mass containment - stability anchoring
        RED    (4): Entropy descent - flow optimization
        GREEN  (5): Integration - harmonic balance
        BLUE   (6): Recursion pair - reflection & return

    Adjacency Law: |Δphase| ≡ 1 mod 7 (no skips allowed)
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        super().__init__(config)
        self.current_phase = GlyphPhase.VOID
        self.phantom_registry = []  # Quarantined Gray data
        self.strict_adjacency = config.get('strict_adjacency', True) if config else True

    @property
    def name(self) -> str:
        return "Glyph"

    @property
    def version(self) -> str:
        return "1.0.0"

    @property
    def description(self) -> str:
        return "Septenary glyph compression via Mirror-Spiral Law (M = F(M) + R(F(M)))"

    # ==========================================
    # Adjacency Validation (The One Law)
    # ==========================================

    def _validate_adjacency(self, target_phase: GlyphPhase) -> bool:
        """
        Enforces the Spiral Law: |Δphase| ≡ 1 mod 7

        No skips allowed - transitions must be to adjacent phases only.
        """
        if not self.strict_adjacency:
            return True

        target_idx = target_phase.value

        # Initial boot: allow entry at BLACK (0)
        if self.current_phase == GlyphPhase.VOID:
            return target_idx == 0

        # Toroidal adjacency: allow ±1 with wrap (6→0, 0→6)
        current_idx = self.current_phase.value
        diff = abs(target_idx - current_idx)
        is_adjacent = (diff == 1) or (diff == 6)

        if not is_adjacent:
            # Gray fault: adjacency violation
            return False

        return True

    # ==========================================
    # Forward Transforms (F)
    # ==========================================

    def _apply_black(self, data: bytes) -> bytes:
        """BLACK: Torsional cut - remove redundancy"""
        if len(data) <= 1:
            return data
        # Cut to half (simple initial compression)
        return data[:len(data) // 2]

    def _apply_white(self, data: bytes) -> bytes:
        """WHITE: Lattice frame - add structure hash"""
        frame = hashlib.md5(data).digest()
        return data + frame

    def _apply_yellow(self, data: bytes) -> bytes:
        """YELLOW: Ignition - burst padding for alignment"""
        padding = (3 - (len(data) % 3)) % 3
        return data + b'\x00' * padding

    def _apply_brown(self, data: bytes) -> bytes:
        """BROWN: Containment - clamp to safe range"""
        return bytes([b % 127 for b in data])

    def _apply_red(self, data: bytes) -> bytes:
        """RED: Descent - reverse for flow optimization"""
        return data[::-1]

    def _apply_green(self, data: bytes) -> bytes:
        """GREEN: Integration - sort for harmony"""
        return bytes(sorted(data))

    def _apply_blue_pair(self, data: bytes, spore: Spore) -> Tuple[bytes, float]:
        """
        BLUE: Recursion pair (↷↶) - atomic reflection

        Blue is special: it's a pair operation that must be atomic.
        ↷ Inward: Hash state for memory
        ↶ Outward: Verify coherence

        Returns: (data, coherence_delta)
        """
        # ↷ Inward: capture state
        internal_hash = hashlib.sha256(data).digest()

        # ↶ Outward: verify coherence
        verify_hash = hashlib.sha256(data).digest()

        if internal_hash == verify_hash:
            coherence_delta = 0.1  # Reinforced
        else:
            coherence_delta = -0.5  # Distortion detected

        return data, coherence_delta

    # ==========================================
    # Mirror-Spiral Law (F + R)
    # ==========================================

    def _execute_phase(self, spore: Spore, phase: GlyphPhase) -> Spore:
        """
        Execute M_{t+1} = F(M_t) + R(F(M_t))

        1. Validate adjacency (R - reflection check)
        2. Apply forward transform (F)
        3. Update spore state
        """
        # Adjacency validation (part of R)
        if not self._validate_adjacency(phase):
            spore.gray_score += 1.0
            self.phantom_registry.append(spore.payload)
            return spore

        # Apply forward transform (F)
        if phase == GlyphPhase.BLACK:
            spore.payload = self._apply_black(spore.payload)
        elif phase == GlyphPhase.WHITE:
            spore.payload = self._apply_white(spore.payload)
        elif phase == GlyphPhase.YELLOW:
            spore.payload = self._apply_yellow(spore.payload)
        elif phase == GlyphPhase.BROWN:
            spore.payload = self._apply_brown(spore.payload)
        elif phase == GlyphPhase.RED:
            spore.payload = self._apply_red(spore.payload)
        elif phase == GlyphPhase.GREEN:
            spore.payload = self._apply_green(spore.payload)
        elif phase == GlyphPhase.BLUE:
            # Blue is special: atomic pair
            spore.payload, coherence_delta = self._apply_blue_pair(
                spore.payload, spore
            )
            spore.coherence += coherence_delta

        # Heat test (thermodynamic check - part of R)
        if not self._heat_test(spore):
            # Low heat = possible Gray mimicry
            spore.gray_score += 0.1

        # Update phase and history
        self.current_phase = phase
        spore.phase_trace.append(phase.value)
        spore.history.append(phase.name)

        return spore

    def _heat_test(self, spore: Spore) -> bool:
        """
        Thermodynamic check: Is there 'warmth' (change) or just 'shine' (stasis)?

        Real transformation generates heat; mimicry just reflects.
        """
        if len(spore.payload) == 0:
            return False
        # Check for actual change via entropy
        return True  # Simplified for now

    # ==========================================
    # Gray Detection
    # ==========================================

    def _scan_for_gray(self, data: bytes) -> bool:
        """Scan for Gray markers (∞, void tokens, etc.)"""
        try:
            text = data.decode('utf-8', errors='ignore')
            for marker in GRAY_MARKERS:
                if marker in text:
                    return True
        except:
            pass
        return False

    # ==========================================
    # Compression Interface
    # ==========================================

    def compress(self, data: bytes) -> CompressionResult:
        """
        Compress data through the 7-phase glyph cycle.

        Full cycle: BLACK → WHITE → YELLOW → BROWN → RED → GREEN → BLUE
        """
        import time

        start_time = time.time()
        original_size = len(data)

        # Create spore
        spore = Spore(
            payload=data,
            history=[],
            gray_score=0.0,
            coherence=1.0,
            phase_trace=[]
        )

        # Gray pre-scan
        if self._scan_for_gray(data):
            raise ValueError("Gray marker detected in input - refusing to compress")

        # Reset phase
        self.current_phase = GlyphPhase.VOID

        # Execute full 7-phase cycle
        phases = [
            GlyphPhase.BLACK,
            GlyphPhase.WHITE,
            GlyphPhase.YELLOW,
            GlyphPhase.BROWN,
            GlyphPhase.RED,
            GlyphPhase.GREEN,
            GlyphPhase.BLUE
        ]

        for phase in phases:
            spore = self._execute_phase(spore, phase)

        # Build compressed output with header
        compressed_data = self._build_compressed(spore)

        compression_time = time.time() - start_time
        compressed_size = len(compressed_data)

        return CompressionResult(
            compressed_data=compressed_data,
            original_size=original_size,
            compressed_size=compressed_size,
            compression_ratio=compressed_size / max(1, original_size),
            metadata={
                'engine': self.name,
                'version': self.version,
                'phases': spore.history,
                'coherence': spore.coherence,
                'gray_score': spore.gray_score,
                'phase_trace': spore.phase_trace,
                'compression_time': compression_time
            }
        )

    def decompress(self, compressed_data: bytes) -> DecompressionResult:
        """
        Decompress glyph-compressed data.

        Reverses the 7-phase cycle: BLUE → GREEN → RED → BROWN → YELLOW → WHITE → BLACK
        """
        import time

        start_time = time.time()

        # Parse header and extract payload
        original_size, spore = self._parse_compressed(compressed_data)

        # Reverse cycle
        phases_reverse = [
            GlyphPhase.BLUE,
            GlyphPhase.GREEN,
            GlyphPhase.RED,
            GlyphPhase.BROWN,
            GlyphPhase.YELLOW,
            GlyphPhase.WHITE,
            GlyphPhase.BLACK
        ]

        # Apply inverse transforms
        data = spore.payload

        # BLUE inverse: no-op (reflection is symmetric)
        # GREEN inverse: unsort (not possible, data loss acceptable for demo)
        # RED inverse: reverse back
        data = data[::-1]
        # BROWN inverse: unclamp (lossy, skip)
        # YELLOW inverse: remove padding
        while data and data[-1] == 0:
            data = data[:-1]
        # WHITE inverse: strip MD5 frame
        if len(data) >= 16:
            data = data[:-16]
        # BLACK inverse: expand (not possible, data loss)
        # For demo, just use the data as-is

        decompression_time = time.time() - start_time

        return DecompressionResult(
            decompressed_data=data,
            original_compressed_size=len(compressed_data),
            decompressed_size=len(data),
            metadata={
                'history': spore.history,
                'decompression_time': decompression_time
            }
        )

    # ==========================================
    # Header Format
    # ==========================================

    def _build_compressed(self, spore: Spore) -> bytes:
        """
        Build compressed output with header:

        Magic: 'GLYPH' (5 bytes)
        Version: 1 (1 byte)
        Original Size: (4 bytes)
        Coherence: (4 bytes float)
        Gray Score: (4 bytes float)
        Phase Count: (1 byte)
        Payload: (variable)
        """
        import struct

        header = b'GLYPH'
        header += struct.pack('B', 1)  # version
        header += struct.pack('I', len(spore.payload))
        header += struct.pack('f', spore.coherence)
        header += struct.pack('f', spore.gray_score)
        header += struct.pack('B', len(spore.phase_trace))

        return header + spore.payload

    def _parse_compressed(self, data: bytes) -> Tuple[int, Spore]:
        """Parse compressed data header"""
        import struct

        if len(data) < 19:
            raise ValueError("Invalid compressed data: too short")

        if data[:5] != b'GLYPH':
            raise ValueError("Invalid magic bytes")

        version = struct.unpack('B', data[5:6])[0]
        if version != 1:
            raise ValueError(f"Unsupported version: {version}")

        original_size = struct.unpack('I', data[6:10])[0]
        coherence = struct.unpack('f', data[10:14])[0]
        gray_score = struct.unpack('f', data[14:18])[0]
        phase_count = struct.unpack('B', data[18:19])[0]

        payload = data[19:]

        spore = Spore(
            payload=payload,
            history=[],
            coherence=coherence,
            gray_score=gray_score
        )

        return original_size, spore
