import argparse
import sys
import os
import re
import json
import hashlib
from utils import save_json_atomic, read_file
from state_manager import StateManager

# Global files that trigger full broadcast (ADR-008)
GLOBAL_FILES = [
    "plan/00-vision.md",
    "plan/01-architecture.md",
    "plan/04-data-model.md",
    "plan/06-non-functional.md"
]

class GraphEngine:
    def __init__(self, blueprint_dir: str = "blueprint"):
        self.blueprint_dir = blueprint_dir
        self.nodes = []
        self.edges = []
        self.path_to_id = {}

    def get_node_id(self, file_path):
        # Extract ID from filename or title
        # e.g. AP-01-scaffold-scripts.md -> AP-01
        basename = os.path.basename(file_path)
        match = re.match(r"(AP-\d+|ADR-\d+)", basename)
        if match:
            return match.group(1)
        # Default to relative path slug
        rel_path = os.path.relpath(file_path, self.blueprint_dir)
        return rel_path.replace(os.sep, "/").replace(".md", "")

    def get_node_type(self, file_path):
        rel_path = os.path.relpath(file_path, self.blueprint_dir)
        if rel_path.startswith("action-points") and "README" not in rel_path: return "ap"
        if rel_path.startswith("decisions") and "README" not in rel_path: return "adr"
        if rel_path.startswith("plan"): return "component"
        return "other"

    def scan(self):
        for root, _, files in os.walk(self.blueprint_dir):
            if ".graph" in root or ".reflection" in root or ".telemetry" in root:
                continue
                
            for file in files:
                if not file.endswith(".md"):
                    continue
                    
                full_path = os.path.join(root, file)
                rel_path = os.path.relpath(full_path, self.blueprint_dir).replace(os.sep, "/")
                
                node_id = self.get_node_id(full_path)
                node_type = self.get_node_type(full_path)
                content = read_file(full_path)
                content_hash = hashlib.sha256(content.encode('utf-8')).hexdigest()
                
                is_global = any(g in rel_path for g in GLOBAL_FILES)
                
                self.nodes.append({
                    "id": node_id,
                    "type": node_type,
                    "path": rel_path,
                    "metadata": {
                        "status": "active",
                        "hash": content_hash,
                        "is_global": is_global
                    }
                })
                self.path_to_id[rel_path] = node_id
                
                # Extract Edges
                # 1. Depends on: (Action Points) - Match header and following line(s)
                # We look for '## Depends on' and capture the text until the next header or empty line
                deps_sections = re.findall(r"## Depends on\s*([\s\S]*?)(?:\n##|\n\n|$)", content)
                for dep_section in deps_sections:
                    for dep in re.split(r"[\n,]\s*", dep_section):
                        dep = dep.strip()
                        # Ignore 'None' and long descriptive lines
                        if dep and dep.lower() != "none" and len(dep) < 20:
                            self.edges.append({
                                "from": node_id,
                                "to": dep,
                                "type": "depends_on"
                            })
                
                # 2. @blueprint/ links (Components/ADRs)
                links = re.findall(r"@blueprint/([\w\-/]+)", content)
                for link in links:
                    # Normalize link to node ID if possible
                    target_id = link.replace(".md", "")
                    self.edges.append({
                        "from": node_id,
                        "to": target_id,
                        "type": "references"
                    })

    def build_json(self):
        return {
            "version": "1.0.0",
            "nodes": self.nodes,
            "edges": self.edges
        }

    def find_rdeps(self, target_id):
        # Transitive closure of reverse dependencies
        affected = {target_id}
        changed = True
        while changed:
            changed = False
            for edge in self.edges:
                if edge["to"] in affected and edge["from"] not in affected:
                    affected.add(edge["from"])
                    changed = True
        return affected

def main():
    parser = argparse.ArgumentParser(description="Bleu Graph Engine - AP-02/AP-15")
    parser.add_argument("--rebuild", action="store_true", help="Rebuild the full graph")
    parser.add_argument("--impact", help="Calculate impact (rdeps) for a node ID")
    args = parser.parse_args()
    
    engine = GraphEngine()
    engine.scan()
    
    manager = StateManager()
    if args.rebuild:
        manager.update_graph(engine.build_json())
        print(f"Graph rebuilt at {manager.graph_file}")
        
    if args.impact:
        # Implicit broadcast check (ADR-008)
        is_global = False
        for node in engine.nodes:
            if node["id"] == args.impact and node["metadata"].get("is_global"):
                is_global = True
                break
        
        if is_global:
            print(f"IMPACT: Node {args.impact} is GLOBAL. Maximum blast radius triggered.")
            print(",".join([n["id"] for n in engine.nodes]))
        else:
            rdeps = engine.find_rdeps(args.impact)
            print(f"IMPACT for {args.impact}: {','.join(rdeps)}")

if __name__ == "__main__":
    main()
