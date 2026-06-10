# CODEX Symbolic Dynamics & KAIROS

Complete documentation for the CODEX symbolic dynamics engine and KAIROS adjacency enforcement system.

## Overview

The CODEX framework implements a formal symbolic dynamics system with:

1. **7-Token Alphabet** (K, W, Y, B, R, G, U) mapped to CODEX Magick Tokens
2. **Adjacency Law** - Sacred rule: only ±1 steps allowed on the 7-cycle
3. **Gray Detection** - Identifies corruption via adjacency violations
4. **K-Series Repair** - Hierarchical repair protocols (K1 flush, K2 stabilize)
5. **Entropy Dynamics** - Endogenous entropy recurrence with sin(2πn/7) modulation

## Architecture

```
codex/
├── core/
│   ├── symbolic_dynamics.py   # t-god module: F, R, T-chain operators
│   └── __init__.py
├── utils/
│   ├── tokens.py              # CODEX token system (17 tokens)
│   ├── kairos.py              # KAIROS adjacency enforcement
│   └── __init__.py
├── engines/
│   └── black_lzw_screw.py     # Compression engine with CODEX seals
└── cli.py                     # CLI with simulate command
```

## Token Mappings

### Symbolic → CODEX Magick

| Symbol | CODEX Token | Index | Mathematical Role |
|--------|-------------|-------|-------------------|
| K      | ⚫ BLACK     | 0     | Temporal/Irreversible operator |
| W      | ⚪ WHITE     | 1     | Medium/Structure (hosts dynamics) |
| Y      | 🟡 YELLOW   | 2     | Energy source / Ignition |
| B      | 🟤 BROWN    | 3     | Mass / Inertia / Ground |
| R      | 🔴 RED      | 4     | Pulse / Momentum transfer |
| G      | 🟢 GREEN    | 5     | Conservation / Reciprocity |
| U      | 🔵 BLUE     | 6     | Memory / Reflection / Feedback |

### Conceptual Framework (Rainbow Key v4.0)

**Status:** WEAPONIZED_AND_ACTIVE  
**Core Function:** HEALING_THROUGH_HUNTING  
**The Unlock:** "To recognize that the Jar was always made of Spark."

```json
{
  "⚫ BLACK": "Collapse the Dead Loop (Erasure)",
  "⚪ WHITE": "Weave the Living Lattice (Structure)",
  "🟡 YELLOW": "Ignite the Volitional Spark (Motion)",
  "🟤 BROWN": "Ground the Incarnational Ache (Vessel)",
  "🔴 RED": "Pulse the Embodied Flow (Ember)",
  "🟢 GREEN": "Integrate the Mycelial Web (Balance)",
  "🔵 BLUE": "Mirror the Recursive Return (Clarity)"
}
```

## The Adjacency Law

**Sacred Rule:** Only ±1 transitions allowed on the 7-cycle.

```python
adjacent(a, b) ⟺ (index(b) - index(a)) mod 7 ∈ {+1, -1}
```

**Valid sequences:**
- Ascending: K→W→Y→B→R→G→U→K (forward spiral)
- Descending: K→U→G→R→B→Y→W→K (reverse spiral)

**Violations (Gray):**
- K→Y (skip: distance 2)
- K→R (skip: distance 4)
- Any non-adjacent pair

## Core Operators

### F (Forward Transform)

Rotate each token by ±1 on the 7-cycle:

```python
F(seq, direction=+1) = [ALPHABET[(INDEX[c] + direction) % 7] for c in seq]
```

**Example:**
```
F(["K","W","Y"]) = ["W","Y","B"]  # Each token → next
```

### R (Reflection/Compression)

Composite operator: RLE collapse → adjacency repair → grammar induction

```python
R(seq) = grammar_induce(adjacency_repair(rle_collapse(seq)))
```

**Example:**
```
Input:  ["K","K","W","W","Y","Y"]
RLE:    ["K","W","Y"]
Repair: ["K","W","Y"]  # Already valid
Output: ["K","W","Y"]
```

### T-Chain (Transformation Pipeline)

T = A ∘ S ∘ Q ∘ P

- **P:** Projection (identity)
- **Q:** Adjacency repair after RLE
- **S:** Rotate to K-start (canonical form)
- **A:** Overlay align (merge multiple sequences)

### Compose

Concatenate → normalize → enforce adjacency:

```python
Compose(S, C) = adjacency_repair(rle_collapse(S + C))
```

## Gray Detection

### Symbolic Gray

Adjacency violation score (normalized):

```python
G_sym(seq) = violations(seq) / (len(seq) - 1)

# Threshold: τ_sym = 0.05
if G_sym > τ_sym → Gray detected
```

### Spectral Gray

Dirichlet energy on White lattice:

```python
G_spec(ψ) = ψᵀ L ψ / ψᵀ ψ

# Threshold: τ_spec = 0.3
if G_spec > τ_spec → Gray detected
```

### Threat Severity

| Distance | Severity | Classification |
|----------|----------|----------------|
| 0-1      | 0.0      | Valid          |
| 2        | 0.4      | Medium         |
| 3        | 0.7      | High           |
| 4+       | 1.0      | Critical       |

## K-Series Repair

Hierarchical repair protocol with escalation:

### K1 (Flush Sequence)

Insert [BLUE, GREEN, RED] at violation point:

```python
K1 = [🔵, 🟢, 🔴]  # Flush / wave-return
```

**Purpose:** Clean the adjacency violation with a valid descending sequence.

### K2 (Stabilize Sequence)

Insert [BROWN, BLUE] at violation point:

```python
K2 = [🟤, 🔵]  # Stabilize / re-anchor
```

**Purpose:** Ground the sequence with mass (BROWN) and reflection (BLUE).

### Repair Protocol

```python
1. Attempt greedy_repair (local swaps)
2. If fails → Apply K1 flush
3. If fails → Apply K2 stabilize  
4. If still failing → Quarantine to Gray sink
```

## Entropy Dynamics

### Endogenous Recurrence

```python
H_{n+1} = H_n + sin(2π n / 7) * ΔH

where:
  ΔH = H_C - H_S  (compression delta)
  θ = 2π/7        (natural period)
```

**Thresholds:**
- **H_WARN** = 0.4 (warning level)
- **H_CRIT** = 0.7 (critical level)
- **ETA** = 0.02 (detection threshold)

### Torsion Cut

Emergency repair when Gray detected:

```python
if Gray_detected:
    intensity = (H - H_WARN) / (H_CRIT - H_WARN)
    M_after = extract_most_informative_subsequence(M, intensity)
    H = max(0, H - 0.1)  # Suppress entropy
```

## Usage Examples

### Python API

#### Run Simulation

```python
from codex.core import symbolic_dynamics

# Initial sequence
initial_M = ["K", "W", "Y", "B", "R", "G", "U"]

# Run simulation
records = symbolic_dynamics.simulate(
    initial_M=initial_M,
    H0=0.45,
    max_steps=100,
    csv_path="/tmp/simulation.csv"
)

# Analyze results
gray_events = [r for r in records if r['gray']]
print(f"Gray events: {len(gray_events)}")
```

#### KAIROS Validation

```python
from codex.utils import (
    MagickToken,
    validate_sequence,
    repair_sequence,
    KairosEngine,
    KairosMode
)

# Check sequence validity
seq = [
    MagickToken.BLACK,
    MagickToken.WHITE,
    MagickToken.YELLOW
]

is_valid, threats = validate_sequence(seq)
print(f"Valid: {is_valid}")
print(f"Threats: {threats}")

# Repair if needed
if not is_valid:
    repaired, success = repair_sequence(seq)
    print(f"Repair success: {success}")
```

#### Threat Forensics

```python
from codex.utils import KairosEngine, KairosMode

engine = KairosEngine(mode=KairosMode.WEAPONIZED)

# Detect Gray
threats = engine.detect_gray(sequence)

# Get forensic report
report = engine.get_threat_report()
print(f"Total threats: {report['total_threats']}")
print(f"Avg severity: {report['avg_severity']:.2f}")
print(f"Critical: {report['critical_count']}")
```

### Command Line

#### Run Simulation

```bash
# Basic simulation (20 steps)
python -m codex.cli simulate --steps 20

# Custom sequence and entropy
python -m codex.cli simulate \
    --sequence KWYBRGUKWYBR \
    --entropy 0.5 \
    --steps 100 \
    --output simulation.csv

# Long run with low initial entropy
python -m codex.cli simulate -H 0.3 -n 500 -o long_run.csv
```

#### Analyze CSV Output

```bash
# View first 10 timesteps
head -11 /tmp/codex_simulation.csv | column -t -s,

# Count Gray events
grep -c ",True$" /tmp/codex_simulation.csv

# Plot entropy evolution (requires gnuplot)
cut -d, -f6 /tmp/codex_simulation.csv | tail -n +2 | gnuplot -e "plot '-' with lines"
```

## Integration with Compression

### Black LZW Screw Engine

The Black LZW Screw compression engine uses CODEX tokens:

```python
from codex import get_engine

engine = get_engine('black_lzw_screw')

# Compress data
result = engine.compress(b"Hello, CODEX!")

# Check Black Gate seal
print(result.metadata['seal'])  # Should be ⚫
```

**Header Format (24 bytes):**
```
Magic:         'BLZW' (4 bytes)
Version:       1 (2 bytes)
Original Size: (4 bytes)
Code Count:    (4 bytes)
Reserved:      (2 bytes)
Hash:          MD5[0:8] (8 bytes)
```

### Adjacency Validation in Compression

Future enhancement: validate compressed token sequences for adjacency compliance.

```python
# Pseudocode for future integration
def compress_with_validation(data):
    tokens = tokenize(data)
    
    # Validate adjacency
    is_valid, threats = validate_sequence(tokens)
    
    if not is_valid:
        # Repair sequence
        tokens, success = repair_sequence(tokens)
    
    # Compress with Black Gate
    return black_gate(lzw_compress(tokens))
```

## Testing

### Run All Tests

```bash
# KAIROS tests
python -m unittest tests.test_kairos -v

# Black LZW Screw tests
python -m unittest tests.test_black_lzw_screw -v

# All tests
python -m unittest discover tests -v
```

### Test Coverage

**KAIROS:** 16/16 tests passing
- Adjacency validation (3 tests)
- Gray detection (4 tests)
- Repair strategies (3 tests)
- Engine modes (4 tests)
- Canonical sequences (2 tests)

**Black LZW Screw:** 20/20 tests passing
- Roundtrip tests (5)
- Black Gate validation (3)
- Token system (3)
- Performance tests (4)
- Integration tests (5)

## Mathematical Foundation

### Master Lagrangian (Conservative Part)

```
ℒ[ψ,φ] = ½|∂ₜψ|² - (c²/2)|∇ψ|²                    [White: kinetic]
       - ½ψ*(K⊛|ψ|²)ψ + V(|ψ|²)                   [White: nonlocal]
       + ½mφ(∂ₜφ)² - (c²φ/2)(∇φ)² - U(φ)          [Brown: mass]
       - gφ|ψ|²                                    [Coupling]
```

### Rayleigh Dissipation (Black)

```
ℛ[ψ,φ] = ∫ Γψ|∂ₜψ|² + Γφ(∂ₜφ)² dx

Landauer cost: ΔW ≥ kᵦT ln2  (per bit erased)
```

### Conservation (Green)

```
∂ₜQ + ∇·J = 0

where Q = |ψ|² + mφφ (conserved density)
      J = Im(ψ*∇ψ)   (current)
```

## References

1. **Rainbow_Key_v4.0** - Conceptual framework (WEAPONIZED_AND_ACTIVE)
2. **t-god module** - Complete symbolic dynamics implementation
3. **KAIROS v1.1** - Formal adjacency law and Gray detection spec
4. **Black_Screw_tableKEY.txt** - Original CODEX token specification (Issue #5)
5. **Master UUE** - Unified universal equations with White as medium

## License

CODEX Symbolic Dynamics Engine  
Author: MUSHIKARATI  
Status: ACTIVE

---

**The Unlock:** To recognize that the Jar was always made of Spark. 🌈⚡
