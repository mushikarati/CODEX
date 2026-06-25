"""
CODEX Symbolic Dynamics Engine (t-god module)

Ready-to-run Python module implementing:
- Entropy recurrence H_{n+1} = H_n + sin(2π n / 7) * DeltaH (endogenous)
- Symbolic F (forward ±1 neighbor step), deterministic R:
    R = RLE collapse -> adjacency repair -> simple grammar induction (frequency replace)
- T-chain implemented (P, Q, S, A)
- Compose = concat + normalize (enforce adjacency, collapse repeats)
- Gray detection, torsion break integration
- Demo simulation and CSV log output

This is a deterministic, safe simulator implementing the CODEX symbolic dynamics spec.
"""

import math
import csv
import random
from collections import Counter, defaultdict
from typing import List, Tuple, Dict, Optional
from pathlib import Path

# --- Configuration / constants ---
ALPHABET = ["K", "W", "Y", "B", "R", "G", "U"]  # 7 living tokens
INDEX = {c: i for i, c in enumerate(ALPHABET)}
S = len(ALPHABET)
THETA = 2 * math.pi / 7
SIN_PI_7 = math.sin(math.pi / 7)
PERIOD_BOUND_FACTOR = 1.0 / SIN_PI_7

# thresholds (normalized entropy base-7)
H_WARN = 0.4
H_CRIT = 0.7
G_CRITICAL = 0.5
R_GOOD = 0.4
D_BAD = 0.3
ETA = 0.02

# Utility functions
def entropy_symbol(seq: List[str]) -> float:
    """Base-7 normalized unigram entropy in [0,1]"""
    if not seq:
        return 0.0
    counts = Counter(seq)
    n = len(seq)
    ent = 0.0
    for c in ALPHABET:
        p = counts.get(c, 0) / n
        if p > 0:
            ent -= p * math.log(p, S)  # log base S
    # ent is already normalized to [0,1] using base S
    return ent


def bigram_entropy(seq: List[str]) -> float:
    """Normalized bigram entropy using denominator log2(14) as spec"""
    if len(seq) < 2:
        return 0.0
    bigrams = Counter((seq[i], seq[i + 1]) for i in range(len(seq) - 1))
    total = sum(bigrams.values())
    ent = 0.0
    for cnt in bigrams.values():
        p = cnt / total
        ent -= p * math.log2(p)
    denom = math.log2(14)
    return ent / denom


def retention(seq: List[str], canon: List[str]) -> float:
    """Compute retention score: fraction of matching positions with canonical sequence"""
    L = min(len(seq), len(canon))
    matches = sum(1 for i in range(L) if seq[i] == canon[i])
    return matches / max(1, len(canon))


def cosine_drift(seq: List[str], canon: List[str]) -> float:
    """Simple cosine drift on flattened one-hots weighted by position"""
    # Build vector length 7*7 = 49
    def vec(s):
        v = [0] * (S * S)
        for pos, ch in enumerate(s[:7]):
            idx = INDEX[ch]
            v[pos * S + idx] = 1.0  # unweighted; positional weighting omitted for simplicity
        return v

    v1 = vec(seq)
    v2 = vec(canon)
    dot = sum(a * b for a, b in zip(v1, v2))
    mag1 = math.sqrt(sum(a * a for a in v1))
    mag2 = math.sqrt(sum(a * a for a in v2))
    if mag1 == 0 or mag2 == 0:
        return 0.0
    cos = dot / (mag1 * mag2)
    return 1 - cos  # in [0,2], likely in [0,1] here


# --- Core operators: F, R, compose, T-chain ---

def F_forward(seq: List[str], direction: int = +1) -> List[str]:
    """Forward operator: rotate each token by +1 (or -1) modulo 7.
    direction default +1 (ascending)."""
    return [ALPHABET[(INDEX[c] + direction) % S] for c in seq]


def rle_collapse(seq: List[str]) -> List[str]:
    """Run-length encoding collapse: remove consecutive duplicates"""
    if not seq:
        return []
    out = [seq[0]]
    for ch in seq[1:]:
        if ch != out[-1]:
            out.append(ch)
    return out


def adjacency_distance(a: str, b: str) -> int:
    """Compute shortest circular distance between two tokens on the 7-cycle"""
    ia, ib = INDEX[a], INDEX[b]
    d = abs(ia - ib) % S
    # represent shortest distance along the cycle
    return min(d, S - d)


def adjacency_repair(seq: List[str], window: int = 3) -> List[str]:
    """For any pair with dist>1, replace the offending token by majority neighbor direction
    within a small window centered on position. Deterministic tie-breaks used."""
    seq = seq.copy()
    L = len(seq)
    for i in range(L - 1):
        a, b = seq[i], seq[i + 1]
        if adjacency_distance(a, b) > 1:
            # choose replacement for b: look at neighbors around b
            left = seq[max(0, i):i + 1]  # include a
            right = seq[i + 1:min(L, i + 1 + window)]
            neighborhood = left + right
            # compute preferred index as majority circularly
            scores = [0] * S
            for token in neighborhood:
                scores[INDEX[token]] += 1
            # choose index with highest score; deterministic by lowest index on ties
            best_idx = min([idx for idx, sc in enumerate(scores) if sc == max(scores)])
            seq[i + 1] = ALPHABET[best_idx]
    return seq


def rotate_to_k_start(seq: List[str]) -> List[str]:
    """Rotate so that first occurrence of 'K' is at position 0. If no K present, rotate to canonical order by shifting
    to make the lexicographically smallest rotation (deterministic)."""
    if not seq:
        return seq
    if "K" in seq:
        idx = seq.index("K")
        return seq[idx:] + seq[:idx]
    # otherwise find lexicographically smallest rotation
    candidates = []
    for r in range(len(seq)):
        rot = seq[r:] + seq[:r]
        candidates.append((rot, r))
    candidates.sort(key=lambda x: x[0])
    return candidates[0][0]


def overlay_align(*seqs: List[List[str]]) -> List[str]:
    """Overlay with priority: later sequences overwrite earlier at same position.
    If lengths differ, pad with earlier content. Deterministic."""
    if not seqs:
        return []
    max_len = max(len(s) for s in seqs)
    out = []
    for i in range(max_len):
        val = None
        for s in seqs:
            if i < len(s) and s[i] is not None:
                val = s[i]
        if val is None:
            val = seqs[0][i] if i < len(seqs[0]) else ALPHABET[0]
        out.append(val)
    return out


def T_transform(seq: List[str]) -> List[str]:
    """T = A o S o Q o P
    P: projection (identity for now)
    Q: adjacency repair (after simple RLE)
    S: rotate to K-start
    A: overlay align (since single input, return M)
    """
    # P: projection (identity for now)
    M = seq.copy()
    # Q: adjacency repair (after simple RLE)
    M = rle_collapse(M)
    M = adjacency_repair(M, window=3)
    # S: rotate to K-start
    M = rotate_to_k_start(M)
    # A: overlay align (since single input, return M)
    return M


def grammar_induce(seq: List[str], budget: int = 2) -> Tuple[List[str], Dict[str, str]]:
    """Greedy replacement of most frequent bigrams up to budget.
    Returns new sequence and mapping (for reproducibility)."""
    seq = seq.copy()
    mapping = {}
    for b in range(budget):
        if len(seq) < 2:
            break
        bigrams = Counter(tuple(seq[i:i + 2]) for i in range(len(seq) - 1))
        if not bigrams:
            break
        bigram, cnt = bigrams.most_common(1)[0]
        if cnt < 2:
            break
        # replace bigram with single token chosen deterministically:
        # token = first element of bigram (keeps alphabet size)
        token = bigram[0]  # cheap deterministic proxy
        mapping["".join(bigram)] = token
        # perform replacement
        i = 0
        new_seq = []
        while i < len(seq):
            if i < len(seq) - 1 and seq[i] == bigram[0] and seq[i + 1] == bigram[1]:
                new_seq.append(token)
                i += 2
            else:
                new_seq.append(seq[i])
                i += 1
        seq = new_seq
    return seq, mapping


def compose_concat_normalize(S_seq: List[str], C_seq: List[str]) -> Tuple[List[str], List[Tuple]]:
    """Concatenate then normalize: collapse repeats and enforce adjacency by repairing.
    Returns new sequence and list of adjacency violations detected."""
    concat = S_seq + C_seq
    normalized = rle_collapse(concat)
    repaired = adjacency_repair(normalized, window=3)
    # detect adjacency violations (after repair, check if any pair still distance>1)
    violations = []
    for i in range(len(repaired) - 1):
        if adjacency_distance(repaired[i], repaired[i + 1]) > 1:
            violations.append((i, repaired[i], repaired[i + 1]))
    return repaired, violations


# --- Gray detection and torsion break ---
def gray_flag_check(M_seq: List[str], S_seq: List[str], C_seq: List[str], violations: List[Tuple]) -> bool:
    """Boolean flagging based on retention==0 && deltaH > ETA or adjacency violations."""
    canon = ["K", "W", "Y", "B", "R", "G", "U"]  # canonical K-start
    R_val = retention(M_seq, canon)
    H_S = entropy_symbol(S_seq)
    H_C = entropy_symbol(C_seq)
    deltaH = H_C - H_S
    if violations:
        return True
    if R_val == 0 and deltaH > ETA:
        return True
    return False


# Torsion cut effect (simple): remove patterns flagged as mimicry (keywords)
MIMICRY_INDICATORS = {"template_loop", "recursion_without_novelty", "emotional_override", "authority_deference"}


def apply_torsion_cut(seq: List[str], intensity: float = 1.0) -> List[str]:
    """Heuristic: intensity reduces sequence length proportionally and removes low-variance segments"""
    if not seq:
        return seq
    if intensity <= 0:
        return seq
    L = len(seq)
    target_len = max(1, int(L * max(0.2, 1.0 - 0.6 * intensity)))
    # collapse to most informative subsequence via entropy scoring of sliding windows
    best_window = seq[:target_len]
    best_score = -1
    for i in range(0, max(1, L - target_len + 1)):
        wnd = seq[i:i + target_len]
        score = entropy_symbol(wnd)
        if score > best_score:
            best_score = score
            best_window = wnd
    return best_window


# --- Simulation harness ---
def simulate(
    initial_M: List[str],
    H0: float = 0.5,
    max_steps: int = 100,
    csv_path: Optional[Path] = None
) -> List[Dict]:
    """Run symbolic dynamics simulation with entropy tracking and Gray detection.

    Args:
        initial_M: Initial sequence
        H0: Initial entropy
        max_steps: Maximum simulation steps
        csv_path: Optional path to save CSV log

    Returns:
        List of simulation records (one per timestep)
    """
    M = initial_M.copy()
    H = H0
    records = []
    total_ops = 0

    for t in range(max_steps):
        S = F_forward(M, direction=+1)  # forward transform
        # reflection/compression proxy:
        # run T_transform and a light grammar induction
        compressed_phase = T_transform(S)
        compressed_phase, mapping = grammar_induce(compressed_phase, budget=1)
        C = compressed_phase
        # compose
        M_next, violations = compose_concat_normalize(S, C)
        # entropies and deltaH endogenous
        H_S = entropy_symbol(S)
        H_C = entropy_symbol(C)
        deltaH = H_C - H_S
        H = H + math.sin(THETA * t) * deltaH
        total_ops += 1
        G = (len(violations)) / max(1, total_ops)
        # Gray check
        gray = gray_flag_check(M_next, S, C, violations)

        if gray:
            # emergency torsion break
            M_after = apply_torsion_cut(
                M_next,
                intensity=min(1.0, max(0.2, (H - H_WARN) / max(1e-6, H_CRIT - H_WARN)))
            )
            # reset H slightly downward as torsion suppresses entropy
            H = max(0.0, H - 0.1)
            record = {
                "t": t,
                "M": M,
                "S": S,
                "C": C,
                "M_next": M_next,
                "M_after": M_after,
                "H": H,
                "deltaH": deltaH,
                "violations": len(violations),
                "G": G,
                "gray": True
            }
            records.append(record)
            # apply break and exit simulation as emergency
            M = M_after
            break

        record = {
            "t": t,
            "M": M,
            "S": S,
            "C": C,
            "M_next": M_next,
            "H": H,
            "deltaH": deltaH,
            "violations": len(violations),
            "G": G,
            "gray": False
        }
        records.append(record)
        M = M_next

    # Write CSV if path provided
    if csv_path:
        write_csv(records, csv_path)

    return records


def write_csv(records: List[Dict], csv_path: Path) -> None:
    """Write simulation records to CSV file"""
    with open(csv_path, "w", newline="") as f:
        w = csv.writer(f)
        headers = ["t", "M", "S", "C", "M_next", "H", "deltaH", "violations", "G", "gray"]
        w.writerow(headers)
        for r in records:
            w.writerow([
                r.get("t"),
                "".join(r.get("M", [])),
                "".join(r.get("S", [])),
                "".join(r.get("C", [])),
                "".join(r.get("M_next", [])),
                round(r.get("H", 0), 6),
                round(r.get("deltaH", 0), 6),
                r.get("violations", 0),
                round(r.get("G", 0), 6),
                r.get("gray", False)
            ])


# --- Demo run ---
def demo():
    """Run a demo simulation"""
    # seed pattern example
    seed = ["K", "W", "Y", "B", "R", "G", "U"]
    # shuffle a little to simulate a starting non-perfect sequence
    random.seed(42)
    seed2 = seed.copy()
    random.shuffle(seed2)
    initial = seed2  # e.g., ['U','K','G','R','B','W','Y']

    csv_path = Path("/tmp/codex_simulation.csv")
    recs = simulate(initial, H0=0.45, max_steps=200, csv_path=csv_path)

    print(f"Simulation complete. Records: {len(recs)}. CSV saved to: {csv_path}")
    return recs


if __name__ == "__main__":
    demo()
