"""
An example showing the comparison of two slightly different DAGs,
building the signature for a straightforward DAG containing a variety
of data types.
"""
import hashlib
from blockdag import build_block_dag, compare_dags


def _hashfunc(value):
    return hashlib.sha256(value).hexdigest()


def _main():
    data_1 = {
        "a": {"data": 4},
        "b": {"data": "potato"},
        "c": {"data": [1, 2, "three", [4]]},
        "d": {"not_data": 4},
    }
    edges_1 = [("a", "b"), ("a", "c"), ("b", "d"), ("c", "d")]
    data_2 = {
        "a": {"data": 4},
        "b": {"data": "potato"},
        "c": {"data": [1, 23, "three", [4]]},
        "d": {"not_data": 5},
    }
    edges_2 = [("a", "b"), ("a", "c"), ("b", "d"), ("c", "d")]
    sig_1 = build_block_dag(data_1, edges_1, _hashfunc, ["data"])
    sig_2 = build_block_dag(data_2, edges_2, _hashfunc, ["data"])
    dags_same, diff_1, diff_2 = compare_dags(sig_1, sig_2)
    if not dags_same:
        print(diff_1)
        print(diff_2)


if __name__ == "__main__":
    _main()
