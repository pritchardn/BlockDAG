from blockdag import build_block_dag, pretty_prints
import hashlib


def hashfunc(value):
    return hashlib.sha256(value).hexdigest()


def binomial_tree(size):
    N = 1
    edges = []
    vertices = {}
    for i in range(size):
        edges += [(edge[0] + N, edge[1] + N) for edge in edges]
        edges += [(0, N)]
        N *= 2
    for i in range(N):
        vertices[i] = {'data': i}
    return vertices, edges


def main():
    data, edges = binomial_tree(15)
    print(f"{len(data)} vertices\n{len(edges)} edges")
    sig = build_block_dag(data, edges, hashfunc, ['data', 'important'])
    print(pretty_prints(data, edges, sig))


if __name__ == "__main__":
    main()
