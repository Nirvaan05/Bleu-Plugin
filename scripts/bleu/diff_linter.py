import argparse
import sys
import os
import json
import subprocess
from state_manager import StateManager
from graph_engine import GraphEngine

class DiffLinter:
    """
    Industrial-grade Differential Linter (AP-04).
    Calculates the blast radius of changes using graph-aware rdeps and implicit dependency propagation.
    """
    def __init__(self, blueprint_dir: str = "blueprint"):
        self.blueprint_dir = blueprint_dir
        self.manager = StateManager(blueprint_dir)
        self.engine = GraphEngine(blueprint_dir)
        self.engine.scan()

    def get_git_changes(self) -> set:
        """Get set of changed file paths relative to blueprint_dir."""
        try:
            # Check staged and unstaged changes
            output = subprocess.check_output(
                ["git", "diff", "HEAD", "--name-only", self.blueprint_dir],
                stderr=subprocess.STDOUT,
                text=True
            )
            changes = set()
            for line in output.splitlines():
                if line.strip():
                    # git diff returns path relative to git root
                    rel_path = os.path.relpath(line.strip(), self.blueprint_dir).replace(os.sep, "/")
                    changes.add(rel_path)
            return changes
        except subprocess.CalledProcessError as e:
            print(f"Warning: Git diff failed: {e.output}", file=sys.stderr)
            return set()

    def calculate_blast_radius(self, seed_files: set) -> set:
        """
        Compute the transitive closure of dependents (rdeps).
        Includes implicit propagation for GLOBAL files (ADR-008).
        """
        affected_ids = set()
        
        # 1. Map seed files to node IDs and check for GLOBAL broadcast
        full_broadcast = False
        for rel_path in seed_files:
            node_id = self.engine.path_to_id.get(rel_path)
            if not node_id:
                # Fallback: if file exists but not in graph yet, we might need a full rebuild
                # but for safety, we'll treat it as a seed if it matches the pattern
                node_id = self.engine.get_node_id(os.path.join(self.blueprint_dir, rel_path))
            
            affected_ids.add(node_id)
            
            # ADR-008: Check if this node triggers a global broadcast
            for node in self.engine.nodes:
                if node["id"] == node_id and node["metadata"].get("is_global"):
                    full_broadcast = True
                    break
        
        if full_broadcast:
            # Maximum blast radius
            return {node["id"] for node in self.engine.nodes}

        # 2. Standard Transitive Closure (rdeps)
        # We use a worklist approach
        worklist = list(affected_ids)
        while worklist:
            current_id = worklist.pop(0)
            # Find all nodes that depend on current_id
            for edge in self.engine.edges:
                # Edge direction is 'from' depends on 'to'
                if edge["to"] == current_id and edge["from"] not in affected_ids:
                    affected_ids.add(edge["from"])
                    worklist.append(edge["from"])
                    
        return affected_ids

    def get_affected_paths(self, affected_ids: set) -> list:
        """Map node IDs back to absolute file paths."""
        id_to_path = {n["id"]: os.path.join(self.blueprint_dir, n["path"]) for n in self.engine.nodes}
        paths = []
        for aid in affected_ids:
            if aid in id_to_path:
                paths.append(id_to_path[aid])
        return sorted(paths)

def main():
    parser = argparse.ArgumentParser(description="Bleu Differential Linter Scope Generator")
    parser.add_argument("--files", nargs="+", help="Explicit list of files to check (bypass git diff)")
    parser.add_argument("--format", choices=["list", "json"], default="list", help="Output format")
    args = parser.parse_args()

    linter = DiffLinter()
    
    if args.files:
        seed_files = {os.path.relpath(f, linter.blueprint_dir).replace(os.sep, "/") for f in args.files}
    else:
        seed_files = linter.get_git_changes()

    if not seed_files:
        if args.format == "json":
            print("[]")
        else:
            print("No changes detected in blueprint/.")
        return

    affected_ids = linter.calculate_blast_radius(seed_files)
    affected_paths = linter.get_affected_paths(affected_ids)

    if args.format == "json":
        print(json.dumps(affected_paths, indent=2))
    else:
        for p in affected_paths:
            print(p)

if __name__ == "__main__":
    main()
