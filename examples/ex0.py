"""
A simple first example, building the signature for a straightforward DAG containing a variety
of data types.
"""
import hashlib
from blockdag import build_block_dag, pretty_prints


def _hashfunc(value):
    return hashlib.sha256(value).hexdigest()


def _main():
    data = {
        "a": {"data": 3, "important": [1, 2], "not_data": "help"},
        "b": {"data": "secrets"},
        "c": {"data": [1, "two", 3], "important": [4, 5]},
        "d": {"not_data": "help"},
    }
    edges = [("a", "c"), ("b", "c"), ("b", "d"), ("c", "d")]
    sig = build_block_dag(data, edges, _hashfunc, ["data", "important"])
    print(pretty_prints(data, edges, sig))


if __name__ == "__main__":
    _main()
