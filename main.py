"""Highest-random-weight placement with deterministic replica candidates."""
import argparse
import hashlib
import json

class Rendezvous:

    def __init__(self, nodes):
        if not isinstance(nodes, (list, tuple)) or any((not isinstance(n, str) or not n for n in nodes)) or len(set(nodes)) != len(nodes):
            raise ValueError('Nodes must be unique nonempty strings')
        self.nodes = tuple(sorted(nodes))

    def rank(self, key, count=1):
        if not isinstance(key, str):
            raise ValueError('Key must be a string')
        if type(count) is not int or not 1 <= count <= len(self.nodes):
            raise ValueError('Requested replica count exceeds membership')
        scores = []
        for node in self.nodes:
            encoded = json.dumps([key, node], ensure_ascii=False, separators=(',', ':')).encode()
            score = int.from_bytes(hashlib.sha256(encoded).digest(), 'big')
            scores.append((-score, node))
        return [node for (_, node) in sorted(scores)[:count]]

def demo():
    group = Rendezvous(['node-a', 'node-b', 'node-c', 'node-d'])
    return {key: group.rank(key, 2) for key in ['synthetic-order-1', 'synthetic-order-2', 'synthetic-session']}
if __name__ == '__main__':
    argparse.ArgumentParser(description=__doc__).parse_args()
    print(json.dumps(demo(), indent=2))
