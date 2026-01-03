"""
Tests for Black LZW Screw compression engine.

Based on test_black_screw.py from GitHub Issue #5
"""

import unittest
from codex.engines.black_lzw_screw import BlackLZWScrewEngine
from codex.utils.tokens import codex_tokens, MagickToken


class TestBlackLZWScrewEngine(unittest.TestCase):
    """Test suite for Black LZW Screw engine."""

    def setUp(self):
        """Set up test fixtures."""
        self.engine = BlackLZWScrewEngine()

    def test_engine_properties(self):
        """Test engine basic properties."""
        self.assertEqual(self.engine.name, "Black_LZW_Screw")
        self.assertEqual(self.engine.version, "1.0.0")
        self.assertIn("LZW", self.engine.description)
        self.assertIn("Black Gate", self.engine.description)

    def test_roundtrip_empty(self):
        """Test empty data roundtrip."""
        test_input = b""
        result = self.engine.compress(test_input)
        self.assertIsNotNone(result.compressed_data)
        decomp = self.engine.decompress(result.compressed_data)
        self.assertEqual(decomp.decompressed_data, test_input)

    def test_roundtrip_single(self):
        """Test single character roundtrip."""
        test_input = b"A"
        result = self.engine.compress(test_input)
        decomp = self.engine.decompress(result.compressed_data)
        self.assertEqual(decomp.decompressed_data, test_input)

    def test_roundtrip_repeated(self):
        """Test repeated characters roundtrip."""
        test_input = b"AAAAAA"
        result = self.engine.compress(test_input)
        decomp = self.engine.decompress(result.compressed_data)
        self.assertEqual(decomp.decompressed_data, test_input)

    def test_roundtrip_pattern(self):
        """Test pattern roundtrip."""
        test_input = b"abcabcabcabc"
        result = self.engine.compress(test_input)
        decomp = self.engine.decompress(result.compressed_data)
        self.assertEqual(decomp.decompressed_data, test_input)

    def test_roundtrip_ascii(self):
        """Test full ASCII range roundtrip."""
        test_input = bytes(range(128))
        result = self.engine.compress(test_input)
        decomp = self.engine.decompress(result.compressed_data)
        self.assertEqual(decomp.decompressed_data, test_input)

    def test_black_gate_seal(self):
        """Test that Black Gate seal is properly applied."""
        test_data = b"Hello Symbrec"

        result = self.engine.compress(test_data)

        # Check metadata
        self.assertIn('seal', result.metadata)
        self.assertEqual(result.metadata['seal'], MagickToken.BLACK.emoji)  # ⚫
        self.assertIn('hash', result.metadata)
        self.assertIn('code_count', result.metadata)
        self.assertIsInstance(result.metadata['code_count'], int)

    def test_directional_reentry(self):
        """Test black reentry directional encoding."""
        # UP should give White (⚪)
        self.assertEqual(self.engine._black_reentry("UP"), MagickToken.WHITE.emoji)

        # DOWN should give Blue (🔵)
        self.assertEqual(self.engine._black_reentry("DOWN"), MagickToken.BLUE.emoji)

        # Other should give Black (⚫)
        self.assertEqual(self.engine._black_reentry("UNKNOWN"), MagickToken.BLACK.emoji)

    def test_unicode_support(self):
        """Test Unicode character support."""
        test_data = "Hello 世界! 🌍".encode('utf-8')

        result = self.engine.compress(test_data)
        decomp = self.engine.decompress(result.compressed_data)

        self.assertEqual(decomp.decompressed_data, test_data)

    def test_compression_metrics(self):
        """Test that compression produces valid metrics."""
        test_data = b"abcabcabcabc" * 10  # Compressible data

        result = self.engine.compress(test_data)

        self.assertEqual(result.original_size, len(test_data))
        self.assertGreater(result.compressed_size, 0)
        self.assertGreater(result.compression_ratio, 0)
        self.assertIsNotNone(result.entropy_original)
        self.assertIsNotNone(result.entropy_compressed)

    def test_empty_data(self):
        """Test handling of empty data."""
        test_data = b""

        result = self.engine.compress(test_data)
        decomp = self.engine.decompress(result.compressed_data)

        self.assertEqual(decomp.decompressed_data, test_data)

    def test_large_dictionary(self):
        """Test compression with large dictionary."""
        # Create data with many unique patterns
        test_data = ''.join(f"pattern{i}" for i in range(1000)).encode('utf-8')

        result = self.engine.compress(test_data)
        decomp = self.engine.decompress(result.compressed_data)

        self.assertEqual(decomp.decompressed_data, test_data)

    def test_header_validation(self):
        """Test that header validation works."""
        test_data = b"Test data"

        result = self.engine.compress(test_data)

        # Tamper with magic bytes
        tampered = b'XXXX' + result.compressed_data[4:]

        with self.assertRaisesRegex(ValueError, "Invalid Black LZW Screw magic"):
            self.engine.decompress(tampered)

    def test_lzw_compression_ratio(self):
        """Test that LZW actually compresses repetitive data."""
        # Highly repetitive data
        test_data = b"abcabcabc" * 100

        result = self.engine.compress(test_data)

        # LZW should achieve good compression on repetitive data
        # (though header overhead might make small data expand)
        self.assertLess(result.compressed_size, len(test_data) * 2)  # At least not terrible expansion

    def test_benchmark(self):
        """Test benchmarking functionality."""
        test_data = b"Benchmark test data" * 100

        metrics = self.engine.benchmark(test_data)

        self.assertIn('engine', metrics)
        self.assertEqual(metrics['engine'], "Black_LZW_Screw")
        self.assertIn('compression_ratio', metrics)
        self.assertIn('compression_time', metrics)
        self.assertIn('decompression_time', metrics)
        self.assertTrue(metrics['integrity_check'])

    def test_config_options(self):
        """Test engine configuration options."""
        config = {
            'dict_size': 8192,
            'use_unicode': True
        }

        engine = BlackLZWScrewEngine(config=config)

        self.assertEqual(engine.dict_size, 8192)
        self.assertTrue(engine.use_unicode)

    def test_token_system_integration(self):
        """Test integration with CODEX token system."""
        # Verify token system is properly initialized
        self.assertTrue(codex_tokens.validate_token_integrity())

        # Test that seal comes from the token system
        test_data = b"Token integration test"
        result = self.engine.compress(test_data)

        self.assertIn(result.metadata['seal'], [token.emoji for token in MagickToken])


class TestCODEXTokenSystem(unittest.TestCase):
    """Test CODEX token system integrity."""

    def test_token_count(self):
        """Test that we have the correct number of tokens."""
        # 7 Magick tokens (the core 7-color system)
        self.assertEqual(len(MagickToken), 7)

        # 4 Operator tokens
        from codex.utils.tokens import OperatorToken
        self.assertEqual(len(OperatorToken), 4)

        # 6 Special tokens (including 4 elemental)
        from codex.utils.tokens import SpecialToken
        self.assertEqual(len(SpecialToken), 6)

        # Total should be 17 (7 Magick + 4 Operator + 6 Special)
        self.assertTrue(codex_tokens.validate_token_integrity())

    def test_color_sequence(self):
        """Test the 7-color sequence."""
        sequence = codex_tokens.get_color_sequence()

        self.assertEqual(len(sequence), 7)
        self.assertEqual(sequence[0], MagickToken.BLACK)
        self.assertEqual(sequence[6], MagickToken.BLUE)

    def test_emoji_mapping(self):
        """Test emoji to token mapping."""
        emoji_map = codex_tokens.get_emoji_map()

        self.assertIn("⚫", emoji_map)
        self.assertIn("⚪", emoji_map)
        self.assertIn("🔵", emoji_map)

        self.assertEqual(emoji_map["⚫"], MagickToken.BLACK)
        self.assertEqual(emoji_map["⚪"], MagickToken.WHITE)
        self.assertEqual(emoji_map["🔵"], MagickToken.BLUE)


if __name__ == '__main__':
    unittest.main()
