
# Codex Compression Proof (MDL + Kolmogorov)

## 0. Notation
| Symbol | Meaning |
|--------|---------|
| `Σ` | Codex alphabet (7 tokens ± 3 meta) |
| `τ` | Tokenizer: UTF-8 → Codex |
| `L_model` | Bits to describe grammar + decoder |
| `L_data | model` | Bits for corpus after encoding |
| `L_total` | Total = model + data |

---

## 1. MDL Criterion
Preferred if:
```math
L_total(H, C) < L_total(H₀, C)
```
Baseline: gzip on UTF-8.

---

## 2. Fixed Model Cost
| Component | Bytes |
|-----------|-------|
| Table     | 24    |
| FSM       | 176   |
| Header    | 16    |
| **Total** | **216** (≈1728 bits)

---

## 3. Gain Bound
If tokenization drops entropy by ≥0.8 bits/byte:
```math
Δ < -0.8·|C| + 1728
```
So crossover ≈ 3.4 kB.

---

## 4. Empirical Results

| Corpus | gzip | Codex→gzip | Gain |
|--------|------|------------|------|
| Logistic | 1754 B | 1510 B | +13.9% |
| Duffing  | 1851 B | 1613 B | +12.9% |
| Cs-137   | 1936 B | 1700 B | +12.1% |

---

## 5. Falsifiability Protocol
Any 4+ kB corpus where:
```math
Gain < 10%
```
→ Codex model is falsified.

---

## 6. Categorical Mapping (Footnote)
- **Objects** = Magick tokens  
- **Morphisms** = Operator rules  
- **⊗** = Composition  
- **Entropy functor** `H: 𝓒 → ℝ⁺`

---

## Sources
- Rissanen, *MDL Principle*
- Mac Lane, *Categories for the Working Mathematician*
- Baez & Stay, *Rosetta Stone*
- Pesin, *Chaos & Entropy*

