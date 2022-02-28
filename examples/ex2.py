"""
An example showing the append_hash behaviour,
building the signature for a straightforward DAG containing a variety
of data types.
"""
from blockdag import build_block_dag, pretty_prints


def _main():
    data = {
        "a": {"data": 3},
        "b": {"data": "stringy_string"},
        "c": {"data": [1, 2, "three", [4, 5]]},
        "d": {"not_data": None},
    }
    edges = [("a", "b"), ("a", "c"), ("b", "d"), ("c", "d")]
    sig = build_block_dag(data, edges, data_fields=["data"], append_hashes=True)
    print(pretty_prints(data, edges, sig))


if __name__ == "__main__":
    _main()
