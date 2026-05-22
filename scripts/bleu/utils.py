import os
import json
import tempfile
import contextlib
import time
from typing import Any, Dict, Optional

class AtomicWriter:
    """
    Atomic state writes (ADR-005).

    The rename via os.replace is atomic on POSIX and Windows: a reader sees
    either the old file or the fully written new one, never a partial. The temp
    file is flushed and fsync'd before the rename so a crash mid-write cannot
    expose a truncated file. (Full crash durability would also fsync the
    containing directory; that is deferred and noted in ADR-005.)
    """
    
    @staticmethod
    @contextlib.contextmanager
    def atomic_write(file_path: str, mode: str = 'w', encoding: str = 'utf-8'):
        """
        Context manager for atomic writes using temp-file + replace.
        """
        dir_name = os.path.dirname(file_path)
        if not dir_name:
            dir_name = '.'
        
        # Ensure directory exists
        os.makedirs(dir_name, exist_ok=True)
        
        # Create a temporary file in the same directory to ensure atomic replace is possible
        fd, temp_path = tempfile.mkstemp(dir=dir_name, prefix='.tmp-', suffix='.tmp')
        try:
            with os.fdopen(fd, mode, encoding=encoding) as f:
                yield f
                f.flush()
                os.fsync(f.fileno())

            # Atomic replace (POSIX compliant, Windows-safe via os.replace)
            os.replace(temp_path, file_path)
        except Exception as e:
            if os.path.exists(temp_path):
                os.remove(temp_path)
            raise e

class FileLocker:
    """
    Simple file-based locking mechanism to prevent concurrent writes.

    A lock left behind by a crashed writer is reclaimed once it is older than
    `stale_after` seconds, so a crash mid-write cannot deadlock every future
    writer. `stale_after` defaults to well above `timeout` so a healthy holder
    is never stolen from.
    """
    def __init__(self, file_path: str, timeout: int = 5, stale_after: float = 30.0):
        self.lock_file = f"{file_path}.lock"
        self.timeout = timeout
        self.stale_after = stale_after

    def _reclaim_if_stale(self):
        try:
            age = time.time() - os.path.getmtime(self.lock_file)
        except FileNotFoundError:
            return
        if age > self.stale_after:
            try:
                os.remove(self.lock_file)
            except FileNotFoundError:
                pass

    @contextlib.contextmanager
    def lock(self):
        dir_name = os.path.dirname(self.lock_file)
        if dir_name:
            os.makedirs(dir_name, exist_ok=True)

        start_time = time.time()
        while True:
            try:
                # Exclusive creation of lock file
                fd = os.open(self.lock_file, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
                os.close(fd)
                break
            except FileExistsError:
                self._reclaim_if_stale()
                if time.time() - start_time > self.timeout:
                    raise TimeoutError(f"Could not acquire lock for {self.lock_file} after {self.timeout}s")
                time.sleep(0.1)

        try:
            yield
        finally:
            if os.path.exists(self.lock_file):
                os.remove(self.lock_file)

def load_json(file_path: str) -> Dict[str, Any]:
    if not os.path.exists(file_path):
        return {}
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_json_atomic(file_path: str, data: Dict[str, Any]):
    locker = FileLocker(file_path)
    with locker.lock():
        with AtomicWriter.atomic_write(file_path) as f:
            json.dump(data, f, indent=2)

def read_file(file_path: str) -> str:
    if not os.path.exists(file_path):
        return ""
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()

def write_file_atomic(file_path: str, content: str):
    locker = FileLocker(file_path)
    with locker.lock():
        with AtomicWriter.atomic_write(file_path) as f:
            f.write(content)
