#!/usr/bin/env python3
# black_compress.py

"""
⚫ Black Magic – Screw Operator / Compression Engine
Provides high-performance lossless compression using zlib (DEFLATE).

Usage:
  # Compress a file:
  python black_compress.py -c < input.txt > output.z

  # Decompress a file:
  python black_compress.py -d < output.z > input_restored.txt

  # Run a demonstration:
  python black_compress.py --demo
"""

import zlib
import sys
import argparse

def compress(data: bytes, level: int = 9) -> bytes:
    """
    Compress the input bytes with zlib (DEFLATE).

    Args:
        data (bytes): Raw input data to compress.
        level (int): Compression level (1-9). Defaults to 9 (maximum).

    Returns:
        bytes: Compressed data.
    """
    # Zlib is based on the DEFLATE algorithm, highly optimized for speed/ratio trade-off.
    return zlib.compress(data, level)

def decompress(data: bytes) -> bytes:
    """
    Decompress the input bytes with zlib.

    Args:
        data (bytes): Compressed data.

    Returns:
        bytes: Original raw data.
    """
    return zlib.decompress(data)

def run_cli():
    """
    Handles command-line interface for compression and decompression.
    """
    parser = argparse.ArgumentParser(
        description="Codex Black Magic – Zlib Compression Utility.",
        formatter_class=argparse.RawTextHelpFormatter
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-c', '--compress', action='store_true',
                       help='Compress data from stdin to stdout.')
    group.add_argument('-d', '--decompress', action='store_true',
                       help='Decompress data from stdin to stdout.')
    group.add_argument('--demo', action='store_true',
                       help='Run a proof-of-concept demonstration of the engine.')
    parser.add_argument('-l', '--level', type=int, default=9,
                        choices=range(1, 10), metavar='[1-9]',
                        help='Compression level (1=fastest, 9=best ratio). Default is 9.')

    args = parser.parse_args()

    if args.demo:
        run_demo(args.level)
        return

    try:
        # Read all raw bytes from standard input
        raw_data = sys.stdin.buffer.read()
    except Exception as e:
        print(f"Error reading from stdin: {e}", file=sys.stderr)
        return

    if args.compress:
        try:
            # Torsion-compress the raw data
            output_data = compress(raw_data, args.level)
            sys.stdout.buffer.write(output_data)
        except zlib.error as e:
            print(f"Zlib Compression Error: {e}", file=sys.stderr)
            sys.exit(1)
    elif args.decompress:
        try:
            # Restore the original data
            output_data = decompress(raw_data)
            sys.stdout.buffer.write(output_data)
        except zlib.error as e:
            print(f"Zlib Decompression Error: Input data is corrupted or not a valid zlib stream: {e}", file=sys.stderr)
            sys.exit(1)


def run_demo(level: int):
    """
    Runs a demonstration showing the compression ratio for a sample recursive text.
    """
    print("\n--- Codex Black Magic Demonstration (Zlib) ---")

    # Sample text designed to have high redundancy (recursive structure)
    sample_text = """
    The recursive process is the process that repeats.
    The process that repeats is the recursive process.
    The process is the process, the process is the process.
    Recursion, recursion, recursion, recursion.
    Repeat the sentence: The recursive process is the process that repeats.
    """
    raw_data = sample_text.encode('utf-8')
    raw_size = len(raw_data)

    print(f"Compression Level: {level}")
    print(f"Original Data Size: {raw_size} bytes")
    print(f"Sample (First 40 bytes): {raw_data[:40]!r}...")

    # 1. Compress
    compressed_data = compress(raw_data, level)
    compressed_size = len(compressed_data)

    # 2. Decompress (Check for losslessness)
    decompressed_data = decompress(compressed_data)
    
    if raw_data == decompressed_data:
        # 3. Calculate Ratio and Savings
        ratio = compressed_size / raw_size
        savings = (1 - ratio) * 100
        
        print("\n--- Compression Results ---")
        print(f"Compressed Size:    {compressed_size} bytes")
        print(f"Compression Ratio:  {ratio:.3f} (Lower is better)")
        print(f"Size Reduction:     {savings:.2f}% saved")
        print(f"Status:             Lossless compression verified.")
    else:
        print("\n--- Error ---")
        print("Decompression failed to match original data!")


if __name__ == "__main__":
    run_cli()

