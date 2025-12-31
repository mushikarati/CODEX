# Codex Framework Developer Guide

## Architecture Overview

The Codex compression framework is designed for **extensibility** and **modularity**. It makes adding new compression engines as simple as creating a single Python file.

### Directory Structure

```
codex/
├── __init__.py              # Package initialization
├── cli.py                   # Command-line interface
├── registry.py              # Engine registration system
├── engines/
│   ├── __init__.py          # Auto-registers all engines
│   ├── base.py              # Abstract base class
│   ├── codex_engine.py      # Codex implementation
│   └── black_lzw_screw.py   # Example stub for new engine
└── utils/
    ├── __init__.py
    ├── entropy.py           # Entropy calculations
    └── tokenizer.py         # Tokenization utilities
```

---

## Adding a New Compression Engine

### Step 1: Create Your Engine Class

Create a new file in `codex/engines/` (e.g., `my_engine.py`):

```python
from .base import CompressionEngine, CompressionResult, DecompressionResult
from ..utils.entropy import calculate_shannon_entropy

class MyEngine(CompressionEngine):
    """My custom compression engine."""

    def __init__(self, config=None):
        super().__init__(config)
        # Initialize your engine-specific parameters

    @property
    def name(self) -> str:
        return "MyEngine"

    @property
    def description(self) -> str:
        return "Description of my compression algorithm"

    @property
    def version(self) -> str:
        return "1.0.0"

    def compress(self, data: bytes) -> CompressionResult:
        # Implement your compression logic
        original_size = len(data)
        compressed_data = self._my_compress_logic(data)

        return CompressionResult(
            compressed_data=compressed_data,
            original_size=original_size,
            compressed_size=len(compressed_data),
            compression_ratio=len(compressed_data) / original_size,
            entropy_original=calculate_shannon_entropy(data),
            entropy_compressed=calculate_shannon_entropy(compressed_data)
        )

    def decompress(self, compressed_data: bytes) -> DecompressionResult:
        # Implement your decompression logic
        decompressed_data = self._my_decompress_logic(compressed_data)

        return DecompressionResult(
            decompressed_data=decompressed_data,
            original_compressed_size=len(compressed_data),
            decompressed_size=len(decompressed_data)
        )
```

### Step 2: Register Your Engine

Add to `codex/engines/__init__.py`:

```python
from .my_engine import MyEngine
from ..registry import register_engine

register_engine(MyEngine)
```

**That's it!** Your engine is now available via CLI and API.

---

## Using the Registry System

### Programmatic Access

```python
from codex import get_engine, list_engines

# List all available engines
engines = list_engines()
print(engines)

# Get a specific engine
engine = get_engine('myengine')

# Compress data
data = b"Hello, World!"
result = engine.compress(data)
print(f"Compressed: {result.compressed_size} bytes")

# Decompress
decompressed = engine.decompress(result.compressed_data)
```

### CLI Access

```bash
# List engines
python -m codex.cli --list

# Compress a file
python -m codex.cli compress --engine myengine input.txt

# Decompress
python -m codex.cli decompress --engine myengine input.txt.cdx

# Benchmark
python -m codex.cli benchmark --engine myengine input.txt
```

---

## Engine Interface Reference

### Required Methods

All engines must implement these abstract methods:

#### `name` (property)
- **Returns**: `str` - Engine name (used for registration)

#### `description` (property)
- **Returns**: `str` - Brief description of the engine

#### `version` (property)
- **Returns**: `str` - Version string (semantic versioning recommended)

#### `compress(data: bytes) -> CompressionResult`
- **Args**: Raw data as bytes
- **Returns**: `CompressionResult` object with:
  - `compressed_data`: Compressed bytes
  - `original_size`: Original data size
  - `compressed_size`: Compressed data size
  - `compression_ratio`: Ratio (compressed/original)
  - `entropy_original`: Shannon entropy of input (optional)
  - `entropy_compressed`: Shannon entropy of output (optional)
  - `metadata`: Dict with engine-specific metrics (optional)

#### `decompress(compressed_data: bytes) -> DecompressionResult`
- **Args**: Compressed data as bytes
- **Returns**: `DecompressionResult` object with:
  - `decompressed_data`: Original data
  - `original_compressed_size`: Compressed size
  - `decompressed_size`: Decompressed size
  - `metadata`: Additional info (optional)

### Optional Methods

#### `_validate_config()`
Override to add custom configuration validation.

#### `benchmark(data: bytes) -> Dict`
Already implemented in base class, but can be overridden for custom benchmarking.

---

## Utility Modules

### Entropy Utils (`codex.utils.entropy`)

```python
from codex.utils.entropy import (
    calculate_shannon_entropy,      # Shannon entropy in bits/byte
    calculate_symbolic_entropy,     # Entropy of token sequences
    calculate_compression_gain,     # Compression metrics
    estimate_kolmogorov_complexity, # K-complexity approximation
    calculate_mdl_score            # Minimum Description Length
)

# Example
entropy = calculate_shannon_entropy(data)
print(f"Entropy: {entropy:.4f} bits/byte")
```

### Tokenizer Utils (`codex.utils.tokenizer`)

```python
from codex.utils.tokenizer import (
    SymbolicTokenizer,    # Base tokenizer class
    CodexTokenizer,       # Codex-specific 7-token alphabet
    create_lzw_tokenizer  # LZW tokenizer factory
)

# Example
tokenizer = CodexTokenizer()
tokens = tokenizer.tokenize("Mathematical: ∫∂∇")
text = tokenizer.detokenize(tokens)
```

---

## Configuration System

Engines accept optional configuration dictionaries:

```python
config = {
    'rewrite_depth': 5,
    'use_secondary_compression': True,
    'min_token_length': 3
}

engine = get_engine('codex', config=config)
```

Configuration is validated in `_validate_config()` method.

---

## Testing Your Engine

Create tests in `tests/test_my_engine.py`:

```python
import unittest
from codex import get_engine

class TestMyEngine(unittest.TestCase):
    def setUp(self):
        self.engine = get_engine('myengine')

    def test_compress_decompress(self):
        data = b"Test data"
        result = self.engine.compress(data)
        decomp = self.engine.decompress(result.compressed_data)
        self.assertEqual(decomp.decompressed_data, data)

    def test_benchmark(self):
        data = b"Test" * 1000
        results = self.engine.benchmark(data)
        self.assertTrue(results['integrity_check'])
```

Run tests:
```bash
python -m unittest discover tests
```

---

## Best Practices

1. **Header Format**: Include a magic number and version in your compressed data header
2. **Error Handling**: Validate input and raise descriptive errors
3. **Entropy Calculation**: Always calculate entropy for comparison purposes
4. **Metadata**: Store algorithm-specific metrics in the `metadata` field
5. **Documentation**: Document your algorithm's theoretical basis
6. **Testing**: Write comprehensive tests including edge cases

---

## Examples

### Example 1: Codex Engine
See `codex/engines/codex_engine.py` for a complete implementation using:
- Symbolic tokenization
- Recursive rewrites
- Category theory morphisms
- Secondary compression

### Example 2: Black_LZW_Screw Stub
See `codex/engines/black_lzw_screw.py` for a template showing:
- Proper class structure
- Header format
- Stub methods for future implementation
- Configuration handling

---

## Troubleshooting

### Engine not appearing in `--list`
- Ensure the engine is imported in `codex/engines/__init__.py`
- Verify `register_engine()` is called
- Check for syntax errors in your engine file

### Import errors
- Make sure all `__init__.py` files are present
- Use relative imports within the package (e.g., `from .base import ...`)

### Compression ratio > 1.0
- This is normal for small files or incompressible data
- Consider adding a fallback to store uncompressed data
- Include model size in your calculations (see MDL criterion)

---

## Advanced Topics

### Custom Tokenizers
Create domain-specific tokenizers by extending `SymbolicTokenizer`:

```python
from codex.utils.tokenizer import SymbolicTokenizer

class DNATokenizer(SymbolicTokenizer):
    def __init__(self):
        token_map = {
            'ATCG': 'CODON1',
            'GCTA': 'CODON2',
            # ... more patterns
        }
        super().__init__(token_map)
```

### Hybrid Engines
Combine multiple compression techniques:

```python
def compress(self, data: bytes) -> CompressionResult:
    # Stage 1: Symbolic compression
    tokens = self.tokenizer.tokenize(data)

    # Stage 2: Dictionary compression
    dict_compressed = self._lzw_compress(tokens)

    # Stage 3: Entropy encoding
    final = self._arithmetic_encode(dict_compressed)

    return CompressionResult(...)
```

### Streaming Compression
For large files, implement streaming variants:

```python
def compress_stream(self, input_stream, output_stream):
    buffer_size = 8192
    while chunk := input_stream.read(buffer_size):
        compressed = self.compress(chunk)
        output_stream.write(compressed.compressed_data)
```

---

## Contributing

When contributing new engines:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/my-engine`)
3. Implement your engine following this guide
4. Add tests to `tests/`
5. Update this guide if needed
6. Submit a pull request

---

## Resources

- **Codex CheatSheet**: `Codex_Compression_CheatSheet.md`
- **Research Paper**: See README.md for citations
- **Base Class**: `codex/engines/base.py`
- **Example Implementation**: `codex/engines/codex_engine.py`

---

*Happy compressing! 🔢*
