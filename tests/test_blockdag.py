"""
Implements basic tests for blockDAG building and comparison functionalities.
"""
import hashlib
import unittest

from blockdag import build_block_dag


def _hashfunc(value):
    return hashlib.sha256(value).hexdigest()


def _gen_simple_dag():
    data = {
        "a": {"data": 5},
        "b": {"data": "potato"},
        "c": {"data": [1, 2, "three", [4]]},
        "d": {"not_data": 4},
    }
    edges = [("a", "b"), ("a", "c"), ("b", "d"), ("c", "d")]
    return data, edges


class BlockDAGTest(unittest.TestCase):
    """
    Runs a number of tests cases for construction and comparison of BlockDAGs.
    """

    def test_simple_unfiltered(self):
        """
        A simple test accepting all data in the generated DAG.
        """
        data, edges = _gen_simple_dag()
        sig = build_block_dag(data, edges, _hashfunc)
        sig.pop("signature")
        for _, sig_val in sig.items():
            self.assertIsNotNone(sig_val["data_hash"])

    def test_simple_filtered(self):
        """
        Makes sure that inclusive filtering works
        """
        data, edges = _gen_simple_dag()
        sig = build_block_dag(data, edges, _hashfunc, ["data"])
        self.assertIsNone(sig["d"]["data_hash"])
        for key in ["a", "b", "c"]:
            self.assertIsNotNone(sig[key]["data_hash"])

    def test_simple_empty(self):
        """
        Tests a dag that is filtered with no fields. Should return None as signature.
        """
        data, edges = _gen_simple_dag()
        sig = build_block_dag(data, edges, _hashfunc, [])
        sig.pop("signature")
        for _, sig_val in sig.items():
            self.assertIsNone(sig_val["data_hash"])

    def test_empty(self):
        """
        Tests a completely empty DAG
        """
        data = {}
        edges = []
        sig = build_block_dag(data, edges, _hashfunc)
        self.assertEqual({"signature": None}, sig)

    def test_filter_to_empty(self):
        """
        Tests a DAG that is filtered to nothing.
        """
        data, edges = _gen_simple_dag()
        sig = build_block_dag(data, edges, _hashfunc, ["non_field"])
        sig.pop("signature")
        for _, sig_val in sig.items():
            self.assertIsNone(sig_val["data_hash"])

    def test_changed_names(self):
        """
        Tests two DAGs with the same structured but different key names.
        Should produce identical signatures.
        """
        data_1, edges_1 = _gen_simple_dag()
        data_2, _ = _gen_simple_dag()
        data_2["ab"] = data_2.pop("b")
        data_2["ba"] = data_2.pop("a")
        edges_2 = [("ba", "ab"), ("ba", "c"), ("ab", "d"), ("c", "d")]
        sig_1 = build_block_dag(data_1, edges_1, _hashfunc)
        sig_2 = build_block_dag(data_2, edges_2, _hashfunc)
        self.assertEqual(sig_1["signature"], sig_2["signature"])

    def test_multiple_parents(self):
        """
        Tests a DAG with multiple identical parents. Parents hashes should append and not be a set.
        """
        data, edges = _gen_simple_dag()
        data["e"] = data["a"].copy()
        edges.append(("e", "b"))
        sig = build_block_dag(data, edges, _hashfunc, ["data"])
        self.assertEqual(sig["a"]["hash"], sig["e"]["hash"])
        self.assertEqual(2, len(sig["b"]["parent_hashes"]))

    def test_cycles(self):
        """
        Tests a graph that is a cycle. It should error.
        """
        data, edges = _gen_simple_dag()
        edges.append(("d", "a"))
        self.assertRaises(
            AssertionError, build_block_dag, data, edges, _hashfunc, ["non_field"]
        )

    def test_non_values(self):
        """
        Tests invocation with no data field.
        """
        _, edges = _gen_simple_dag()
        self.assertRaises(AttributeError, build_block_dag, None, edges, _hashfunc)

    def test_no_edges(self):
        """
        Tests invocation with no edges.
        """
        data, _ = _gen_simple_dag()
        self.assertRaises(AttributeError, build_block_dag, data, None, _hashfunc)

    def test_no_hashfunction(self):
        """
        Tests invocation with no hash function supplied (uses default).
        """
        data, edges = _gen_simple_dag()
        sig_1 = build_block_dag(data, edges)
        sig_2 = build_block_dag(data, edges, _hashfunc)
        self.assertEqual(sig_1["signature"], sig_2["signature"])

    def test_append_hash(self):
        """
        Tests append_hash functionality. Makes sure all vertices have a hash value.
        """
        data, edges = _gen_simple_dag()
        build_block_dag(data, edges, _hashfunc, append_hashes=True)
        for _, val in data.items():
            self.assertIsNotNone(val["hash"])

    def test_append_hash_preexisting(self):
        """
        Tests append_hash functionality and that append_hashes overwrites pre-existing values.
        """
        data, edges = _gen_simple_dag()
        sig = build_block_dag(data, edges, _hashfunc, append_hashes=True)
        data["a"]["data"] = [5, 6, 7, 8]
        sig_2 = build_block_dag(data, edges, _hashfunc, append_hashes=True)
        self.assertNotEqual(sig["signature"], sig_2["signature"])

    def test_traversal_function(self):
        data, edges = _gen_simple_dag()

        def simple_sum(element_id, element, **kwargs):
            for key, val in kwargs.items():
                element[key] = val

        for element in data.values():
            self.assertNotIn("i", element)
        sig = build_block_dag(data, edges, _hashfunc, ["i"], False)
        sig_2 = build_block_dag(data, edges, _hashfunc, ["i"], False, simple_sum, i=42)
        for element in data.values():
            self.assertIn("i", element)
            self.assertEqual(42, element["i"])
        self.assertNotEqual(sig["signature"], sig_2["signature"])
