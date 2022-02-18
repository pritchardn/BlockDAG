from merkledag import build_merkle_dag
import hashlib
import json


def hashfunc(value):
    return hashlib.sha256(value).hexdigest()


def main():
    data = {'a': {'data': 3},
            'b': {'data': "potato"},
            'c': {'data': [1, 2, "three", [4]]},
            'd': {'not_data': 4}
            }
    edges = [('a', 'b'), ('a', 'c'), ('b', 'd'), ('c', 'd')]
    sig = build_merkle_dag(data, edges, hashfunc, ['data'])
    print(json.dumps(sig, indent=4))


if __name__ == "__main__":
    main()
