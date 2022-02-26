import unittest
import hashlib
from blockdag import build_block_dag


def hashfunc(value):
    return hashlib.sha256(value).hexdigest()


def gen_simple_dag():
    data = {'a': {'data': 3},
            'b': {'data': "potato"},
            'c': {'data': [1, 2, "three", [4]]},
            'd': {'not_data': 4}
            }
    edges = [('a', 'b'), ('a', 'c'), ('b', 'd'), ('c', 'd')]
    return data, edges


class BlockDAGTest(unittest.TestCase):

    def test_simple_unfiltered(self):
        data, edges = gen_simple_dag()
        sig = build_block_dag(data, edges, hashfunc)
        sig.pop('signature')
        for key, sig_val in sig.items():
            self.assertIsNotNone(sig_val['data_hash'])

    def test_simple_filtered(self):
        data, edges = gen_simple_dag()
        sig = build_block_dag(data, edges, hashfunc, ['data'])
        self.assertIsNone(sig['d']['data_hash'])
        for key in ['a', 'b', 'c']:
            self.assertIsNotNone(sig[key]['data_hash'])

    def test_simple_empty(self):
        data, edges = gen_simple_dag()
        sig = build_block_dag(data, edges, hashfunc, [])
        sig.pop('signature')
        for key, sig_val in sig.items():
            self.assertIsNone(sig_val['data_hash'])

    def test_empty(self):
        data = {}
        edges = []
        sig = build_block_dag(data, edges, hashfunc)
        self.assertEqual({'signature': None}, sig)

    def test_filter_to_empty(self):
        data, edges = gen_simple_dag()
        sig = build_block_dag(data, edges, hashfunc, ['non_field'])
        sig.pop('signature')
        for key, sig_val in sig.items():
            self.assertIsNone(sig_val['data_hash'])

    def test_changed_names(self):
        data_1, edges_1 = gen_simple_dag()
        data_2, _ = gen_simple_dag()
        data_2['ab'] = data_2.pop('b')
        data_2['ba'] = data_2.pop('a')
        edges_2 = [('ba', 'ab'), ('ba', 'c'), ('ab', 'd'), ('c', 'd')]
        sig_1 = build_block_dag(data_1, edges_1, hashfunc)
        sig_2 = build_block_dag(data_2, edges_2, hashfunc)
        self.assertEqual(sig_1['signature'], sig_2['signature'])

    def test_multiple_parents(self):
        data, edges = gen_simple_dag()
        data['e'] = data['a'].copy()
        edges.append(('e', 'b'))
        sig = build_block_dag(data, edges, hashfunc, ['data'])
        self.assertEqual(sig['a']['hash'], sig['e']['hash'])
        self.assertEqual(2, len(sig['b']['parent_hashes']))

    def test_cycles(self):
        data, edges = gen_simple_dag()
        edges.append(('d', 'a'))
        self.assertRaises(AssertionError, build_block_dag, data, edges, hashfunc, ['non_field'])

    def test_non_values(self):
        data, edges = gen_simple_dag()
        self.assertRaises(AttributeError, build_block_dag, None, edges, hashfunc)

    def test_no_edges(self):
        data, edges = gen_simple_dag()
        self.assertRaises(AttributeError, build_block_dag, data, None, hashfunc)

    def test_no_hashfunction(self):
        data, edges = gen_simple_dag()
        sig_1 = build_block_dag(data, edges, None)
        sig_2 = build_block_dag(data, edges, hashfunc)
        self.assertEqual(sig_1['signature'], sig_2['signature'])

    def test_append_hash(self):
        data, edges = gen_simple_dag()
        build_block_dag(data, edges, hashfunc, append_hashes=True)
        for key, val in data.items():
            self.assertIsNotNone(val['hash'])

    def test_append_hash_preexisting(self):
        data, edges = gen_simple_dag()
        sig = build_block_dag(data, edges, hashfunc, append_hashes=True)
        data['a']['data'] = [5, 6, 7, 8]
        sig_2 = build_block_dag(data, edges, hashfunc, append_hashes=True)
        self.assertNotEqual(sig['signature'], sig_2['signature'])
