import importlib.util
from pathlib import Path
import sys
import unittest
_spec = importlib.util.spec_from_file_location('lab_' + Path(__file__).parent.name.replace('-', '_'), Path(__file__).with_name('main.py'))
m = importlib.util.module_from_spec(_spec)
sys.modules[_spec.name] = m
_spec.loader.exec_module(m)

class RendezvousTests(unittest.TestCase):

    def test_membership_order_is_irrelevant(self):
        a = m.Rendezvous(['a', 'b', 'c'])
        b = m.Rendezvous(['c', 'b', 'a'])
        self.assertEqual(a.rank('x', 3), b.rank('x', 3))

    def test_replicas_are_unique(self):
        r = m.Rendezvous(['a', 'b', 'c'])
        self.assertEqual(set(r.rank('x', 3)), {'a', 'b', 'c'})

    def test_add_moves_only_to_new_member(self):
        a = m.Rendezvous(['a', 'b'])
        b = m.Rendezvous(['a', 'b', 'c'])
        for key in map(str, range(500)):
            if a.rank(key) != b.rank(key):
                self.assertEqual(b.rank(key), ['c'])

    def test_removal_preserves_relative_ranking(self):
        a = m.Rendezvous(['a', 'b', 'c'])
        b = m.Rendezvous(['a', 'c'])
        for key in map(str, range(100)):
            self.assertEqual([n for n in a.rank(key, 3) if n != 'b'], b.rank(key, 2))

    def test_invalid_count_and_nodes(self):
        with self.assertRaises(ValueError):
            m.Rendezvous(['a', 'a'])
        with self.assertRaises(ValueError):
            m.Rendezvous(['a']).rank('x', 2)
        with self.assertRaises(ValueError):
            m.Rendezvous([]).rank('x')

    def test_single_node(self):
        self.assertEqual(m.Rendezvous(['a']).rank('anything'), ['a'])
if __name__ == '__main__':
    unittest.main()
