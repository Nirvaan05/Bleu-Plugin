import unittest
import json
import random
import os
import sys

# Add scripts/bleu to path
sys.path.append(os.path.join(os.getcwd(), 'scripts', 'bleu'))
from dag_validator import DAGValidator

class TestDAGValidator(unittest.TestCase):

    def test_valid_dag_determinism(self):
        """AP-12: Ensure stable ordering with lexicographical tie-breaking."""
        graph_data = {
            "nodes": [
                {"id": "AP-01", "type": "ap", "path": "p1"},
                {"id": "AP-02", "type": "ap", "path": "p2"},
                {"id": "AP-03", "type": "ap", "path": "p3"},
                {"id": "AP-04", "type": "ap", "path": "p4"}
            ],
            "edges": [
                {"from": "AP-02", "to": "AP-01", "type": "depends_on"},
                {"from": "AP-03", "to": "AP-01", "type": "depends_on"},
                {"from": "AP-04", "to": "AP-02", "type": "depends_on"},
                {"from": "AP-04", "to": "AP-03", "type": "depends_on"}
            ]
        }
        
        validator = DAGValidator(graph_data)
        errors, groups = validator.validate()
        self.assertEqual(len(errors), 0)
        
        # Expected Levels:
        # L1: AP-01 (In-degree 0 in execution order)
        # L2: AP-02, AP-03 (Both depend on 01)
        # L3: AP-04 (Depends on 02, 03)
        expected = [["AP-01"], ["AP-02", "AP-03"], ["AP-04"]]
        self.assertEqual(groups, expected)

        # Randomized nodes/edges order should not change output
        for _ in range(5):
            random.shuffle(graph_data["nodes"])
            random.shuffle(graph_data["edges"])
            v2 = DAGValidator(graph_data)
            e2, g2 = v2.validate()
            self.assertEqual(g2, expected)

    def test_direct_cycle(self):
        graph_data = {
            "nodes": [
                {"id": "AP-01", "type": "ap", "path": "p1"},
                {"id": "AP-02", "type": "ap", "path": "p2"}
            ],
            "edges": [
                {"from": "AP-01", "to": "AP-02", "type": "depends_on"},
                {"from": "AP-02", "to": "AP-01", "type": "depends_on"}
            ]
        }
        validator = DAGValidator(graph_data)
        errors, _ = validator.validate()
        self.assertTrue(any("cycle detected" in e.lower() for e in errors))

    def test_transitive_cycle(self):
        graph_data = {
            "nodes": [
                {"id": "AP-01", "type": "ap", "path": "p1"},
                {"id": "AP-02", "type": "ap", "path": "p2"},
                {"id": "AP-03", "type": "ap", "path": "p3"}
            ],
            "edges": [
                {"from": "AP-01", "to": "AP-03", "type": "depends_on"},
                {"from": "AP-02", "to": "AP-01", "type": "depends_on"},
                {"from": "AP-03", "to": "AP-02", "type": "depends_on"}
            ]
        }
        validator = DAGValidator(graph_data)
        errors, _ = validator.validate()
        self.assertTrue(any("cycle detected" in e.lower() for e in errors))

    def test_orphan_node(self):
        graph_data = {
            "nodes": [
                {"id": "AP-01", "type": "ap", "path": "p1"},
                {"id": "AP-02", "type": "ap", "path": "p2"},
                {"id": "AP-03", "type": "ap", "path": "p3"}
            ],
            "edges": [
                {"from": "AP-02", "to": "AP-01", "type": "depends_on"}
            ]
        }
        validator = DAGValidator(graph_data)
        errors, _ = validator.validate()
        self.assertTrue(any("orphan action point" in e.lower() for e in errors))
        self.assertTrue(any("AP-03" in e for e in errors))

    def test_reference_only_node_is_not_orphan(self):
        """A node wired in only via a 'references' edge is connected, not an orphan."""
        graph_data = {
            "nodes": [
                {"id": "AP-01", "type": "ap", "path": "p1"},
                {"id": "AP-02", "type": "ap", "path": "p2"},
                {"id": "AP-03", "type": "ap", "path": "p3"},
            ],
            "edges": [
                {"from": "AP-02", "to": "AP-01", "type": "depends_on"},
                # AP-03 has no depends_on edge, only a reference to AP-01.
                {"from": "AP-03", "to": "AP-01", "type": "references"},
            ],
        }
        validator = DAGValidator(graph_data)
        errors, _ = validator.validate()
        self.assertFalse(any("AP-03" in e and "orphan" in e.lower() for e in errors))

    def test_missing_dependency(self):
        graph_data = {
            "nodes": [
                {"id": "AP-01", "type": "ap", "path": "p1"}
            ],
            "edges": [
                {"from": "AP-01", "to": "AP-NON-EXISTENT", "type": "depends_on"}
            ]
        }
        validator = DAGValidator(graph_data)
        errors, _ = validator.validate()
        self.assertTrue(any("depends on non-existent node" in e.lower() for e in errors))

    def test_duplicate_ids(self):
        graph_data = {
            "nodes": [
                {"id": "AP-01", "type": "ap", "path": "p1"},
                {"id": "AP-01", "type": "ap", "path": "p2"}
            ],
            "edges": []
        }
        validator = DAGValidator(graph_data)
        errors, _ = validator.validate()
        self.assertTrue(any("duplicate node id" in e.lower() for e in errors))

if __name__ == "__main__":
    unittest.main()
