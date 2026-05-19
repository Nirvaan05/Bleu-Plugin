import os
from utils import save_json_atomic, write_file_atomic, load_json, read_file

class StateManager:
    """
    Wraps critical blueprint files in atomic write logic.
    """
    def __init__(self, blueprint_dir: str = "blueprint"):
        self.blueprint_dir = blueprint_dir
        self.session_file = os.path.join(blueprint_dir, "SESSION.md")
        self.next_file = os.path.join(blueprint_dir, "NEXT.md")
        self.graph_file = os.path.join(blueprint_dir, ".graph", "graph.json")
        self.counters_file = os.path.join(blueprint_dir, ".reflection", "counters.json")

    def update_session(self, content: str):
        write_file_atomic(self.session_file, content)

    def update_next(self, content: str):
        write_file_atomic(self.next_file, content)

    def update_graph(self, data: dict):
        save_json_atomic(self.graph_file, data)

    def update_counters(self, data: dict):
        save_json_atomic(self.counters_file, data)

    def get_session(self) -> str:
        return read_file(self.session_file)

    def get_graph(self) -> dict:
        return load_json(self.graph_file)
