import os
import sys
import tempfile
import time
import unittest

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from utils import AtomicWriter, FileLocker, read_file, write_file_atomic


class TestAtomicWriter(unittest.TestCase):
    def test_atomic_write_persists_content(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = os.path.join(tmp, "sub", "state.md")
            write_file_atomic(target, "hello")
            self.assertEqual(read_file(target), "hello")

    def test_no_temp_files_left_behind(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = os.path.join(tmp, "state.md")
            write_file_atomic(target, "x")
            leftovers = [f for f in os.listdir(tmp) if f.startswith(".tmp-")]
            self.assertEqual(leftovers, [])


class TestFileLocker(unittest.TestCase):
    def test_stale_lock_is_reclaimed(self):
        """A lock left by a crashed writer must not deadlock future writers."""
        with tempfile.TemporaryDirectory() as tmp:
            target = os.path.join(tmp, "state.md")
            stale = target + ".lock"
            with open(stale, "w") as f:
                f.write("")
            # Backdate the lock well past the stale threshold.
            old = time.time() - 120
            os.utime(stale, (old, old))

            locker = FileLocker(target, timeout=2, stale_after=30.0)
            with locker.lock():
                pass  # acquires by reclaiming the stale lock instead of timing out
            self.assertFalse(os.path.exists(stale))

    def test_fresh_lock_is_not_stolen(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = os.path.join(tmp, "state.md")
            fresh = target + ".lock"
            with open(fresh, "w") as f:
                f.write("")
            locker = FileLocker(target, timeout=1, stale_after=30.0)
            with self.assertRaises(TimeoutError):
                with locker.lock():
                    pass


if __name__ == "__main__":
    unittest.main()
