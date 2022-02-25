from blockdag import build_hash_dag, pretty_prints
import hashlib


def hashfunc(value):
    return hashlib.sha256(value).hexdigest()


def main():
    data = {'a': {'data': 3, 'important': [1, 2], 'not_data': 'help'},
            'b': {'data': "secrets"},
            'c': {'data': [1, 'two', 3], 'important': [4, 5]},
            'd': {'not_data': 'help'}
            }
    edges = [('a', 'c'), ('b', 'c'), ('b', 'd'), ('c', 'd')]
    sig = build_hash_dag(data, edges, hashfunc, ['data', 'important'])
    print(pretty_prints(data, edges, sig))


if __name__ == "__main__":
    main()
