# Python Implementation of Codex Compression Framework

## Overview

This repository now includes a complete Python implementation of the Codex compression framework with an **extensible architecture** designed to easily accommodate multiple compression engines.

## Features

✨ **Modular Engine Architecture**
- Abstract base class for all compression engines
- Automatic engine registration and discovery
- Plugin-style extensibility

🔢 **Codex Engine Implementation**
- 7-token symbolic alphabet (∘⊗→∫∂∇⊕)
- Category theory-based morphism rewrites
- Recursive homotopy transformations
- Entropy minimization via symbolic invariants

📊 **Comprehensive Metrics**
- Shannon entropy calculation
- Compression ratio tracking
- Symbolic entropy for token sequences
- MDL (Minimum Description Length) scoring
- Benchmarking with throughput metrics

🛠️ **Developer-Friendly**
- Simple API for adding new engines
- Full CLI interface
- Extensive documentation
- Complete test suite

---

## Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/MUSHIKARATI/CODEX.git
cd CODEX

# Install in development mode
pip install -e .
```

### Basic Usage

#### Python API

```python
from codex import get_engine

# Get the Codex engine
engine = get_engine('codex')

# Compress data
data = b"Hello, World!"
result = engine.compress(data)
print(f"Compressed: {result.compressed_size} bytes")
print(f"Ratio: {result.compression_ratio:.2%}")

# Decompress
decompressed = engine.decompress(result.compressed_data)
print(f"Original: {decompressed.decompressed_data}")
```

#### Command Line

```bash
# List available engines
python -m codex.cli --list

# Compress a file
python -m codex.cli compress --engine codex input.txt

# Decompress
python -m codex.cli decompress --engine codex input.txt.cdx

# Benchmark
python -m codex.cli benchmark --engine codex input.txt
```

---

## Architecture

### Directory Structure

```
codex/
├── __init__.py              # Main package interface
├── cli.py                   # Command-line interface
├── registry.py              # Engine registration system
│
├── engines/                 # Compression engines
│   ├── __init__.py          # Auto-registration
│   ├── base.py              # Abstract base class
│   ├── codex_engine.py      # Codex implementation
│   └── black_lzw_screw.py   # Example stub for new engines
│
└── utils/                   # Utility modules
    ├── entropy.py           # Entropy calculations
    └── tokenizer.py         # Symbolic tokenization

tests/                       # Test suite
examples/                    # Usage examples
```

### Key Components

#### 1. Base Engine Interface (`codex/engines/base.py`)

All compression engines inherit from `CompressionEngine`:

```python
class CompressionEngine(ABC):
    @abstractmethod
    def compress(data: bytes) -> CompressionResult

    @abstractmethod
    def decompress(compressed_data: bytes) -> DecompressionResult

    # + properties: name, description, version
    # + built-in: benchmark(), get_info()
```

#### 2. Engine Registry (`codex/registry.py`)

Automatic discovery and instantiation:

```python
from codex import list_engines, get_engine

# List all registered engines
engines = list_engines()

# Get an engine by name
engine = get_engine('codex', config={'rewrite_depth': 5})
```

#### 3. Codex Engine (`codex/engines/codex_engine.py`)

Implementation of the symbolic compression algorithm:

- **Tokenization**: UTF-8 → 7-token symbolic alphabet
- **Rewrites**: Category theory morphisms (composition, tensor, etc.)
- **Optimization**: Recursive entropy minimization
- **Encoding**: Token serialization + optional gzip

#### 4. Utility Modules

**Entropy** (`codex/utils/entropy.py`):
- Shannon entropy
- Symbolic entropy
- Kolmogorov complexity estimation
- MDL scoring
- Compression gain metrics

**Tokenizer** (`codex/utils/tokenizer.py`):
- Symbolic tokenization
- Codex 7-token alphabet
- Extensible for custom token grammars

---

## Adding New Engines

Adding a new compression engine is simple - just **3 steps**:

### Step 1: Create Engine Class

Create `codex/engines/my_engine.py`:

```python
from .base import CompressionEngine, CompressionResult, DecompressionResult

class MyEngine(CompressionEngine):
    @property
    def name(self) -> str:
        return "MyEngine"

    @property
    def description(self) -> str:
        return "My custom compression algorithm"

    @property
    def version(self) -> str:
        return "1.0.0"

    def compress(self, data: bytes) -> CompressionResult:
        # Your compression logic here
        pass

    def decompress(self, compressed_data: bytes) -> DecompressionResult:
        # Your decompression logic here
        pass
```

### Step 2: Register Engine

Add to `codex/engines/__init__.py`:

```python
from .my_engine import MyEngine
from ..registry import register_engine

register_engine(MyEngine)
```

### Step 3: Use It!

```python
engine = get_engine('myengine')
result = engine.compress(data)
```

That's it! Your engine is now available via both API and CLI.

---

## Example: Black_LZW_Screw Engine (Stub)

See `codex/engines/black_lzw_screw.py` for a complete template showing:

- Proper class structure
- Configuration handling
- Header format design
- Stub methods for future implementation
- Registration pattern

This serves as a blueprint for adding engines like:
- **Black_LZW_Screw**: LZW + screw transformations + black encoding
- **Huffman variants**: Custom Huffman with symbolic preprocessing
- **Arithmetic coding**: With category theory optimizations
- **Neural compressors**: Learned compression models
- And many more...

---

## Running Tests

```bash
# Run all tests
python -m unittest discover tests

# Run specific test
python -m unittest tests.test_codex_engine

# Run with verbose output
python -m unittest discover tests -v
```

---

## Running Examples

```bash
# Run all usage examples
python examples/basic_usage.py
```

This will demonstrate:
1. Listing engines
2. Basic compression/decompression
3. Custom configuration
4. Benchmarking
5. File compression

---

## API Reference

### Main Interface

```python
from codex import (
    get_engine,          # Get engine instance
    list_engines,        # List all engines
    CompressionEngine,   # Base class
    CompressionResult,   # Compression result type
    DecompressionResult  # Decompression result type
)
```

### Compression Result

```python
result = engine.compress(data)

result.compressed_data      # bytes
result.original_size        # int
result.compressed_size      # int
result.compression_ratio    # float (0.0 - 1.0+)
result.entropy_original     # Optional[float]
result.entropy_compressed   # Optional[float]
result.metadata            # Optional[Dict[str, Any]]
```

### Engine Methods

```python
# Compress data
result = engine.compress(data: bytes) -> CompressionResult

# Decompress data
result = engine.decompress(compressed_data: bytes) -> DecompressionResult

# Benchmark
metrics = engine.benchmark(data: bytes) -> Dict[str, Any]

# Get engine info
info = engine.get_info() -> Dict[str, str]
```

### Utilities

```python
from codex.utils.entropy import (
    calculate_shannon_entropy,
    calculate_symbolic_entropy,
    calculate_compression_gain,
    estimate_kolmogorov_complexity,
    calculate_mdl_score
)

from codex.utils.tokenizer import (
    CodexTokenizer,
    SymbolicTokenizer,
    create_lzw_tokenizer
)
```

---

## Configuration

Engines accept optional configuration:

```python
config = {
    'rewrite_depth': 5,
    'use_secondary_compression': True,
    'min_token_length': 2
}

engine = get_engine('codex', config=config)
```

Each engine defines its own configuration schema.

---

## Performance Notes

### Codex Engine Performance

- **Best for**: Symbol-heavy text, mathematical expressions, structured data
- **Crossover point**: ~3.4 KB (where it beats gzip)
- **Typical gain**: 10-15% over gzip on suitable data
- **Model cost**: 216 bytes (24B table + 176B FSM + 16B header)

### Optimization Tips

1. **Increase rewrite depth** for more aggressive symbolic optimization
2. **Enable secondary compression** for better final ratios
3. **Adjust min_token_length** based on data characteristics
4. **Benchmark different engines** on your specific data

---

## Development

### Setting up development environment

```bash
# Install with dev dependencies
pip install -e ".[dev]"

# Run linting
flake8 codex tests

# Type checking
mypy codex

# Format code
black codex tests
```

### Code Style

- Follow PEP 8
- Use type hints
- Document all public APIs
- Write tests for new features

---

## Roadmap

Future engines planned:

- [ ] **Black_LZW_Screw** - Full implementation
- [ ] **Arithmetic_Codex** - Arithmetic coding variant
- [ ] **Neural_Codex** - ML-based compression
- [ ] **Quantum_Codex** - Quantum-inspired algorithms
- [ ] **Fractal_Codex** - Fractal-based compression

---

## Documentation

- **Developer Guide**: See `DEVELOPER_GUIDE.md` for detailed implementation guide
- **Compression Theory**: See `Codex_Compression_CheatSheet.md` for mathematical foundations
- **Research Paper**: See `README.md` for citations and publications

---

## Citation

If you use this implementation in your research:

```bibtex
@software{codex2025,
  author = {MUSHIKARATI},
  title = {Codex: A Symbolic Compression Engine Framework},
  year = {2025},
  publisher = {GitHub},
  url = {https://github.com/MUSHIKARATI/CODEX},
  doi = {10.5281/zenodo.16096831}
}
```

---

## License

MIT License - See `LICENSE` file for details

---

## Contributing

Contributions welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Ensure all tests pass
5. Submit a pull request

See `DEVELOPER_GUIDE.md` for detailed contribution guidelines.

---

## Support

- **Issues**: https://github.com/MUSHIKARATI/CODEX/issues
- **Discussions**: https://github.com/MUSHIKARATI/CODEX/discussions

---

*Built with ❤️ for the compression research community*
