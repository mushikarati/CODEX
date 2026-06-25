"""
Tests for Glyph Engine - Septenary compression via Mirror-Spiral Law
"""

import unittest
from codex.engines.glyph_engine import GlyphEngine, GlyphPhase, Spore
from codex.core import is_adjacent, validate_sequence


class TestGlyphPhaseAdjacency(unittest.TestCase):
    """Test adjacency law for Glyph phases"""

    def test_adjacent_phases(self):
        """Test that sequential phases are adjacent"""
        phases = [
            GlyphPhase.BLACK,
            GlyphPhase.WHITE,
            GlyphPhase.YELLOW,
            GlyphPhase.BROWN,
            GlyphPhase.RED,
            GlyphPhase.GREEN,
            GlyphPhase.BLUE
        ]

        for i in range(len(phases) - 1):
            diff = abs(phases[i + 1].value - phases[i].value)
            self.assertEqual(diff, 1, f"{phases[i]} -> {phases[i+1]} should be adjacent")

    def test_wrap_around_adjacency(self):
        """Test BLUE -> BLACK wrap-around is adjacent"""
        self.assertEqual(abs(GlyphPhase.BLACK.value - GlyphPhase.BLUE.value), 6)

    def test_non_adjacent_phases(self):
        """Test that skipping phases violates adjacency"""
        # BLACK (0) -> YELLOW (2) is a skip
        diff = abs(GlyphPhase.YELLOW.value - GlyphPhase.BLACK.value)
        self.assertEqual(diff, 2)  # Not 1, so not adjacent


class TestSpore(unittest.TestCase):
    """Test Spore data container"""

    def test_spore_creation(self):
        """Test creating a basic spore"""
        spore = Spore(
            payload=b"test data",
            history=[]
        )
        self.assertEqual(spore.payload, b"test data")
        self.assertEqual(spore.gray_score, 0.0)
        self.assertEqual(spore.coherence, 1.0)

    def test_spore_phase_tracking(self):
        """Test that spore tracks phase history"""
        spore = Spore(payload=b"test", history=[])
        spore.phase_trace.append(0)
        spore.phase_trace.append(1)
        self.assertEqual(len(spore.phase_trace), 2)


class TestGlyphEngineBasics(unittest.TestCase):
    """Test basic Glyph engine functionality"""

    def setUp(self):
        self.engine = GlyphEngine()

    def test_engine_properties(self):
        """Test engine metadata"""
        self.assertEqual(self.engine.name, "Glyph")
        self.assertEqual(self.engine.version, "1.0.0")
        self.assertIn("Mirror-Spiral", self.engine.description)

    def test_initial_phase_void(self):
        """Test engine starts in VOID phase"""
        self.assertEqual(self.engine.current_phase, GlyphPhase.VOID)

    def test_strict_adjacency_enabled(self):
        """Test strict adjacency is enabled by default"""
        self.assertTrue(self.engine.strict_adjacency)


class TestGlyphTransforms(unittest.TestCase):
    """Test individual phase transforms"""

    def setUp(self):
        self.engine = GlyphEngine()

    def test_black_transform(self):
        """BLACK: Torsional cut - remove redundancy"""
        data = b"hello world"
        result = self.engine._apply_black(data)
        # Should cut to half
        self.assertEqual(len(result), len(data) // 2)

    def test_white_transform(self):
        """WHITE: Lattice frame - add structure hash"""
        data = b"test"
        result = self.engine._apply_white(data)
        # Should append MD5 hash (16 bytes)
        self.assertEqual(len(result), len(data) + 16)

    def test_yellow_transform(self):
        """YELLOW: Ignition - burst padding for alignment"""
        data = b"test"  # len=4, 4%3=1, so needs 2 bytes padding
        result = self.engine._apply_yellow(data)
        expected_padding = (3 - (len(data) % 3)) % 3
        self.assertEqual(len(result), len(data) + expected_padding)

    def test_brown_transform(self):
        """BROWN: Containment - clamp to safe range"""
        data = bytes([200, 150, 100, 50])
        result = self.engine._apply_brown(data)
        # All values should be < 127
        for byte in result:
            self.assertLess(byte, 127)

    def test_red_transform(self):
        """RED: Descent - reverse for flow optimization"""
        data = b"hello"
        result = self.engine._apply_red(data)
        self.assertEqual(result, data[::-1])

    def test_green_transform(self):
        """GREEN: Integration - sort for harmony"""
        data = b"dcba"
        result = self.engine._apply_green(data)
        self.assertEqual(result, bytes(sorted(data)))

    def test_blue_pair_transform(self):
        """BLUE: Recursion pair - atomic reflection"""
        spore = Spore(payload=b"test", history=[])
        data, coherence_delta = self.engine._apply_blue_pair(b"test", spore)
        # Should return data unchanged and coherence delta
        self.assertEqual(data, b"test")
        self.assertIsInstance(coherence_delta, float)


class TestAdjacencyValidation(unittest.TestCase):
    """Test adjacency validation in engine"""

    def setUp(self):
        self.engine = GlyphEngine()

    def test_void_to_black_allowed(self):
        """VOID -> BLACK is allowed (entry point)"""
        self.assertTrue(self.engine._validate_adjacency(GlyphPhase.BLACK))

    def test_void_to_other_forbidden(self):
        """VOID -> anything except BLACK is forbidden"""
        self.assertFalse(self.engine._validate_adjacency(GlyphPhase.WHITE))
        self.assertFalse(self.engine._validate_adjacency(GlyphPhase.YELLOW))

    def test_sequential_adjacency(self):
        """Test sequential phase transitions are allowed"""
        self.engine.current_phase = GlyphPhase.BLACK
        self.assertTrue(self.engine._validate_adjacency(GlyphPhase.WHITE))

        self.engine.current_phase = GlyphPhase.WHITE
        self.assertTrue(self.engine._validate_adjacency(GlyphPhase.YELLOW))

    def test_skip_forbidden(self):
        """Test skipping phases is forbidden"""
        self.engine.current_phase = GlyphPhase.BLACK
        # BLACK (0) -> YELLOW (2) is a skip
        self.assertFalse(self.engine._validate_adjacency(GlyphPhase.YELLOW))

    def test_wrap_around_adjacency(self):
        """Test BLUE -> BLACK wrap-around is allowed"""
        self.engine.current_phase = GlyphPhase.BLUE
        self.assertTrue(self.engine._validate_adjacency(GlyphPhase.BLACK))


class TestGlyphCompression(unittest.TestCase):
    """Test full compression cycle"""

    def setUp(self):
        self.engine = GlyphEngine()

    def test_compress_simple(self):
        """Test compression of simple data"""
        data = b"Hello, CODEX!"
        result = self.engine.compress(data)

        self.assertIsNotNone(result.compressed_data)
        self.assertEqual(result.original_size, len(data))
        self.assertGreater(result.compressed_size, 0)

    def test_compress_metadata(self):
        """Test compression metadata"""
        data = b"test data"
        result = self.engine.compress(data)

        self.assertEqual(result.metadata['engine'], 'Glyph')
        self.assertEqual(result.metadata['version'], '1.0.0')
        self.assertIn('phases', result.metadata)
        self.assertIn('coherence', result.metadata)
        self.assertIn('gray_score', result.metadata)

    def test_compress_phases_executed(self):
        """Test that all 7 phases are executed"""
        data = b"test"
        result = self.engine.compress(data)

        phases = result.metadata['phases']
        expected_phases = ['BLACK', 'WHITE', 'YELLOW', 'BROWN', 'RED', 'GREEN', 'BLUE']
        self.assertEqual(phases, expected_phases)

    def test_compress_gray_detection(self):
        """Test Gray marker detection"""
        data = "test ∞ data".encode('utf-8')

        with self.assertRaises(ValueError) as ctx:
            self.engine.compress(data)

        self.assertIn("Gray marker", str(ctx.exception))

    def test_header_format(self):
        """Test compressed data has valid header"""
        data = b"test"
        result = self.engine.compress(data)

        # Check magic bytes
        self.assertEqual(result.compressed_data[:5], b'GLYPH')


class TestGlyphDecompression(unittest.TestCase):
    """Test decompression"""

    def setUp(self):
        self.engine = GlyphEngine()

    def test_decompress_simple(self):
        """Test basic decompression"""
        original = b"test data"
        compressed_result = self.engine.compress(original)

        decompressed_result = self.engine.decompress(compressed_result.compressed_data)

        self.assertIsNotNone(decompressed_result.decompressed_data)
        self.assertGreater(decompressed_result.decompressed_size, 0)

    def test_invalid_header(self):
        """Test decompression fails on invalid header"""
        bad_data = b"NOTGLYPH" + b"\x00" * 20

        with self.assertRaises(ValueError) as ctx:
            self.engine.decompress(bad_data)

        self.assertIn("Invalid", str(ctx.exception))

    def test_too_short_data(self):
        """Test decompression fails on truncated data"""
        with self.assertRaises(ValueError) as ctx:
            self.engine.decompress(b"GLY")

        self.assertIn("too short", str(ctx.exception))


class TestGlyphConfiguration(unittest.TestCase):
    """Test engine configuration options"""

    def test_strict_adjacency_disabled(self):
        """Test disabling strict adjacency"""
        engine = GlyphEngine(config={'strict_adjacency': False})
        self.assertFalse(engine.strict_adjacency)

    def test_strict_adjacency_enabled_default(self):
        """Test strict adjacency enabled by default"""
        engine = GlyphEngine()
        self.assertTrue(engine.strict_adjacency)


class TestGlyphIntegration(unittest.TestCase):
    """Test integration with CODEX framework"""

    def test_engine_registration(self):
        """Test that engine is registered"""
        from codex import list_engines

        engines = list_engines()
        engine_names = [e['name'] for e in engines]

        self.assertIn('Glyph', engine_names)

    def test_get_engine(self):
        """Test retrieving engine via registry"""
        from codex import get_engine

        engine = get_engine('glyph')
        self.assertIsInstance(engine, GlyphEngine)


if __name__ == '__main__':
    unittest.main()
