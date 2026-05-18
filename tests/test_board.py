import unittest

from board import Board


class TestBoard(unittest.TestCase):

    def test_initial_state_no_active(self):
        b = Board()
        self.assertEqual(b.level, 0)
        self.assertFalse(b.is_won)
        self.assertEqual(b.total_moves, 0)
        self.assertEqual(b.total_lights, 0)
        self.assertEqual(b.total_ms, 0)

    def test_start_loads_level_1(self):
        b = Board()
        self.assertTrue(b.start())
        self.assertEqual(b.level, 1)

    def test_push_unknown_level_fails(self):
        b = Board()
        self.assertFalse(b.push_map(99999))

    def test_push_valid_level_changes_level(self):
        b = Board()
        b.start()
        b.push_map(3)
        self.assertEqual(b.level, 3)

    def test_reset_all_returns_to_level_1(self):
        b = Board()
        b.start()
        b.push_map(5)
        b.reset_all()
        self.assertEqual(b.level, 1)
        self.assertFalse(b.is_won)
        self.assertEqual(b.total_moves, 0)
        self.assertEqual(b.total_lights, 0)
        self.assertEqual(b.total_ms, 0)

    def test_reset_level_when_no_active_returns_false(self):
        b = Board()
        self.assertFalse(b.reset_level())

    def test_reset_level_keeps_id(self):
        b = Board()
        b.push_map(3)
        self.assertTrue(b.reset_level())
        self.assertEqual(b.level, 3)

    def test_add_move_when_no_active_noop(self):
        b = Board()
        b.add_move()  # ne doit pas crasher
        self.assertEqual(b.total_moves, 0)

    def test_is_on_when_no_active(self):
        b = Board()
        self.assertFalse(b.is_on(0, 0))

    def test_high_light_when_no_active_noop(self):
        b = Board()
        b.high_light(0, 0)  # ne doit pas crasher

    def test_high_light_corner_toggles_2x2(self):
        b = Board()
        b.push_map(1)
        before = [[b.is_on(r, c) for c in range(5)] for r in range(5)]
        b.high_light(0, 0)
        after = [[b.is_on(r, c) for c in range(5)] for r in range(5)]
        # Coin haut-gauche : (0,0), (0,1), (1,0), (1,1) = 4 cases
        changed_cells = {
            (r, c) for r in range(5) for c in range(5)
            if before[r][c] != after[r][c]
        }
        self.assertEqual(changed_cells, {(0, 0), (0, 1), (1, 0), (1, 1)})

    def test_high_light_center_toggles_3x3(self):
        b = Board()
        b.push_map(1)
        before = [[b.is_on(r, c) for c in range(5)] for r in range(5)]
        b.high_light(2, 2)
        after = [[b.is_on(r, c) for c in range(5)] for r in range(5)]
        changed_cells = {
            (r, c) for r in range(5) for c in range(5)
            if before[r][c] != after[r][c]
        }
        expected = {(r, c) for r in range(1, 4) for c in range(1, 4)}
        self.assertEqual(changed_cells, expected)

    def test_high_light_edge_toggles_2x3(self):
        b = Board()
        b.push_map(1)
        before = [[b.is_on(r, c) for c in range(5)] for r in range(5)]
        b.high_light(0, 2)
        after = [[b.is_on(r, c) for c in range(5)] for r in range(5)]
        changed_cells = {
            (r, c) for r in range(5) for c in range(5)
            if before[r][c] != after[r][c]
        }
        expected = {(0, 1), (0, 2), (0, 3), (1, 1), (1, 2), (1, 3)}
        self.assertEqual(changed_cells, expected)

    def test_high_light_increments_lighting_counter(self):
        b = Board()
        b.push_map(1)
        m_before = b.coups_level
        b.high_light(0, 0)
        # Le compteur "light" du niveau a été incrémenté
        self.assertIn('light: 1', b.coups_level)


if __name__ == '__main__':
    unittest.main()
