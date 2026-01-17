"""
Test suite for 2XKO Analyzer
"""

import unittest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from frame_data import (
    get_frame_data, is_safe_on_block, get_block_advantage,
    is_combo_starter, get_move_category, BLITZCRANK_FRAME_DATA
)
from analysis_engine import PlaystyleAnalyzer, RecommendationEngine, MistakeType


class TestFrameData(unittest.TestCase):
    """Test frame data database"""
    
    def test_frame_data_loaded(self):
        """Check that frame data exists"""
        self.assertTrue(len(BLITZCRANK_FRAME_DATA) > 0)
    
    def test_get_frame_data(self):
        """Test retrieving move data"""
        data = get_frame_data("5L")
        self.assertIsNotNone(data)
        self.assertEqual(data["damage"], 45)
        self.assertEqual(data["startup"], 8)
    
    def test_unknown_move(self):
        """Test querying non-existent move"""
        data = get_frame_data("NONEXISTENT")
        self.assertIsNone(data)
    
    def test_is_safe_on_block(self):
        """Test safe on block detection"""
        # 5L is -2f, so unsafe
        self.assertFalse(is_safe_on_block("5L"))
        
        # 5S1 is +4f, so safe
        self.assertTrue(is_safe_on_block("5S1"))
    
    def test_is_combo_starter(self):
        """Test combo starter detection"""
        self.assertTrue(is_combo_starter("2H"))  # Anti-air launcher
        self.assertTrue(is_combo_starter("5H"))  # Ground bounce on charge
        self.assertFalse(is_combo_starter("5L"))  # Light punch
    
    def test_get_move_category(self):
        """Test move categorization"""
        self.assertEqual(get_move_category("5S1"), "grab")
        self.assertEqual(get_move_category("2S2"), "special")
        self.assertEqual(get_move_category("Super1"), "super")
        self.assertEqual(get_move_category("Ultimate"), "ultimate")
        self.assertEqual(get_move_category("5L"), "normal")


class TestPlaystyleAnalyzer(unittest.TestCase):
    """Test playstyle detection"""
    
    def test_grab_heavy_playstyle(self):
        """Test detection of grab-heavy player"""
        analyzer = PlaystyleAnalyzer()
        
        moves = [
            {"move": "5S1"},
            {"move": "5S1"},
            {"move": "5S1"},
            {"move": "5L"},
            {"move": "2S2"},
        ]
        
        style = analyzer.analyze_playstyle(moves)
        self.assertIn("Grab", style)
    
    def test_strike_heavy_playstyle(self):
        """Test detection of strike-heavy player"""
        analyzer = PlaystyleAnalyzer()
        
        moves = [
            {"move": "5L"},
            {"move": "5M"},
            {"move": "5H"},
            {"move": "2L"},
            {"move": "2M"},
            {"move": "2H"},
        ]
        
        style = analyzer.analyze_playstyle(moves)
        self.assertIn("Strike", style)


class TestRecommendationEngine(unittest.TestCase):
    """Test recommendation generation"""
    
    def test_unsafe_move_recommendation(self):
        """Test unsafe move warning"""
        frame_data = {"on_block": -15}
        
        recommendations = RecommendationEngine.get_move_recommendations(
            "5H", "on_block", frame_data
        )
        
        self.assertTrue(any("UNSAFE" in rec for rec in recommendations))
    
    def test_blitzcrank_tips_loaded(self):
        """Test that Blitzcrank tips are available"""
        tips = RecommendationEngine.get_blitzcrank_tips()
        
        self.assertIn("neutral_game", tips)
        self.assertIn("mixup_game", tips)
        self.assertIn("steam_mechanic", tips)
        self.assertTrue(len(tips["neutral_game"]) > 0)


class TestMoveDatabaseCompleteness(unittest.TestCase):
    """Verify frame data completeness"""
    
    def test_move_has_required_fields(self):
        """Check each move has minimum required fields"""
        required_fields = ["damage", "startup", "recovery"]
        
        for move_name, data in BLITZCRANK_FRAME_DATA.items():
            for field in required_fields:
                self.assertIn(field, data, f"Move {move_name} missing {field}")
    
    def test_startup_less_than_recovery(self):
        """Verify startup is typically less than recovery"""
        for move_name, data in BLITZCRANK_FRAME_DATA.items():
            startup = data.get("startup", 0)
            recovery = data.get("recovery", float('inf'))
            
            # Most moves should have startup < recovery
            if move_name not in ["Ultimate", "2T"]:  # Some exceptions
                self.assertLessEqual(startup, recovery + 10, 
                    f"Suspicious startup/recovery for {move_name}")


def run_tests():
    """Run all tests"""
    print("\n" + "="*60)
    print("Running 2XKO Analyzer Tests")
    print("="*60 + "\n")
    
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    suite.addTests(loader.loadTestsFromTestCase(TestFrameData))
    suite.addTests(loader.loadTestsFromTestCase(TestPlaystyleAnalyzer))
    suite.addTests(loader.loadTestsFromTestCase(TestRecommendationEngine))
    suite.addTests(loader.loadTestsFromTestCase(TestMoveDatabaseCompleteness))
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    print("\n" + "="*60)
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print("="*60 + "\n")
    
    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)
