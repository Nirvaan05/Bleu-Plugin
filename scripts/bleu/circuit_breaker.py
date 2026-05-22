import argparse
import sys
import os
import re
import json
from datetime import datetime
from utils import load_json, save_json_atomic, read_file, write_file_atomic
from state_manager import StateManager

# ADR-003: Foundational files
FOUNDATIONAL_FILES = [
    "plan/00-vision.md",
    "plan/01-architecture.md",
    "plan/04-data-model.md",
    "plan/06-non-functional.md"
]

def is_foundational(proposal_path):
    # Check if the path matches any foundational file
    # Proposal path is usually something like 'plan/03-components/auth.md'
    return any(f in proposal_path for f in FOUNDATIONAL_FILES)

def update_session_blocked(manager, node_path, global_stop=False):
    content = manager.get_session()
    if global_stop:
        # Global Hard Stop
        status_line = "Status: BLOCKED (GLOBAL HARD STOP)"
        block_msg = f"\n\n## !! GLOBAL HARD STOP !!\n\nFoundational file `{node_path}` has reached the reflection limit (N=2 rejections). Autonomous execution is frozen. Human review required."
    else:
        # Partial Isolation
        status_line = "Status: in-progress (PARTIAL ISOLATION)"
        block_msg = f"\n\n## [BLOCKED] {node_path}\n\nThis node has reached the reflection limit (N=2 rejections). It and its downstream dependents are quarantined. See `decisions/pending-resolution.md`."

    # Update only the first (header) Status line, anchored to line start, so
    # per-node status entries elsewhere in SESSION.md are not clobbered.
    content = re.sub(r"^Status: .*", status_line, content, count=1, flags=re.MULTILINE)
    
    # Append block message before "Where to read first" or at the end
    if "## Where to read first" in content:
        content = content.replace("## Where to read first", f"{block_msg}\n\n## Where to read first")
    else:
        content += block_msg
    
    manager.update_session(content)

def main():
    parser = argparse.ArgumentParser(description="Bleu Reflection Circuit Breaker (AP-06)")
    parser.add_argument("--id", required=True, help="Proposal ID (hash or path)")
    parser.add_argument("--verdict", required=True, choices=["APPROVE", "REJECT", "ESCALATE"], help="Auditor verdict")
    parser.add_argument("--path", help="Path of the affected node/file")
    args = parser.parse_args()
    
    manager = StateManager()
    counters = load_json(manager.counters_file)
    
    if "proposals" not in counters:
        counters["proposals"] = {}
        
    prop_id = args.id
    if prop_id not in counters["proposals"]:
        counters["proposals"][prop_id] = {
            "rejection_count": 0,
            "last_verdict": None,
            "timestamp": None
        }
    
    entry = counters["proposals"][prop_id]
    entry["last_verdict"] = args.verdict
    entry["timestamp"] = datetime.now().isoformat()
    
    if args.verdict == "REJECT":
        entry["rejection_count"] += 1
        
    # Save counters atomically
    manager.update_counters(counters)
    
    if entry["rejection_count"] >= 2:
        print(f"BLOCK_SIGNAL: Node {args.path or prop_id} reached rejection ceiling.")
        
        # Isolation Logic
        node_path = args.path or prop_id
        global_stop = is_foundational(node_path)
        
        update_session_blocked(manager, node_path, global_stop=global_stop)
        
        # Trigger exit code 1 to stop the hook/process
        sys.exit(1)
        
    print(f"Verdict {args.verdict} recorded for {prop_id}. Count: {entry['rejection_count']}")
    sys.exit(0)

if __name__ == "__main__":
    main()
