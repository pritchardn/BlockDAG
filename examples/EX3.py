from blockdag import build_block_dag, pretty_prints, compare_dags
import hashlib


def hashfunc(value):
    return hashlib.sha256(value).hexdigest()


def main():
    data = {'a': {'data': 3},
            'b': {'data': "potato"},
            'c': {'data': [1, 2, "three", [4]]},
            'd': {'not_data': 4}
            }
    edges = [('a', 'b'), ('a', 'c'), ('b', 'd'), ('c', 'd')]
    sig = build_block_dag(data, edges, hashfunc, ['data'], append_hashes=True)
    print(pretty_prints(data, edges, sig))
    print(compare_dags(data, sig))


if __name__ == "__main__":
    main()
