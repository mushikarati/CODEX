"""
Tests for the Codex compression engine.
"""

import unittest
from codex import CodexEngine, get_engine


class TestCodexEngine(unittest.TestCase):
    """Test cases for Codex engine."""

    def setUp(self):
        """Set up test fixtures."""
        self.engine = CodexEngine()

    def test_engine_properties(self):
        """Test engine basic properties."""
        self.assertEqual(self.engine.name, "Codex")
        self.assertIsNotNone(self.engine.description)
        self.assertIsNotNone(self.engine.version)

    def test_compress_decompress_simple(self):
        """Test basic compression and decompression."""
        test_data = b"Hello, World! This is a test message."

        # Compress
        result = self.engine.compress(test_data)
        self.assertIsNotNone(result.compressed_data)
        self.assertEqual(result.original_size, len(test_data))
        self.assertGreater(result.compressed_size, 0)

        # Decompress
        decomp_result = self.engine.decompress(result.compressed_data)
        self.assertEqual(decomp_result.decompressed_data, test_data)

    def test_compress_decompress_unicode(self):
        """Test compression with Unicode characters."""
        test_data = "Mathematical symbols: ∫∂∇⊗∘→ and text: Hello!".encode('utf-8')

        result = self.engine.compress(test_data)
        decomp_result = self.engine.decompress(result.compressed_data)

        self.assertEqual(decomp_result.decompressed_data, test_data)

    def test_compression_metrics(self):
        """Test that compression produces valid metrics."""
        test_data = b"ABCDEFGH" * 100  # Compressible but varied data

        result = self.engine.compress(test_data)

        self.assertIsNotNone(result.entropy_original)
        self.assertIsNotNone(result.entropy_compressed)
        self.assertGreater(result.entropy_original, 0)
        self.assertGreaterEqual(result.compression_ratio, 0)
        self.assertLessEqual(result.compression_ratio, 1.5)  # Should compress or expand slightly

    def test_empty_data(self):
        """Test handling of empty data."""
        test_data = b""

        result = self.engine.compress(test_data)
        decomp_result = self.engine.decompress(result.compressed_data)

        self.assertEqual(decomp_result.decompressed_data, test_data)

    def test_benchmark(self):
        """Test benchmarking functionality."""
        test_data = b"Test data for benchmarking" * 100

        benchmark_results = self.engine.benchmark(test_data)

        self.assertIn('engine', benchmark_results)
        self.assertIn('compression_ratio', benchmark_results)
        self.assertIn('compression_time', benchmark_results)
        self.assertIn('decompression_time', benchmark_results)
        self.assertTrue(benchmark_results['integrity_check'])

    def test_registry_integration(self):
        """Test that engine is registered and accessible."""
        engine = get_engine('codex')
        self.assertIsInstance(engine, CodexEngine)
        self.assertEqual(engine.name, "Codex")


class TestCodexTokenizer(unittest.TestCase):
    """Test cases for Codex tokenizer."""

    def test_tokenization(self):
        """Test basic tokenization."""
        from codex.utils.tokenizer import CodexTokenizer

        tokenizer = CodexTokenizer()
        text = "∘∂∇"

        tokens = tokenizer.tokenize(text)
        self.assertEqual(len(tokens), 3)
        self.assertIn('COMPOSE', tokens)
        self.assertIn('PARTIAL', tokens)
        self.assertIn('GRADIENT', tokens)

    def test_detokenization(self):
        """Test reverse tokenization."""
        from codex.utils.tokenizer import CodexTokenizer

        tokenizer = CodexTokenizer()
        text = "Test ∘ data"

        tokens = tokenizer.tokenize(text)
        reconstructed = tokenizer.detokenize(tokens)

        self.assertEqual(reconstructed, text)


class TestEntropyUtils(unittest.TestCase):
    """Test cases for entropy utilities."""

    def test_shannon_entropy(self):
        """Test Shannon entropy calculation."""
        from codex.utils.entropy import calculate_shannon_entropy

        # Uniform data - maximum entropy
        uniform_data = b"abcdefgh" * 100
        entropy = calculate_shannon_entropy(uniform_data)
        self.assertGreater(entropy, 2.5)

        # Repetitive data - low entropy
        repetitive_data = b"aaaaaaaa" * 100
        entropy = calculate_shannon_entropy(repetitive_data)
        self.assertLess(entropy, 0.1)

    def test_compression_gain(self):
        """Test compression gain calculation."""
        from codex.utils.entropy import calculate_compression_gain

        gain = calculate_compression_gain(
            original_entropy=8.0,
            compressed_entropy=4.0,
            original_size=1000,
            compressed_size=500
        )

        self.assertEqual(gain['entropy_reduction'], 4.0)
        self.assertEqual(gain['compression_ratio'], 0.5)
        self.assertEqual(gain['space_saving'], 0.5)


if __name__ == '__main__':
    unittest.main()
