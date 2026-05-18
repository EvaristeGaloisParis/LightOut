import unittest

from scores import Score


class TestScore(unittest.TestCase):

    def test_date_auto_stamped(self):
        s = Score(nom='A', moves=10, lights=5, time_ms=1000)
        # Format attendu : YYYY-MM-DD HH:MM
        self.assertRegex(s.date, r'^\d{4}-\d{2}-\d{2} \d{2}:\d{2}$')

    def test_date_can_be_overridden(self):
        s = Score(nom='A', moves=10, lights=5, time_ms=1000, date='2020-01-01 00:00')
        self.assertEqual(s.date, '2020-01-01 00:00')

    def test_key_returns_moves_then_time(self):
        s = Score(nom='A', moves=10, lights=5, time_ms=1000)
        self.assertEqual(s.key, (10, 1000))

    def test_sort_by_moves_then_time(self):
        a = Score(nom='A', moves=10, lights=0, time_ms=5000)
        b = Score(nom='B', moves=8,  lights=0, time_ms=10000)
        c = Score(nom='C', moves=10, lights=0, time_ms=3000)
        # B (8 coups) < C (10 coups, 3000 ms) < A (10 coups, 5000 ms)
        ordered = sorted([a, b, c], key=lambda s: s.key)
        self.assertEqual([s.nom for s in ordered], ['B', 'C', 'A'])


if __name__ == '__main__':
    unittest.main()
