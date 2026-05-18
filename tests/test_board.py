import unittest

from board import Board


class TestBoard(unittest.TestCase):
    """Tests basés sur le vrai fichier de maps (factory from_file)."""

    def test_initial_state_no_active(self):
        b = Board.from_file()
        self.assertEqual(b.level, 0)
        self.assertFalse(b.is_won)
        self.assertEqual(b.total_moves, 0)
        self.assertEqual(b.total_lights, 0)
        self.assertEqual(b.total_ms, 0)

    def test_start_loads_level_1(self):
        b = Board.from_file()
        self.assertTrue(b.start())
        self.assertEqual(b.level, 1)

    def test_push_unknown_level_fails(self):
        b = Board.from_file()
        self.assertFalse(b.push_map(99999))

    def test_push_valid_level_changes_level(self):
        b = Board.from_file()
        b.start()
        b.push_map(3)
        self.assertEqual(b.level, 3)

    def test_reset_all_returns_to_level_1(self):
        b = Board.from_file()
        b.start()
        b.push_map(5)
        b.reset_all()
        self.assertEqual(b.level, 1)
        self.assertFalse(b.is_won)
        self.assertEqual(b.total_moves, 0)
        self.assertEqual(b.total_lights, 0)
        self.assertEqual(b.total_ms, 0)

    def test_reset_level_when_no_active_returns_false(self):
        b = Board.from_file()
        self.assertFalse(b.reset_level())

    def test_reset_level_keeps_id(self):
        b = Board.from_file()
        b.push_map(3)
        self.assertTrue(b.reset_level())
        self.assertEqual(b.level, 3)

    def test_add_move_when_no_active_noop(self):
        b = Board.from_file()
        b.add_move()
        self.assertEqual(b.total_moves, 0)

    def test_is_on_when_no_active(self):
        b = Board.from_file()
        self.assertFalse(b.is_on(0, 0))

    def test_high_light_when_no_active_noop(self):
        b = Board.from_file()
        b.high_light(0, 0)

    def test_high_light_corner_toggles_2x2(self):
        b = Board.from_file()
        b.push_map(1)
        before = [[b.is_on(r, c) for c in range(5)] for r in range(5)]
        b.high_light(0, 0)
        after = [[b.is_on(r, c) for c in range(5)] for r in range(5)]
        changed = {(r, c) for r in range(5) for c in range(5) if before[r][c] != after[r][c]}
        self.assertEqual(changed, {(0, 0), (0, 1), (1, 0), (1, 1)})

    def test_high_light_center_toggles_3x3(self):
        b = Board.from_file()
        b.push_map(1)
        before = [[b.is_on(r, c) for c in range(5)] for r in range(5)]
        b.high_light(2, 2)
        after = [[b.is_on(r, c) for c in range(5)] for r in range(5)]
        changed = {(r, c) for r in range(5) for c in range(5) if before[r][c] != after[r][c]}
        expected = {(r, c) for r in range(1, 4) for c in range(1, 4)}
        self.assertEqual(changed, expected)

    def test_high_light_edge_toggles_2x3(self):
        b = Board.from_file()
        b.push_map(1)
        before = [[b.is_on(r, c) for c in range(5)] for r in range(5)]
        b.high_light(0, 2)
        after = [[b.is_on(r, c) for c in range(5)] for r in range(5)]
        changed = {(r, c) for r in range(5) for c in range(5) if before[r][c] != after[r][c]}
        expected = {(0, 1), (0, 2), (0, 3), (1, 1), (1, 2), (1, 3)}
        self.assertEqual(changed, expected)

    def test_high_light_increments_lighting_counter(self):
        b = Board.from_file()
        b.push_map(1)
        b.high_light(0, 0)
        self.assertIn('light: 1', b.coups_level)


class TestBoardInjection(unittest.TestCase):
    """Tests qui injectent un dict de maps minimal pour vérifier la progression
    et la fin de partie sans dépendre du vrai fichier."""

    @staticmethod
    def _pattern_coin_haut_gauche() -> int:
        """Bits allumés exactement par une pression en (0,0).
        Presser (0,0) sur cette map la résout en un seul coup."""
        return (1 << 24) | (1 << 23) | (1 << 19) | (1 << 18)

    def test_progression_d_un_niveau(self):
        # Deux niveaux triviaux à un coup
        pattern = self._pattern_coin_haut_gauche()
        b = Board({1: pattern, 2: pattern})
        b.start()
        self.assertEqual(b.level, 1)
        b.high_light(0, 0)               # résout le niveau 1
        self.assertEqual(b.level, 2)     # progression automatique
        self.assertFalse(b.is_won)

    def test_is_won_apres_dernier_niveau(self):
        # Un seul niveau dans l'univers de jeu
        b = Board({1: self._pattern_coin_haut_gauche()})
        b.start()
        b.high_light(0, 0)               # résout l'unique niveau
        self.assertTrue(b.is_won)
        self.assertEqual(b.level, 0)     # plus de niveau actif
        self.assertEqual(b.total_lights, 1)

    def test_totaux_cumulent_apres_resolution(self):
        pattern = self._pattern_coin_haut_gauche()
        b = Board({1: pattern, 2: pattern})
        b.start()
        # Quelques déplacements puis résolution
        b.add_move()
        b.add_move()
        b.high_light(0, 0)
        self.assertEqual(b.total_moves, 2)
        self.assertEqual(b.total_lights, 1)

    def test_reset_all_apres_victoire(self):
        b = Board({1: self._pattern_coin_haut_gauche()})
        b.start()
        b.high_light(0, 0)
        self.assertTrue(b.is_won)
        b.reset_all()
        self.assertFalse(b.is_won)
        self.assertEqual(b.level, 1)
        self.assertEqual(b.total_lights, 0)

    def test_coups_level_format_sans_actif(self):
        b = Board({1: 0})
        self.assertEqual(b.coups_level, 'move: 0 - light: 0 - time: 00:00')

    def test_coups_format_avec_actif(self):
        b = Board({1: 0})
        b.start()
        self.assertIn('move: 0', b.coups)
        self.assertIn('light: 0', b.coups)
        self.assertIn('time:', b.coups)


if __name__ == '__main__':
    unittest.main()
