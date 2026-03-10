# Rendezvous hashing

Choose stable primary and replica candidates by ranking node-specific hashes.

Educational implementation with synthetic examples.

## Run

Python 3.9 or newer; standard library only. From this directory:

```sh
python3 main.py
python3 main.py --help
python3 -m unittest -v
```

The default example uses synthetic data and needs no credentials, installation, or network connection. The script also works by absolute path from another working directory.

## Behavior

For each key, SHA-256 scores every node. Highest score wins, with a stable node-name tie break. Top-k ranking yields distinct replica candidates. Removing a member preserves the relative ranking of remaining members.

## Use in Python

```python
from main import Rendezvous

placement = Rendezvous(['node-a', 'node-b', 'node-c'])
primary, replica = placement.rank('example-key', count=2)
assert primary != replica
```

## Design limits

Placement is unweighted and costs O(nodes) hashing plus sorting per lookup. It does not move data or verify replica health. Members must share the same node IDs and algorithm. Replica candidates are labels only, with no stored data or cluster integration.

## Verification

The unit tests cover successful operations, failure paths, and invariants. These are local correctness checks, not production performance or security certification.

## Repository checks

```sh
python3 verify.py
```

This runs the isolated test suite, synthetic example, and CLI help. The included GitHub Actions workflow repeats these checks when the repository is published. No hosted CI result is claimed by the local verification report.
