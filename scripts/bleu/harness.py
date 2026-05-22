import os
import sys
import json
import time
import argparse
import subprocess
from datetime import datetime
from typing import Dict, Any, List

# Add scripts/bleu to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from state_manager import StateManager
from graph_engine import GraphEngine
from sanitizer import RegexSanitizer, load_config as load_sanitizer_config
from circuit_breaker import is_foundational, update_session_blocked

class BleuHarness:
    """
    Thin adapter between Claude Code hooks and Bleu Deterministic Core.
    Implements recursion guards, structured telemetry, and idempotency.
    """
    def __init__(self, blueprint_dir: str = "blueprint"):
        self.blueprint_dir = blueprint_dir
        self.manager = StateManager(blueprint_dir)
        self.telemetry_file = os.path.join(blueprint_dir, ".telemetry", "events.jsonl")
        os.makedirs(os.path.dirname(self.telemetry_file), exist_ok=True)

    def log_event(self, event_type: str, metadata: Dict[str, Any]):
        """Structured observability (Rule 6)."""
        event = {
            "timestamp": datetime.now().isoformat(),
            "event": event_type,
            "metadata": metadata
        }
        with open(self.telemetry_file, "a", encoding="utf-8") as f:
            f.write(json.dumps(event) + "\n")

    def enter_recursion_guard(self, hook_name: str) -> bool:
        """Guard against in-process re-entry (Rule 2).

        Note: Claude Code dispatches each hook as a separate process, so this
        env-var flag only prevents recursion *within a single* harness
        invocation. Cross-process loop protection is handled at the hook layer
        (e.g. the git-autocommit stop_hook_active check), not here.
        """
        guard_var = f"BLEU_HOOK_ACTIVE_{hook_name.upper()}"
        if os.environ.get(guard_var) == "1":
            return False
        os.environ[guard_var] = "1"
        return True

    def on_file_changed(self, file_path: str):
        """
        Safety-first ingestion and indexing (Rule 3).
        1. Sanitize raw/ ingest.
        2. Rebuild graph for plan/ changes.
        """
        if not self.enter_recursion_guard("file_changed"):
            return

        rel_path = os.path.relpath(file_path, os.getcwd()).replace(os.sep, "/")
        self.log_event("HOOK_FILE_CHANGED", {"path": rel_path})

        try:
            # 1. Sanitize BEFORE indexing (Rule 3)
            if "blueprint/raw/" in rel_path:
                config = load_sanitizer_config(".claude/bleu/sanitizer-config.json")
                sanitizer = RegexSanitizer(config)
                from utils import read_file, write_file_atomic
                raw_content = read_file(file_path)
                sanitized = sanitizer.sanitize(raw_content)
                
                header = f"---\nbleu_trust_level: low\nbleu_sanitized_at: {datetime.now().isoformat()}\n---"
                final = f"{header}\n<trust_boundary>\n{sanitized}\n</trust_boundary>"
                write_file_atomic(file_path, final)
                self.log_event("SANITIZATION_COMPLETE", {"path": rel_path, "redactions": sanitizer.redactions})

            # 2. Rebuild graph if plan or APs changed
            if "blueprint/plan/" in rel_path or "blueprint/action-points/" in rel_path:
                engine = GraphEngine(self.blueprint_dir)
                engine.scan()
                self.manager.update_graph(engine.build_json())
                self.log_event("GRAPH_REBUILT", {"trigger": rel_path})

        except Exception as e:
            self.log_event("HOOK_FAILURE", {"hook": "file_changed", "error": str(e)})
            print(f"Bleu Error in FileChanged: {e}", file=sys.stderr)
        finally:
            os.environ[f"BLEU_HOOK_ACTIVE_FILE_CHANGED"] = "0"

    def on_subagent_stop(self, agent_name: str):
        """
        Observability hook for the linter subagent (Rule 7).

        This records that the linter finished; it does NOT itself trip the
        circuit breaker. Verdict recording and rejection-ceiling logic live in
        circuit_breaker.py, which is invoked separately with the Auditor's
        explicit verdict (APPROVE / REJECT / ESCALATE) - that is the only place
        a proposal's rejection count is mutated. Keeping the breaker decision in
        one deterministic entry point avoids double-counting from this hook.
        """
        if agent_name != "kb-linter":
            return
        self.log_event("HOOK_SUBAGENT_STOP", {"agent": agent_name})

    def on_session_start(self):
        """
        Recovery and status surface.
        """
        self.log_event("HOOK_SESSION_START", {})
        
        # 1. Verify SESSION.md Integrity
        session_path = os.path.join(self.blueprint_dir, "SESSION.md")
        if not os.path.exists(session_path) or os.path.getsize(session_path) == 0:
            self.log_event("RECOVERY_TRIGGERED", {"reason": "missing_session"})
            from recovery_engine import RecoveryEngine
            recovery = RecoveryEngine(self.blueprint_dir)
            recovery.reconstruct()
            
        # 2. Rebuild Graph for idempotency (Rule 5)
        engine = GraphEngine(self.blueprint_dir)
        engine.scan()
        self.manager.update_graph(engine.build_json())

def main():
    parser = argparse.ArgumentParser(description="Bleu Claude Code Hook Harness")
    parser.add_argument("--hook", required=True, choices=["file_changed", "subagent_stop", "session_start"])
    parser.add_argument("--file", help="Path for file_changed")
    parser.add_argument("--agent", help="Agent name for subagent_stop")
    args = parser.parse_args()

    harness = BleuHarness()
    
    if args.hook == "file_changed":
        if args.file:
            harness.on_file_changed(args.file)
    elif args.hook == "subagent_stop":
        harness.on_subagent_stop(args.agent)
    elif args.hook == "session_start":
        harness.on_session_start()

if __name__ == "__main__":
    main()
