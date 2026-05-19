import argparse
import sys
import os
import json
from typing import List, Dict, Set, Tuple
from state_manager import StateManager

class DAGValidator:
    """
    Industrial-grade DAG Validator (AP-03 & AP-12).
    Implements Kahn's Algorithm with lexicographical tie-breaking for deterministic execution ordering.
    """
    def __init__(self, graph_data: Dict):
        self.nodes = graph_data.get("nodes", [])
        self.edges = graph_data.get("edges", [])
        self.ap_nodes = {n["id"]: n for n in self.nodes if n["type"] == "ap"}
        self.ap_ids = sorted(list(self.ap_nodes.keys())) # AP-12: Deterministic base order

    def validate(self) -> Tuple[List[str], List[List[str]]]:
        errors = []
        
        # 1. Check for Duplicate Node IDs (Safety check)
        seen_ids = {}
        for node in self.nodes:
            nid = node["id"]
            if nid in seen_ids:
                errors.append(f"Duplicate Node ID detected: {nid} (paths: {seen_ids[nid]}, {node['path']})")
            seen_ids[nid] = node["path"]

        # 2. Build Adjacency List for APs
        # Map: ID -> List of IDs that DEPEND on it
        adj = {ap_id: [] for ap_id in self.ap_ids}
        in_degree = {ap_id: 0 for ap_id in self.ap_ids}
        
        for edge in self.edges:
            if edge["type"] != "depends_on":
                continue
                
            u, v = edge["from"], edge["to"]
            
            # Skip non-AP edges for DAG validation (only validate implementation sequence)
            if u not in self.ap_ids or v not in self.ap_ids:
                if u in self.ap_ids and v not in self.ap_ids:
                    # Check if dependency exists in graph at all
                    target_exists = any(n["id"] == v for n in self.nodes)
                    if not target_exists:
                        errors.append(f"AP {u} depends on non-existent node: {v}")
                continue

            # Edge: u depends on v (v -> u in execution order)
            adj[v].append(u)
            in_degree[u] += 1

        # 3. Kahn's Algorithm with Lexicographical Tie-Breaking (AP-12)
        queue = sorted([ap_id for ap_id in self.ap_ids if in_degree[ap_id] == 0])
        execution_groups = []
        visited_count = 0
        ordered_sequence = []

        while queue:
            # We take the current level of independent tasks as a 'parallel group'
            current_group = sorted(list(queue))
            execution_groups.append(current_group)
            
            next_queue = []
            for u in current_group:
                ordered_sequence.append(u)
                visited_count += 1
                for v in adj[u]:
                    in_degree[v] -= 1
                    if in_degree[v] == 0:
                        next_queue.append(v)
            
            # AP-12: Ensure next queue is deterministically sorted
            queue = sorted(next_queue)

        # 4. Cycle Detection
        if visited_count != len(self.ap_ids):
            # Trace cycles using DFS on remaining nodes
            remaining = [ap_id for ap_id in self.ap_ids if ap_id not in ordered_sequence]
            cycle_path = self._trace_cycle(remaining, adj)
            errors.append(f"Dependency cycle detected: {' -> '.join(cycle_path)}")

        # 5. Orphan Detection (Disconnected subgraphs)
        # In a real project, all APs should eventually lead to a terminal goal
        # but for now, we just flag nodes with 0 total edges as 'suspicious'
        for ap_id in self.ap_ids:
            has_edge = any(e["from"] == ap_id or e["to"] == ap_id for e in self.edges if e["type"] == "depends_on")
            if not has_edge and len(self.ap_ids) > 1:
                errors.append(f"Orphan Action Point (no dependencies): {ap_id}")

        return errors, execution_groups

    def _trace_cycle(self, nodes: List[str], adj: Dict[str, List[str]]) -> List[str]:
        visited = set()
        stack = []
        path = []

        def dfs(u):
            if u in stack:
                # Cycle found
                idx = stack.index(u)
                return stack[idx:] + [u]
            if u in visited:
                return None
            
            visited.add(u)
            stack.append(u)
            for v in adj.get(u, []):
                res = dfs(v)
                if res: return res
            stack.pop()
            return None

        for node in nodes:
            res = dfs(node)
            if res: return res
        return ["Unknown Cycle"]

    def generate_mermaid(self, groups: List[List[str]]) -> str:
        lines = ["graph TD"]
        # Add group styling
        for i, group in enumerate(groups):
            lines.append(f"    subgraph Group_{i+1} [Level {i+1}]")
            for ap_id in group:
                lines.append(f"        {ap_id}")
            lines.append("    end")

        for edge in self.edges:
            if edge["type"] == "depends_on":
                u, v = edge["from"], edge["to"]
                if u in self.ap_ids and v in self.ap_ids:
                    # Mermaid typically shows data flow or sequence (v comes before u)
                    lines.append(f"    {v} --> {u}")
        return "\n".join(lines)

def main():
    parser = argparse.ArgumentParser(description="Bleu Deterministic DAG Validator")
    parser.add_argument("--mermaid", action="store_true", help="Generate Mermaid output")
    parser.add_argument("--json", action="store_true", help="Output execution groups as JSON")
    args = parser.parse_args()

    manager = StateManager()
    graph_data = manager.get_graph()
    
    if not graph_data:
        print("Error: No graph data found. Run graph_engine --rebuild first.")
        sys.exit(1)

    validator = DAGValidator(graph_data)
    errors, groups = validator.validate()

    if errors:
        print("DAG VALIDATION FAILED:", file=sys.stderr)
        for err in errors:
            print(f"  - {err}", file=sys.stderr)
        sys.exit(1)

    if args.json:
        print(json.dumps(groups, indent=2))
    elif args.mermaid:
        print(validator.generate_mermaid(groups))
    else:
        print("DAG VALIDATION PASSED.")
        print(f"Execution Order (Deterministic):")
        for i, group in enumerate(groups):
            print(f"  Level {i+1}: {', '.join(group)}")

if __name__ == "__main__":
    main()
