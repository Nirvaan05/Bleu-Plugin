import argparse
import sys
import os
import re
from typing import Optional, Dict
from utils import read_file, write_file_atomic
from state_manager import StateManager

class RecoveryEngine:
    """
    Industrial-grade Recovery Engine (AP-14).
    Reconstructs blueprint state from the append-only journal.md.
    """
    def __init__(self, blueprint_dir: str = "blueprint"):
        self.blueprint_dir = blueprint_dir
        self.manager = StateManager(blueprint_dir)
        self.journal_path = os.path.join(blueprint_dir, "journal.md")

    def find_last_valid_state(self) -> Optional[Dict]:
        """
        Parses journal.md from bottom up to find the most recent session summary.
        """
        if not os.path.exists(self.journal_path):
            return None
            
        content = read_file(self.journal_path)
        # Session headers are usually ## Session <timestamp>
        # Let's split by session
        sessions = re.split(r"## Session ", content)
        if len(sessions) < 2:
            return None
            
        # Get the last non-empty session
        last_session = sessions[-1].strip()
        
        state = {
            "phase": "Unknown",
            "status": "in-progress",
            "timestamp": None,
            "outcome": "",
            "did": [],
            "decisions": []
        }
        
        # Extract Phase (usually in Goal or Outcome)
        phase_match = re.search(r"Phase (\d+)", last_session)
        if phase_match:
            state["phase"] = f"Phase {phase_match.group(1)}"
            
        # Extract Outcome
        outcome_match = re.search(r"\*\*Outcome\*\*:\s*(.*)", last_session)
        if outcome_match:
            state["outcome"] = outcome_match.group(1)
            
        # Extract Did list
        did_match = re.search(r"\*\*Did\*\*:\n(.*?)\n\n", last_session, re.DOTALL)
        if did_match:
            state["did"] = [line.strip("- ").strip() for line in did_match.group(1).splitlines() if line.strip()]
            
        # Extract Decisions
        dec_match = re.search(r"\*\*Decisions made.*?\*\*:\n(.*?)\n\n", last_session, re.DOTALL)
        if dec_match:
            state["decisions"] = [line.strip("- ").strip() for line in dec_match.group(1).splitlines() if line.strip()]

        return state

    def reconstruct(self):
        state = self.find_last_valid_state()
        if not state:
            print("Error: Could not find valid state in journal.md.", file=sys.stderr)
            return False
            
        # 1. Reconstruct SESSION.md
        session_template = f"""# SESSION — Reconstructed

> Reconstructed from journal.md
> Last valid phase detected: {state['phase']}
> Status: {state['status']}

## Reconstructed Summary
{state['outcome']}

## Last completed actions (from Journal)
"""
        for item in state['did']:
            session_template += f"- {item}\n"
            
        session_template += "\n## Where to read first on resume\n1. NEXT.md\n2. decisions/README.md\n"
        
        # 2. Reconstruct NEXT.md (minimal stub)
        next_template = f"""# NEXT — Reconstructed

> This file was reconstructed. Verify before proceeding.

## Immediate next steps
1. Review implementation progress
2. Run graph_engine --rebuild
3. Run dag_validator
"""
        
        self.manager.update_session(session_template)
        self.manager.update_next(next_template)
        
        print("Recovery complete. SESSION.md and NEXT.md have been reconstructed.")
        return True

def main():
    parser = argparse.ArgumentParser(description="Bleu Recovery Engine")
    parser.add_argument("--reconstruct", action="store_true", help="Attempt state reconstruction")
    args = parser.parse_args()

    engine = RecoveryEngine()
    
    if args.reconstruct:
        engine.reconstruct()
    else:
        state = engine.find_last_valid_state()
        if state:
            print(f"Detected State: {state['phase']} | Outcome: {state['outcome']}")
        else:
            print("No valid state detected in journal.")

if __name__ == "__main__":
    main()
