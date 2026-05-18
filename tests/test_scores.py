import json
import os
import tempfile
import unittest
from unittest.mock import patch

import scores as scores_module
from scores import Score, Scores


class TestScores(unittest.TestCase):

    def setUp(self):
        fd, self._path = tempfile.mkstemp(suffix='.json')
        os.close(fd)
        os.unlink(self._path)   # on veut un fichier qui n'existe pas encore
        self._patcher = patch.object(scores_module, 'SCORES_FILE', self._path)
        self._patcher.start()

    def tearDown(self):
        self._patcher.stop()
        if os.path.exists(self._path):
            os.unlink(self._path)

    def test_empty_when_file_missing(self):
        s = Scores()
        self.assertEqual(s.top(10), [])

    def test_add_returns_rank_one(self):
        s = Scores()
        rank = s.add(Score(nom='A', moves=10, lights=0, time_ms=1000))
        self.assertEqual(rank, 1)

    def test_add_persists(self):
        s = Scores()
        s.add(Score(nom='A', moves=10, lights=0, time_ms=1000))
        with open(self._path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['nom'], 'A')
        self.assertIn('date', data[0])

    def test_ranks_by_moves_then_time(self):
        s = Scores()
        s.add(Score(nom='A', moves=10, lights=0, time_ms=5000))
        rank_b = s.add(Score(nom='B', moves=8,  lights=0, time_ms=10000))
        rank_c = s.add(Score(nom='C', moves=10, lights=0, time_ms=3000))
        self.assertEqual(rank_b, 1)   # B (8 coups) prend la tête
        self.assertEqual(rank_c, 2)   # C (10 coups, 3 s) avant A (10 coups, 5 s)
        self.assertEqual([x.nom for x in s.top(3)], ['B', 'C', 'A'])

    def test_top_limits_to_n(self):
        s = Scores()
        for i in range(5):
            s.add(Score(nom=f'P{i}', moves=10 + i, lights=0, time_ms=1000))
        self.assertEqual(len(s.top(3)), 3)

    def test_top_accepts_more_than_available(self):
        s = Scores()
        s.add(Score(nom='A', moves=1, lights=0, time_ms=1))
        self.assertEqual(len(s.top(99)), 1)

    def test_loads_existing_file(self):
        data = [{'nom': 'X', 'moves': 5, 'lights': 0, 'time_ms': 1000, 'date': '2020-01-01 00:00'}]
        with open(self._path, 'w', encoding='utf-8') as f:
            json.dump(data, f)
        s = Scores()
        self.assertEqual(len(s.top(10)), 1)
        self.assertEqual(s.top(1)[0].nom, 'X')
        self.assertEqual(s.top(1)[0].date, '2020-01-01 00:00')


if __name__ == '__main__':
    unittest.main()
