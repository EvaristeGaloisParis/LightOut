import os
os.environ.setdefault('SDL_VIDEODRIVER', 'dummy')

import time
import unittest

import pygame
pygame.init()

from map import Map


class TestMap(unittest.TestCase):

    def test_initial_value_full_mask(self):
        """Toutes les cases sont allumées quand initial_value couvre les 25 bits."""
        m = Map(idx=1, initial_value=0xFFFFFFFF)
        for r in range(5):
            for c in range(5):
                self.assertTrue(m.is_on(r, c))

    def test_initial_value_zero(self):
        m = Map(idx=1, initial_value=0)
        for r in range(5):
            for c in range(5):
                self.assertFalse(m.is_on(r, c))
        self.assertTrue(m.is_finish())

    def test_bit_position_top_left(self):
        # Position (0,0) = bit le plus à gauche (24)
        m = Map(idx=1, initial_value=1 << 24)
        self.assertTrue(m.is_on(0, 0))
        self.assertFalse(m.is_on(0, 1))
        self.assertFalse(m.is_on(4, 4))

    def test_bit_position_bottom_right(self):
        # Position (4,4) = bit 0
        m = Map(idx=1, initial_value=1)
        self.assertTrue(m.is_on(4, 4))
        self.assertFalse(m.is_on(4, 3))
        self.assertFalse(m.is_on(0, 0))

    def test_change_toggles(self):
        m = Map(idx=1, initial_value=0)
        self.assertFalse(m.is_on(2, 2))
        m.change(2, 2)
        self.assertTrue(m.is_on(2, 2))
        m.change(2, 2)
        self.assertFalse(m.is_on(2, 2))

    def test_change_only_affects_target(self):
        m = Map(idx=1, initial_value=0)
        m.change(1, 3)
        self.assertTrue(m.is_on(1, 3))
        # Aucune autre case allumée
        for r in range(5):
            for c in range(5):
                if (r, c) != (1, 3):
                    self.assertFalse(m.is_on(r, c))

    def test_is_finish(self):
        m = Map(idx=1, initial_value=0)
        self.assertTrue(m.is_finish())
        m.change(0, 0)
        self.assertFalse(m.is_finish())
        m.change(0, 0)
        self.assertTrue(m.is_finish())

    def test_add_coup_counters(self):
        m = Map(idx=1, initial_value=0)
        m.add_coup(move=True, light=False)
        m.add_coup(move=True, light=False)
        m.add_coup(move=False, light=True)
        self.assertEqual(m.moves, 2)
        self.assertEqual(m.lighting, 1)

    def test_level_id(self):
        m = Map(idx=42, initial_value=0)
        self.assertEqual(m.level_id, 42)

    def test_elapsed_advances_before_stop(self):
        m = Map(idx=1, initial_value=0)
        t1 = m.elapsed_ms
        time.sleep(0.05)
        t2 = m.elapsed_ms
        self.assertGreater(t2, t1)

    def test_stop_timer_freezes(self):
        m = Map(idx=1, initial_value=0)
        time.sleep(0.02)
        m.stop_timer()
        t1 = m.elapsed_ms
        time.sleep(0.05)
        t2 = m.elapsed_ms
        self.assertEqual(t1, t2)

    def test_stop_timer_idempotent(self):
        m = Map(idx=1, initial_value=0)
        time.sleep(0.02)
        m.stop_timer()
        t1 = m.elapsed_ms
        time.sleep(0.02)
        m.stop_timer()        # ne doit pas écraser
        t2 = m.elapsed_ms
        self.assertEqual(t1, t2)


if __name__ == '__main__':
    unittest.main()
