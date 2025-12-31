# CODEX GitHub Actions Workflows

Automated testing and benchmarking for the compression engine framework.

## Workflows

### 1. **test.yml** - Unit Tests
**Trigger**: Every push to main or `claude/*` branches, all PRs

**What it does**:
- Runs full test suite on Python 3.8, 3.9, 3.10, 3.11
- Verifies all 11 unit tests pass
- Tests package imports
- Ensures engines can be loaded

**Status badge**:
```markdown
![Tests](https://github.com/MUSHIKARATI/CODEX/workflows/Compression%20Tests/badge.svg)
```

---

### 2. **benchmark.yml** - Performance Benchmarks
**Trigger**: Push to main, PRs, manual dispatch

**What it does**:
- Benchmarks all registered engines
- Measures compression ratio, speed, integrity
- Runs comparison script
- Reports throughput in MB/s

**Run manually**:
- Go to Actions tab → Compression Benchmarks → Run workflow

---

### 3. **performance-regression.yml** - Regression Detection
**Trigger**: Pull requests to main

**What it does**:
- Benchmarks PR version of code
- Benchmarks main branch version
- Compares performance metrics
- Detects compression ratio regressions
- Catches speed degradations

**Prevents**:
- Accidental performance drops
- Compression ratio decreases
- Speed regressions

---

### 4. **engine-validation.yml** - New Engine Validation
**Trigger**: PRs that modify `codex/engines/**`

**What it does**:
- Validates new engines follow interface
- Checks for required methods/properties
- Ensures engines are properly registered
- Tests basic compress/decompress functionality

**Catches**:
- Missing abstract methods
- Registration errors
- Interface violations
- Broken implementations

---

## Setup

No additional setup needed! Workflows run automatically on:
- ✅ Push to main or claude/* branches
- ✅ Pull requests
- ✅ Manual dispatch (some workflows)

---

## Local Testing

Run the same checks locally before pushing:

```bash
# Run tests
python -m unittest discover tests -v

# Run benchmarks
python examples/compare_engines.py

# Validate engines
python -c "from codex import list_engines; print(list_engines())"
```

---

## Adding New Workflows

To add compression-specific workflows:

1. Create `.github/workflows/your-workflow.yml`
2. Use existing workflows as templates
3. Focus on compression-specific tasks:
   - Multi-trial benchmarks (like your 50-trial experiments)
   - Chart generation (PNG comparison graphs)
   - CSV export of results
   - Cross-platform testing

---

## Workflow Ideas for Future

- **Nightly benchmarks**: Run extensive tests overnight
- **Chart generation**: Auto-generate comparison PNGs
- **Release automation**: Tag versions, build packages
- **Comparison reports**: Post results as PR comments
- **Performance badges**: Update README with latest metrics
