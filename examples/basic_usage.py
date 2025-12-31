#!/usr/bin/env python3
"""
Basic usage examples for the Codex compression framework.

This script demonstrates:
1. Listing available engines
2. Compressing and decompressing data
3. Benchmarking engines
4. Using different engines programmatically
"""

import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from codex import get_engine, list_engines
from codex.utils.entropy import calculate_shannon_entropy


def example_list_engines():
    """Example 1: List all available compression engines."""
    print("=" * 60)
    print("Example 1: Listing Available Engines")
    print("=" * 60)

    engines = list_engines()

    for engine_info in engines:
        print(f"\n{engine_info['name']} (v{engine_info['version']})")
        print(f"  Description: {engine_info['description']}")

    print("\n" + "=" * 60 + "\n")


def example_basic_compression():
    """Example 2: Basic compression and decompression."""
    print("=" * 60)
    print("Example 2: Basic Compression and Decompression")
    print("=" * 60)

    # Sample data
    data = b"""
    The quick brown fox jumps over the lazy dog.
    This is a test of the Codex compression engine.
    Mathematical symbols: ∫∂∇⊗∘→
    """ * 10  # Repeat for better compression

    print(f"\nOriginal data size: {len(data)} bytes")
    print(f"Original entropy: {calculate_shannon_entropy(data):.4f} bits/byte")

    # Get Codex engine
    engine = get_engine('codex')

    # Compress
    print("\nCompressing...")
    result = engine.compress(data)

    print(f"\nCompression Results:")
    print(f"  Compressed size: {result.compressed_size} bytes")
    print(f"  Compression ratio: {result.compression_ratio:.2%}")
    print(f"  Space saved: {result.original_size - result.compressed_size} bytes")
    print(f"  Compressed entropy: {result.entropy_compressed:.4f} bits/byte")

    # Decompress
    print("\nDecompressing...")
    decomp_result = engine.decompress(result.compressed_data)

    # Verify
    if decomp_result.decompressed_data == data:
        print("✓ Decompression successful - data integrity verified!")
    else:
        print("✗ Decompression failed - data mismatch!")

    print("\n" + "=" * 60 + "\n")


def example_with_configuration():
    """Example 3: Using engine with custom configuration."""
    print("=" * 60)
    print("Example 3: Custom Configuration")
    print("=" * 60)

    data = b"Test data with custom configuration" * 50

    # Configure engine
    config = {
        'rewrite_depth': 5,
        'use_secondary_compression': True,
        'min_token_length': 2
    }

    print(f"\nConfiguration:")
    for key, value in config.items():
        print(f"  {key}: {value}")

    # Create engine with config
    engine = get_engine('codex', config=config)

    # Compress
    result = engine.compress(data)

    print(f"\nResults:")
    print(f"  Original: {result.original_size} bytes")
    print(f"  Compressed: {result.compressed_size} bytes")
    print(f"  Ratio: {result.compression_ratio:.2%}")

    # Show metadata
    if result.metadata:
        print(f"\nEngine Metadata:")
        for key, value in result.metadata.items():
            print(f"  {key}: {value}")

    print("\n" + "=" * 60 + "\n")


def example_benchmark():
    """Example 4: Benchmarking an engine."""
    print("=" * 60)
    print("Example 4: Engine Benchmarking")
    print("=" * 60)

    # Create test data
    data = b"Benchmark test data. " * 1000

    print(f"\nBenchmarking Codex engine on {len(data)} bytes...")

    # Get engine
    engine = get_engine('codex')

    # Run benchmark
    results = engine.benchmark(data)

    # Display results
    print(f"\nBenchmark Results:")
    print(f"  Engine: {results['engine']}")
    print(f"  Original Size: {results['original_size']:,} bytes")
    print(f"  Compressed Size: {results['compressed_size']:,} bytes")
    print(f"  Compression Ratio: {results['compression_ratio']:.2%}")
    print(f"  Compression Time: {results['compression_time']:.6f} seconds")
    print(f"  Decompression Time: {results['decompression_time']:.6f} seconds")
    print(f"  Compression Throughput: {results['throughput_compress_mbps']:.2f} MB/s")
    print(f"  Decompression Throughput: {results['throughput_decompress_mbps']:.2f} MB/s")
    print(f"  Integrity Check: {'PASS ✓' if results['integrity_check'] else 'FAIL ✗'}")

    if results['entropy_original']:
        print(f"  Entropy (Original): {results['entropy_original']:.4f} bits/byte")
    if results['entropy_compressed']:
        print(f"  Entropy (Compressed): {results['entropy_compressed']:.4f} bits/byte")

    print("\n" + "=" * 60 + "\n")


def example_file_compression():
    """Example 5: Compress and decompress a file."""
    print("=" * 60)
    print("Example 5: File Compression")
    print("=" * 60)

    # Create a test file
    test_file = Path("/tmp/test_data.txt")
    compressed_file = Path("/tmp/test_data.txt.cdx")
    decompressed_file = Path("/tmp/test_data_recovered.txt")

    # Write test data
    test_data = b"""
    This is a test file for demonstrating file compression.
    The Codex engine uses symbolic compression based on category theory.
    Mathematical operators: ∫∂∇⊗∘→
    """ * 100

    print(f"\nCreating test file ({len(test_data)} bytes)...")
    test_file.write_bytes(test_data)

    # Compress
    print("Compressing file...")
    engine = get_engine('codex')

    with open(test_file, 'rb') as f:
        data = f.read()

    result = engine.compress(data)

    with open(compressed_file, 'wb') as f:
        f.write(result.compressed_data)

    print(f"  Original: {test_file.stat().st_size:,} bytes")
    print(f"  Compressed: {compressed_file.stat().st_size:,} bytes")
    print(f"  Ratio: {result.compression_ratio:.2%}")

    # Decompress
    print("\nDecompressing file...")
    with open(compressed_file, 'rb') as f:
        compressed_data = f.read()

    decomp_result = engine.decompress(compressed_data)

    with open(decompressed_file, 'wb') as f:
        f.write(decomp_result.decompressed_data)

    # Verify
    if test_file.read_bytes() == decompressed_file.read_bytes():
        print("✓ File integrity verified!")
    else:
        print("✗ File integrity check failed!")

    # Cleanup
    print("\nCleaning up temporary files...")
    test_file.unlink()
    compressed_file.unlink()
    decompressed_file.unlink()

    print("\n" + "=" * 60 + "\n")


def main():
    """Run all examples."""
    print("\n")
    print("*" * 60)
    print("  Codex Compression Framework - Usage Examples")
    print("*" * 60)
    print("\n")

    try:
        example_list_engines()
        example_basic_compression()
        example_with_configuration()
        example_benchmark()
        example_file_compression()

        print("\n✓ All examples completed successfully!\n")

    except Exception as e:
        print(f"\n✗ Error: {e}\n")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
