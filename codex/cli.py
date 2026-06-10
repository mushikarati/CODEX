#!/usr/bin/env python3
"""
Command-line interface for Codex compression engines.

Provides easy access to compression, decompression, and benchmarking.
"""

import argparse
import sys
from pathlib import Path
from typing import Optional

from . import get_engine, list_engines
from .core import symbolic_dynamics


def compress_file(engine_name: str, input_path: str, output_path: Optional[str] = None,
                 config: Optional[dict] = None) -> None:
    """
    Compress a file using the specified engine.

    Args:
        engine_name: Name of the compression engine
        input_path: Path to input file
        output_path: Path to output file (default: input_path + '.cdx')
        config: Optional engine configuration
    """
    # Read input file
    with open(input_path, 'rb') as f:
        data = f.read()

    print(f"Compressing {len(data)} bytes with {engine_name} engine...")

    # Get engine and compress
    engine = get_engine(engine_name, config)
    result = engine.compress(data)

    # Determine output path
    if output_path is None:
        output_path = input_path + '.cdx'

    # Write compressed data
    with open(output_path, 'wb') as f:
        f.write(result.compressed_data)

    print(f"\nCompression complete!")
    print(result)
    print(f"Output written to: {output_path}")


def decompress_file(engine_name: str, input_path: str, output_path: Optional[str] = None,
                   config: Optional[dict] = None) -> None:
    """
    Decompress a file using the specified engine.

    Args:
        engine_name: Name of the compression engine
        input_path: Path to compressed file
        output_path: Path to output file (default: input_path + '.decoded')
        config: Optional engine configuration
    """
    # Read compressed file
    with open(input_path, 'rb') as f:
        compressed_data = f.read()

    print(f"Decompressing {len(compressed_data)} bytes with {engine_name} engine...")

    # Get engine and decompress
    engine = get_engine(engine_name, config)
    result = engine.decompress(compressed_data)

    # Determine output path
    if output_path is None:
        # Remove .cdx extension if present
        if input_path.endswith('.cdx'):
            output_path = input_path[:-4]
        else:
            output_path = input_path + '.decoded'

    # Write decompressed data
    with open(output_path, 'wb') as f:
        f.write(result.decompressed_data)

    print(f"\nDecompression complete!")
    print(f"Decompressed {result.decompressed_size} bytes")
    print(f"Output written to: {output_path}")


def benchmark_engine(engine_name: str, input_path: str, config: Optional[dict] = None) -> None:
    """
    Benchmark an engine on a file.

    Args:
        engine_name: Name of the compression engine
        input_path: Path to input file
        config: Optional engine configuration
    """
    # Read input file
    with open(input_path, 'rb') as f:
        data = f.read()

    print(f"Benchmarking {engine_name} engine on {len(data)} bytes...\n")

    # Get engine and run benchmark
    engine = get_engine(engine_name, config)
    results = engine.benchmark(data)

    # Print results
    print("=" * 60)
    print(f"Engine: {results['engine']}")
    print("=" * 60)
    print(f"Original Size:        {results['original_size']:,} bytes")
    print(f"Compressed Size:      {results['compressed_size']:,} bytes")
    print(f"Compression Ratio:    {results['compression_ratio']:.2%}")
    print(f"Space Saved:          {results['original_size'] - results['compressed_size']:,} bytes")
    print(f"Compression Time:     {results['compression_time']:.6f} seconds")
    print(f"Decompression Time:   {results['decompression_time']:.6f} seconds")
    print(f"Compress Throughput:  {results['throughput_compress_mbps']:.2f} MB/s")
    print(f"Decompress Throughput:{results['throughput_decompress_mbps']:.2f} MB/s")
    print(f"Integrity Check:      {'PASS' if results['integrity_check'] else 'FAIL'}")
    if results['entropy_original']:
        print(f"Entropy (Original):   {results['entropy_original']:.4f} bits/byte")
    if results['entropy_compressed']:
        print(f"Entropy (Compressed): {results['entropy_compressed']:.4f} bits/byte")
    print("=" * 60)


def show_engines() -> None:
    """Display all available engines."""
    engines = list_engines()

    if not engines:
        print("No compression engines registered.")
        return

    print("\n" + "=" * 60)
    print("Available Compression Engines")
    print("=" * 60)

    for engine_info in engines:
        print(f"\n{engine_info['name']} (v{engine_info['version']})")
        print(f"  {engine_info['description']}")

    print("\n" + "=" * 60)


def run_simulation(
    initial_sequence: Optional[str] = None,
    max_steps: int = 100,
    initial_entropy: float = 0.45,
    output_csv: Optional[str] = None
) -> None:
    """
    Run CODEX symbolic dynamics simulation.

    Args:
        initial_sequence: Initial token sequence (e.g., 'KWYBRGUKWYBR')
        max_steps: Maximum simulation steps
        initial_entropy: Initial entropy H0
        output_csv: Path to save CSV output
    """
    import random

    # Parse initial sequence or use shuffled default
    if initial_sequence:
        # Parse sequence string into list
        initial_M = list(initial_sequence.upper())
    else:
        # Use shuffled canonical sequence
        seed = ["K", "W", "Y", "B", "R", "G", "U"]
        random.seed(42)
        initial_M = seed.copy()
        random.shuffle(initial_M)

    print("=" * 60)
    print("CODEX Symbolic Dynamics Simulation")
    print("=" * 60)
    print(f"Initial sequence: {''.join(initial_M)}")
    print(f"Initial entropy:  H0 = {initial_entropy:.4f}")
    print(f"Max steps:        {max_steps}")
    print("=" * 60)

    # Run simulation
    csv_path = Path(output_csv) if output_csv else Path("/tmp/codex_simulation.csv")
    records = symbolic_dynamics.simulate(
        initial_M=initial_M,
        H0=initial_entropy,
        max_steps=max_steps,
        csv_path=csv_path
    )

    # Display results
    print(f"\nSimulation complete! {len(records)} timesteps executed.\n")

    # Show first few records
    print("First 10 timesteps:")
    print("-" * 80)
    print(f"{'t':<4} {'M':<10} {'S':<10} {'C':<10} {'H':<8} {'ΔH':<8} {'Viol':<5} {'Gray'}")
    print("-" * 80)

    for r in records[:10]:
        t = r['t']
        M_str = ''.join(r.get('M', []))[:8]
        S_str = ''.join(r.get('S', []))[:8]
        C_str = ''.join(r.get('C', []))[:8]
        H = r.get('H', 0)
        dH = r.get('deltaH', 0)
        viol = r.get('violations', 0)
        gray = '⚠️' if r.get('gray', False) else ''

        print(f"{t:<4} {M_str:<10} {S_str:<10} {C_str:<10} {H:<8.4f} {dH:<8.4f} {viol:<5} {gray}")

    print("-" * 80)

    # Show Gray events
    gray_events = [r for r in records if r.get('gray', False)]
    if gray_events:
        print(f"\n⚠️  Gray Events Detected: {len(gray_events)}")
        for event in gray_events:
            print(f"  - Timestep {event['t']}: {event['violations']} violations, "
                  f"H={event['H']:.4f}")
    else:
        print("\n✓ No Gray events detected")

    print(f"\nCSV log saved to: {csv_path}")
    print("=" * 60)


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Codex Compression Engine Framework",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # List available engines
  codex --list

  # Compress a file
  codex compress --engine codex input.txt

  # Decompress a file
  codex decompress --engine codex input.txt.cdx

  # Benchmark an engine
  codex benchmark --engine codex input.txt
        """
    )

    parser.add_argument('--version', action='version', version='Codex 1.0.0')
    parser.add_argument('--list', action='store_true', help='List available engines')

    subparsers = parser.add_subparsers(dest='command', help='Command to execute')

    # Compress command
    compress_parser = subparsers.add_parser('compress', help='Compress a file')
    compress_parser.add_argument('input', help='Input file path')
    compress_parser.add_argument('-o', '--output', help='Output file path')
    compress_parser.add_argument('-e', '--engine', default='codex', help='Engine name (default: codex)')

    # Decompress command
    decompress_parser = subparsers.add_parser('decompress', help='Decompress a file')
    decompress_parser.add_argument('input', help='Input file path')
    decompress_parser.add_argument('-o', '--output', help='Output file path')
    decompress_parser.add_argument('-e', '--engine', default='codex', help='Engine name (default: codex)')

    # Benchmark command
    benchmark_parser = subparsers.add_parser('benchmark', help='Benchmark an engine')
    benchmark_parser.add_argument('input', help='Input file path')
    benchmark_parser.add_argument('-e', '--engine', default='codex', help='Engine name (default: codex)')

    # Simulate command
    simulate_parser = subparsers.add_parser('simulate', help='Run symbolic dynamics simulation')
    simulate_parser.add_argument('-s', '--sequence', help='Initial token sequence (e.g., KWYBRGUKWYBR)')
    simulate_parser.add_argument('-n', '--steps', type=int, default=100, help='Max simulation steps (default: 100)')
    simulate_parser.add_argument('-H', '--entropy', type=float, default=0.45, help='Initial entropy (default: 0.45)')
    simulate_parser.add_argument('-o', '--output', help='CSV output path (default: /tmp/codex_simulation.csv)')

    args = parser.parse_args()

    try:
        if args.list:
            show_engines()
        elif args.command == 'compress':
            compress_file(args.engine, args.input, args.output)
        elif args.command == 'decompress':
            decompress_file(args.engine, args.input, args.output)
        elif args.command == 'benchmark':
            benchmark_engine(args.engine, args.input)
        elif args.command == 'simulate':
            run_simulation(
                initial_sequence=args.sequence,
                max_steps=args.steps,
                initial_entropy=args.entropy,
                output_csv=args.output
            )
        else:
            parser.print_help()

    except KeyError as e:
        print(f"Error: {e}", file=sys.stderr)
        print("\nUse --list to see available engines", file=sys.stderr)
        sys.exit(1)
    except FileNotFoundError as e:
        print(f"Error: File not found - {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
