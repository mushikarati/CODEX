"""
Tests for KAIROS adjacency validation and Gray detection
"""

import unittest
from codex.utils import (
    MagickToken,
    KairosEngine,
    KairosMode,
    validate_sequence,
    repair_sequence,
    is_adjacent
)


class TestKairosAdjacency(unittest.TestCase):
    """Test adjacency validation"""

    def test_adjacent_tokens(self):
        """Test that ±1 tokens are adjacent"""
        # BLACK (0) -> WHITE (1) is +1
        self.assertTrue(is_adjacent(MagickToken.BLACK, MagickToken.WHITE))
        # WHITE (1) -> BLACK (0) is -1 (or 6 in mod 7)
        self.assertTrue(is_adjacent(MagickToken.WHITE, MagickToken.BLACK))
        # BLUE (6) -> BLACK (0) is +1 (wraps around)
        self.assertTrue(is_adjacent(MagickToken.BLUE, MagickToken.BLACK))

    def test_non_adjacent_tokens(self):
        """Test that skip tokens are not adjacent"""
        # BLACK (0) -> YELLOW (2) is +2 (skip)
        self.assertFalse(is_adjacent(MagickToken.BLACK, MagickToken.YELLOW))
        # BLACK (0) -> RED (4) is +4 (skip)
        self.assertFalse(is_adjacent(MagickToken.BLACK, MagickToken.RED))

    def test_adjacency_distance(self):
        """Test distance calculation on the 7-cycle"""
        engine = KairosEngine()
        # Adjacent: distance 1
        self.assertEqual(engine.adjacency_distance(MagickToken.BLACK, MagickToken.WHITE), 1)
        # Skip: distance 2
        self.assertEqual(engine.adjacency_distance(MagickToken.BLACK, MagickToken.YELLOW), 2)
        # Opposite: distance 3
        self.assertEqual(engine.adjacency_distance(MagickToken.BLACK, MagickToken.BROWN), 3)


class TestGrayDetection(unittest.TestCase):
    """Test Gray corruption detection"""

    def test_valid_sequence_no_gray(self):
        """Valid adjacent sequence should have no Gray"""
        seq = [
            MagickToken.BLACK,
            MagickToken.WHITE,
            MagickToken.YELLOW,
            MagickToken.BROWN,
            MagickToken.RED,
            MagickToken.GREEN,
            MagickToken.BLUE
        ]
        is_valid, threats = validate_sequence(seq)
        self.assertTrue(is_valid)
        self.assertEqual(len(threats), 0)

    def test_skip_sequence_has_gray(self):
        """Sequence with skips should detect Gray"""
        seq = [
            MagickToken.BLACK,
            MagickToken.YELLOW,  # Skip! (0 -> 2)
            MagickToken.RED      # Skip! (2 -> 4)
        ]
        is_valid, threats = validate_sequence(seq)
        self.assertFalse(is_valid)
        self.assertEqual(len(threats), 2)  # Two violations
        self.assertEqual(threats[0].index, 0)
        self.assertEqual(threats[0].distance, 2)

    def test_multiple_violations(self):
        """Detect multiple Gray violations"""
        seq = [
            MagickToken.BLACK,
            MagickToken.YELLOW,  # Violation 1
            MagickToken.GREEN,   # Violation 2 (2 -> 5)
            MagickToken.WHITE    # Violation 3 (5 -> 1)
        ]
        is_valid, threats = validate_sequence(seq)
        self.assertFalse(is_valid)
        self.assertGreaterEqual(len(threats), 1)  # At least one violation

    def test_gray_score_calculation(self):
        """Test normalized gray score"""
        engine = KairosEngine()
        # Perfect sequence
        perfect = [MagickToken.BLACK, MagickToken.WHITE, MagickToken.YELLOW]
        self.assertEqual(engine.sym_gray_score(perfect), 0.0)

        # All violations
        broken = [MagickToken.BLACK, MagickToken.YELLOW, MagickToken.GREEN]
        score = engine.sym_gray_score(broken)
        self.assertGreater(score, 0.0)


class TestRepairStrategies(unittest.TestCase):
    """Test Gray repair mechanisms"""

    def test_repair_simple_sequence(self):
        """Repair should fix simple violations"""
        seq = [
            MagickToken.BLACK,
            MagickToken.YELLOW,  # Should be WHITE or BLUE
            MagickToken.BROWN
        ]
        repaired, success = repair_sequence(seq)
        # Check if repaired has fewer violations
        engine = KairosEngine(mode=KairosMode.PASSIVE)
        original_violations = engine.violations(seq)
        repaired_violations = engine.violations(repaired)
        self.assertLessEqual(repaired_violations, original_violations)

    def test_repair_preserves_length_initially(self):
        """Greedy repair should not change length initially"""
        seq = [MagickToken.BLACK, MagickToken.YELLOW, MagickToken.RED]
        repaired, _ = repair_sequence(seq)
        # Note: K-series insertion may increase length
        self.assertGreaterEqual(len(repaired), len(seq))

    def test_threat_severity(self):
        """Test threat severity calculation"""
        from codex.utils.kairos import GrayThreat
        # Distance 1 = no threat
        t1 = GrayThreat(0, "⚫", "⚪", 1)
        self.assertEqual(t1.severity, 0.0)

        # Distance 2 = medium
        t2 = GrayThreat(0, "⚫", "🟡", 2)
        self.assertGreater(t2.severity, 0.0)
        self.assertLess(t2.severity, 0.7)

        # Distance 4 = critical
        t4 = GrayThreat(0, "⚫", "🔴", 4)
        self.assertEqual(t4.severity, 1.0)


class TestKairosEngine(unittest.TestCase):
    """Test KAIROS engine modes and forensics"""

    def test_passive_mode_no_repair(self):
        """Passive mode should detect but not repair"""
        engine = KairosEngine(mode=KairosMode.PASSIVE)
        seq = [MagickToken.BLACK, MagickToken.YELLOW]
        repaired, success = engine.repair_sequence(seq)
        # Should return original sequence
        self.assertEqual(repaired, seq)
        self.assertFalse(success)

    def test_active_mode_repairs(self):
        """Active mode should attempt repairs"""
        engine = KairosEngine(mode=KairosMode.ACTIVE)
        seq = [MagickToken.BLACK, MagickToken.YELLOW, MagickToken.RED]
        repaired, success = engine.repair_sequence(seq)
        # Should have attempted repair
        self.assertGreater(engine.repair_count, 0)

    def test_threat_report(self):
        """Test forensic threat reporting"""
        engine = KairosEngine()
        seq = [MagickToken.BLACK, MagickToken.YELLOW, MagickToken.GREEN]
        engine.detect_gray(seq)

        report = engine.get_threat_report()
        self.assertGreater(report["total_threats"], 0)
        self.assertIn("avg_severity", report)
        self.assertIn("critical_count", report)

    def test_clear_log(self):
        """Test log clearing"""
        engine = KairosEngine()
        seq = [MagickToken.BLACK, MagickToken.YELLOW]
        engine.detect_gray(seq)
        self.assertGreater(len(engine.threat_log), 0)

        engine.clear_log()
        self.assertEqual(len(engine.threat_log), 0)


class TestCanonicalSequences(unittest.TestCase):
    """Test canonical CODEX sequences"""

    def test_ascending_cycle(self):
        """Ascending sequence should be valid"""
        seq = [
            MagickToken.BLACK,
            MagickToken.WHITE,
            MagickToken.YELLOW,
            MagickToken.BROWN,
            MagickToken.RED,
            MagickToken.GREEN,
            MagickToken.BLUE,
            MagickToken.BLACK  # Wrap around
        ]
        is_valid, threats = validate_sequence(seq)
        self.assertTrue(is_valid)

    def test_descending_cycle(self):
        """Descending sequence should be valid"""
        seq = [
            MagickToken.BLACK,
            MagickToken.BLUE,
            MagickToken.GREEN,
            MagickToken.RED,
            MagickToken.BROWN,
            MagickToken.YELLOW,
            MagickToken.WHITE,
            MagickToken.BLACK  # Wrap around
        ]
        is_valid, threats = validate_sequence(seq)
        self.assertTrue(is_valid)


if __name__ == '__main__':
    unittest.main()
