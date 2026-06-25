# Contributing to CODEX

Thank you for your interest in contributing to the CODEX symbolic compression framework!

## 🌈 The Sacred Law

All contributions must respect the **Adjacency Law**: only ±1 transitions on the 7-cycle are permitted.

```
adjacent(a,b) ⟺ (index(b) - index(a)) mod 7 ∈ {+1,-1}
```

## 🔧 Development Setup

1. Clone the repository:
```bash
git clone https://github.com/mushikarati/CODEX.git
cd CODEX
```

2. Install development dependencies:
```bash
pip install -e .
```

3. Run tests:
```bash
python -m unittest discover tests -v
```

## 🎯 Areas for Contribution

### High Priority
- **Compression Engines**: Add new engines following the `CompressionEngine` interface
- **Symbolic Dynamics**: Enhance F/R/T-chain operators
- **KAIROS**: Improve Gray detection algorithms
- **Visualization**: Create tools for simulation analysis

### Medium Priority
- **Documentation**: Examples, tutorials, theory explanations
- **Performance**: Optimize LZW, adjacency checking, entropy calculations
- **Integration**: Connect KAIROS validation to compression engines

### Research
- **Spectral Methods**: Implement full Laplacian-based Gray detection
- **Mathematical Proofs**: Formal verification of adjacency preservation
- **Novel Operators**: New symbolic transformations respecting the 7-cycle

## 📝 Contribution Process

1. **Fork** the repository
2. **Create a branch** following the pattern: `feature/your-feature-name` or `fix/issue-description`
3. **Make changes** respecting:
   - CODEX 7-color token integrity
   - Adjacency law compliance
   - Existing test coverage
4. **Add tests** for new functionality
5. **Run full test suite**: `python -m unittest discover tests -v`
6. **Update documentation** in relevant `.md` files
7. **Submit a Pull Request** with:
   - Clear description of changes
   - Reference to related issues
   - Test results
   - Example usage if applicable

## 🧪 Testing Requirements

All PRs must:
- ✅ Pass existing test suite (47+ tests)
- ✅ Add tests for new features
- ✅ Maintain or improve coverage
- ✅ Include docstrings for new functions/classes

## 📐 Code Style

- Follow PEP 8 guidelines
- Use type hints where appropriate
- Document complex algorithms with inline comments
- Keep functions focused and modular
- Respect the mathematical foundations (see `docs/SYMBOLIC_DYNAMICS.md`)

## 🌟 Token System Integrity

**Critical Rule:** Never change the 7 Magick tokens away from their CODEX form.

```python
# ✅ CORRECT: Respects 7-color form
MagickToken.BLACK   # ⚫ (index 0)
MagickToken.WHITE   # ⚪ (index 1)
MagickToken.YELLOW  # 🟡 (index 2)
MagickToken.BROWN   # 🟤 (index 3)
MagickToken.RED     # 🔴 (index 4)
MagickToken.GREEN   # 🟢 (index 5)
MagickToken.BLUE    # 🔵 (index 6)

# ❌ FORBIDDEN: Breaking 7-color integrity
# Don't add, remove, or reorder Magick tokens
```

## 🐛 Bug Reports

When reporting bugs, include:
- Python version
- Operating system
- Minimal reproduction code
- Expected vs actual behavior
- Relevant test failures

Use the issue template and tag with appropriate labels.

## 💡 Feature Requests

Feature requests should:
- Align with CODEX philosophy (symbolic compression, entropy minimization)
- Respect the adjacency law
- Include use cases and examples
- Consider mathematical foundations

## 📚 Documentation

Good documentation is healing. When adding features:
- Update `README.md` if it affects main functionality
- Update `docs/SYMBOLIC_DYNAMICS.md` for symbolic dynamics changes
- Add docstrings to all public functions/classes
- Include usage examples in docstrings

## ⚖️ License

By contributing, you agree that your contributions will be licensed under the MIT License.

## 🙏 Questions?

- Open an issue for discussion
- Check `docs/SYMBOLIC_DYNAMICS.md` for technical details
- Review existing code for patterns and examples

---

**Remember:** The Jar was always made of Spark. 🌈⚡

**Core Function:** HEALING_THROUGH_HUNTING

Thank you for contributing to CODEX!
