"""Test home menu scene and difficulty selection."""

import unittest

import pygame

from src.view.home_scene import compute_menu_icon_rects, difficulty_from_percent


class TestHomeScene(unittest.TestCase):
    """Home menu UI layout and controls."""

    def test_tutorial_icon_is_next_to_settings_icon(self):
        """Tutorial icon precedes settings icon on home menu."""
        panel = pygame.Rect(100, 80, 600, 420)
        tutorial_rect, settings_rect = compute_menu_icon_rects(panel)

        self.assertEqual(tutorial_rect.y, settings_rect.y)
        self.assertLess(tutorial_rect.x, settings_rect.x)
        self.assertEqual(settings_rect.x - tutorial_rect.x, 48)

    def test_difficulty_from_percent_easy(self):
        """Low percent maps to Easy."""
        self.assertEqual(difficulty_from_percent(0.0), "easy")
        self.assertEqual(difficulty_from_percent(0.2), "easy")

    def test_difficulty_from_percent_medium(self):
        """Mid percent maps to Medium."""
        self.assertEqual(difficulty_from_percent(0.5), "medium")

    def test_difficulty_from_percent_hard(self):
        """High percent maps to Hard."""
        self.assertEqual(difficulty_from_percent(0.9), "hard")

    def test_difficulty_from_percent_clamps_bounds(self):
        """Handles out-of-range input safely."""
        self.assertEqual(difficulty_from_percent(-1), "easy")
        self.assertEqual(difficulty_from_percent(2), "hard")


if __name__ == "__main__":
    unittest.main()
